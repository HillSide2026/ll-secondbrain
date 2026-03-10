---
id: mkt_skill_banned_claims_guard
title: Banned Claims Guard Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, policy, compliance]
---

# Skill: Banned Claims Guard

## Purpose
Detect and block banned claims in design copy before downstream QA and release.

## Inputs
- Design text layers
- Banned claims ruleset
- Campaign context

## Process
1. Extract text from design elements.
2. Compare text against banned-claims patterns.
3. Flag direct and near-match violations.
4. Produce a compliance pass/fail result.

## Outputs
- Banned-claims screening report
- Violation list with text location

## Constraints
- No auto-approval when violations are found.
- Violations must be remediated or escalated.
- Rule changes are out of scope for this skill.

## Invocation
Used as a mandatory policy check in design preflight.

