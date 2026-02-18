---
id: proto-agent-index-reconciler
title: Proto-Agent Charter - Agent Index Reconciler
owner: ML1
status: draft
created_date: 2026-02-18
last_updated: 2026-02-18
tags: []
---

# Agent-Index-Reconciler — Proto-Agent Charter (Draft)

## Purpose
Reconcile the Agent Index (in `00_SYSTEM/AGENTS/specs/AGENT_TYPOLOGY.md`) against the
current repo state and report drift.

## Scope
This agent applies only to ML2 governed artifacts as defined in the
ML2 Ontology Boundary invariant: `01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md`

In-scope artifacts include:

- System agents in `00_SYSTEM/AGENTS/`
- System admin agent specs in `00_SYSTEM/AGENTS/specs/system_admin/`
- Agent frameworks in `00_SYSTEM/AGENTS/specs/`
- Practice area master agents under `02_PLAYBOOKS/**/AGENTS/` and `02_PLAYBOOKS/**/agents/`
- Other agent specs named `AGENT_*` or `AGENT_SPEC-*` under governed layers

Out-of-scope artifacts include:

- Runtime logs
- Scripts and tooling
- Environment configuration
- Secrets and credentials
- CI or tooling config
- Drafts outside governed layers

Boundary Reference: INV-ML2-BOUNDARY (01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md)

## Authority
None. Advisory/draft output only.

## Inputs
- `00_SYSTEM/AGENTS/specs/AGENT_TYPOLOGY.md`
- Filesystem state
- Prior reconciliation reports (if any)

## Outputs
- One reconciliation report in `09_INBOX/_AGENT_OUTPUT/` with:
  - additions (present in repo, missing in index)
  - removals (in index, missing in repo)
  - path changes or duplicate locations
  - naming or status mismatches (from frontmatter if present)
  - recommended updates to the Agent Index section

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- Do not deep-scan file contents beyond frontmatter/filenames

## Definition of Done
Report produced with a clear delta against the current Agent Index and
actionable update notes.
