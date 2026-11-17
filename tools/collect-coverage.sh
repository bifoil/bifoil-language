#!/usr/bin/env bash
# Collect real validator coverage; never leave an old report after a failed run.
set -euo pipefail
repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repository_root"
report_directory=.bifoil/development/sonar
mkdir -p "$report_directory"
rm -f "$report_directory/python-coverage.xml"
temporary_directory="$(mktemp -d "$report_directory/coverage.XXXXXX")"
trap 'rm -rf -- "$temporary_directory"' EXIT
coverage_command=(uv run --no-project --with coverage==7.17.0 --python python3 python -m coverage)
"${coverage_command[@]}" erase
"${coverage_command[@]}" run -m unittest discover -s tools -p 'test_*.py'
"${coverage_command[@]}" xml -o "$temporary_directory/python-coverage.xml"
mv "$temporary_directory/python-coverage.xml" "$report_directory/python-coverage.xml"
printf 'Coverage report ready in %s\n' "$report_directory"
