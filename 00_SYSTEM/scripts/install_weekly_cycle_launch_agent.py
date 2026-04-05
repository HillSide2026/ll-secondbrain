#!/usr/bin/env python3
"""
Install or remove the local launchd job for the weekly SMA cycle.

Schedules run_weekly_cycle.py every Monday at 09:00 Toronto time.
The sweep chains: System Admin Sweep (SAA) → System Management Sweep (SMA-001..005).
"""

from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path


LABEL = "ca.levinelaw.ml2.weekly-cycle"
REPO_ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = REPO_ROOT / "00_SYSTEM" / "scripts" / "run_weekly_cycle.py"
LAUNCH_AGENTS_DIR = Path.home() / "Library" / "LaunchAgents"
PLIST_PATH = LAUNCH_AGENTS_DIR / f"{LABEL}.plist"
LOG_DIR = REPO_ROOT / "06_RUNS" / "logs" / "weekly_cycle"

# Monday = 2 in launchd Weekday (0=Sunday, 1=Monday... wait, launchd uses 0=Sunday)
WEEKDAY_MONDAY = 1
HOUR = 9
MINUTE = 0


def launchctl_domain() -> str:
    return f"gui/{os.getuid()}"


def service_target() -> str:
    return f"{launchctl_domain()}/{LABEL}"


def build_plist() -> dict:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return {
        "Label": LABEL,
        "ProgramArguments": [sys.executable, str(RUNNER_PATH)],
        "WorkingDirectory": str(REPO_ROOT),
        "RunAtLoad": False,
        "ProcessType": "Background",
        "StartCalendarInterval": {
            "Weekday": WEEKDAY_MONDAY,
            "Hour": HOUR,
            "Minute": MINUTE,
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
    print(f"Scheduled: every Monday at {HOUR:02d}:{MINUTE:02d} (America/Toronto)")


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
    parser = argparse.ArgumentParser(description="Install or remove the weekly SMA cycle launch agent.")
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
