---
id: proto-registry-sync
title: Proto-Agent Charter - Registry Sync
owner: ML1
status: draft
created_date: 2026-02-14
last_updated: 2026-02-14
tags: []
---

# Registry-Sync — Proto-Agent Charter (Draft)

## Purpose
Verify that playbook registry entries reflect actual playbooks.

## Scope
`02_PLAYBOOKS/_registry/PLAYBOOK_INDEX.md` vs actual playbook folders and their `metadata.yaml`.

## Authority
None. Advisory/draft output only.

## Inputs
- `02_PLAYBOOKS/_registry/PLAYBOOK_INDEX.md`
- `02_PLAYBOOKS/**/metadata.yaml`
- Repo file tree under `02_PLAYBOOKS/`

## Outputs
- One registry sync report in `09_INBOX/_AGENT_OUTPUT/`

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation

## Definition of Done
Report produced listing missing registry entries, ghost entries, and status mismatches.
