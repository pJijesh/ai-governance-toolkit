#!/usr/bin/env python3
"""Validate the toolkit's CSV data and generate the markdown views.

What it does
------------
1. Validates the three framework item files (required columns, ID format, no duplicates).
2. Validates data/control_matrix.csv (required columns, ID format, no duplicates,
   no orphan mappings to framework items, template files exist).
3. Validates the worked-example registers in examples/ and the blank CSV templates
   (enumerated values, scoring arithmetic, cross-references between registers).
4. Checks that relative links in markdown files point at files that exist.
5. Generates docs/control-matrix.md and docs/coverage-report.md.

Standard library only. Python 3.9 or later.

Usage
-----
    python tools/validate_and_report.py            # validate, then write the generated docs
    python tools/validate_and_report.py --check    # validate and fail if generated docs are stale
    python tools/validate_and_report.py --root PATH

Exit codes: 0 success, 1 validation errors, 2 generated documents are out of date (--check).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------- #
# Specifications
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class FrameworkSpec:
    key: str
    label: str
    file: str
    id_pattern: str
    required: Tuple[str, ...]
    matrix_column: str


FRAMEWORKS: Tuple[FrameworkSpec, ...] = (
    FrameworkSpec(
        key="iso",
        label="ISO/IEC 42001:2023",
        file="data/frameworks/iso42001_items.csv",
        id_pattern=r"^(?:(?:[4-9]|10)\.\d{1,2}(?:\.\d{1,2})?|A\.\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)$",
        required=("id", "type", "area", "title", "verification"),
        matrix_column="iso42001_refs",
    ),
    FrameworkSpec(
        key="eu",
        label="EU AI Act (Regulation (EU) 2024/1689)",
        file="data/frameworks/eu_ai_act_items.csv",
        id_pattern=r"^Art \d{1,3}$",
        required=("id", "chapter", "title", "applies_to", "coverage_expected", "verification", "note"),
        matrix_column="eu_ai_act_refs",
    ),
    FrameworkSpec(
        key="nist",
        label="NIST AI RMF 1.0",
        file="data/frameworks/nist_ai_rmf_items.csv",
        id_pattern=r"^(?:GOVERN|MAP|MEASURE|MANAGE) \d{1,2}\.\d{1,2}$",
        required=("id", "function", "category", "title", "verification"),
        matrix_column="nist_ai_rmf_refs",
    ),
)

MATRIX_FILE = "data/control_matrix.csv"
MATRIX_REQUIRED = (
    "control_id",
    "domain",
    "control_name",
    "objective",
    "iso42001_refs",
    "eu_ai_act_refs",
    "nist_ai_rmf_refs",
    "suggested_owner",
    "evidence_examples",
    "template",
)
CONTROL_ID_PATTERN = r"^TK-(GOV|INV|RSK|LIF|DAT|USE|THR|INC|CON)-\d{2}$"
DOMAIN_CODES = {
    "GOV": "Governance",
    "INV": "Inventory and classification",
    "RSK": "Risk and impact",
    "LIF": "Lifecycle",
    "DAT": "Data",
    "USE": "Responsible use and transparency",
    "THR": "Third parties",
    "INC": "Incidents and monitoring",
    "CON": "Provider conformity",
}
VERIFICATION_VALUES = {"secondary-checked", "unchecked"}
YES_NO = {"yes", "no"}

# Register specifications --------------------------------------------------- #

INVENTORY_REQUIRED = (
    "system_id", "name", "description", "business_owner", "technical_owner", "vendor",
    "source_type", "purpose", "affected_people", "personal_data", "eu_ai_act_role",
    "eu_risk_tier", "annex_area", "internal_risk_rating", "human_oversight",
    "impact_assessment_ref", "status", "go_live_date", "next_review_date", "notes",
)
RISK_REQUIRED = (
    "risk_id", "system_id", "risk_title", "description", "category", "likelihood", "impact",
    "inherent_score", "inherent_rating", "existing_controls", "treatment", "treatment_actions",
    "risk_owner", "target_date", "residual_likelihood", "residual_impact", "residual_score",
    "residual_rating", "status", "last_reviewed",
)
INCIDENT_REQUIRED = (
    "incident_id", "system_id", "date_detected", "description", "category", "severity",
    "affected_people", "immediate_action", "root_cause", "corrective_action", "related_controls",
    "reportable_externally", "external_report_date", "status", "closed_date", "lessons",
)

BLANK_TEMPLATES = {
    "templates/ai-system-inventory.csv": INVENTORY_REQUIRED,
    "templates/ai-risk-register.csv": RISK_REQUIRED,
    "templates/ai-incident-log.csv": INCIDENT_REQUIRED,
}
EXAMPLE_DIR = "examples/fernhill"
INVENTORY_EXAMPLE = f"{EXAMPLE_DIR}/ai-system-inventory.csv"
RISK_EXAMPLE = f"{EXAMPLE_DIR}/ai-risk-register.csv"
INCIDENT_EXAMPLE = f"{EXAMPLE_DIR}/ai-incident-log.csv"

ENUMS = {
    "source_type": {"bought", "built", "embedded", "open-source", "hybrid"},
    "personal_data": {"yes", "no", "unknown"},
    "eu_ai_act_role": {"deployer", "provider", "provider-and-deployer", "importer", "distributor", "not-assessed"},
    "eu_risk_tier": {"prohibited", "high-risk", "high-risk-provisional", "transparency", "minimal", "not-assessed"},
    "internal_risk_rating": {"low", "medium", "high", "critical", "not-assessed"},
    "inventory_status": {"proposed", "pilot", "live", "suspended", "retired"},
    "risk_category": {
        "bias-fairness", "privacy", "security", "accuracy-reliability", "transparency",
        "legal-regulatory", "third-party", "operational", "misuse", "human-oversight",
    },
    "treatment": {"mitigate", "accept", "transfer", "avoid"},
    "risk_status": {"open", "mitigating", "accepted", "closed"},
    "incident_category": {
        "harmful-output", "bias-discrimination", "data-leak", "security-breach",
        "outage", "misuse", "drift-degradation", "other",
    },
    "severity": {"low", "medium", "high", "critical"},
    "reportable": {"yes", "no", "under-assessment"},
    "incident_status": {"open", "investigating", "closed"},
}

SYSTEM_ID_RE = re.compile(r"^[A-Z]{2,6}-AI-\d{3}$")
RISK_ID_RE = re.compile(r"^[A-Z]{2,6}-R-\d{3}$")
INCIDENT_ID_RE = re.compile(r"^[A-Z]{2,6}-INC-\d{3}$")

GENERATED_FILES = ("docs/control-matrix.md", "docs/coverage-report.md")

# --------------------------------------------------------------------------- #
# Issue collection and CSV helpers
# --------------------------------------------------------------------------- #


@dataclass
class Issues:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def error(self, where: str, message: str) -> None:
        self.errors.append(f"{where}: {message}")

    def warn(self, where: str, message: str) -> None:
        self.warnings.append(f"{where}: {message}")


Row = Dict[str, str]


def read_table(root: Path, rel: str, required: Sequence[str], issues: Issues,
               exact_header: bool = False) -> List[Row]:
    """Read a CSV file. Returns rows (each with a '_line' key). Records issues on problems."""
    path = root / rel
    if not path.is_file():
        issues.error(rel, "file not found")
        return []
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            try:
                header = [h.strip() for h in next(reader)]
            except StopIteration:
                issues.error(rel, "file is empty")
                return []
            missing = [c for c in required if c not in header]
            extra = [c for c in header if c not in required]
            if missing:
                issues.error(rel, f"missing required column(s): {', '.join(missing)}")
                return []
            if exact_header and list(header) != list(required):
                issues.error(rel, "header does not match the expected columns and order")
            elif extra:
                issues.warn(rel, f"unexpected extra column(s): {', '.join(extra)}")
            dupes = sorted({h for h in header if header.count(h) > 1})
            if dupes:
                issues.error(rel, f"duplicate column name(s): {', '.join(dupes)}")
                return []
            rows: List[Row] = []
            for line_no, raw in enumerate(reader, start=2):
                if not any(cell.strip() for cell in raw):
                    continue
                if len(raw) != len(header):
                    issues.error(rel, f"line {line_no} has {len(raw)} fields but the header has {len(header)}")
                    continue
                row = {h: v.strip() for h, v in zip(header, raw)}
                row["_line"] = str(line_no)
                rows.append(row)
            return rows
    except UnicodeDecodeError:
        issues.error(rel, "file is not valid UTF-8")
        return []


def check_unique(rows: Sequence[Row], column: str, rel: str, issues: Issues) -> None:
    seen: Dict[str, str] = {}
    for row in rows:
        value = row.get(column, "")
        if not value:
            issues.error(rel, f"line {row['_line']}: empty {column}")
            continue
        if value in seen:
            issues.error(rel, f"line {row['_line']}: duplicate {column} '{value}' (first seen on line {seen[value]})")
        else:
            seen[value] = row["_line"]


def split_refs(cell: str) -> List[str]:
    return [part.strip() for part in cell.split(";") if part.strip()]


def parse_date(value: str) -> Optional[dt.date]:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #


def validate_frameworks(root: Path, issues: Issues) -> Dict[str, List[Row]]:
    loaded: Dict[str, List[Row]] = {}
    for spec in FRAMEWORKS:
        rows = read_table(root, spec.file, spec.required, issues)
        loaded[spec.key] = rows
        pattern = re.compile(spec.id_pattern)
        check_unique(rows, "id", spec.file, issues)
        for row in rows:
            where = f"{spec.file}"
            if row["id"] and not pattern.match(row["id"]):
                issues.error(where, f"line {row['_line']}: id '{row['id']}' does not match the expected format")
            if not row["title"]:
                issues.error(where, f"line {row['_line']}: empty title")
            if row["verification"] not in VERIFICATION_VALUES:
                issues.error(where, f"line {row['_line']}: verification must be one of {sorted(VERIFICATION_VALUES)}")
            if spec.key == "eu" and row["coverage_expected"] not in YES_NO:
                issues.error(where, f"line {row['_line']}: coverage_expected must be yes or no")
            if spec.key == "iso" and row["type"] not in {"clause", "annex_a_control"}:
                issues.error(where, f"line {row['_line']}: type must be clause or annex_a_control")
            if spec.key == "nist" and row["id"] and not row["id"].startswith(row["function"] + " "):
                issues.error(where, f"line {row['_line']}: id '{row['id']}' does not belong to function '{row['function']}'")
    return loaded


def validate_matrix(root: Path, frameworks: Dict[str, List[Row]], issues: Issues) -> List[Row]:
    rows = read_table(root, MATRIX_FILE, MATRIX_REQUIRED, issues)
    check_unique(rows, "control_id", MATRIX_FILE, issues)
    known = {spec.key: {r["id"] for r in frameworks.get(spec.key, [])} for spec in FRAMEWORKS}
    id_re = re.compile(CONTROL_ID_PATTERN)
    for row in rows:
        loc = f"line {row['_line']}"
        cid = row["control_id"]
        match = id_re.match(cid)
        if cid and not match:
            issues.error(MATRIX_FILE, f"{loc}: control_id '{cid}' does not match TK-XXX-NN with a known domain code")
        elif match and DOMAIN_CODES[match.group(1)] != row["domain"]:
            issues.error(MATRIX_FILE, f"{loc}: domain '{row['domain']}' does not match the code in {cid}")
        for column in ("control_name", "objective", "suggested_owner", "evidence_examples"):
            if not row[column]:
                issues.error(MATRIX_FILE, f"{loc}: empty {column}")
        total_refs = 0
        for spec in FRAMEWORKS:
            refs = split_refs(row[spec.matrix_column])
            total_refs += len(refs)
            if len(set(refs)) != len(refs):
                issues.error(MATRIX_FILE, f"{loc}: duplicate reference in {spec.matrix_column}")
            for ref in refs:
                if ref not in known[spec.key]:
                    issues.error(MATRIX_FILE, f"{loc}: orphan mapping '{ref}' in {spec.matrix_column} (not in {spec.file})")
        if total_refs == 0:
            issues.error(MATRIX_FILE, f"{loc}: {cid} maps to no framework item")
        template = row["template"]
        if not template:
            issues.warn(MATRIX_FILE, f"{loc}: {cid} has no template or guidance file")
        elif not (root / template).is_file():
            issues.error(MATRIX_FILE, f"{loc}: template '{template}' does not exist")
    return rows


def _enum(row: Row, column: str, allowed: set, rel: str, issues: Issues, allow_empty: bool = False) -> None:
    value = row.get(column, "")
    if not value and allow_empty:
        return
    if value not in allowed:
        issues.error(rel, f"line {row['_line']}: {column} '{value}' is not one of {sorted(allowed)}")


def _date(row: Row, column: str, rel: str, issues: Issues, required: bool = True) -> Optional[dt.date]:
    value = row.get(column, "")
    if not value:
        if required:
            issues.error(rel, f"line {row['_line']}: {column} is required")
        return None
    parsed = parse_date(value)
    if parsed is None:
        issues.error(rel, f"line {row['_line']}: {column} '{value}' is not an ISO date (YYYY-MM-DD)")
    return parsed


def rating_for(score: int) -> str:
    if score <= 4:
        return "low"
    if score <= 9:
        return "medium"
    if score <= 16:
        return "high"
    return "critical"


def validate_inventory(root: Path, issues: Issues) -> List[Row]:
    rel = INVENTORY_EXAMPLE
    rows = read_table(root, rel, INVENTORY_REQUIRED, issues)
    check_unique(rows, "system_id", rel, issues)
    for row in rows:
        loc = f"line {row['_line']}"
        if row["system_id"] and not SYSTEM_ID_RE.match(row["system_id"]):
            issues.error(rel, f"{loc}: system_id '{row['system_id']}' does not match the pattern XX-AI-000")
        for column in ("name", "description", "business_owner", "purpose", "affected_people"):
            if not row[column]:
                issues.error(rel, f"{loc}: empty {column}")
        _enum(row, "source_type", ENUMS["source_type"], rel, issues)
        _enum(row, "personal_data", ENUMS["personal_data"], rel, issues)
        _enum(row, "eu_ai_act_role", ENUMS["eu_ai_act_role"], rel, issues)
        _enum(row, "eu_risk_tier", ENUMS["eu_risk_tier"], rel, issues)
        _enum(row, "internal_risk_rating", ENUMS["internal_risk_rating"], rel, issues)
        _enum(row, "status", ENUMS["inventory_status"], rel, issues)
        go_live = _date(row, "go_live_date", rel, issues, required=row["status"] in {"live", "pilot", "suspended"})
        review = _date(row, "next_review_date", rel, issues, required=row["status"] != "retired")
        if go_live and review and review < go_live:
            issues.error(rel, f"{loc}: next_review_date is before go_live_date")
        if row["eu_risk_tier"].startswith("high-risk"):
            if not row["annex_area"]:
                issues.error(rel, f"{loc}: a high-risk tier needs an annex_area (Annex III point or Annex I)")
            if not row["impact_assessment_ref"]:
                issues.error(rel, f"{loc}: a high-risk tier needs an impact_assessment_ref")
        if row["status"] in {"live", "pilot"} and not row["human_oversight"]:
            issues.error(rel, f"{loc}: live or pilot systems need a human_oversight description")
    return rows


def _check_scores(row: Row, prefix: str, rel: str, issues: Issues) -> None:
    loc = f"line {row['_line']}"
    lik_col = "likelihood" if prefix == "inherent" else "residual_likelihood"
    imp_col = "impact" if prefix == "inherent" else "residual_impact"
    score_col = f"{prefix}_score"
    rating_col = f"{prefix}_rating"
    try:
        lik, imp, score = int(row[lik_col]), int(row[imp_col]), int(row[score_col])
    except ValueError:
        issues.error(rel, f"{loc}: {lik_col}, {imp_col} and {score_col} must be whole numbers")
        return
    if not (1 <= lik <= 5 and 1 <= imp <= 5):
        issues.error(rel, f"{loc}: {lik_col} and {imp_col} must be between 1 and 5")
        return
    if score != lik * imp:
        issues.error(rel, f"{loc}: {score_col} is {score} but {lik_col} x {imp_col} is {lik * imp}")
    if row[rating_col] != rating_for(lik * imp):
        issues.error(rel, f"{loc}: {rating_col} should be '{rating_for(lik * imp)}' for a score of {lik * imp}")


def validate_risk_register(root: Path, system_ids: set, control_ids: set, issues: Issues) -> List[Row]:
    rel = RISK_EXAMPLE
    rows = read_table(root, rel, RISK_REQUIRED, issues)
    check_unique(rows, "risk_id", rel, issues)
    for row in rows:
        loc = f"line {row['_line']}"
        if row["risk_id"] and not RISK_ID_RE.match(row["risk_id"]):
            issues.error(rel, f"{loc}: risk_id '{row['risk_id']}' does not match the pattern XX-R-000")
        if row["system_id"] not in system_ids:
            issues.error(rel, f"{loc}: system_id '{row['system_id']}' is not in the inventory (orphan risk)")
        for column in ("risk_title", "description", "risk_owner", "treatment_actions"):
            if not row[column]:
                issues.error(rel, f"{loc}: empty {column}")
        _enum(row, "category", ENUMS["risk_category"], rel, issues)
        _enum(row, "treatment", ENUMS["treatment"], rel, issues)
        _enum(row, "status", ENUMS["risk_status"], rel, issues)
        _check_scores(row, "inherent", rel, issues)
        _check_scores(row, "residual", rel, issues)
        try:
            if int(row["residual_score"]) > int(row["inherent_score"]):
                issues.warn(rel, f"{loc}: residual score is higher than inherent score")
        except ValueError:
            pass
        for ref in split_refs(row["existing_controls"]):
            if ref not in control_ids:
                issues.error(rel, f"{loc}: existing_controls references unknown control '{ref}'")
        _date(row, "target_date", rel, issues)
        _date(row, "last_reviewed", rel, issues)
    return rows


def validate_incident_log(root: Path, system_ids: set, control_ids: set, issues: Issues) -> List[Row]:
    rel = INCIDENT_EXAMPLE
    rows = read_table(root, rel, INCIDENT_REQUIRED, issues)
    check_unique(rows, "incident_id", rel, issues)
    for row in rows:
        loc = f"line {row['_line']}"
        if row["incident_id"] and not INCIDENT_ID_RE.match(row["incident_id"]):
            issues.error(rel, f"{loc}: incident_id '{row['incident_id']}' does not match the pattern XX-INC-000")
        if row["system_id"] not in system_ids:
            issues.error(rel, f"{loc}: system_id '{row['system_id']}' is not in the inventory (orphan incident)")
        if not row["description"]:
            issues.error(rel, f"{loc}: empty description")
        _enum(row, "category", ENUMS["incident_category"], rel, issues)
        _enum(row, "severity", ENUMS["severity"], rel, issues)
        _enum(row, "reportable_externally", ENUMS["reportable"], rel, issues)
        _enum(row, "status", ENUMS["incident_status"], rel, issues)
        detected = _date(row, "date_detected", rel, issues)
        closed = _date(row, "closed_date", rel, issues, required=row["status"] == "closed")
        reported = _date(row, "external_report_date", rel, issues, required=row["reportable_externally"] == "yes")
        if detected and closed and closed < detected:
            issues.error(rel, f"{loc}: closed_date is before date_detected")
        if detected and reported and reported < detected:
            issues.error(rel, f"{loc}: external_report_date is before date_detected")
        if row["status"] == "closed" and not row["corrective_action"]:
            issues.error(rel, f"{loc}: a closed incident needs a corrective_action")
        for ref in split_refs(row["related_controls"]):
            if ref not in control_ids:
                issues.error(rel, f"{loc}: related_controls references unknown control '{ref}'")
    return rows


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def check_markdown_links(root: Path, issues: Issues) -> int:
    """Check relative links in markdown files. Returns the number of links checked."""
    checked = 0
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") and part != ".github" for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        # Ignore fenced code blocks so that examples are not treated as links.
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            checked += 1
            if not (path.parent / file_part).resolve().exists():
                issues.error(str(path.relative_to(root)), f"broken relative link '{target}'")
    return checked


def validate_blank_templates(root: Path, issues: Issues) -> None:
    for rel, columns in BLANK_TEMPLATES.items():
        rows = read_table(root, rel, columns, issues, exact_header=True)
        if rows:
            issues.warn(rel, "blank template contains data rows; it should hold the header only")


# --------------------------------------------------------------------------- #
# Coverage analysis
# --------------------------------------------------------------------------- #


@dataclass
class FrameworkCoverage:
    spec: FrameworkSpec
    items: List[Row]
    mapped: Dict[str, List[str]]  # item id -> control ids
    expected: List[Row]
    excluded: List[Row]
    unmapped_expected: List[Row]
    single_control: List[Row]

    @property
    def mapped_expected_count(self) -> int:
        return len(self.expected) - len(self.unmapped_expected)

    @property
    def percent(self) -> str:
        if not self.expected:
            return "n/a"
        return f"{100 * self.mapped_expected_count / len(self.expected):.0f}%"


def compute_coverage(frameworks: Dict[str, List[Row]], controls: List[Row]) -> List[FrameworkCoverage]:
    result = []
    for spec in FRAMEWORKS:
        items = frameworks.get(spec.key, [])
        mapped: Dict[str, List[str]] = {r["id"]: [] for r in items}
        for control in controls:
            for ref in split_refs(control[spec.matrix_column]):
                if ref in mapped:
                    mapped[ref].append(control["control_id"])
        if spec.key == "eu":
            expected = [r for r in items if r["coverage_expected"] == "yes"]
            excluded = [r for r in items if r["coverage_expected"] != "yes"]
        else:
            expected, excluded = list(items), []
        unmapped = [r for r in expected if not mapped[r["id"]]]
        single = [r for r in expected if len(mapped[r["id"]]) == 1]
        result.append(FrameworkCoverage(spec, items, mapped, expected, excluded, unmapped, single))
    return result


# --------------------------------------------------------------------------- #
# Markdown generation
# --------------------------------------------------------------------------- #

GENERATED_NOTICE = (
    "<!-- Generated by tools/validate_and_report.py from the CSV files in data/. "
    "Do not edit by hand; edit the CSV and run the tool again. -->"
)


def rel_link(target: str, from_dir: str) -> str:
    """Return a relative link from a file in `from_dir` to `target` (both repo-relative)."""
    from_parts = [p for p in from_dir.split("/") if p]
    target_parts = target.split("/")
    common = 0
    while common < len(from_parts) and common < len(target_parts) - 1 and from_parts[common] == target_parts[common]:
        common += 1
    return "/".join([".."] * (len(from_parts) - common) + target_parts[common:])


def md_cell(text: str) -> str:
    return text.replace("|", "\\|")


def build_matrix_markdown(frameworks: Dict[str, List[Row]], controls: List[Row]) -> str:
    coverage = compute_coverage(frameworks, controls)
    titles = {spec.key: {r["id"]: r["title"] for r in frameworks.get(spec.key, [])} for spec in FRAMEWORKS}
    lines: List[str] = [
        GENERATED_NOTICE,
        "",
        "# Control matrix (generated view)",
        "",
        "This page is generated from [`data/control_matrix.csv`](../data/control_matrix.csv), which is the source of truth. "
        "It links each toolkit control to related items in ISO/IEC 42001:2023, the EU AI Act and the NIST AI RMF 1.0.",
        "",
        "Read the mappings as \"related to\", not \"equivalent to\". They are the author's professional judgement and are not an official crosswalk. "
        "Control names and item titles are paraphrased. See [sources and verification](sources-and-verification.md) before relying on any identifier. "
        "This is not legal advice.",
        "",
        f"The matrix holds {len(controls)} controls across {len({c['domain'] for c in controls})} domains.",
        "",
        "## 1. Control library",
        "",
    ]
    domains: List[str] = []
    for control in controls:
        if control["domain"] not in domains:
            domains.append(control["domain"])
    for domain in domains:
        lines += [f"### {domain}", "", "| Control | Name | ISO/IEC 42001 | EU AI Act | NIST AI RMF | Guidance |", "|---|---|---|---|---|---|"]
        for c in (c for c in controls if c["domain"] == domain):
            template = c["template"]
            link = f"[{Path(template).name}]({rel_link(template, 'docs')})" if template else ""
            lines.append(
                f"| {c['control_id']} | {md_cell(c['control_name'])} | {md_cell(', '.join(split_refs(c['iso42001_refs'])))} "
                f"| {md_cell(', '.join(split_refs(c['eu_ai_act_refs'])))} | {md_cell(', '.join(split_refs(c['nist_ai_rmf_refs'])))} | {link} |"
            )
        lines.append("")
    for number, cov in enumerate(coverage, start=2):
        lines += [f"## {number}. Reverse view: {cov.spec.label}", "", "| Item | Title (paraphrased) | Mapped controls |", "|---|---|---|"]
        for item in cov.items:
            ids = cov.mapped[item["id"]]
            shown = ", ".join(ids) if ids else "none"
            lines.append(f"| {item['id']} | {md_cell(titles[cov.spec.key][item['id']])} | {shown} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_coverage_markdown(frameworks: Dict[str, List[Row]], controls: List[Row]) -> str:
    coverage = compute_coverage(frameworks, controls)
    lines: List[str] = [
        GENERATED_NOTICE,
        "",
        "# Coverage report (sample output)",
        "",
        "This report is produced by `python tools/validate_and_report.py` from the files in `data/`. "
        "\"Mapped\" means at least one toolkit control relates to the item. It does not mean the item is satisfied in any organisation. "
        "Actual conformity depends on how controls are implemented and evidenced.",
        "",
        "## Summary",
        "",
        "| Framework | Items | In scope for coverage | Mapped | Unmapped | Coverage |",
        "|---|---|---|---|---|---|",
    ]
    for cov in coverage:
        lines.append(
            f"| {cov.spec.label} | {len(cov.items)} | {len(cov.expected)} | {cov.mapped_expected_count} "
            f"| {len(cov.unmapped_expected)} | {cov.percent} |"
        )
    lines += ["", f"Controls in the library: {len(controls)}.", ""]
    for cov in coverage:
        lines += [f"## {cov.spec.label}", "", "### Items with no mapped control", ""]
        if cov.unmapped_expected:
            lines += ["| Item | Title (paraphrased) |", "|---|---|"]
            lines += [f"| {r['id']} | {md_cell(r['title'])} |" for r in cov.unmapped_expected]
        else:
            lines.append("None. Every in-scope item has at least one mapped control.")
        lines.append("")
        if cov.excluded:
            lines += ["### Items excluded from coverage by design", "", "| Item | Title (paraphrased) | Reason |", "|---|---|---|"]
            lines += [f"| {r['id']} | {md_cell(r['title'])} | {md_cell(r['note'] or r['applies_to'])} |" for r in cov.excluded]
            lines.append("")
        lines += ["### Items supported by only one control", ""]
        if cov.single_control:
            lines.append(", ".join(f"{r['id']} ({cov.mapped[r['id']][0]})" for r in cov.single_control))
        else:
            lines.append("None.")
        lines.append("")
    # Control-level observations
    domain_counts: Dict[str, int] = {}
    for c in controls:
        domain_counts[c["domain"]] = domain_counts.get(c["domain"], 0) + 1
    lines += ["## Control library observations", "", "### Controls per domain", "", "| Domain | Controls |", "|---|---|"]
    lines += [f"| {d} | {n} |" for d, n in domain_counts.items()]
    lines.append("")
    no_eu = [c["control_id"] for c in controls if not split_refs(c["eu_ai_act_refs"])]
    no_iso = [c["control_id"] for c in controls if not split_refs(c["iso42001_refs"])]
    no_nist = [c["control_id"] for c in controls if not split_refs(c["nist_ai_rmf_refs"])]
    lines += [
        "### Controls with no mapping in a framework",
        "",
        f"- No ISO/IEC 42001 reference: {', '.join(no_iso) if no_iso else 'none'}",
        f"- No EU AI Act reference: {', '.join(no_eu) if no_eu else 'none'}",
        f"- No NIST AI RMF reference: {', '.join(no_nist) if no_nist else 'none'}",
        "",
        "A control without a reference in one framework is not an error. Some good practice has no direct counterpart in a given framework.",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #


@dataclass
class RunResult:
    issues: Issues
    frameworks: Dict[str, List[Row]]
    controls: List[Row]
    generated: Dict[str, str]
    stale: List[str]
    links_checked: int = 0


def run(root: Path, write: bool = True, check: bool = False) -> RunResult:
    issues = Issues()
    frameworks = validate_frameworks(root, issues)
    controls = validate_matrix(root, frameworks, issues)
    control_ids = {c["control_id"] for c in controls}
    inventory = validate_inventory(root, issues)
    system_ids = {r["system_id"] for r in inventory}
    validate_risk_register(root, system_ids, control_ids, issues)
    validate_incident_log(root, system_ids, control_ids, issues)
    validate_blank_templates(root, issues)

    generated: Dict[str, str] = {}
    stale: List[str] = []
    if not issues.errors:
        generated["docs/control-matrix.md"] = build_matrix_markdown(frameworks, controls)
        generated["docs/coverage-report.md"] = build_coverage_markdown(frameworks, controls)
        for rel, text in generated.items():
            path = root / rel
            if check:
                current = path.read_text(encoding="utf-8") if path.is_file() else None
                if current != text:
                    stale.append(rel)
            elif write:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("w", encoding="utf-8", newline="\n") as handle:
                    handle.write(text)
    # Links are checked last so that links to the generated documents resolve on a first run.
    links_checked = check_markdown_links(root, issues)
    return RunResult(issues, frameworks, controls, generated, stale, links_checked)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate toolkit CSVs and generate markdown views.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: parent of tools/)")
    parser.add_argument("--check", action="store_true",
                        help="do not write; fail if generated documents differ from the CSV data")
    args = parser.parse_args(argv)

    result = run(args.root, write=not args.check, check=args.check)
    for warning in result.issues.warnings:
        print(f"WARNING {warning}")
    for error in result.issues.errors:
        print(f"ERROR   {error}")

    counts = ", ".join(f"{spec.label}: {len(result.frameworks.get(spec.key, []))}" for spec in FRAMEWORKS)
    print(f"Framework items loaded ({counts}); controls: {len(result.controls)}; "
          f"markdown links checked: {result.links_checked}")
    if result.issues.errors:
        print(f"FAILED with {len(result.issues.errors)} error(s) and {len(result.issues.warnings)} warning(s).")
        return 1
    if result.stale:
        for rel in result.stale:
            print(f"STALE   {rel} is out of date; run: python tools/validate_and_report.py")
        return 2
    action = "verified up to date" if args.check else "written"
    print(f"OK ({len(result.issues.warnings)} warning(s)). Generated documents {action}: {', '.join(GENERATED_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
