---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_004_micro_saas_build_and_launch__planning__scope_definition_md
title: Develop and Launch Micro SaaS (TariffLookup.ca) - Scope Statement
owner: ML1
status: active
created_date: 2026-03-12
last_updated: 2026-03-14
tags: [micro-saas, planning, scope]
---

# Scope Statement

Project ID: HBP-004
Project Path: 04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-004_MICRO_SAAS_BUILD_AND_LAUNCH
Stage: Planning

## Decision Use
Use this file for supplemental scope rationale; canonical project scope is maintained in `WORKPLAN.md`.

## Selected Product Concept
TariffLookup.ca for Canadian exporters evaluating new destination markets.

## In Scope
- Target users: Canadian exporters and trade consultants supporting export-market evaluation.
- User inputs: one HS code and one destination country per query.
- User outputs: MFN tariff, preferential tariff (if applicable), agreement basis, and eligibility notes.
- Initial jurisdictions: United States, European Union, United Kingdom, Japan, South Korea, Australia.
- Minimum dataset elements per jurisdiction:
  - tariff schedule by HS code
  - preferential tariff schedules under applicable trade agreements
  - agreement eligibility rules needed for output notes
- Basic architecture boundary:
  - frontend for input and results display
  - backend for tariff query and agreement logic
  - database for tariff schedules, jurisdiction metadata, and HS mappings

## Out of Scope
- Multi-country comparison output in one request for the initial MVP.
- Non-tariff barrier summaries.
- Landed cost estimation and duty-savings calculator.
- Export opportunity recommendation engine.
- Enterprise custom data pipelines before initial launch validation.

## Illustrative Query (MVP)
- Input:
  - HS Code: `8208.30`
  - Destination: `Japan`
- Output format:
  - MFN tariff rate
  - Preferential tariff rate (if applicable)
  - Agreement basis (if applicable)
  - Eligibility notes

## Execution Readiness Deliverables
- `WORKPLAN.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `COMMUNICATION_PLAN.md`
- `OKR.md`
- `VALIDATION_REVIEW.md`
- `ML1_METRIC_APPROVAL.md`

## Gate Criteria for Executing Authorization
- Target users, core workflow, and MVP boundaries are explicit and frozen.
- Jurisdiction list and data/rule requirements are explicit and feasible.
- Risks to data correctness, schedule, and budget have active mitigations.
- KPI package is reproducible and thresholded for ML1 decision.
