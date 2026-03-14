#!/usr/bin/env python3
"""Wrapper for scripts/archive_soft_junk_selection.py."""

from pathlib import Path
import runpy


REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "scripts" / "archive_soft_junk_selection.py"

runpy.run_path(str(TARGET), run_name="__main__")
