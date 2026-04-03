---
id: mkt_skill_securities_law_analysis
title: Securities Law Analysis Skill
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [marketing, skill, securities, analysis]
---

# Securities Law Analysis Skill

## Purpose
Analyze whether a Funnel 3 fact pattern likely raises Canadian securities-law
registration, marketplace, distribution, custody, or resale issues.

## Capabilities
- Assess whether a fact pattern is primarily `FINTRAC`, primarily
  `securities`, or an `overlap` case
- Map business functions to likely instrument relevance
- Rate client-model risk and touchability in commercially useful terms
- Separate "possible to structure" from "prudent to take on"

## Inputs
- Fact pattern or entity-model summary
- Business functions and asset model
- Jurisdictional hooks
- Available source documents

## Outputs
- Securities-adjacent issue map
- Instrument applicability assessment
- Risk rating and touchability assessment
- ML1 next-decision recommendation

## Boundary Rules
- Do not collapse preliminary issue spotting into definitive legal conclusions.
- Do not ignore missing facts; mark confidence accordingly.
- Do not optimize toward permissive answers.
- Escalate when the model appears too risky to touch without major change.
