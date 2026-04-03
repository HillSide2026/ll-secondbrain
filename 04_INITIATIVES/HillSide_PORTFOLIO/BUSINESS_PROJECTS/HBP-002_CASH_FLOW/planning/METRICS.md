---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_002_cash_flow__planning__metrics_md
title: Cash Flow - Metrics
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-04-03
tags: [cash-flow, planning, metrics]
---

# Metrics

Project ID: `HBP-002`
Stage: `Planning`

## Planning Metric Rule

This planning artifact adopts the core metric definitions recorded in
`../METRICS.md` and translates them into execution-readiness tests for the
monthly management-pack build.

## Locked Current Inputs

- Levine Law -> Matthew compensation target for 2026: `CAD 72,000` salary + `CAD 8,000` bonus = `CAD 80,000`
- This target should be modeled in the pack as compensation inflow within the Levine Law source line, not as a separate entity-revenue metric.
- Slightly more than `CAD 27,000` has already been received from the sale of YellowBricks into `17513721 Canada Inc`.
- Andersen fees are received by `17513721 Canada Inc`, while Andersen operational matters are tracked inside Levine Law and credited to Levine Law in the 2026 operating picture.

## Planning Exit Metrics

| Metric | Definition | Target | Evidence |
| --- | --- | --- | --- |
| Boundary clarity | The reporting boundary is explicit across Matthew and the five in-scope entities | one frozen in-scope list with no material ambiguity | `SCOPE_STATEMENT.md`, `ASSUMPTIONS_CONSTRAINTS.md` |
| Formula clarity | Matthew-level gross-inflow, gross-outflow, and net-cash-flow formulas are explicit enough for CPA-style review | one approved formula set and treatment rule set | `../METRICS.md`, `ASSUMPTIONS_CONSTRAINTS.md` |
| Source-record completeness | Each in-scope entity and cash-movement family has a named primary source set | all core metric families mapped to source records | `DEPENDENCIES.md`, `../METRICS.md` |
| Close-process readiness | The monthly close and review loop can deliver within 10 business days of month-end | one workable close calendar and review owner defined | `PROJECT_PLAN.md`, `COMMUNICATION_PLAN.md` |
| Pack readiness | The minimum viable management-pack structure is explicit enough to build for the Matthew-level view | one execution-ready pack design and scope boundary | `PROJECT_PLAN.md`, planning folder |
| ML1 gate readiness | The planning packet is complete enough for a `Planning -> Executing` decision | all required planning artifacts drafted and coherent | planning folder and `../APPROVAL_RECORD.md` |

## 2027 Onwards — Business Income Vs Investment Income

The management pack should distinguish between two different Matthew-level
lanes:

- business income to Matthew: cash actually paid from `Levine Professional
  Corporation` or `17513721 Canada Inc` to Matthew, including compensation,
  bonus, dividends, and approved distributions
- investment income / return on capital: high-interest savings interest,
  portfolio dividends, realized gains, and broader portfolio-performance effects
  on the personal capital base

The current explicit 2026 business-income model (`CAD 72,000` salary +
`CAD 8,000` bonus = `CAD 80,000`) approximately equals living costs. At this
level, business income covers expenses but generates no material net savings.
Wealth-path progress therefore still depends mostly on the investment-return
lane.

| Threshold | Implication |
|-----------|-------------|
| Business income to Matthew ~CAD 80,000 | Net savings from business income ≈ CAD 0; refill is weak and wealth growth depends mostly on the investment-return lane |
| Business income to Matthew high enough to create ~CAD 50,000–70,000 of annual net savings | materially accelerates wealth accumulation and reduces dependence on hitting investment-return targets |
| Business income to Matthew strong and durable | provides real reserve-refill capacity and margin against return shortfalls |

**Planning requirement from 2027:** The monthly management pack must include
separate lines for business income to Matthew, investment income / return on
capital, and net savings from business income. It should not rely on one
undifferentiated "income" line or only on gross inflow. This is the metric
structure that connects HBP-002 (Cash Flow) to HBP-001 (Wealth Management) and
to the growth targets in HBP-008 (Levine Law 2027) and HBP-009 (2027 Business
Ideas).

Whether business income to Matthew becomes strong enough to create material net
savings will depend on Levine Law growth, `17513721 Canada Inc` distributions,
or other venture income from 2027 onward. Until it does, the net-savings line
should remain near zero in the reporting and should not be assumed away.

---

## Measurement Rule

Planning is not complete when the formulas merely sound professional. Planning
is complete only when the reporting boundary, source map, close process, and
pack design are specific enough to run in execution.
