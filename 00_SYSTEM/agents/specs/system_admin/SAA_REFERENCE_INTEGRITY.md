---
id: proto-reference-integrity
title: Proto-Agent Charter - Reference Integrity
owner: ML1
status: draft
created_date: 2026-02-14
last_updated: 2026-02-14
tags: []
---

# Reference-Integrity — Proto-Agent Charter (Draft)

## Purpose
Detect broken internal links, stale file references, and orphaned docs.

## Scope
Markdown links and referenced paths across the repo; identifies dead links, moved file references, missing assets, and orphaned docs.

## Authority
None. Advisory/draft output only.

## Inputs
- Repo file tree
- Markdown files and link targets
- `02_PLAYBOOKS/_registry/PLAYBOOK_INDEX.md`

## Outputs
- One integrity report in `09_INBOX/_AGENT_OUTPUT/` listing failures and suggested fixes

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- Flag ambiguity as policy questions

## Definition of Done
Report produced with dead links, stale references, missing assets, and orphaned docs clearly listed, plus repair recommendations.
