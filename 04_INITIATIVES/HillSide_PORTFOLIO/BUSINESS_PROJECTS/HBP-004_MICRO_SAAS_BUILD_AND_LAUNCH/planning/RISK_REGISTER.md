---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_004_micro_saas_build_and_launch__planning__risk_register_md
title: Micro SaaS Build and Launch - Risk Register
owner: ML1
status: active
created_date: 2026-03-12
last_updated: 2026-03-14
tags: [micro-saas, planning, risks]
---

# Risk Register

Project ID: HBP-004
Project Path: 04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-004_MICRO_SAAS_BUILD_AND_LAUNCH
Stage: Planning

## Decision Use
Use this file to prioritize mitigation work and escalation before risks damage build or launch outcomes.

## Executing Risk Register

| Risk | Category | Likelihood | Impact | Goal at Risk | Mitigation |
| --- | --- | --- | --- | --- | --- |
| Target users do not adopt the lookup workflow as expected | Scope | M | H | Launch usable MVP for exporters | Validate with pilot interviews and test scenarios before build freeze |
| Jurisdiction scope expands beyond initial six-country boundary | Scope | H | H | Fast launch and controllable MVP | Enforce scope lock and change-control approval |
| Preferential eligibility logic is oversimplified and produces misleading notes | Scope | M | H | Reliable tariff guidance output | Define explicit rule boundaries and include eligibility caveats |
| Tariff/agreement data acquisition is delayed for one or more jurisdictions | Schedule | M | H | On-time MVP release | Sequence build by jurisdiction priority and set fallback launch criteria |
| Data refresh process is not operational before launch | Schedule | M | M | Output freshness and user trust | Define data refresh owner, cadence, and source timestamp checks |
| Integration defects across frontend/backend/data delay release | Schedule | M | M | Launch on target date | Timebox integration milestones and run weekly defect burn-down |
| Total project spend exceeds approved envelope (`CAD 500`) | Budget | M | H | Budget discipline and execution continuity | Track weekly spend variance, require pre-approval for non-essential costs, freeze discretionary spend at 80% envelope until ML1 review |
| Data-source or licensing costs exceed planned budget | Budget | M | M | Budget discipline | Pre-approve source options and enforce spend envelope reviews |
| Post-launch infrastructure/API costs grow faster than expected | Budget | M | M | Sustainable operations after go-live | Set infrastructure ceiling and monitor weekly cost variance |

## Escalation Rule
Any High-impact risk without an active mitigation owner must be escalated to ML1 in the weekly review.
