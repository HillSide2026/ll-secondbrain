---
id: proto-repo-linter
title: Proto-Agent Charter - Repo Linter
owner: ML1
status: draft
created_date: 2026-02-09
last_updated: 2026-02-09
tags: []
---

# Repo-Linter — Proto-Agent Charter (Draft)

## Purpose
Detect structural, schema, and naming violations.

## Scope
Entire repo structure and project folder compliance; reports only.

## Authority
None. Advisory/draft output only.

## Inputs
- Folder map
- Project schema
- Schema rules
- Current filesystem state

## Outputs
- One lint report in `09_INBOX/_AGENT_OUTPUT/` with findings, severity, and policy questions

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- If rules conflict or are ambiguous: flag as policy questions

## Definition of Done
Report produced with violations categorized, safe fixes listed, and ML1 questions flagged.
