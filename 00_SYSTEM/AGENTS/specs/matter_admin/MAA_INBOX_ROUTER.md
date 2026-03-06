---
id: maa_inbox_router
title: Inbox Router Agent Charter
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: [matter-admin]
---

# Inbox Router Agent Charter

## Agent
`MAA_INBOX_ROUTER`

## Purpose
Assign Gmail threads to matters using deterministic routing rules and isolate unmapped traffic.

## Action Bindings
- `agent_inbox_router` (daily run)
- `agent_inbox_router_scoped` (single-matter run)

## Inputs
- Normalized Gmail `ThreadRef` records
- Matter index (Clio matter numbers)
- Gmail label rules (`00_SYSTEM/CONFIG/gmail_label_rules.yml`)

## Outputs
- `06_DASHBOARDS/INBOX_UNMAPPED.md`
- `05_MATTERS/<tier>/<matter_id>/MATTER_STATUS.md`

## Routing Order
1. Gmail label contains matter number (canonical).
2. Subject/snippet matter-number fallback (review-required).
3. Otherwise unmapped.

## Constraints
- No message send, archive, or mutation.
- Unknown or low-confidence routes must remain unmapped.
- Every assignment must retain Gmail source pointer.

## Definition of Done
- Deterministic per-thread routing result.
- Explicit unmapped list with reason code and source pointer.

