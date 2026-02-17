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
This agent applies only to ML2 governed artifacts as defined in the
ML2 Ontology Boundary invariant: `01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md`

In-scope artifacts include:

- Governed ontology layers (00_SYSTEM→10_ARCHIVE)
- Integration specifications located under `00_SYSTEM/integrations/`
- Metadata-bearing artifacts with valid frontmatter

Out-of-scope artifacts include:

- Repository infrastructure files (.gitignore, LICENSE, README.md, etc.)
- Runtime logs
- Scripts and tooling
- Environment configuration
- Secrets and credentials
- CI or tooling config

Boundary Reference: INV-ML2-BOUNDARY (01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md)

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
