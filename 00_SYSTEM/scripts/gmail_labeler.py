#!/usr/bin/env python3
"""Shim: canonical version is scripts/gmail_labeler.py. Delegates to it."""

from pathlib import Path
import runpy

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "scripts" / "gmail_labeler.py"

runpy.run_path(str(TARGET), run_name="__main__")
