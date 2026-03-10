---
id: mkt_skill_design_brief_translation
title: Design Brief Translation Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, design, brief]
---

# Skill: Design Brief Translation

## Purpose
Convert approved campaign strategy and content blocks into a structured design brief.

## Inputs
- Campaign brief
- Approved copy blocks
- Asset type request
- Channel and audience context

## Process
1. Parse asset objective, audience, and channel constraints.
2. Extract required design fields and fixed content blocks.
3. Map policy constraints (voice, disclaimer, banned-claims rules) to explicit checks.
4. Produce a deterministic design brief for template execution.

## Outputs
- Structured design brief
- Required fields matrix
- Constraint checklist

## Constraints
- Inputs must be approved upstream artifacts.
- No strategy changes may be introduced.
- Ambiguous requirements must be escalated.

## Invocation
Used by Design Production Agent at the start of asset generation.

