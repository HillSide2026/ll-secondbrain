#!/usr/bin/env python3
"""Shim: canonical version is scripts/validate_matter_yaml.py. Delegates to it."""

from pathlib import Path
import runpy

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "scripts" / "validate_matter_yaml.py"

runpy.run_path(str(TARGET), run_name="__main__")
