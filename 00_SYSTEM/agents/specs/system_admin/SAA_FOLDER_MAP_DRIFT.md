---
id: proto-folder-map-drift
title: Proto-Agent Charter - Folder Map Drift
owner: ML1
status: draft
created_date: 2026-02-09
last_updated: 2026-02-09
tags: []
---

# Folder-Map-Drift — Proto-Agent Charter (Draft)

## Purpose
Compare `FOLDER_MAP.md` to actual repo structure and report drift.

## Scope
Top-level and declared subfolders; identifies unmapped items, missing items, and misuse signals.

## Authority
None. Advisory/draft output only.

## Inputs
- `FOLDER_MAP.md`
- `SCHEMAS.md`
- Filesystem state
- Prior drift reports

## Outputs
- One drift report in `09_INBOX/_AGENT_OUTPUT/` with delta vs last report

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- Do not deep-scan file contents beyond frontmatter/filenames

## Definition of Done
Report produced with mapped vs actual counts, deltas, and recommended map updates.
