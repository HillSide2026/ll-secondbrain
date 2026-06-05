---
id: readme_md
title: Second Brain — Layer 1 Knowledge Repository
owner: ML1
status: draft
created_date: 2026-01-25
last_updated: 2026-01-25
tags: []
---

# Second Brain — Layer 1 Knowledge Repository

This repository is the **Layer 1 system of record** for Matthew Levine’s Second Brain,
focused on Levine Law (2026).

## Purpose
This repository exists to preserve, structure, and govern:
- ML1-approved doctrine
- Derived playbooks and templates
- Research and reference material
- Decision provenance and system rules

It is **file-based, Git-versioned, and auditable by design**.

## Authority Model
- **ML1 (Matthew Levine)** retains final judgment and approval authority
- This repository records and enforces those decisions
- No agent, tool, or workflow outranks the contents of this repository

## Structure
All structure, schemas, and governance rules are defined in `/00_SYSTEM`.
No content outside `/00_SYSTEM` may contradict it.

## What This Repository Is Not
- Not an execution environment
- Not an agent runtime
- Not a scratchpad
- Not a place for unapproved policy

Execution systems may read from or write to this repository
*only* according to its rules.

## Plane Ticket Sync

Plane is the source of truth for ticket status, assignee, priority, labels,
cycle, and project. This repository stores Git-versioned Markdown snapshots
inside explicitly mapped project folders for second-brain reading and linking.

Setup:

1. Use Node 22 or newer.
2. Copy `.env.example` to your local environment manager and set:
   - `PLANE_API_KEY`
   - `PLANE_WORKSPACE_SLUG`
   - `PLANE_API_BASE_URL` such as `https://api.plane.so`
3. Map Plane projects in
   `00_SYSTEM/integrations/plane/project-map.json`. Unmapped Plane projects are
   skipped with a warning; the sync never creates project folders from Plane.
4. Run:

```sh
npm run sync:plane
```

The sync fetches Plane projects and work items, writes snapshots named
`PLANE-{issue_id}.md` into each mapped project's configured ticket directory,
and preserves manual sections beginning at `## Links`. It is safe to rerun.

GitHub Actions runs `.github/workflows/sync-plane.yml` on a schedule and via
manual dispatch. Add the same Plane values as repository secrets; do not commit
credentials.
