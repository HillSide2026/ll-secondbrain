---
id: PRO-015
title: Marketing Stage Classification and Handoff
owner: ML1
status: draft
version: 0.1
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [protocol, marketing, lifecycle, handoff]
---

# PRO-015 — Marketing Stage Classification and Handoff

Enforces Policies: POL-032, POL-033

Trigger condition:
- A marketing run, campaign, asset, or report is created, updated, or promoted.
- A stage transition is requested.

Required stage taxonomy:
- `discovery`
- `interest`
- `consideration`
- `inquiry` (alias: `intake`)
- `conversion` (alias: `onboarding`)

Protocol steps:
1. Classify each governed marketing artifact/run with exactly one lifecycle stage from the required taxonomy.
2. Normalize aliases (`intake -> inquiry`, `onboarding -> conversion`) in canonical structured fields.
3. If stage is `conversion`, validate objective evidence exists (`engagement agreement signed`, `retainer received`, or `invoice paid`) and attach evidence reference(s).
4. If conversion evidence is valid, mark marketing lifecycle as complete and initiate handoff classification to non-marketing processes.
5. Route post-conversion artifacts to non-marketing classes (`client_service`, `delivery`, `retention`, `expansion`) under their governing doctrine.

Block condition:
- Stage value not in required taxonomy.
- Conversion/Onboarding asserted without required evidence.
- Post-conversion artifact retained in marketing stage classification.

Escalation path:
- Escalate ambiguous stage assignment, missing evidence, or handoff conflicts to ML1.

Logging requirement:
- Record stage classification, normalized alias handling, evidence references, transition decision, and handoff target in run artifacts.

Version: 0.1
Status: Draft
