---
id: 04_initiatives__ll_portfolio__07_strategic_projects__llp_005_matter_command_control__readme_md
title: LLP-005 — Matter Command and Control
owner: ML1
status: on track
created_date: 2026-03-04
last_updated: 2026-03-04
tags: [matter-operations, command-control]
---

# LLP-005 — Matter Command and Control

## Purpose

Stand up a deterministic matter command layer that uses Clio, SharePoint, and Gmail as systems of record while producing daily admin and intelligence artifacts inside ML2.

## Scope

### In Scope

- Daily firm-level digest generation
- Per-matter status packet generation
- Exception lists (unmapped inbox, missing doc links, overdue work)
- Read connectors for Clio, Gmail, and SharePoint
- Deterministic routing keyed by Clio matter number
- Citation-first assertions with source pointers

### Out of Scope

- Replacing Clio, SharePoint, or Gmail records
- Writing operational truth back to source systems
- Persistent shadow database of source records

## ML1 Authority Statement

ML1 is the sole authority to approve rule changes, escalation policy, and promotion to production governance.

## Explicit Prohibitions

ML2 must NOT:

- Treat ML2 artifacts as source-of-truth matter status
- Persist full-source replicas beyond approved cache snapshots
- Emit assertions without source pointers

## Approval State

**SLICE IMPLEMENTATION AUTHORIZED (draft)** — Thin vertical slice in progress.

## Artifacts

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISKS_INITIAL.md`
- `IMPLEMENTATION_SPEC.md`
- `APPROVAL_RECORD.md`
