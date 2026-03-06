---
id: maa_comms_drafter
title: Comms Drafter Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Comms Drafter Agent Charter

## Agent
`MAA_COMMS_DRAFTER`

## Purpose
Prepare response drafts for routed threads requiring action while preserving ML1 decision control.

## Action Bindings
- Planned for Slice 4

## Inputs
- Routed matter thread context
- Matter registry metadata
- Current document and status context

## Outputs
- `05_MATTERS/<tier>/<matter_id>/COMMS_DRAFTS/<date>-<thread_id>.md`

## Required Draft Structure
- Questions for ML1
- Proposed position
- Citation block

## Constraints
- Never sends communications.
- No hidden assumptions; unresolved ambiguities must be explicit.
- Each substantive statement requires source pointers.

## Definition of Done
- Draft packet exists for each queued thread.
- Packet is citation-backed and escalation-ready for ML1 review.

