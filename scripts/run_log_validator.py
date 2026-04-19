#!/usr/bin/env python3
"""
Run Log Validator — scripts/run_log_validator.py

Validates run log entries in 06_RUNS/ against PRO-023 (Run Log Standard).
Covers: SLA-ML2-001 (Record Integrity), KPI-ML2-004 (Schema Compliance)

Output:
  06_RUNS/ops/sla_audit/run_log_validation_{run_id}.json
  06_RUNS/ops/sla_audit/run_log_validation_{run_id}.md

Exit codes:
  0 — all logs pass
  1 — one or more violations found
"""

import json
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DEFAULT_SCAN_DIR = REPO_ROOT / "06_RUNS"
OUTPUT_DIR = REPO_ROOT / "06_RUNS" / "ops" / "sla_audit"

VALID_STATUSES = {"complete", "partial", "failed"}
VALID_OUTPUT_CLASSIFICATIONS = {"internal", "ll-consumable"}

# Required frontmatter fields and their validation rules
REQUIRED_FIELDS = [
    "run_id",
    "run_date",
    "run_time",
    "agent_or_script",
    "matter_id",
    "task",
    "slas_covered",
    "output_classification",
    "status",
]

# Keywords that must appear as headings in the body
REQUIRED_BODY_SECTIONS = ["summary", "findings", "violations", "next actions"]

RUN_ID_PATTERN = re.compile(r"^\d{8}_\d{6}_.+$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_PATTERN = re.compile(r"^\d{2}:\d{2}:\d{2}")

NULL_VALUES = {"", "~", "null", "none"}


def parse_frontmatter(path: Path):
    """Extract YAML frontmatter dict and body from a markdown file."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return None, None, f"Cannot read file: {e}"

    if not content.startswith("---"):
        return None, content, None

    end = content.find("\n---", 3)
    if end == -1:
        return None, content, "Unclosed frontmatter block"

    fm_block = content[3:end].strip()
    body = content[end + 4:].strip()

    fields = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # Parse list values like [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            items = [x.strip() for x in inner.split(",") if x.strip()]
            fields[key] = items
        else:
            fields[key] = val

    return fields, body, None


def check_file(path: Path, rel_path: str) -> list:
    """Check a single run log file. Returns list of violation dicts."""
    violations = []

    fm, body, parse_error = parse_frontmatter(path)

    if parse_error:
        violations.append({
            "file": rel_path,
            "field": "frontmatter",
            "severity": "critical",
            "issue": f"Parse error: {parse_error}",
        })
        return violations

    if fm is None:
        violations.append({
            "file": rel_path,
            "field": "frontmatter",
            "severity": "critical",
            "issue": "No frontmatter block found",
        })
        return violations

    # Check required fields present and non-null
    for field in REQUIRED_FIELDS:
        val = fm.get(field)
        if val is None:
            violations.append({
                "file": rel_path,
                "field": field,
                "severity": "critical",
                "issue": f"Missing required field: {field}",
            })
        elif isinstance(val, str) and val.lower() in NULL_VALUES:
            violations.append({
                "file": rel_path,
                "field": field,
                "severity": "critical",
                "issue": f"Null value for required field: {field} = '{val}'",
            })
        elif isinstance(val, list) and len(val) == 0:
            # Empty list allowed only for slas_covered with justification check
            if field == "slas_covered":
                # Body should contain justification — just warn
                violations.append({
                    "file": rel_path,
                    "field": field,
                    "severity": "warning",
                    "issue": "slas_covered is empty — add justification if intentional",
                })

    # Format validations (only if field present)
    run_id = fm.get("run_id", "")
    if run_id and isinstance(run_id, str) and run_id.lower() not in NULL_VALUES:
        if not RUN_ID_PATTERN.match(run_id):
            violations.append({
                "file": rel_path,
                "field": "run_id",
                "severity": "major",
                "issue": f"run_id format invalid: '{run_id}' (expected YYYYMMDD_HHMMSS_<agent>)",
            })

    run_date = fm.get("run_date", "")
    if run_date and isinstance(run_date, str) and run_date.lower() not in NULL_VALUES:
        if not DATE_PATTERN.match(run_date):
            violations.append({
                "file": rel_path,
                "field": "run_date",
                "severity": "major",
                "issue": f"run_date format invalid: '{run_date}' (expected YYYY-MM-DD)",
            })

    output_class = fm.get("output_classification", "")
    if output_class and isinstance(output_class, str) and output_class.lower() not in NULL_VALUES:
        if output_class.lower() not in VALID_OUTPUT_CLASSIFICATIONS:
            violations.append({
                "file": rel_path,
                "field": "output_classification",
                "severity": "major",
                "issue": f"Invalid output_classification: '{output_class}' (must be 'internal' or 'll-consumable')",
            })

    status = fm.get("status", "")
    if status and isinstance(status, str) and status.lower() not in NULL_VALUES:
        if status.lower() not in VALID_STATUSES:
            violations.append({
                "file": rel_path,
                "field": "status",
                "severity": "major",
                "issue": f"Invalid status: '{status}' (must be complete/partial/failed)",
            })

    # Check body sections
    if body:
        body_lower = body.lower()
        for section in REQUIRED_BODY_SECTIONS:
            # Look for markdown heading containing the keyword
            if section not in body_lower:
                violations.append({
                    "file": rel_path,
                    "field": "body",
                    "severity": "major",
                    "issue": f"Missing required body section: '{section}'",
                })
    else:
        violations.append({
            "file": rel_path,
            "field": "body",
            "severity": "major",
            "issue": "Empty body — required sections missing",
        })

    return violations


def is_run_log(path: Path) -> bool:
    """Return True if this .md file looks like a run log (has frontmatter with run_id indicator)."""
    if path.suffix != ".md":
        return False
    # Skip the ops/sla_audit outputs themselves (they're audit reports, not run logs)
    # But still check ones that claim to be run logs via frontmatter
    try:
        first_bytes = path.read_text(encoding="utf-8", errors="ignore")[:500]
    except Exception:
        return False
    return "run_id:" in first_bytes or "run_date:" in first_bytes


def run_validation(scan_dir: Path) -> dict:
    """Scan scan_dir recursively and validate all run log files."""
    ts = datetime.now(timezone.utc)
    run_id = ts.strftime("%Y%m%d_%H%M%S") + "_run_log_validator"

    results = {
        "run_id": run_id,
        "run_date": ts.strftime("%Y-%m-%d"),
        "run_time": ts.strftime("%H:%M:%S UTC"),
        "agent_or_script": "run_log_validator.py",
        "scan_dir": str(scan_dir.relative_to(REPO_ROOT)),
        "files_scanned": 0,
        "files_passed": 0,
        "files_failed": 0,
        "violation_count": 0,
        "violations": [],
        "sla_summary": {},
        "exit_code": 0,
    }

    all_violations = []
    files_scanned = 0
    files_failed_set = set()

    for md_path in sorted(scan_dir.rglob("*.md")):
        if not is_run_log(md_path):
            continue
        # Skip files that are audit outputs themselves to avoid circular validation
        if "sla_audit" in str(md_path) and md_path.name.startswith(("audit_", "integration_health_", "run_log_validation_", "monthly_review_")):
            continue

        files_scanned += 1
        rel_path = str(md_path.relative_to(REPO_ROOT))
        violations = check_file(md_path, rel_path)

        if violations:
            all_violations.extend(violations)
            files_failed_set.add(rel_path)

    results["files_scanned"] = files_scanned
    results["files_failed"] = len(files_failed_set)
    results["files_passed"] = files_scanned - len(files_failed_set)
    results["violation_count"] = len(all_violations)
    results["violations"] = all_violations

    # SLA summary
    critical = [v for v in all_violations if v.get("severity") == "critical"]
    major = [v for v in all_violations if v.get("severity") == "major"]
    warnings = [v for v in all_violations if v.get("severity") == "warning"]

    if critical:
        schema_compliance = (
            results["files_passed"] / max(results["files_scanned"], 1)
        )
        results["sla_summary"] = {
            "SLA-ML2-001": "BREACH" if critical else "PASS",
            "KPI-ML2-004_schema_compliance": f"{schema_compliance:.1%}",
        }
        results["exit_code"] = 1
    elif major:
        results["sla_summary"] = {
            "SLA-ML2-001": "PASS",
            "KPI-ML2-004_schema_compliance": f"{(results['files_passed'] / max(results['files_scanned'], 1)):.1%}",
        }
        results["exit_code"] = 1
    else:
        results["sla_summary"] = {
            "SLA-ML2-001": "PASS",
            "KPI-ML2-004_schema_compliance": "100.0%",
        }

    return results


def write_json(results: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{results['run_id']}.json"
    path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return path


def write_md(results: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{results['run_id']}.md"

    violations = results["violations"]
    critical = [v for v in violations if v.get("severity") == "critical"]
    major = [v for v in violations if v.get("severity") == "major"]
    warnings = [v for v in violations if v.get("severity") == "warning"]

    overall = "PASS" if results["exit_code"] == 0 else "FAIL"
    sla_ml2_001 = results["sla_summary"].get("SLA-ML2-001", "N/A")
    kpi_ml2_004 = results["sla_summary"].get("KPI-ML2-004_schema_compliance", "N/A")

    lines = [
        "---",
        f"run_id: {results['run_id']}",
        f"run_date: {results['run_date']}",
        f"run_time: {results['run_time']}",
        "agent_or_script: run_log_validator.py",
        "matter_id: none",
        "task: Validate run log entries against PRO-023 Run Log Standard",
        "slas_covered: [SLA-ML2-001, KPI-ML2-004]",
        "output_classification: internal",
        f"status: {'complete' if results['exit_code'] == 0 else 'complete'}",
        "---",
        "",
        f"# Run Log Validation — {results['run_date']}",
        "",
        "## Summary",
        "",
        f"Scanned `{results['scan_dir']}` for run log files.",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Files scanned | {results['files_scanned']} |",
        f"| Files passed | {results['files_passed']} |",
        f"| Files with violations | {results['files_failed']} |",
        f"| Total violations | {results['violation_count']} |",
        f"| Overall result | **{overall}** |",
        "",
        "## SLA Status",
        "",
        f"| SLA | Status |",
        f"|-----|--------|",
        f"| SLA-ML2-001 Record Integrity | {sla_ml2_001} |",
        f"| KPI-ML2-004 Schema Compliance | {kpi_ml2_004} |",
        "",
        "## Findings",
        "",
    ]

    if not violations:
        lines.append("All run log files pass PRO-023 schema validation.")
    else:
        if critical:
            lines.append(f"### Critical ({len(critical)})")
            lines.append("")
            for v in critical:
                lines.append(f"- **{v['file']}** — `{v['field']}`: {v['issue']}")
            lines.append("")
        if major:
            lines.append(f"### Major ({len(major)})")
            lines.append("")
            for v in major:
                lines.append(f"- **{v['file']}** — `{v['field']}`: {v['issue']}")
            lines.append("")
        if warnings:
            lines.append(f"### Warnings ({len(warnings)})")
            lines.append("")
            for v in warnings:
                lines.append(f"- **{v['file']}** — `{v['field']}`: {v['issue']}")
            lines.append("")

    lines += [
        "## Violations",
        "",
    ]
    if not violations:
        lines.append("None")
    else:
        lines.append(f"See Findings above. {len(violations)} total violation(s).")

    lines += [
        "",
        "## Next Actions",
        "",
    ]
    if results["exit_code"] == 0:
        lines.append("None — all run logs compliant.")
    else:
        lines.append(f"Fix {results['violation_count']} violation(s) identified above. Re-run validator after corrections.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Validate run log entries against PRO-023 Run Log Standard"
    )
    parser.add_argument(
        "--scan-dir",
        default=str(DEFAULT_SCAN_DIR),
        help=f"Directory to scan (default: {DEFAULT_SCAN_DIR})",
    )
    parser.add_argument(
        "--output-dir",
        default=str(OUTPUT_DIR),
        help=f"Output directory (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Write JSON output only, skip markdown",
    )
    args = parser.parse_args()

    scan_dir = Path(args.scan_dir)
    output_dir = Path(args.output_dir)

    if not scan_dir.exists():
        print(f"ERROR: Scan directory not found: {scan_dir}", file=sys.stderr)
        sys.exit(2)

    results = run_validation(scan_dir)

    json_path = write_json(results, output_dir)
    if not args.json_only:
        md_path = write_md(results, output_dir)
        print(f"Run log validation complete.")
        print(f"  Files scanned: {results['files_scanned']}")
        print(f"  Violations: {results['violation_count']}")
        print(f"  JSON: {json_path.relative_to(REPO_ROOT)}")
        print(f"  MD:   {md_path.relative_to(REPO_ROOT)}")
    else:
        print(f"Run log validation complete. JSON: {json_path.relative_to(REPO_ROOT)}")

    sys.exit(results["exit_code"])


if __name__ == "__main__":
    main()
