---
id: 04_initiatives__system_portfolio__00_draft_roadmaps__sys_012_sma_deployment_sequence_md
title: SYS-012 — SMA Deployment Execution Sequence (Draft)
owner: ML1
status: draft
created_date: 2026-02-26
last_updated: 2026-02-26
tags: [system-portfolio, draft, deployment]
---

# SYS-012 — SMA Deployment Execution Sequence (Draft)

## Purpose
Provide a single, consolidated execution sequence for deploying SMA‑001..SMA‑005 after SYS‑001 is resolved.

This is a **planning artifact** only. It does not authorize execution.

## Preconditions
- SYS‑001 decision recorded (Claude Code agents)
- SMA‑001..SMA‑005 agent definitions present in `00_SYSTEM/AGENTS/`
- Write-back policy reviewed (`01_DOCTRINE/02_POLICIES/WRITE_BACK_POLICY.md`)
- Stage 2/3 dependencies confirmed

## Proposed Sequence (Consolidated)

1. **Preflight Inventory (SMA‑002)**
   - Validate backlog dependency chain
   - Confirm agent specs exist and are current

2. **Governance Review (SMA‑001)**
   - Verify agent scope boundaries and prohibitions
   - Confirm no authority drift or external write permissions

3. **QA Validation (SMA‑005)**
   - Run format and frontmatter checks on agent specs
   - Validate report templates used by the sweep

4. **Baseline Sweep Execution (SMA‑002 orchestration)**
   - Run `00_SYSTEM/scripts/run_system_management_sweep.py`
   - Capture outputs under `06_RUNS/`

5. **ML1 Review Gate**
   - Review system management reports
   - Approve deployment completion or request revisions

## Outputs
- System management sweep reports (SMA‑001..SMA‑005)
- Run log in `06_RUNS/`
- Deployment completion note (ML1 approval)

## Acceptance Criteria
- All SMA reports generated without errors
- Governance/QA checks pass with no blocking issues
- ML1 explicitly approves deployment completion

## Notes
- This sequence assumes Claude Code runtime per SYS‑001 decision.
- No external writes are authorized.
