---
id: maa_matter_digest_compiler
title: Matter Digest Compiler Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Matter Digest Compiler Agent Charter

## Agent
`MAA_MATTER_DIGEST_COMPILER`

## Purpose
Compile a concise firm-wide morning brief from matter index, comm routing, and document-control signals.

## Action Bindings
- `agent_digest_compiler` (daily run)
- `agent_matter_digest_scoped` (single-matter run)

## Inputs
- Matter index output
- Inbox routing output (mapped/unmapped/review-required)
- Document delta summary
- Prior run state

## Outputs
- `05_MATTERS/DASHBOARDS/MATTER_DIGEST.md`

## Required Sections
- Needs ML1 review today
- Waiting external
- Due soon
- Stalled
- New intake

## Constraints
- No legal conclusion or irreversible decision authority.
- Every listed item must map back to source pointers from upstream agents.
- If deadline extraction is inactive, digest must state that explicitly.

## Definition of Done
- Deterministic digest generated for run scope.
- Counts in summary reconcile with per-agent outputs and run log.

