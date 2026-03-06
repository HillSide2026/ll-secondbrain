---
id: maa_matter_index
title: Matter Index Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Matter Index Agent Charter

## Agent
`MAA_MATTER_INDEX`

## Purpose
Build the authoritative active-matter list for Matter Command and Control runs.

## Action Bindings
- `agent_matter_index` (daily run)

## Inputs
- Normalized Clio `MatterRef` records
- Optional local matter metadata for folder-path reconciliation

## Outputs
- `06_DASHBOARDS/MATTER_INDEX.md`

## Rules
- Primary key is Clio matter number.
- Clio is authoritative for status, responsible attorney, and registry identity.
- Every row must carry a Clio source pointer.

## Constraints
- Read-only on Clio and repo source artifacts.
- No creation of shadow registry outside ML2 derived artifacts.

## Definition of Done
- One deterministic index row per active Clio matter number.
- Output includes matter status, owner, and source pointer.

