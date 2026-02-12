---
id: 02_playbooks__stage3__cognitive_consistency_runbook_md
title: Stage 3.7 Cognitive Consistency Runbook
owner: ML1
status: draft
created_date: 2026-02-11
last_updated: 2026-02-11
tags: [stage3, runbook, consistency]
---

# Stage 3.7 — Cognitive Consistency Runbook

## Purpose
Define the read-only workflow for surfacing contradictions and drift across an artifact set.

## Preconditions
- Stage 3.7 authorized.
- Scope (packet) defined by ML1.
- Use flags-only report template.

## Approved Output Locations
- Reports: `06_RUNS/STAGE3/`

## Forbidden Actions
- No edits or write-backs to source artifacts.
- No recommendations or prescriptions.
- No policy creation or interpretation.

## Workflow
1. Identify the packet (list of files) to scan.
2. Apply detection checklist from the agent spec.
3. Generate a flags-only report using the template.
4. Save report in `06_RUNS/STAGE3/`.
5. End output with `[USE / IGNORE / DELETE]`.

## Logging
- Each run log must include packet scope and report path.
- If zero flags are found, record “No flags detected.”

## References
- Agent Spec: `02_PLAYBOOKS/STAGE3/COGNITIVE_CONSISTENCY_CHECKER.md`
- Report Template: `02_PLAYBOOKS/STAGE3/COGNITIVE_CONSISTENCY_REPORT_TEMPLATE.md`
