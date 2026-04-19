#!/usr/bin/env python3
"""
ML2 Schema Audit — scripts/ml2_schema_audit.py

Audits ML2 canonical directories against SLA requirements.

SLAs covered:
  SLA-ML2-002  Approval Traceability (approved_by + approved_date required)
  SLA-ML2-005  Status Clarity (only approved/draft/superseded permitted)
  KPI-ML2-001  Doctrine Approval Coverage (target: >= 95%)
  KPI-ML2-002  Draft Backlog Size (target: <= 10; no draft > 30 days without reason)
  KPI-ML2-004  Schema Compliance Rate (target: 100%)

Usage:
  python3 scripts/ml2_schema_audit.py
  python3 scripts/ml2_schema_audit.py --paths 01_DOCTRINE 02_PLAYBOOKS

Output:
  06_RUNS/ops/sla_audit/audit_{timestamp}.json
  06_RUNS/ops/sla_audit/audit_{timestamp}.md
"""

import os
import re
import sys
import json
import glob
import argparse
from datetime import datetime, date
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent

DEFAULT_SCAN_PATHS = ["01_DOCTRINE", "02_PLAYBOOKS"]

VALID_STATUSES = {"approved", "draft", "superseded"}

# Fields required in every scanned artifact
REQUIRED_FIELDS = {"id", "title", "owner", "status"}

# Additional fields required when status == approved
APPROVED_REQUIRED_FIELDS = {"approved_by", "approved_date"}

# Null/empty values that don't count as present
NULL_VALUES = {"", "~", "null", "none", "tbd"}

# Draft age threshold (days) before flagging without a recorded reason
DRAFT_MAX_AGE_DAYS = 30

# KPI targets
TARGET_APPROVAL_COVERAGE = 0.95   # KPI-ML2-001
TARGET_DRAFT_CEILING = 10         # KPI-ML2-002
TARGET_SCHEMA_COMPLIANCE = 1.0    # KPI-ML2-004

OUTPUT_DIR = REPO_ROOT / "06_RUNS" / "ops" / "sla_audit"

# ── Frontmatter Parser ────────────────────────────────────────────────────────

def parse_frontmatter(path: Path) -> dict:
    """
    Extract YAML frontmatter from a .md or .yaml file.
    Returns a flat dict of key: value strings, or None if no frontmatter found.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # For .yaml files, parse the whole file as frontmatter
    if path.suffix == ".yaml":
        return _parse_yaml_block(text)

    # For .md files, extract --- ... --- block
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    return _parse_yaml_block(match.group(1))


def _parse_yaml_block(block: str) -> dict:
    """Minimal YAML key:value parser (no external dependencies)."""
    result = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip("'\"")
        if key:
            result[key] = val
    return result


# ── Checks ────────────────────────────────────────────────────────────────────

def check_file(path: Path, rel_path: str) -> list:
    """
    Run all checks against a single file.
    Returns a list of violation dicts (empty = compliant).
    """
    fm = parse_frontmatter(path)
    violations = []

    if fm is None:
        violations.append({
            "file": rel_path,
            "sla": "SLA-ML2-004",
            "check": "no_frontmatter",
            "detail": "File has no parseable frontmatter — cannot validate"
        })
        return violations

    # ── Required fields ──
    for field in REQUIRED_FIELDS:
        val = fm.get(field, "")
        if not val or val.lower() in NULL_VALUES:
            violations.append({
                "file": rel_path,
                "sla": "SLA-ML2-004",
                "check": "missing_required_field",
                "detail": f"Required field missing or null: {field}"
            })

    # ── Valid status vocabulary (SLA-ML2-005) ──
    status = fm.get("status", "").lower()
    if status and status not in VALID_STATUSES:
        violations.append({
            "file": rel_path,
            "sla": "SLA-ML2-005",
            "check": "invalid_status_value",
            "detail": f"status: '{status}' is not in approved vocabulary {{approved, draft, superseded}}"
        })

    # ── Approval traceability (SLA-ML2-002) ──
    if status == "approved":
        for field in APPROVED_REQUIRED_FIELDS:
            val = fm.get(field, "")
            if not val or val.lower() in NULL_VALUES:
                violations.append({
                    "file": rel_path,
                    "sla": "SLA-ML2-002",
                    "check": "missing_approval_metadata",
                    "detail": f"status: approved but {field} is missing or null"
                })

    # ── Draft age (KPI-ML2-002) ──
    if status == "draft":
        age_days = _draft_age_days(fm)
        if age_days is not None and age_days > DRAFT_MAX_AGE_DAYS:
            violations.append({
                "file": rel_path,
                "sla": "KPI-ML2-002",
                "check": "stale_draft",
                "detail": f"Draft is {age_days} days old (threshold: {DRAFT_MAX_AGE_DAYS} days) — requires recorded blocker reason or promotion"
            })

    return violations


def _draft_age_days(fm: dict) -> int:
    """Calculate age in days from last_updated or created_date."""
    for field in ("last_updated", "created_date"):
        val = fm.get(field, "")
        if val:
            try:
                d = date.fromisoformat(val.strip("'\""))
                return (date.today() - d).days
            except ValueError:
                continue
    return None


# ── Audit Runner ──────────────────────────────────────────────────────────────

def is_doctrine_artifact(path: Path) -> bool:
    """Return True if this file should be validated as a doctrine artifact.

    Rules:
    - All .md files are doctrine artifacts.
    - .yaml files in 01_DOCTRINE are doctrine artifacts (index files, etc.).
    - .yaml files in 02_PLAYBOOKS are workflow config/data (steps.yaml,
      metadata.yaml, etc.) and are NOT doctrine artifacts — skip schema checks.
    """
    if path.suffix == ".md":
        return True
    if path.suffix == ".yaml":
        parts = path.parts
        for part in parts:
            if part == "01_DOCTRINE":
                return True
        return False
    return False


def run_audit(scan_paths: list) -> dict:
    """Scan all paths and return audit results."""
    all_files = []
    for rel in scan_paths:
        base = REPO_ROOT / rel
        for ext in ("*.md", "*.yaml"):
            for p in base.rglob(ext):
                if is_doctrine_artifact(p):
                    all_files.append(p)

    total = 0
    approved_count = 0
    draft_count = 0
    superseded_count = 0
    schema_compliant = 0
    all_violations = []

    for path in sorted(all_files):
        rel_path = str(path.relative_to(REPO_ROOT))
        fm = parse_frontmatter(path)

        # Skip files with no frontmatter — they get a violation below
        status = (fm.get("status", "") if fm else "").lower()

        total += 1
        if status == "approved":
            approved_count += 1
        elif status == "draft":
            draft_count += 1
        elif status == "superseded":
            superseded_count += 1

        violations = check_file(path, rel_path)
        all_violations.extend(violations)

        # Schema compliant = no SLA-ML2-004 or SLA-ML2-002 violations
        file_violations = [v for v in violations
                           if v["sla"] in ("SLA-ML2-004", "SLA-ML2-002")]
        if not file_violations:
            schema_compliant += 1

    # ── KPI calculations ──
    approval_coverage = round(approved_count / total, 4) if total else 0
    schema_compliance_rate = round(schema_compliant / total, 4) if total else 0

    kpis = {
        "KPI-ML2-001_approval_coverage": {
            "value": approval_coverage,
            "pct": f"{approval_coverage * 100:.1f}%",
            "target": f">= {TARGET_APPROVAL_COVERAGE * 100:.0f}%",
            "pass": approval_coverage >= TARGET_APPROVAL_COVERAGE
        },
        "KPI-ML2-002_draft_backlog": {
            "value": draft_count,
            "target": f"<= {TARGET_DRAFT_CEILING}",
            "pass": draft_count <= TARGET_DRAFT_CEILING,
            "stale_drafts": len([v for v in all_violations if v["check"] == "stale_draft"])
        },
        "KPI-ML2-004_schema_compliance": {
            "value": schema_compliance_rate,
            "pct": f"{schema_compliance_rate * 100:.1f}%",
            "target": "100%",
            "pass": schema_compliance_rate == 1.0
        }
    }

    # ── SLA pass/fail ──
    sla_violations = {}
    for v in all_violations:
        sla_violations.setdefault(v["sla"], []).append(v)

    slas = {
        "SLA-ML2-002": {"pass": "SLA-ML2-002" not in sla_violations,
                        "violation_count": len(sla_violations.get("SLA-ML2-002", []))},
        "SLA-ML2-005": {"pass": "SLA-ML2-005" not in sla_violations,
                        "violation_count": len(sla_violations.get("SLA-ML2-005", []))},
        "SLA-ML2-004": {"pass": "SLA-ML2-004" not in sla_violations,
                        "violation_count": len(sla_violations.get("SLA-ML2-004", []))},
    }

    return {
        "run_id": datetime.utcnow().strftime("%Y%m%d-%H%M%S"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "scan_paths": scan_paths,
        "summary": {
            "total_artifacts": total,
            "approved": approved_count,
            "draft": draft_count,
            "superseded": superseded_count,
            "other_or_missing_status": total - approved_count - draft_count - superseded_count,
            "total_violations": len(all_violations)
        },
        "slas": slas,
        "kpis": kpis,
        "violations": all_violations
    }


# ── Output Writers ────────────────────────────────────────────────────────────

def write_json(results: dict, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"audit_{results['run_id']}.json"
    path.write_text(json.dumps(results, indent=2))
    return path


def write_md(results: dict, output_dir: Path) -> Path:
    s = results["summary"]
    kpis = results["kpis"]
    slas = results["slas"]
    violations = results["violations"]

    def status_icon(passing: bool) -> str:
        return "PASS" if passing else "FAIL"

    lines = [
        "---",
        f"run_id: {results['run_id']}",
        f"timestamp: {results['timestamp']}",
        "type: ml2_schema_audit",
        "classification: internal_working_material",
        "---",
        "",
        "# ML2 Schema Audit",
        f"**Run:** {results['run_id']}  ",
        f"**Paths:** {', '.join(results['scan_paths'])}",
        "",
        "## Summary",
        "",
        f"| | Count |",
        f"|---|---|",
        f"| Total artifacts | {s['total_artifacts']} |",
        f"| Approved | {s['approved']} |",
        f"| Draft | {s['draft']} |",
        f"| Superseded | {s['superseded']} |",
        f"| Status missing/other | {s['other_or_missing_status']} |",
        f"| **Total violations** | **{s['total_violations']}** |",
        "",
        "## SLA Results",
        "",
        "| SLA | Result | Violations |",
        "|---|---|---|",
    ]
    for sla_id, data in slas.items():
        lines.append(f"| {sla_id} | {status_icon(data['pass'])} | {data['violation_count']} |")

    lines += [
        "",
        "## KPI Results",
        "",
        "| KPI | Value | Target | Result |",
        "|---|---|---|---|",
    ]
    for kpi_id, data in kpis.items():
        val = data.get("pct", data.get("value"))
        lines.append(f"| {kpi_id.split('_', 1)[0]} | {val} | {data['target']} | {status_icon(data['pass'])} |")

    if violations:
        lines += ["", "## Violations", ""]
        by_sla: dict[str, list] = {}
        for v in violations:
            by_sla.setdefault(v["sla"], []).append(v)
        for sla_id in sorted(by_sla):
            lines.append(f"### {sla_id}")
            for v in by_sla[sla_id]:
                lines.append(f"- `{v['file']}` — {v['check']}: {v['detail']}")
            lines.append("")
    else:
        lines += ["", "## Violations", "", "None — fully compliant.", ""]

    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"audit_{results['run_id']}.md"
    path.write_text("\n".join(lines))
    return path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ML2 Schema Audit")
    parser.add_argument("--paths", nargs="+", default=DEFAULT_SCAN_PATHS,
                        help="Repo-relative paths to scan")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR),
                        help="Output directory for audit reports")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    print(f"Scanning: {', '.join(args.paths)}")

    results = run_audit(args.paths)
    json_path = write_json(results, output_dir)
    md_path = write_md(results, output_dir)

    s = results["summary"]
    print(f"\nArtifacts: {s['total_artifacts']} total  |  "
          f"{s['approved']} approved  |  {s['draft']} draft  |  "
          f"{s['superseded']} superseded")
    print(f"Violations: {s['total_violations']}")
    print()
    for sla_id, data in results["slas"].items():
        icon = "✓" if data["pass"] else "✗"
        print(f"  {icon} {sla_id}: {data['violation_count']} violations")
    print()
    for kpi_id, data in results["kpis"].items():
        icon = "✓" if data["pass"] else "✗"
        val = data.get("pct", data.get("value"))
        print(f"  {icon} {kpi_id.split('_', 1)[0]}: {val} (target {data['target']})")
    print(f"\nReports:\n  {json_path}\n  {md_path}")

    sys.exit(0 if s["total_violations"] == 0 else 1)


if __name__ == "__main__":
    main()
