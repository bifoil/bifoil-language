"""The shell collector must publish only complete observations and clean owned staging."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CoverageCollector(unittest.TestCase):
    def test_shell_collection_preserves_failure_and_cleans_staging(self):
        with tempfile.TemporaryDirectory(prefix="bifoil validator coverage Ω ") as temporary:
            root = Path(temporary)
            (root / "tools").mkdir()
            script = root / "tools/collect-coverage.sh"
            shutil.copyfile(ROOT / "tools/collect-coverage.sh", script)
            commands = root / "commands"
            commands.mkdir()
            uv = commands / "uv"
            uv.write_text(f"#!{sys.executable}\n" + r'''
import json, os, pathlib, sys
arguments = sys.argv[1:]
with open(os.environ["BIFOIL_COLLECTOR_TRACE"], "a", encoding="utf-8") as trace:
    trace.write(json.dumps(arguments) + "\n")
if os.environ["BIFOIL_COLLECTOR_FAIL"] == "run" and "run" in arguments[9:]:
    raise SystemExit(9)
if "xml" in arguments:
    pathlib.Path(arguments[arguments.index("-o") + 1]).write_text("Original validator report\n")
    if os.environ["BIFOIL_COLLECTOR_FAIL"] == "xml":
        raise SystemExit(9)
''')
            uv.chmod(0o755)
            trace = root / "calls.jsonl"
            environment = dict(os.environ, PATH=str(commands) + os.pathsep + os.environ["PATH"],
                               BIFOIL_COLLECTOR_TRACE=str(trace))
            reports = root / ".bifoil/development/sonar"
            for phase in ["run", "xml", "success"]:
                with self.subTest(phase=phase):
                    reports.mkdir(parents=True, exist_ok=True)
                    report = reports / "python-coverage.xml"
                    report.write_text("Stale validator report")
                    trace.write_text("")
                    environment["BIFOIL_COLLECTOR_FAIL"] = phase
                    result = subprocess.run(["bash", str(script)], cwd=root, env=environment,
                                            text=True, capture_output=True, check=False, timeout=10)
                    self.assertFalse(list(reports.glob("coverage.*")), result.stderr)
                    if phase != "success":
                        self.assertEqual(result.returncode, 9, result.stderr)
                        self.assertFalse(report.exists())
                    else:
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(report.read_text(), "Original validator report\n")
                        calls = [json.loads(row) for row in trace.read_text().splitlines()]
                        self.assertEqual(len(calls), 3)
                        self.assertTrue(all("coverage==7.17.0" in call for call in calls))
                        self.assertIn("unittest", calls[1])
                        self.assertIn("xml", calls[2])


if __name__ == "__main__":
    unittest.main()
