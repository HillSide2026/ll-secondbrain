#!/usr/bin/env python3
"""
Integration Health Check — scripts/integration_health_check.py

Validates all integration paths and configurations against SLA-SYS-001
(Integration Integrity): all integrations must connect to the correct
resources with correct scope.

Checks:
  .mcp.json        — MCP server script paths exist and are executable
  .claude/settings.json — PreToolUse hook path exists and is executable;
                          MCP server paths (if duplicated there) are correct

Usage:
  python3 scripts/integration_health_check.py

Output:
  06_RUNS/ops/sla_audit/integration_health_{timestamp}.json
  06_RUNS/ops/sla_audit/integration_health_{timestamp}.md
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MCP_JSON = REPO_ROOT / ".mcp.json"
SETTINGS_JSON = REPO_ROOT / ".claude" / "settings.json"
OUTPUT_DIR = REPO_ROOT / "06_RUNS" / "ops" / "sla_audit"


# ── Checkers ──────────────────────────────────────────────────────────────────

def check_path(label: str, path_str: str, require_executable: bool = True) -> dict:
    """Check whether a declared script path exists and (optionally) is executable.

    When command is an interpreter (python3, node), the script file does not
    need the executable bit — the interpreter is invoked directly on the file.
    Pass require_executable=False for those cases.
    """
    p = Path(path_str)
    exists = p.exists()
    executable = os.access(p, os.X_OK) if exists else False
    if require_executable:
        status = "pass" if (exists and executable) else "fail"
        issue = None
        if not exists:
            issue = f"Path does not exist: {path_str}"
        elif not executable:
            issue = f"Path exists but is not executable: {path_str}"
    else:
        status = "pass" if exists else "fail"
        issue = None if exists else f"Path does not exist: {path_str}"
    return {
        "label": label,
        "declared_path": path_str,
        "exists": exists,
        "executable": executable,
        "status": status,
        "issue": issue
    }


def check_mcp_json() -> list:
    results = []
    if not MCP_JSON.exists():
        results.append({
            "label": ".mcp.json",
            "status": "fail",
            "issue": ".mcp.json not found at repo root"
        })
        return results

    try:
        cfg = json.loads(MCP_JSON.read_text())
    except Exception as e:
        results.append({"label": ".mcp.json", "status": "fail",
                        "issue": f"Cannot parse .mcp.json: {e}"})
        return results

    for server_name, server_cfg in cfg.get("mcpServers", {}).items():
        args = server_cfg.get("args", [])
        command = server_cfg.get("command", "")
        is_interpreter = command in ("python3", "python", "node", "nodejs")
        script_path = next((a for a in args if a.endswith(".py") or a.endswith(".js")), None)
        if script_path:
            results.append(check_path(
                f".mcp.json → {server_name}", script_path,
                require_executable=not is_interpreter))
        else:
            results.append({
                "label": f".mcp.json → {server_name}",
                "status": "warn",
                "issue": "No .py script path found in args — cannot verify"
            })
    return results


def check_settings_json() -> list:
    results = []
    if not SETTINGS_JSON.exists():
        results.append({
            "label": ".claude/settings.json",
            "status": "fail",
            "issue": ".claude/settings.json not found"
        })
        return results

    try:
        cfg = json.loads(SETTINGS_JSON.read_text())
    except Exception as e:
        results.append({"label": ".claude/settings.json", "status": "fail",
                        "issue": f"Cannot parse settings.json: {e}"})
        return results

    # Check PreToolUse hook
    hooks = cfg.get("hooks", {}).get("PreToolUse", [])
    for hook_group in hooks:
        for hook in hook_group.get("hooks", []):
            cmd = hook.get("command", "")
            if cmd:
                # Extract path from "python3 /some/path.py"
                parts = cmd.split()
                script_path = next((p for p in parts if p.endswith(".py")), None)
                if script_path:
                    results.append(check_path(
                        ".claude/settings.json → PreToolUse hook", script_path))

    # Check MCP server paths if present (may duplicate .mcp.json)
    for server_name, server_cfg in cfg.get("mcpServers", {}).items():
        args = server_cfg.get("args", [])
        command = server_cfg.get("command", "")
        is_interpreter = command in ("python3", "python", "node", "nodejs")
        script_path = next((a for a in args if a.endswith(".py") or a.endswith(".js")), None)
        if script_path:
            result = check_path(
                f".claude/settings.json → mcpServer:{server_name}", script_path,
                require_executable=not is_interpreter)
            if result["status"] == "fail":
                result["note"] = ("MCP servers are primarily configured in "
                                  ".mcp.json — this entry may be stale")
            results.append(result)

    return results


# ── Output Writers ────────────────────────────────────────────────────────────

def write_output(results: dict, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = results["run_id"]

    # JSON
    json_path = output_dir / f"integration_health_{run_id}.json"
    json_path.write_text(json.dumps(results, indent=2))

    # Markdown
    checks = results["checks"]
    overall = results["overall_status"]

    lines = [
        "---",
        f"run_id: {run_id}",
        f"timestamp: {results['timestamp']}",
        "type: integration_health_check",
        "sla: SLA-SYS-001",
        "classification: internal_working_material",
        "---",
        "",
        "# Integration Health Check",
        f"**Run:** {run_id}  ",
        f"**Overall:** {'PASS' if overall == 'pass' else 'FAIL'}",
        "",
        "## Results",
        "",
        "| Integration | Status | Issue |",
        "|---|---|---|",
    ]
    for c in checks:
        status = c.get("status", "unknown").upper()
        issue = c.get("issue") or c.get("note") or "—"
        label = c.get("label", "unknown")
        lines.append(f"| {label} | {status} | {issue} |")

    failures = [c for c in checks if c.get("status") == "fail"]
    if failures:
        lines += ["", "## Failures", ""]
        for f in failures:
            lines.append(f"- **{f['label']}**: {f.get('issue', 'unknown')}")

    md_path = output_dir / f"integration_health_{run_id}.md"
    md_path.write_text("\n".join(lines))

    return json_path, md_path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    run_id = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    timestamp = datetime.utcnow().isoformat() + "Z"

    checks = []
    checks.extend(check_mcp_json())
    checks.extend(check_settings_json())

    failures = [c for c in checks if c.get("status") == "fail"]
    overall = "pass" if not failures else "fail"

    results = {
        "run_id": run_id,
        "timestamp": timestamp,
        "sla": "SLA-SYS-001",
        "overall_status": overall,
        "total_checks": len(checks),
        "failures": len(failures),
        "checks": checks
    }

    json_path, md_path = write_output(results, OUTPUT_DIR)

    print(f"Integration Health Check — {overall.upper()}")
    print(f"Checks: {len(checks)}  |  Failures: {len(failures)}")
    for c in checks:
        icon = "✓" if c.get("status") == "pass" else ("!" if c.get("status") == "warn" else "✗")
        print(f"  {icon} {c['label']}: {c.get('status', 'unknown').upper()}")
        if c.get("issue"):
            print(f"    → {c['issue']}")
    print(f"\nReports:\n  {json_path}\n  {md_path}")

    sys.exit(0 if overall == "pass" else 1)


if __name__ == "__main__":
    main()
