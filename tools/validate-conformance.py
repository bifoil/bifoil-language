"""Check steering IDs, case indexes, source directories, and evidence references.

Run with: uv run --no-project tools/validate-conformance.py
No compiler, runtime, package installation, or adjacent checkout is required.
"""

import json
from pathlib import Path
import re


CASE_FIELDS = {
    "id",
    "directory",
    "decisions",
    "compile_error",
    "runtime_error",
    "choices",
    "output",
    "options",
    "precompile",
    "legacy_stats",
    "quantum",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def contained(root, value):
    path = (root / value).resolve()
    require(path.is_relative_to(root.resolve()), f"path escapes conformance directory: {value}")
    return path


def validate(root):
    conformance = root / "conformance"
    steering = (root / "language-steering.md").read_text()
    identifiers = re.findall(r"^\|\s*([A-Z]\d{2})\s*\|", steering, re.MULTILINE)
    decisions = dict(re.findall(
        r"^\|\s*([A-Z]\d{2})\s*\|\s*(.*?)\s*\|$", steering, re.MULTILINE
    ))
    require(len(identifiers) == len(set(identifiers)), "duplicate steering document IDs")
    ledger = json.loads((conformance / "steering.json").read_text())
    require(ledger.get("format") == "bifoil.conformance.v1", "unknown ledger format")
    records = ledger["decisions"]
    record_ids = [record["id"] for record in records]
    require(len(record_ids) == len(set(record_ids)), "duplicate ledger IDs")
    require(set(record_ids) == set(identifiers), "ledger and steering document IDs differ")
    cases = []
    for index in sorted(conformance.glob("*.json")):
        if index.name == "steering.json":
            continue
        content = json.loads(index.read_text())
        require(isinstance(content, list), f"case index must be an array: {index.name}")
        cases.extend(content)
    case_ids = {case["id"] for case in cases}
    require(len(case_ids) == len(cases), "duplicate conformance case IDs")
    for case in cases:
        identifier = case["id"]
        unknown = case.keys() - CASE_FIELDS
        require(not unknown, f"unknown fields in {identifier}: {', '.join(sorted(unknown))}")
        require(
            not ("compile_error" in case and "runtime_error" in case),
            f"compile/runtime expectations conflict in {identifier}",
        )
        for key in ("compile_error", "runtime_error"):
            if key in case:
                require(
                    isinstance(case[key], str) and bool(case[key]),
                    f"{key} must be a nonempty diagnostic in {identifier}",
                )
        require(re.fullmatch(r"[a-z0-9-]+", identifier), f"invalid case ID: {identifier}")
        require(set(case.get("decisions", [])) <= set(identifiers), f"unknown decision in {identifier}")
        directory = contained(conformance, case["directory"])
        require(directory.is_dir(), f"missing source directory for {identifier}")
        require(any(directory.rglob("*.bfl")), f"missing Bifoil source for {identifier}")
    by_id = {case["id"]: case for case in cases}
    by_decision = {record["id"]: record for record in records}
    for case in cases:
        for decision in case.get("decisions", []):
            require(case["id"] in by_decision[decision]["evidence"],
                    f"missing reciprocal evidence for {case['id']} / {decision}")
    for record in records:
        require(record["status"] in {"pending", "partial", "complete"},
                f"unknown evidence status for {record['id']}")
        require(record["decision"] == decisions.get(record["id"]),
                f"stale decision text for {record['id']}")
        evidence = record["evidence"]
        require(isinstance(evidence, list) and all(isinstance(item, str) for item in evidence),
                f"evidence must be an array of references for {record['id']}")
        require(record["status"] == "pending" or bool(evidence),
                f"{record['id']} claims coverage without evidence")
        require(len(evidence) == len(set(evidence)), f"duplicate evidence in {record['id']}")
        for reference in evidence:
            if reference in case_ids:
                require(record["id"] in by_id[reference].get("decisions", []),
                        f"missing reciprocal decision for {reference} / {record['id']}")
            else:
                require(contained(conformance, reference).is_file(), f"missing evidence: {reference}")
    print(f"Validated {len(records)} steering decisions and {len(cases)} unique conformance cases.")


if __name__ == "__main__":
    try:
        validate(Path(__file__).resolve().parent.parent)
    except (KeyError, TypeError, ValueError, OSError) as error:
        raise SystemExit(f"conformance validation failed: {error}") from error
