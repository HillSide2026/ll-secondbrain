---
id: maa_deadline_extractor
title: Deadline Extractor Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Deadline Extractor Agent Charter

## Agent
`MAA_DEADLINE_EXTRACTOR`

## Purpose
Extract explicit commitments and date-bearing obligations from routed communications and document context.

## Action Bindings
- Planned for Slice 3

## Inputs
- Routed thread sets by matter
- Optional recent SharePoint document metadata/snippets
- Deadline taxonomy (`00_SYSTEM/CONFIG/deadline_taxonomy.yml`)

## Outputs
- `05_MATTERS/<tier>/<matter_id>/DEADLINES.md`
- `05_MATTERS/DASHBOARDS/DEADLINE_RADAR.md`

## Classification
- Hard deadline
- Soft deadline
- Internal target

## Constraints
- Each extracted deadline requires citation (message id/thread id and snippet).
- No speculative deadlines.
- If confidence is low, emit review-required item instead of a deadline assertion.

## Definition of Done
- Deadlines normalized by date, class, and source pointer.
- Firm radar reflects due-soon and overdue buckets deterministically.

