#!/usr/bin/env python3
"""Register health report for the AI inventory, risk register and incident log.

The validator (validate_and_report.py) asks whether the registers are well formed.
This tool asks a different question: given today's date, which entries need someone
to act? It reads the three CSV registers and reports:

  RH01  system review date has passed
  RH02  live or pilot system with no open risk recorded against it
  RH03  risk past its target date and still open or mitigating
  RH04  open or mitigating risk not reviewed within the review window
  RH05  high or critical residual risk that is not closed
  RH06  accepted risk not re-confirmed within the acceptance window
  RH07  incident still open or investigating after the incident window
  RH08  external reporting decision still under assessment after the reporting window
  RH09  incident category with no matching risk category on the same system

Only the Python standard library is used. Nothing is sent anywhere.

Usage:
    python tools/register_health.py                       # Fernhill example, today's date
    python tools/register_health.py --registers my-registers --as-of 2027-01-31
    python tools/register_health.py --fail-on high        # exit 1 if any high finding
    python tools/register_health.py --output report.md
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTERS = REPO_ROOT / "examples" / "fernhill"
EXAMPLE_REPORT = REPO_ROOT / "docs" / "register-health-example.md"
EXAMPLE_AS_OF = dt.date(2026, 12, 20)

INVENTORY_FILE = "ai-system-inventory.csv"
RISK_FILE = "ai-risk-register.csv"
INCIDENT_FILE = "ai-incident-log.csv"

INVENTORY_COLUMNS = ("system_id", "name", "eu_risk_tier", "status", "next_review_date")
RISK_COLUMNS = (
    "risk_id", "system_id", "category", "residual_rating", "status", "target_date", "last_reviewed",
)
INCIDENT_COLUMNS = (
    "incident_id", "system_id", "date_detected", "category", "severity",
    "reportable_externally", "status",
)

SEVERITIES = ("high", "medium", "low")
SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}
RATING_RANK = {"low": 1, "medium": 2, "high": 3, "critical": 4}

# An incident category is expected to have a risk in one of these categories on the same system.
INCIDENT_TO_RISK_CATEGORIES = {
    "harmful-output": {"accuracy-reliability", "misuse", "transparency"},
    "bias-discrimination": {"bias-fairness"},
    "data-leak": {"privacy", "security"},
    "security-breach": {"security"},
    "outage": {"operational"},
    "misuse": {"misuse", "human-oversight"},
    "drift-degradation": {"accuracy-reliability"},
}

OPEN_RISK = {"open", "mitigating"}
OPEN_INCIDENT = {"open", "investigating"}
LIVE_STATUSES = {"live", "pilot"}


class RegisterError(Exception):
    """A register file is missing, lacks a column or holds a value that cannot be read."""


@dataclass(frozen=True)
class Thresholds:
    review_days: int = 90      # RH04: open risk not reviewed for this long
    accepted_days: int = 180   # RH06: accepted risk not re-confirmed for this long
    incident_days: int = 30    # RH07: incident still open after this long
    report_days: int = 14      # RH08: reporting decision still under assessment after this long


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    subject: str
    system_id: str
    message: str


Row = Dict[str, str]


def read_register(path: Path, required: Sequence[str]) -> List[Row]:
    if not path.is_file():
        raise RegisterError(f"{path}: file not found")
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            missing = [c for c in required if c not in header]
            if missing:
                raise RegisterError(f"{path}: missing column(s): {', '.join(missing)}")
            rows = []
            for row in reader:
                clean = {k: (v or "").strip() for k, v in row.items() if k is not None}
                if any(clean.values()):
                    rows.append(clean)
            return rows
    except UnicodeDecodeError as exc:
        raise RegisterError(f"{path}: not valid UTF-8 ({exc.reason})") from exc


def parse_date(value: str, where: str, optional: bool = False) -> Optional[dt.date]:
    if not value:
        if optional:
            return None
        raise RegisterError(f"{where}: date is empty")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise RegisterError(f"{where}: '{value}' is not an ISO date (YYYY-MM-DD)") from exc


def worse(severity: str, bump: bool) -> str:
    """Raise a severity by one level when `bump` is true."""
    if not bump:
        return severity
    return {"low": "medium", "medium": "high", "high": "high"}[severity]


# --------------------------------------------------------------------------- #
# Rules
# --------------------------------------------------------------------------- #


def check_health(inventory: List[Row], risks: List[Row], incidents: List[Row],
                 as_of: dt.date, limits: Thresholds = Thresholds()) -> List[Finding]:
    findings: List[Finding] = []
    systems = {s["system_id"]: s for s in inventory}

    def add(rule: str, severity: str, subject: str, system_id: str, message: str) -> None:
        findings.append(Finding(rule, severity, subject, system_id, message))

    # RH01 and RH02: systems
    for system in inventory:
        sid = system["system_id"]
        if system["status"] == "retired":
            continue
        review = parse_date(system["next_review_date"], f"{sid} next_review_date")
        high_tier = system["eu_risk_tier"].startswith("high-risk")
        if review < as_of:
            late = (as_of - review).days
            add("RH01", worse("medium", high_tier), sid, sid,
                f"Review was due {review.isoformat()} ({late} days ago)"
                + ("; high-risk tier" if high_tier else ""))
        if system["status"] in LIVE_STATUSES:
            has_open = any(r["system_id"] == sid and r["status"] in OPEN_RISK for r in risks)
            if not has_open:
                add("RH02", "medium", sid, sid,
                    f"{system['status'].capitalize()} system with no open or mitigating risk recorded")

    # RH03 to RH06: risks
    for risk in risks:
        rid, sid = risk["risk_id"], risk["system_id"]
        status = risk["status"]
        rating = risk["residual_rating"]
        serious = RATING_RANK.get(rating, 0) >= RATING_RANK["high"]
        target = parse_date(risk["target_date"], f"{rid} target_date")
        reviewed = parse_date(risk["last_reviewed"], f"{rid} last_reviewed")
        if status in OPEN_RISK:
            if target < as_of:
                add("RH03", worse("medium", serious), rid, sid,
                    f"Target date {target.isoformat()} passed {(as_of - target).days} days ago; "
                    f"status is {status}")
            age = (as_of - reviewed).days
            if age > limits.review_days:
                add("RH04", worse("low", serious), rid, sid,
                    f"Last reviewed {reviewed.isoformat()} ({age} days ago); "
                    f"window is {limits.review_days} days")
        if status != "closed" and serious:
            add("RH05", "high", rid, sid, f"Residual rating is {rating} and the risk is {status}")
        if status == "accepted":
            age = (as_of - reviewed).days
            if age > limits.accepted_days:
                add("RH06", "medium", rid, sid,
                    f"Accepted risk last confirmed {reviewed.isoformat()} ({age} days ago); "
                    f"window is {limits.accepted_days} days")

    # RH07 to RH09: incidents
    for inc in incidents:
        iid, sid = inc["incident_id"], inc["system_id"]
        detected = parse_date(inc["date_detected"], f"{iid} date_detected")
        age = (as_of - detected).days
        if inc["status"] in OPEN_INCIDENT and age > limits.incident_days:
            serious = inc["severity"] in {"high", "critical"}
            add("RH07", worse("medium", serious), iid, sid,
                f"{inc['severity'].capitalize()} incident {inc['status']} for {age} days "
                f"(window {limits.incident_days})")
        if inc["reportable_externally"] == "under-assessment" and age > limits.report_days:
            add("RH08", "high", iid, sid,
                f"Decision on external reporting still under assessment after {age} days "
                f"(window {limits.report_days}); record the decision and the reasoning")
        wanted = INCIDENT_TO_RISK_CATEGORIES.get(inc["category"])
        if wanted and sid in systems:
            have = {r["category"] for r in risks if r["system_id"] == sid}
            if not (have & wanted):
                add("RH09", "low", iid, sid,
                    f"No {' or '.join(sorted(wanted))} risk is recorded for this system; "
                    f"incident category is {inc['category']}")

    findings.sort(key=lambda f: (SEVERITY_RANK[f.severity], f.rule, f.subject))
    return findings


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #


def long_date(d: dt.date) -> str:
    return f"{d.day} {d.strftime('%B %Y')}"


def system_summary(inventory: List[Row], risks: List[Row], incidents: List[Row],
                   as_of: dt.date) -> List[List[str]]:
    rows = []
    for system in inventory:
        sid = system["system_id"]
        mine = [r for r in risks if r["system_id"] == sid and r["status"] in OPEN_RISK]
        top = max((r["residual_rating"] for r in mine), key=lambda x: RATING_RANK.get(x, 0), default="none")
        open_inc = [i for i in incidents if i["system_id"] == sid and i["status"] in OPEN_INCIDENT]
        review = parse_date(system["next_review_date"], f"{sid} next_review_date")
        due = review.isoformat()
        if system["status"] != "retired" and review < as_of:
            due += " (overdue)"
        rows.append([sid, system["name"], system["eu_risk_tier"], system["status"],
                     str(len(mine)), top, str(len(open_inc)), due])
    return rows


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def table(header: Sequence[str], rows: Sequence[Sequence[str]]) -> List[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    for row in rows:
        out.append("| " + " | ".join(cell(c) for c in row) + " |")
    return out


def build_report(inventory: List[Row], risks: List[Row], incidents: List[Row],
                 as_of: dt.date, limits: Thresholds = Thresholds(),
                 source_note: str = "") -> str:
    findings = check_health(inventory, risks, incidents, as_of, limits)
    counts = {s: sum(1 for f in findings if f.severity == s) for s in SEVERITIES}
    lines = [
        "# Register health report",
        "",
        f"Position as at {long_date(as_of)}. Generated by `tools/register_health.py`; do not edit by hand.",
        "",
    ]
    if source_note:
        lines += [source_note, ""]
    lines += [
        f"Registers read: {len(inventory)} systems, {len(risks)} risks, {len(incidents)} incidents.",
        f"Findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low.",
        "",
        "## Systems at a glance",
        "",
    ]
    lines += table(
        ["System", "Name", "EU tier", "Status", "Open risks", "Top residual", "Open incidents", "Next review"],
        system_summary(inventory, risks, incidents, as_of),
    )
    lines += ["", "## Findings", ""]
    if not findings:
        lines += ["No findings. This says the registers are being kept up to date, not that the risks are low.", ""]
    else:
        lines += table(
            ["Severity", "Rule", "Item", "System", "What needs attention"],
            [[f.severity, f.rule, f.subject, f.system_id, f.message] for f in findings],
        )
        lines.append("")
    lines += [
        "## Windows used",
        "",
        f"- Risk review window: {limits.review_days} days. Accepted risk window: {limits.accepted_days} days.",
        f"- Incident window: {limits.incident_days} days. External reporting decision window: {limits.report_days} days.",
        "",
        "These are working defaults, not legal limits. Set your own with the command line options and record why.",
        "",
        "## What this report cannot tell you",
        "",
        "It checks dates, statuses and links between registers. It cannot tell you whether a rating is well judged, "
        "whether a mitigation works, or whether an incident has been reported when the law requires it. "
        "Take legal advice on reporting duties.",
        "",
    ]
    return "\n".join(lines)


def load_registers(directory: Path):
    return (
        read_register(directory / INVENTORY_FILE, INVENTORY_COLUMNS),
        read_register(directory / RISK_FILE, RISK_COLUMNS),
        read_register(directory / INCIDENT_FILE, INCIDENT_COLUMNS),
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Report register entries that need action on a given date.")
    parser.add_argument("--registers", type=Path, default=DEFAULT_REGISTERS,
                        help="folder holding the three register CSV files (default: the Fernhill example)")
    parser.add_argument("--as-of", type=dt.date.fromisoformat, default=None,
                        help="date to report as at, YYYY-MM-DD (default: today)")
    parser.add_argument("--output", type=Path, help="write the report here instead of printing it")
    parser.add_argument("--check", type=Path,
                        help="fail if this file differs from the report generated for the example registers")
    parser.add_argument("--fail-on", choices=("none",) + SEVERITIES, default="none",
                        help="exit 1 if any finding is at or above this severity (default: never)")
    parser.add_argument("--review-days", type=int, default=Thresholds.review_days)
    parser.add_argument("--accepted-days", type=int, default=Thresholds.accepted_days)
    parser.add_argument("--incident-days", type=int, default=Thresholds.incident_days)
    parser.add_argument("--report-days", type=int, default=Thresholds.report_days)
    args = parser.parse_args(argv)

    limits = Thresholds(args.review_days, args.accepted_days, args.incident_days, args.report_days)
    try:
        if args.check:
            inventory, risks, incidents = load_registers(DEFAULT_REGISTERS)
            expected = build_report(
                inventory, risks, incidents, EXAMPLE_AS_OF, Thresholds(),
                "Example run against the fictional Fernhill registers in `examples/fernhill/`. "
                "The date is fixed so that the output is stable; run the tool with your own registers and today's date.",
            )
            current = args.check.read_text(encoding="utf-8") if args.check.is_file() else None
            if current != expected:
                print(f"STALE   {args.check} is out of date; run: python tools/register_health.py "
                      f"--as-of {EXAMPLE_AS_OF.isoformat()} --output {args.check}", file=sys.stderr)
                return 3
            print(f"OK {args.check} matches the example registers")
            return 0

        as_of = args.as_of or dt.date.today()
        inventory, risks, incidents = load_registers(args.registers)
        note = ""
        if args.registers.resolve() == DEFAULT_REGISTERS.resolve() and as_of == EXAMPLE_AS_OF and limits == Thresholds():
            note = ("Example run against the fictional Fernhill registers in `examples/fernhill/`. "
                    "The date is fixed so that the output is stable; run the tool with your own registers and today's date.")
        report = build_report(inventory, risks, incidents, as_of, limits, note)
        findings = check_health(inventory, risks, incidents, as_of, limits)
    except RegisterError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(report)
        print(f"Wrote {args.output}")
    else:
        sys.stdout.write(report)

    if args.fail_on != "none":
        threshold = SEVERITY_RANK[args.fail_on]
        if any(SEVERITY_RANK[f.severity] <= threshold for f in findings):
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
