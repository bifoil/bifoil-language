"""Integrity regressions; validating metadata does not execute language programs."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest


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
