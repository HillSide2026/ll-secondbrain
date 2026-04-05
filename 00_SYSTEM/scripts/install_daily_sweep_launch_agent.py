#!/usr/bin/env python3
"""
Install or remove the local launchd job for the daily full sweep.

Schedules run_daily_full_sweep.py at 06:30 Toronto time (America/Toronto).
The sweep chains: Matter Admin → Portfolio Agents → Chief of Staff Synthesis.
"""

from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Tuple

import yaml


LABEL = "ca.levinelaw.ml2.daily-sweep"
REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "00_SYSTEM" / "CONFIG" / "run_schedule.yml"
RUNNER_PATH = REPO_ROOT / "00_SYSTEM" / "scripts" / "run_daily_full_sweep.py"
LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"
PLIST_PATH = LAUNCH_AGENTS_DIR / f"{LABEL}.plist"
LOG_DIR = REPO_ROOT / "06_RUNS" / "logs" / "daily_sweep"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def parse_schedule() -> Tuple[int, int]:
    config = load_yaml(CONFIG_PATH)
    run_cfg = ((config.get("runs") or {}).get("daily_full_sweep") or {})
    schedule_local = str(run_cfg.get("schedule_local") or "06:30").strip()
    hour_text, minute_text = schedule_local.split(":", 1)
    return int(hour_text), int(minute_text)


def launchctl_domain() -> str:
    return f"gui/{os.getuid()}"


def service_target() -> str:
    return f"{launchctl_domain()}/{LABEL}"


def build_plist() -> dict:
    hour, minute = parse_schedule()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return {
        "Label": LABEL,
        "ProgramArguments": [sys.executable, str(RUNNER_PATH)],
        "WorkingDirectory": str(REPO_ROOT),
        "RunAtLoad": False,
        "ProcessType": "Background",
        "StartCalendarInterval": {
            "Hour": hour,
            "Minute": minute,
        },
        "StandardOutPath": str(LOG_DIR / "launchd.stdout.log"),
        "StandardErrorPath": str(LOG_DIR / "launchd.stderr.log"),
    }


def run_launchctl(*args: str, check: bool) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["launchctl", *args],
        capture_output=True,
        text=True,
        check=check,
    )


def install() -> None:
    LAUNCH_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    with PLIST_PATH.open("wb") as handle:
        plistlib.dump(build_plist(), handle)

    run_launchctl("bootout", launchctl_domain(), str(PLIST_PATH), check=False)
    run_launchctl("bootstrap", launchctl_domain(), str(PLIST_PATH), check=True)
    run_launchctl("enable", service_target(), check=False)
    print(f"Installed launch agent: {PLIST_PATH}")
    print(f"Service target: {service_target()}")
    hour, minute = parse_schedule()
    print(f"Scheduled daily at {hour:02d}:{minute:02d} (America/Toronto)")


def uninstall() -> None:
    run_launchctl("bootout", launchctl_domain(), str(PLIST_PATH), check=False)
    if PLIST_PATH.exists():
        PLIST_PATH.unlink()
    print(f"Removed launch agent: {PLIST_PATH}")


def status() -> int:
    if not PLIST_PATH.exists():
        print(f"Launch agent plist not found: {PLIST_PATH}")
        return 1
    result = run_launchctl("print", service_target(), check=False)
    if result.returncode == 0:
        print(f"Loaded: {service_target()}")
        return 0
    print(result.stderr.strip() or result.stdout.strip() or f"Not loaded: {service_target()}")
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install or remove the daily full sweep launch agent.")
    parser.add_argument("--uninstall", action="store_true", help="Remove the launch agent.")
    parser.add_argument("--status", action="store_true", help="Print current launch agent status.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.status:
        return status()
    if args.uninstall:
        uninstall()
        return 0
    install()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
