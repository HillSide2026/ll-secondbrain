#!/usr/bin/env python3
"""
Trade Remedies Daily Runner.

Executes the configured daily CITT watchlist scans and writes lightweight run
logs under `06_RUNS/logs/trade_remedies/citt_daily/`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "00_SYSTEM" / "CONFIG" / "run_schedule.yml"
SCAN_SCRIPT = REPO_ROOT / "00_SYSTEM" / "scripts" / "scan_citt_updates.py"
RUN_LOG_DIR = REPO_ROOT / "06_RUNS" / "logs" / "trade_remedies" / "citt_daily"
LATEST_RUNLOG_PATH = RUN_LOG_DIR / "runlog.md"
LATEST_PROVENANCE_PATH = RUN_LOG_DIR / "provenance.json"
HISTORY_DIR = RUN_LOG_DIR / "history"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def generate_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%H%M%SZ")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"RUN-{date}-TRADE-REMEDIES-CITT-DAILY-{stamp}"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def resolve_repo_path(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def configured_watches(config: dict) -> List[dict]:
    runs = config.get("runs") or {}
    trade_remedies = runs.get("trade_remedies_citt_daily") or {}
    scope = trade_remedies.get("scope") or {}
    return list(scope.get("watches") or [])


def run_watch(watch: dict, dry_run: bool) -> Dict[str, Any]:
    watchlist_path = resolve_repo_path(str(watch["watchlist"]))
    report_path = resolve_repo_path(str(watch["report"]))
    state_path = resolve_repo_path(str(watch["state"]))
    cmd = [
        sys.executable,
        str(SCAN_SCRIPT),
        "--watchlist",
        str(watchlist_path),
        "--report",
        str(report_path),
        "--state",
        str(state_path),
    ]
    started_at = utc_now()
    if dry_run:
        return {
            "watchlist": str(watchlist_path),
            "report": str(report_path),
            "state": str(state_path),
            "command": cmd,
            "started_at": started_at,
            "finished_at": utc_now(),
            "return_code": 0,
            "status": "dry-run",
            "stdout": "",
            "stderr": "",
        }

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    status = "ok" if result.returncode == 0 else "failed"
    return {
        "watchlist": str(watchlist_path),
        "report": str(report_path),
        "state": str(state_path),
        "command": cmd,
        "started_at": started_at,
        "finished_at": utc_now(),
        "return_code": result.returncode,
        "status": status,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def render_runlog(run_id: str, schedule_cfg: dict, results: List[dict], dry_run: bool) -> str:
    lines = [
        "# Trade Remedies CITT Daily Run Log",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at: `{utc_now()}`",
        f"- Schedule: `{schedule_cfg.get('schedule_local', 'unknown')} {schedule_cfg.get('timezone', 'local')}`",
        f"- Mode: `{'dry-run' if dry_run else 'live'}`",
        "",
        "## Watches",
        "",
    ]
    for result in results:
        lines.extend(
            [
                f"### {Path(result['watchlist']).name}",
                "",
                f"- Status: `{result['status']}`",
                f"- Return code: `{result['return_code']}`",
                f"- Watchlist: `{result['watchlist']}`",
                f"- Report: `{result['report']}`",
                f"- State: `{result['state']}`",
                f"- Started at: `{result['started_at']}`",
                f"- Finished at: `{result['finished_at']}`",
                "",
            ]
        )
        if result["stderr"]:
            lines.append("```text")
            lines.append(result["stderr"])
            lines.append("```")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def write_run_artifacts(run_id: str, payload: dict, runlog: str) -> None:
    RUN_LOG_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    LATEST_RUNLOG_PATH.write_text(runlog, encoding="utf-8")
    LATEST_PROVENANCE_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    compact = run_id.replace("RUN-", "").replace(":", "").replace("/", "-")
    (HISTORY_DIR / f"{compact}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the configured daily trade-remedies CITT scans.")
    parser.add_argument("--dry-run", action="store_true", help="Validate config and planned commands without executing the scanner.")
    parser.add_argument("--run-id", help="Override run ID (default: auto-generated).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_yaml(CONFIG_PATH)
    run_cfg = ((config.get("runs") or {}).get("trade_remedies_citt_daily") or {})
    if not run_cfg.get("enabled", False):
        print("Trade remedies CITT daily run is disabled in run_schedule.yml.")
        return 0

    watches = configured_watches(config)
    if not watches:
        raise SystemExit("No trade-remedies CITT watches configured in run_schedule.yml.")

    run_id = args.run_id or generate_run_id()
    results = [run_watch(watch, dry_run=args.dry_run) for watch in watches]
    runlog = render_runlog(run_id, run_cfg, results, dry_run=args.dry_run)
    payload = {
        "run_id": run_id,
        "generated_at": utc_now(),
        "mode": "dry-run" if args.dry_run else "live",
        "schedule": {
            "schedule_local": run_cfg.get("schedule_local"),
            "timezone": run_cfg.get("timezone"),
        },
        "results": results,
    }
    write_run_artifacts(run_id, payload, runlog)

    failed = [result for result in results if result["return_code"] != 0]
    print(f"Trade remedies CITT daily run complete: {LATEST_RUNLOG_PATH}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
