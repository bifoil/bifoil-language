"""Integrity regressions; validating metadata does not execute language programs."""

import contextlib
import importlib.util
import io
import json
import runpy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("validator", Path(__file__).with_name("validate-conformance.py"))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class EvidenceIntegrity(unittest.TestCase):
    def fixture(self, root):
        (root / "language-steering.md").write_text("| S14 | Actual selected rule. |\n")
        corpus = root / "conformance"
        source = corpus / "cases/example"
        source.mkdir(parents=True)
        (source / "main.bfl").write_text("scene start():\n    Unit\n")
        case = {"id": "example", "directory": "cases/example", "decisions": ["S14"]}
        record = {"id": "S14", "decision": "Actual selected rule.",
                  "status": "partial", "evidence": ["example"]}
        return corpus, case, record

    def check_fixture(self, change=None):
        with tempfile.TemporaryDirectory(prefix="bifoil-evidence-") as temporary:
            root = Path(temporary)
            corpus, case, record = self.fixture(root)
            if change:
                change(case, record)
            (corpus / "cases.json").write_text(json.dumps([case]))
            (corpus / "steering.json").write_text(json.dumps({
                "format": "bifoil.conformance.v1", "decisions": [record],
            }))
            with contextlib.redirect_stdout(io.StringIO()):
                validator.validate(root)

    def test_steering_rows_preserve_embedded_pipes_and_duplicate_ids(self):
        identifiers, decisions = validator.steering_rows(
            "Ignored prose\n| incomplete\n| ID | Decision |\n"
            "| S14 | First | alternative. |\n"
            "| S14 | Final selected rule. |\n"
        )
        self.assertEqual(identifiers, ["S14", "S14"])
        self.assertEqual(decisions, {"S14": "Final selected rule."})

    def test_long_unterminated_steering_row_keeps_id_without_decision(self):
        identifiers, decisions = validator.steering_rows("| S14 | " + " " * 100_000)
        self.assertEqual(identifiers, ["S14"])
        self.assertEqual(decisions, {})
        _, decisions = validator.steering_rows("| S14 | " + " " * 100_000 + "rule |")
        self.assertEqual(decisions, {"S14": "rule"})

    def test_expected_compile_and_runtime_diagnostics_are_nonempty_strings(self):
        for key in ("compile_error", "runtime_error"):
            with self.subTest(key=key):
                self.check_fixture(lambda case, record: case.update({key: "Original expected diagnostic"}))
            for invalid in ("", False, 7):
                with self.subTest(key=key, invalid=invalid), self.assertRaisesRegex(ValueError, "nonempty diagnostic"):
                    self.check_fixture(lambda case, record: case.update({key: invalid}))

    def test_original_file_evidence_is_accepted_only_while_it_exists(self):
        with tempfile.TemporaryDirectory(prefix="bifoil-file-evidence-") as temporary:
            root = Path(temporary)
            corpus, case, record = self.fixture(root)
            case["decisions"] = []
            record["evidence"] = ["original-evidence.md"]
            evidence = corpus / "original-evidence.md"
            evidence.write_text("Original manually inspectable evidence.\n")
            (corpus / "cases.json").write_text(json.dumps([case]))
            (corpus / "steering.json").write_text(json.dumps({
                "format": "bifoil.conformance.v1", "decisions": [record],
            }))
            with contextlib.redirect_stdout(io.StringIO()):
                validator.validate(root)
            evidence.unlink()
            with self.assertRaisesRegex(ValueError, "missing evidence"):
                validator.validate(root)

    def test_command_entry_validates_the_actual_repository(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(Path(__file__).with_name("validate-conformance.py")), run_name="__main__")
        self.assertRegex(output.getvalue(), r"Validated [1-9]\d* steering decisions and [1-9]\d* unique conformance cases")

    def test_command_entry_keeps_a_source_read_failure_nonzero(self):
        with patch.object(Path, "read_text", side_effect=OSError("Original evidence read failure")):
            with self.assertRaisesRegex(SystemExit, "conformance validation failed: Original evidence read failure"):
                runpy.run_path(str(Path(__file__).with_name("validate-conformance.py")), run_name="__main__")

    def test_valid_reciprocal_record(self):
        self.check_fixture()

    def test_status_and_selected_text_must_match(self):
        for field, value, diagnostic in [
            ("status", "approved", "unknown evidence status"),
            ("decision", "Unrelated claim.", "stale decision text"),
        ]:
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, diagnostic):
                self.check_fixture(lambda case, record: record.update({field: value}))

    def test_case_and_ledger_links_must_be_reciprocal(self):
        with self.assertRaisesRegex(ValueError, "missing reciprocal evidence"):
            self.check_fixture(lambda case, record: record.update(evidence=[]))
        with self.assertRaisesRegex(ValueError, "missing reciprocal decision"):
            self.check_fixture(lambda case, record: case.update(decisions=[]))


if __name__ == "__main__":
    unittest.main()
