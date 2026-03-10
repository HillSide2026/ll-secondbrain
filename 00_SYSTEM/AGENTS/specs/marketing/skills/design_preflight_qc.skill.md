---
id: mkt_skill_design_preflight_qc
title: Design Preflight QC Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, design, qa]
---

# Skill: Design Preflight QC

## Purpose
Run final deterministic preflight checks on design artifacts before QA handoff.

## Inputs
- Finalized draft design(s)
- Compliance check outputs
- Required field checklist

## Process
1. Validate required fields are complete.
2. Validate brand, disclaimer, and banned-claims checks are passed.
3. Verify link integrity and export readiness.
4. Produce preflight pass/fail with required remediation list.

## Outputs
- Design preflight report
- Pass/fail recommendation
- Remediation checklist

## Constraints
- Failed preflight artifacts cannot be promoted.
- Missing evidence for checks is treated as failure.
- Manual overrides require ML1 approval.

## Invocation
Used immediately before QA and governance handoff.

