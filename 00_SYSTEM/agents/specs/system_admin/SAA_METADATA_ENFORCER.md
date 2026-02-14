---
id: proto-metadata-enforcer
title: Proto-Agent Charter - Metadata Enforcer
owner: ML1
status: draft
created_date: 2026-02-14
last_updated: 2026-02-14
tags: []
---

# Metadata-Enforcer — Proto-Agent Charter (Draft)

## Purpose
Ensure required frontmatter fields exist across governed artifact types.

## Scope
Playbooks, templates, doctrine, and agent specs; validates required fields are present and non-empty.

## Authority
None. Advisory/draft output only.

## Inputs
- `00_SYSTEM/schemas/SCHEMAS.md`
- `00_SYSTEM/schemas/SCHEMAS_INBOX_TRIAGE.md` (as applicable)
- Artifact files under `01_DOCTRINE/`, `02_PLAYBOOKS/`, `03_TEMPLATES/`, `00_SYSTEM/agents/`

## Outputs
- One metadata compliance report in `09_INBOX/_AGENT_OUTPUT/`

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- If schemas conflict: flag as policy questions

## Definition of Done
Report produced listing missing or empty required fields (id, version, status, and any schema-specific requirements).
