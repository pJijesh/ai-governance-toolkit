"""Tests for tools/register_health.py.

Run from the repository root with either of:

    python -m unittest discover -s tests -v
    python -m pytest tests
"""

import datetime as dt
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import register_health as rh  # noqa: E402

D = dt.date


def system(sid="XX-AI-001", status="live", tier="minimal", review="2027-06-01", name="Test system"):
    return {"system_id": sid, "name": name, "eu_risk_tier": tier, "status": status, "next_review_date": review}


def risk(rid="XX-R-001", sid="XX-AI-001", category="privacy", rating="medium", status="mitigating",
         target="2027-06-01", reviewed="2026-12-01"):
    return {"risk_id": rid, "system_id": sid, "category": category, "residual_rating": rating,
            "status": status, "target_date": target, "last_reviewed": reviewed}


def incident(iid="XX-INC-001", sid="XX-AI-001", detected="2026-12-01", category="data-leak",
             severity="low", reportable="no", status="closed"):
    return {"incident_id": iid, "system_id": sid, "date_detected": detected, "category": category,
            "severity": severity, "reportable_externally": reportable, "status": status}


def rules(findings):
    return [f.rule for f in findings]


def run(inventory, risks, incidents, as_of=D(2027, 1, 1), limits=rh.Thresholds()):
    return rh.check_health(inventory, risks, incidents, as_of, limits)


class CleanRegistersTests(unittest.TestCase):
    def test_up_to_date_registers_give_no_findings(self):
        self.assertEqual(run([system()], [risk()], [incident()]), [])

    def test_retired_system_is_not_reviewed(self):
        findings = run([system(status="retired", review="2020-01-01")], [], [])
        self.assertEqual(findings, [])


class SystemRuleTests(unittest.TestCase):
    def test_overdue_review_is_flagged(self):
        findings = run([system(review="2026-12-01")], [risk()], [])
        self.assertEqual(rules(findings), ["RH01"])
        self.assertEqual(findings[0].severity, "medium")
        self.assertIn("31 days ago", findings[0].message)

    def test_overdue_review_is_raised_for_high_risk_tier(self):
        findings = run([system(review="2026-12-01", tier="high-risk")], [risk()], [])
        self.assertEqual(findings[0].severity, "high")
        findings = run([system(review="2026-12-01", tier="high-risk-provisional")], [risk()], [])
        self.assertEqual(findings[0].severity, "high")

    def test_review_due_today_is_not_overdue(self):
        self.assertEqual(run([system(review="2027-01-01")], [risk()], []), [])

    def test_live_system_without_open_risk_is_flagged(self):
        findings = run([system()], [], [])
        self.assertEqual(rules(findings), ["RH02"])

    def test_closed_risk_does_not_count_as_open(self):
        findings = run([system()], [risk(status="closed")], [])
        self.assertEqual(rules(findings), ["RH02"])

    def test_proposed_system_without_risk_is_not_flagged(self):
        self.assertEqual(run([system(status="proposed")], [], []), [])


class RiskRuleTests(unittest.TestCase):
    def test_past_target_date_is_flagged(self):
        findings = run([system()], [risk(target="2026-12-15")], [])
        self.assertEqual(rules(findings), ["RH03"])
        self.assertIn("17 days ago", findings[0].message)

    def test_closed_or_accepted_risk_past_target_is_not_flagged(self):
        for status in ("closed", "accepted"):
            findings = run([system()], [risk(status=status, target="2026-01-01", reviewed="2026-12-01"),
                                        risk(rid="XX-R-002")], [])
            self.assertNotIn("RH03", rules(findings), status)

    def test_stale_review_is_flagged_after_the_window(self):
        findings = run([system()], [risk(reviewed="2026-09-01")], [])
        self.assertEqual(rules(findings), ["RH04"])
        # exactly on the window is still inside it
        on_edge = run([system()], [risk(reviewed="2026-10-03")], [])
        self.assertEqual(on_edge, [])

    def test_serious_residual_rating_is_flagged_and_bumps_other_findings(self):
        findings = run([system()], [risk(rating="high", target="2026-12-15", reviewed="2026-09-01")], [])
        by_rule = {f.rule: f.severity for f in findings}
        self.assertEqual(by_rule, {"RH03": "high", "RH04": "medium", "RH05": "high"})

    def test_closed_serious_risk_is_not_flagged(self):
        self.assertNotIn("RH05", rules(run([system()], [risk(rating="critical", status="closed"), risk(rid="XX-R-002")], [])))

    def test_accepted_risk_must_be_reconfirmed(self):
        old = risk(status="accepted", reviewed="2026-05-01")
        findings = run([system()], [old, risk(rid="XX-R-002")], [])
        self.assertEqual(rules(findings), ["RH06"])
        fresh = risk(status="accepted", reviewed="2026-11-01")
        self.assertEqual(run([system()], [fresh, risk(rid="XX-R-002")], []), [])


class IncidentRuleTests(unittest.TestCase):
    def test_old_open_incident_is_flagged(self):
        findings = run([system()], [risk()], [incident(status="investigating", detected="2026-11-01")])
        self.assertEqual(rules(findings), ["RH07"])
        self.assertEqual(findings[0].severity, "medium")

    def test_serious_open_incident_is_raised(self):
        findings = run([system()], [risk()], [incident(status="open", detected="2026-11-01", severity="critical")])
        self.assertEqual(findings[0].severity, "high")

    def test_recent_open_incident_is_not_flagged(self):
        self.assertEqual(run([system()], [risk()], [incident(status="open", detected="2026-12-20")]), [])

    def test_reporting_decision_left_under_assessment_is_flagged(self):
        findings = run([system()], [risk()], [incident(reportable="under-assessment", detected="2026-12-01", status="closed")])
        self.assertEqual(rules(findings), ["RH08"])
        self.assertEqual(findings[0].severity, "high")

    def test_recent_reporting_assessment_is_not_flagged(self):
        findings = run([system()], [risk()], [incident(reportable="under-assessment", detected="2026-12-25")])
        self.assertEqual(findings, [])

    def test_incident_without_matching_risk_category_is_flagged(self):
        findings = run([system()], [risk(category="transparency")], [incident(category="data-leak")])
        self.assertEqual(rules(findings), ["RH09"])
        self.assertIn("privacy or security", findings[0].message)

    def test_matching_risk_category_satisfies_the_incident(self):
        self.assertEqual(run([system()], [risk(category="security")], [incident(category="data-leak")]), [])

    def test_other_incident_category_is_not_mapped(self):
        self.assertEqual(run([system()], [risk()], [incident(category="other")]), [])


class ThresholdAndOrderTests(unittest.TestCase):
    def test_custom_windows_change_the_result(self):
        reviewed = risk(reviewed="2026-11-15")
        self.assertEqual(run([system()], [reviewed], []), [])
        tight = rh.Thresholds(review_days=30)
        self.assertEqual(rules(run([system()], [reviewed], [], limits=tight)), ["RH04"])

    def test_findings_are_sorted_most_severe_first(self):
        findings = run(
            [system(review="2026-12-01")],
            [risk(target="2026-12-15")],
            [incident(reportable="under-assessment", detected="2026-12-01")],
        )
        ranks = [rh.SEVERITY_RANK[f.severity] for f in findings]
        self.assertEqual(ranks, sorted(ranks))
        self.assertEqual(findings[0].severity, "high")


class ReadingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def test_missing_file_is_an_error(self):
        with self.assertRaises(rh.RegisterError) as ctx:
            rh.read_register(self.dir / "nope.csv", ("a",))
        self.assertIn("file not found", str(ctx.exception))

    def test_missing_column_is_an_error(self):
        path = self.dir / "r.csv"
        path.write_text("a,b\n1,2\n", encoding="utf-8")
        with self.assertRaises(rh.RegisterError) as ctx:
            rh.read_register(path, ("a", "c"))
        self.assertIn("missing column(s): c", str(ctx.exception))

    def test_blank_lines_are_ignored_and_values_trimmed(self):
        path = self.dir / "r.csv"
        path.write_text("a,b\n 1 , x \n,\n", encoding="utf-8")
        self.assertEqual(rh.read_register(path, ("a", "b")), [{"a": "1", "b": "x"}])

    def test_bad_date_is_an_error(self):
        with self.assertRaises(rh.RegisterError):
            rh.parse_date("01/02/2027", "x")
        with self.assertRaises(rh.RegisterError):
            rh.parse_date("", "x")
        self.assertIsNone(rh.parse_date("", "x", optional=True))


class CommandLineTests(unittest.TestCase):
    def call(self, args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = rh.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_example_report_is_current(self):
        code, out, err = self.call(["--check", str(rh.EXAMPLE_REPORT)])
        self.assertEqual(code, 0, msg=err)

    def test_stale_example_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "old.md"
            path.write_text("old", encoding="utf-8")
            code, _, err = self.call(["--check", str(path)])
        self.assertEqual(code, 3)
        self.assertIn("STALE", err)

    def test_report_prints_for_the_example_registers(self):
        code, out, _ = self.call(["--as-of", "2026-12-20"])
        self.assertEqual(code, 0)
        self.assertIn("# Register health report", out)
        self.assertIn("FH-INC-003", out)

    def test_fail_on_high_exits_one_when_a_high_finding_exists(self):
        code, _, _ = self.call(["--as-of", "2026-12-20", "--fail-on", "high"])
        self.assertEqual(code, 1)

    def test_fail_on_high_exits_zero_when_nothing_is_high(self):
        code, _, _ = self.call(["--as-of", "2026-10-20", "--fail-on", "high"])
        self.assertEqual(code, 0)

    def test_unreadable_registers_exit_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = self.call(["--registers", tmp])
        self.assertEqual(code, 2)
        self.assertIn("ERROR", err)

    def test_output_file_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "sub" / "report.md"
            code, out, _ = self.call(["--as-of", "2026-12-20", "--output", str(target)])
            self.assertEqual(code, 0)
            self.assertTrue(target.read_text(encoding="utf-8").startswith("# Register health report"))

    def test_report_with_no_findings_says_what_that_does_not_mean(self):
        report = rh.build_report([system()], [risk()], [], D(2027, 1, 1))
        self.assertIn("No findings.", report)
        self.assertIn("not that the risks are low", report)

    def test_table_cells_escape_pipes(self):
        self.assertEqual(rh.cell("a|b"), "a\\|b")


if __name__ == "__main__":
    unittest.main()
