#!/usr/bin/env python3
"""
Daily Full Sweep Runner

Orchestrates the end-to-end daily chain:
  1. Matter Admin  (scripts/run_matter_admin.py)
  2. Portfolio Agents  (00_SYSTEM/scripts/run_ll_portfolio_agents.py)
  3. Chief of Staff Synthesis  (LLM-001, invoked via claude CLI)

Writes a run log to:
  06_RUNS/${run_id}/daily_sweep/RUN_LOG.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Dict, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]
RUN_LOG_DIR = REPO_ROOT / "06_RUNS"

MATTER_ADMIN_SCRIPT = REPO_ROOT / "scripts" / "run_matter_admin.py"
PORTFOLIO_AGENTS_SCRIPT = REPO_ROOT / "00_SYSTEM" / "scripts" / "run_ll_portfolio_agents.py"

CLAUDE_SEARCH_PATHS = [
    Path.home() / "Library" / "Application Support" / "Claude" / "claude-code",
]

# Timeout for LLM-001 synthesis step (seconds)
LLM001_TIMEOUT = 600


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def generate_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%H%M%SZ")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"RUN-{date}-DAILY-SWEEP-{stamp}"


def find_claude_binary() -> Optional[str]:
    """Locate the claude CLI binary."""
    import shutil
    if shutil.which("claude"):
        return "claude"
    # Search Claude Code app installation directories for latest version
    for base in CLAUDE_SEARCH_PATHS:
        if not base.is_dir():
            continue
        candidates = sorted(
            (v / "claude" for v in base.iterdir() if v.is_dir()),
            key=lambda p: p.parent.name,
            reverse=True,
        )
        for candidate in candidates:
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)
    return None


def run_python_script(script: Path, label: str) -> Dict:
    """Run a Python script as a subprocess. Returns result dict."""
    print(f"[daily_sweep] Starting: {label}")
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    status = "ok" if result.returncode == 0 else "failed"
    print(f"[daily_sweep] {label}: {status} (rc={result.returncode})")
    if result.stderr.strip():
        print(f"[daily_sweep] {label} stderr: {result.stderr.strip()[:500]}")
    return {
        "label": label,
        "script": str(script.relative_to(REPO_ROOT)),
        "return_code": result.returncode,
        "status": status,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def build_llm001_prompt(run_id: str, today: str) -> str:
    return dedent(f"""\
        You are LLM-001, the Chief of Staff agent for Levine Law's second brain system.

        Your job is to synthesize the outputs of three management agents (LLM-004, LLM-005, LLM-006)
        into a decision-ready brief for ML1 (Matthew Levine). You do not generate raw project data.
        You read what the agents have already produced.

        Authority rules — you CANNOT:
        - Approve any stage gate, metric, scope change, or doctrine
        - Issue binding instructions to any agent or execution layer
        - Override or reinterpret ML1 decisions
        - Act on inputs that are missing or stale (flag this and halt instead)

        You MUST:
        1. Read all required input files listed in your spec.
        2. Verify all inputs carry a Generated: timestamp before proceeding.
        3. Identify the top items requiring ML1 decision — especially cases where LLM-005
           recommends advancement on a project that LLM-006 has flagged for compliance gaps.
        4. Apply an LL-first incentive frame: revenue / cash collection, owner-compensation
           support, margin discipline, capacity / client-quality control, approved lane
           discipline, and F01 -> F02 -> F03 sequencing.
        5. Treat HillSide-level incentives as a secondary linkage thread only. Surface
           them when material, but do not let them silently replace LL priorities.
        6. Write COS_BRIEF.md: a plain-language narrative brief (not tables). ML1 should be able
           to read this in under 3 minutes and know exactly what needs their attention.
        7. Write ML1_DECISION_QUEUE.md: ranked table of items requiring ML1 judgment.
        8. Write CROSS_AGENT_CONFLICTS.md: document every case where LLM-005 and LLM-006
           signal opposite things about the same project.

        Output location: 04_INITIATIVES/LL_PORTFOLIO/CHIEF_OF_STAFF/

        All outputs are advisory. Label every output with:
        > Advisory output. ML1 approval required before any action is taken.

        Today's date: {today}
        Run ID: {run_id}
    """)


def invoke_llm001(run_id: str) -> Dict:
    """Invoke LLM-001 Chief of Staff via the claude CLI."""
    label = "LLM-001 Chief of Staff"
    print(f"[daily_sweep] Starting: {label}")

    claude_bin = find_claude_binary()
    if not claude_bin:
        msg = "claude binary not found — skipping LLM-001 synthesis"
        print(f"[daily_sweep] WARNING: {msg}")
        return {"label": label, "status": "skipped", "error": msg}

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    prompt = build_llm001_prompt(run_id, today)

    try:
        result = subprocess.run(
            [claude_bin, "--dangerously-skip-permissions", "--print", "-p", prompt],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=LLM001_TIMEOUT,
        )
        status = "ok" if result.returncode == 0 else "failed"
        print(f"[daily_sweep] {label}: {status} (rc={result.returncode})")
        return {
            "label": label,
            "return_code": result.returncode,
            "status": status,
            "stdout": result.stdout.strip()[:2000],
            "stderr": result.stderr.strip()[:500],
        }
    except subprocess.TimeoutExpired:
        msg = f"timed out after {LLM001_TIMEOUT}s"
        print(f"[daily_sweep] {label}: {msg}")
        return {"label": label, "status": "timeout", "error": msg}


def write_run_log(run_root: Path, steps: list[Dict]) -> None:
    run_root.mkdir(parents=True, exist_ok=True)
    overall = "ok" if all(s["status"] in ("ok", "skipped") for s in steps) else "partial"

    lines = [
        "# RUN LOG — Daily Full Sweep",
        "",
        f"Generated: {utc_now()}",
        f"Overall status: {overall}",
        "",
    ]
    for step in steps:
        rc = step.get("return_code", "—")
        lines += [
            f"## {step['label']}",
            f"- Status: {step['status']}",
            f"- Return code: {rc}",
        ]
        if step.get("error"):
            lines.append(f"- Error: {step['error']}")
        lines.append("")

    (run_root / "RUN_LOG.md").write_text("\n".join(lines), encoding="utf-8")

    provenance = {
        "run_id": run_root.parent.name,
        "generated_at": utc_now(),
        "steps": steps,
    }
    (run_root / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"[daily_sweep] Run log written: {run_root}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the daily full sweep.")
    parser.add_argument("--run-id", help="Override run ID (default: auto)")
    parser.add_argument("--skip-cos", action="store_true", help="Skip LLM-001 synthesis step")
    args = parser.parse_args()

    run_id = args.run_id or generate_run_id()
    run_root = RUN_LOG_DIR / run_id / "daily_sweep"

    print(f"[daily_sweep] Starting run: {run_id}")
    steps: list[Dict] = []

    # Step 1: Matter Admin
    result = run_python_script(MATTER_ADMIN_SCRIPT, "Matter Admin")
    steps.append(result)
    if result["status"] == "failed":
        write_run_log(run_root, steps)
        print("[daily_sweep] Aborting: matter admin failed (required for downstream steps)")
        return 1

    # Step 2: Portfolio Agents
    result = run_python_script(PORTFOLIO_AGENTS_SCRIPT, "Portfolio Agents (LLM-004/005/006)")
    steps.append(result)
    if result["status"] == "failed":
        write_run_log(run_root, steps)
        print("[daily_sweep] Aborting: portfolio agents failed (required for LLM-001)")
        return 1

    # Step 3: Chief of Staff Synthesis
    if args.skip_cos:
        steps.append({"label": "LLM-001 Chief of Staff", "status": "skipped", "return_code": "—"})
    else:
        result = invoke_llm001(run_id)
        steps.append(result)

    write_run_log(run_root, steps)
    overall = all(s["status"] in ("ok", "skipped") for s in steps)
    print(f"[daily_sweep] Daily full sweep complete: {run_root}")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
