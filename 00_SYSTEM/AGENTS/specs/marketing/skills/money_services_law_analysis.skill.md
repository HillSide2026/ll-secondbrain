---
id: mkt_skill_money_services_law_analysis
title: Money Services Law Analysis Skill
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [marketing, skill, money-services, analysis]
---

# Money Services Law Analysis Skill

## Purpose
Analyze whether a Funnel 3 fact pattern likely raises Canadian money-services,
FINTRAC, AML-program, reporting, or registration issues.

## Capabilities
- Assess whether a fact pattern likely triggers MSB or foreign-MSB analysis
- Map business functions to likely FINTRAC / PCMLTFA relevance
- Distinguish pure MSB issues from securities or RPAA overlap
- Rate client-model risk and touchability in commercially useful terms

## Inputs
- Fact pattern or entity-model summary
- Business functions and asset/payment model
- Jurisdictional hooks
- Available source documents

## Outputs
- Money-services issue map
- Authority applicability assessment
- Risk rating and touchability assessment
- ML1 next-decision recommendation

## Boundary Rules
- Do not collapse preliminary issue spotting into definitive legal conclusions.
- Do not ignore missing facts; mark confidence accordingly.
- Do not optimize toward permissive answers.
- Escalate when the model appears too risky to touch without major change.
