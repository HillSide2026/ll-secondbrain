#!/usr/bin/env python3
"""
Pre-write validation hook for canonical path writes.
Runs as a Claude Code PreToolUse hook on Write and Edit tool calls.
Warns (non-blocking) when canonical artifacts are missing required metadata.
"""
import json
import sys

CANONICAL_PREFIXES = [
    "01_DOCTRINE",
    "02_PLAYBOOKS",
    "03_TEMPLATES",
    "05_MATTERS",
    "00_SYSTEM/AGENTS",
]

EXEMPT_FRAGMENTS = [
    "06_RUNS",
    "DRAFTS/",
    "_drafts/",
    "10_ARCHIVE",
    ".claude/",
    "scripts/",
    "09_INBOX",
]

REQUIRED_FRONTMATTER_FIELDS = ["status:", "owner:"]


def is_canonical_path(file_path):
    for exempt in EXEMPT_FRAGMENTS:
        if exempt in file_path:
            return False
    for prefix in CANONICAL_PREFIXES:
        if prefix in file_path:
            return True
    return False


def check_frontmatter(content):
    if not content or "---" not in content[:200]:
        return []
    warnings = []
    header = content[:600]
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in header:
            warnings.append("Missing '{}' in frontmatter".format(field.rstrip(":")))
    return warnings


def main():
    try:
        raw = sys.stdin.read()
        tool_input = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    if not file_path or not is_canonical_path(file_path):
        sys.exit(0)

    warnings = check_frontmatter(content)
    if warnings:
        print("[CANONICAL WRITE WARNING] {}:".format(file_path), file=sys.stderr)
        for w in warnings:
            print("  {}".format(w), file=sys.stderr)
        print("  Canonical artifacts should carry status: and owner: frontmatter fields.", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
