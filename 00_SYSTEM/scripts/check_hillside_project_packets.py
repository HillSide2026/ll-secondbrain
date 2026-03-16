#!/usr/bin/env python3
"""
Report initiation-packet drift for HillSide business projects.

Default behavior is report-only. Use --fail-on-findings to return a non-zero
exit code when packet-started projects are missing required artifacts.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECTS_DIR = REPO_ROOT / "04_INITIATIVES" / "HillSide_PORTFOLIO" / "BUSINESS_PROJECTS"
FULL_INITIATION = [
    "PROJECT_CHARTER.md",
    "PROBLEM_STATEMENT.md",
    "SUCCESS_CRITERIA.md",
    "STAKEHOLDERS.md",
    "RISK_SCAN.md",
    "APPROVAL_RECORD.md",
]
DECISION_INITIATION = [
    "PROJECT_CHARTER.md",
    "PROBLEM_STATEMENT.md",
    "RISK_SCAN.md",
    "APPROVAL_RECORD.md",
]
PACKET_STARTERS = set(FULL_INITIATION + DECISION_INITIATION + ["BUSINESS_CASE.md"])
PROJECT_TYPE_PATTERN = re.compile(r"(?im)^(?:\*\*Project Type:\*\*|Project Type:)\s*(.+?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Return exit code 1 when packet-started projects are missing required artifacts.",
    )
    return parser.parse_args()


def detect_project_type(project_dir: Path) -> str | None:
    charter = project_dir / "PROJECT_CHARTER.md"
    if not charter.exists():
        return None
    match = PROJECT_TYPE_PATTERN.search(charter.read_text(encoding="utf-8"))
    if not match:
        return None
    return match.group(1).strip()


def packet_started(file_names: set[str]) -> bool:
    return any(name in file_names for name in PACKET_STARTERS)


def required_type_specific_artifacts(project_type: str | None) -> list[str]:
    if not project_type:
        return list(FULL_INITIATION)
    normalized = project_type.strip().lower()
    if normalized.startswith("strategic"):
        return list(FULL_INITIATION) + ["BUSINESS_CASE.md"]
    if normalized.startswith("decision"):
        return list(DECISION_INITIATION)
    return list(FULL_INITIATION)


def main() -> int:
    args = parse_args()
    findings = []
    shell_only = []

    for project_dir in sorted(PROJECTS_DIR.glob("HBP-*")):
        if not project_dir.is_dir():
            continue

        file_names = {path.name for path in project_dir.iterdir() if path.is_file()}
        project_type = detect_project_type(project_dir)

        if not packet_started(file_names):
            shell_only.append(project_dir.name)
            continue

        missing = []
        for artifact_name in required_type_specific_artifacts(project_type):
            if artifact_name not in file_names:
                missing.append(artifact_name)

        if missing:
            findings.append((project_dir.name, project_type or "Unknown", missing))

    print("HillSide business project packet check")
    print(f"Projects directory: {PROJECTS_DIR.relative_to(REPO_ROOT)}")
    print()

    if findings:
        print("Packet-started projects with missing initiation artifacts:")
        for project_name, project_type, missing in findings:
            print(f"- {project_name} [{project_type}]: {', '.join(missing)}")
    else:
        print("No missing initiation artifacts found in packet-started HillSide projects.")

    print()
    if shell_only:
        print("Shell-only projects (allowed before Initiating):")
        for project_name in shell_only:
            print(f"- {project_name}")

    if findings and args.fail_on_findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
