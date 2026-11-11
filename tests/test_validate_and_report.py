"""Tests for tools/validate_and_report.py.

Run from the repository root with either of:

    python -m unittest discover -s tests -v
    python -m pytest tests

Each test that changes data works on a temporary copy of the repository, so the real
files are never modified.
"""

import csv
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate_and_report as vr  # noqa: E402


def copy_repo(destination: Path) -> Path:
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache")
    target = destination / "repo"
    shutil.copytree(REPO_ROOT, target, ignore=ignore)
    return target


def edit_csv(path: Path, change) -> None:
    """Load a CSV, let `change(header, rows)` modify it in place, and write it back."""
    with path.open(newline="", encoding="utf-8") as handle:
        data = list(csv.reader(handle))
    header, rows = data[0], data[1:]
    change(header, rows)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def col(header, name):
    return header.index(name)


class TempRepoTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = copy_repo(Path(self._tmp.name))

    def run_validator(self, check=False):
        return vr.run(self.root, write=False, check=check)

    def assert_error_contains(self, result, fragment):
        joined = "\n".join(result.issues.errors)
        self.assertIn(fragment, joined, msg=f"expected an error containing {fragment!r}, got:\n{joined}")


class RealRepositoryTests(unittest.TestCase):
    def test_repository_data_has_no_errors(self):
        result = vr.run(REPO_ROOT, write=False, check=False)
        self.assertEqual(result.issues.errors, [])

    def test_generated_documents_are_current(self):
        result = vr.run(REPO_ROOT, write=False, check=True)
        self.assertEqual(result.issues.errors, [])
        self.assertEqual(result.stale, [], msg="run python tools/validate_and_report.py to regenerate docs")

    def test_framework_item_counts(self):
        result = vr.run(REPO_ROOT, write=False, check=False)
        iso = result.frameworks["iso"]
        self.assertEqual(sum(1 for r in iso if r["type"] == "annex_a_control"), 38)
        self.assertEqual(sum(1 for r in iso if r["type"] == "clause"), 27)
        nist = result.frameworks["nist"]
        by_function = {}
        for row in nist:
            by_function[row["function"]] = by_function.get(row["function"], 0) + 1
        self.assertEqual(by_function, {"GOVERN": 19, "MAP": 18, "MEASURE": 22, "MANAGE": 13})
        self.assertEqual(len(nist), 72)

    def test_every_control_maps_somewhere_and_ids_are_unique(self):
        result = vr.run(REPO_ROOT, write=False, check=False)
        ids = [c["control_id"] for c in result.controls]
        self.assertEqual(len(ids), len(set(ids)))
        for control in result.controls:
            total = sum(len(vr.split_refs(control[s.matrix_column])) for s in vr.FRAMEWORKS)
            self.assertGreater(total, 0, control["control_id"])

    def test_cli_check_mode_succeeds(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = vr.main(["--root", str(REPO_ROOT), "--check"])
        self.assertEqual(code, 0, msg=buffer.getvalue())

    def test_markdown_links_are_checked(self):
        result = vr.run(REPO_ROOT, write=False, check=False)
        self.assertGreater(result.links_checked, 20)


class FrameworkValidationTests(TempRepoTestCase):
    def test_missing_required_column_is_reported(self):
        path = self.root / "data/frameworks/nist_ai_rmf_items.csv"
        edit_csv(path, lambda h, rows: self._drop_column(h, rows, "category"))
        self.assert_error_contains(self.run_validator(), "missing required column(s): category")

    @staticmethod
    def _drop_column(header, rows, name):
        index = header.index(name)
        del header[index]
        for row in rows:
            del row[index]

    def test_duplicate_framework_id_is_reported(self):
        path = self.root / "data/frameworks/eu_ai_act_items.csv"
        edit_csv(path, lambda h, rows: rows.append(list(rows[0])))
        self.assert_error_contains(self.run_validator(), "duplicate id 'Art 2'")

    def test_bad_nist_id_format_is_reported(self):
        path = self.root / "data/frameworks/nist_ai_rmf_items.csv"

        def change(h, rows):
            rows[0][col(h, "id")] = "GOVERN1.1"

        edit_csv(path, change)
        self.assert_error_contains(self.run_validator(), "does not match the expected format")

    def test_invalid_verification_value_is_reported(self):
        path = self.root / "data/frameworks/iso42001_items.csv"

        def change(h, rows):
            rows[0][col(h, "verification")] = "trust-me"

        edit_csv(path, change)
        self.assert_error_contains(self.run_validator(), "verification must be one of")

    def test_short_row_is_reported(self):
        path = self.root / "data/frameworks/iso42001_items.csv"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("9.9,clause\n")
        self.assert_error_contains(self.run_validator(), "fields but the header has")


class MatrixValidationTests(TempRepoTestCase):
    matrix = "data/control_matrix.csv"

    def test_missing_matrix_column_is_reported(self):
        edit_csv(self.root / self.matrix, lambda h, rows: FrameworkValidationTests._drop_column(h, rows, "objective"))
        self.assert_error_contains(self.run_validator(), "missing required column(s): objective")

    def test_duplicate_control_id_is_reported(self):
        edit_csv(self.root / self.matrix, lambda h, rows: rows.append(list(rows[0])))
        self.assert_error_contains(self.run_validator(), "duplicate control_id 'TK-GOV-01'")

    def test_orphan_iso_mapping_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "iso42001_refs")] += ";99.9"

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "orphan mapping '99.9'")

    def test_orphan_eu_and_nist_mappings_are_reported(self):
        def change(h, rows):
            rows[1][col(h, "eu_ai_act_refs")] = "Art 999"
            rows[1][col(h, "nist_ai_rmf_refs")] = "MAP 9.9"

        edit_csv(self.root / self.matrix, change)
        result = self.run_validator()
        self.assert_error_contains(result, "orphan mapping 'Art 999'")
        self.assert_error_contains(result, "orphan mapping 'MAP 9.9'")

    def test_bad_control_id_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "control_id")] = "CTRL-1"

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "does not match TK-XXX-NN")

    def test_domain_must_match_id_code(self):
        def change(h, rows):
            rows[0][col(h, "domain")] = "Data"

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "does not match the code in TK-GOV-01")

    def test_control_without_any_mapping_is_reported(self):
        def change(h, rows):
            for name in ("iso42001_refs", "eu_ai_act_refs", "nist_ai_rmf_refs"):
                rows[2][col(h, name)] = ""

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "maps to no framework item")

    def test_duplicate_reference_in_a_cell_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "nist_ai_rmf_refs")] = "GOVERN 1.2;GOVERN 1.2"

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "duplicate reference in nist_ai_rmf_refs")

    def test_missing_template_file_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "template")] = "templates/does-not-exist.md"

        edit_csv(self.root / self.matrix, change)
        self.assert_error_contains(self.run_validator(), "does not exist")


class RegisterValidationTests(TempRepoTestCase):
    inventory = "examples/fernhill/ai-system-inventory.csv"
    risks = "examples/fernhill/ai-risk-register.csv"
    incidents = "examples/fernhill/ai-incident-log.csv"

    def test_orphan_risk_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "system_id")] = "FH-AI-999"

        edit_csv(self.root / self.risks, change)
        self.assert_error_contains(self.run_validator(), "orphan risk")

    def test_score_arithmetic_is_checked(self):
        def change(h, rows):
            rows[0][col(h, "inherent_score")] = "7"

        edit_csv(self.root / self.risks, change)
        self.assert_error_contains(self.run_validator(), "inherent_score is 7 but likelihood x impact is 12")

    def test_rating_band_is_checked(self):
        def change(h, rows):
            rows[0][col(h, "inherent_rating")] = "low"

        edit_csv(self.root / self.risks, change)
        self.assert_error_contains(self.run_validator(), "inherent_rating should be 'high'")

    def test_unknown_control_in_risk_register_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "existing_controls")] = "TK-XXX-99"

        edit_csv(self.root / self.risks, change)
        self.assert_error_contains(self.run_validator(), "unknown control 'TK-XXX-99'")

    def test_duplicate_risk_id_is_reported(self):
        edit_csv(self.root / self.risks, lambda h, rows: rows.append(list(rows[0])))
        self.assert_error_contains(self.run_validator(), "duplicate risk_id 'FH-R-001'")

    def test_high_risk_inventory_row_needs_annex_area(self):
        def change(h, rows):
            for row in rows:
                if row[col(h, "system_id")] == "FH-AI-002":
                    row[col(h, "annex_area")] = ""

        edit_csv(self.root / self.inventory, change)
        self.assert_error_contains(self.run_validator(), "a high-risk tier needs an annex_area")

    def test_invalid_inventory_enum_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "eu_risk_tier")] = "scary"

        edit_csv(self.root / self.inventory, change)
        self.assert_error_contains(self.run_validator(), "eu_risk_tier 'scary'")

    def test_invalid_date_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "next_review_date")] = "01/03/2027"

        edit_csv(self.root / self.inventory, change)
        self.assert_error_contains(self.run_validator(), "is not an ISO date")

    def test_closed_incident_needs_closed_date_and_order(self):
        def change(h, rows):
            rows[0][col(h, "closed_date")] = "2026-01-01"

        edit_csv(self.root / self.incidents, change)
        self.assert_error_contains(self.run_validator(), "closed_date is before date_detected")

    def test_incident_orphan_system_is_reported(self):
        def change(h, rows):
            rows[0][col(h, "system_id")] = "FH-AI-404"

        edit_csv(self.root / self.incidents, change)
        self.assert_error_contains(self.run_validator(), "orphan incident")

    def test_blank_template_header_is_checked(self):
        path = self.root / "templates/ai-risk-register.csv"
        text = path.read_text(encoding="utf-8").replace("risk_id", "risk_ref", 1)
        path.write_text(text, encoding="utf-8")
        result = self.run_validator()
        self.assertTrue(result.issues.errors)


class LinkCheckTests(TempRepoTestCase):
    def test_broken_relative_link_is_reported(self):
        readme = self.root / "docs/how-to-adopt.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nSee [missing](nowhere.md).\n", encoding="utf-8")
        self.assert_error_contains(self.run_validator(), "broken relative link 'nowhere.md'")

    def test_external_and_anchor_links_are_ignored(self):
        doc = self.root / "docs/how-to-adopt.md"
        doc.write_text(doc.read_text(encoding="utf-8") + "\n[a](https://example.org/x) [b](#top)\n", encoding="utf-8")
        self.assertEqual(self.run_validator().issues.errors, [])


class CoverageAndGenerationTests(TempRepoTestCase):
    def test_removed_mapping_appears_as_a_gap(self):
        def change(h, rows):
            for row in rows:
                refs = [r for r in row[col(h, "nist_ai_rmf_refs")].split(";") if r and r != "GOVERN 1.7"]
                row[col(h, "nist_ai_rmf_refs")] = ";".join(refs)

        edit_csv(self.root / "data/control_matrix.csv", change)
        result = self.run_validator()
        self.assertEqual(result.issues.errors, [])
        report = result.generated["docs/coverage-report.md"]
        self.assertIn("| GOVERN 1.7 |", report)

    def test_excluded_eu_items_are_not_counted_as_gaps(self):
        result = self.run_validator()
        coverage = {c.spec.key: c for c in vr.compute_coverage(result.frameworks, result.controls)}
        eu = coverage["eu"]
        no_count = sum(1 for r in result.frameworks["eu"] if r["coverage_expected"] == "no")
        self.assertEqual(len(eu.excluded), no_count)
        self.assertEqual(len(eu.expected) + len(eu.excluded), len(result.frameworks["eu"]))
        self.assertNotIn("Art 99", [r["id"] for r in eu.unmapped_expected])

    def test_generated_markdown_is_deterministic_and_has_no_em_dash(self):
        first = self.run_validator().generated
        second = self.run_validator().generated
        self.assertEqual(first, second)
        for text in first.values():
            self.assertNotIn(chr(0x2014), text)

    def test_check_mode_flags_stale_documents(self):
        vr.run(self.root, write=True, check=False)
        report = self.root / "docs/coverage-report.md"
        report.write_text(report.read_text(encoding="utf-8") + "\nstale\n", encoding="utf-8")
        result = vr.run(self.root, write=False, check=True)
        self.assertEqual(result.stale, ["docs/coverage-report.md"])
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = vr.main(["--root", str(self.root), "--check"])
        self.assertEqual(code, 2)

    def test_cli_returns_one_on_errors(self):
        edit_csv(self.root / "data/control_matrix.csv", lambda h, rows: rows.append(list(rows[0])))
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = vr.main(["--root", str(self.root)])
        self.assertEqual(code, 1)
        self.assertIn("FAILED", buffer.getvalue())

    def test_generated_docs_not_written_when_errors_exist(self):
        (self.root / "docs/control-matrix.md").unlink()
        edit_csv(self.root / "data/control_matrix.csv", lambda h, rows: rows.append(list(rows[0])))
        vr.run(self.root, write=True, check=False)
        self.assertFalse((self.root / "docs/control-matrix.md").exists())


class HelperTests(unittest.TestCase):
    def test_rating_bands(self):
        self.assertEqual(vr.rating_for(1), "low")
        self.assertEqual(vr.rating_for(4), "low")
        self.assertEqual(vr.rating_for(5), "medium")
        self.assertEqual(vr.rating_for(9), "medium")
        self.assertEqual(vr.rating_for(10), "high")
        self.assertEqual(vr.rating_for(16), "high")
        self.assertEqual(vr.rating_for(20), "critical")
        self.assertEqual(vr.rating_for(25), "critical")

    def test_every_possible_product_gets_a_rating(self):
        for likelihood in range(1, 6):
            for impact in range(1, 6):
                self.assertIn(vr.rating_for(likelihood * impact), {"low", "medium", "high", "critical"})

    def test_split_refs(self):
        self.assertEqual(vr.split_refs("A;B; C ;"), ["A", "B", "C"])
        self.assertEqual(vr.split_refs(""), [])

    def test_rel_link(self):
        self.assertEqual(vr.rel_link("templates/x.md", "docs"), "../templates/x.md")
        self.assertEqual(vr.rel_link("docs/y.md", "docs"), "y.md")

    def test_parse_date(self):
        self.assertIsNotNone(vr.parse_date("2026-11-04"))
        self.assertIsNone(vr.parse_date("04/11/2026"))
        self.assertIsNone(vr.parse_date("2026-02-30"))


if __name__ == "__main__":
    unittest.main()
