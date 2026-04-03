---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_001_wealth_management__planning__metrics_md
title: Wealth Management - Metrics
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-04-03
tags: [wealth-management, planning, metrics]
---

# Metrics

Project ID: `HBP-001`
Stage: `Planning`

## Planning Exit Metrics

| Metric | Definition | Target | Evidence |
| --- | --- | --- | --- |
| Baseline completeness | Share of in-scope assets and liabilities classified under one approved methodology | all material in-scope items classified | `SCOPE_STATEMENT.md`, `OPENING_BALANCE_SHEET.md`, `VALUATION_AND_CLASSIFICATION_POLICY.md` |
| Opening baseline | Consolidated net worth as at `2026-03-23` | CAD 1,600,000 (first-pass; subject to valuation confirmation) | `OPENING_BALANCE_SHEET.md`, ML1 |
| Gap to SG-01 | CAD 2,000,000 − CAD 1,600,000 | CAD 400,000 remaining; requires ~4.8% CAGR on existing base over 4.75 years — path is primarily investment income and compounding, not retained net savings from business income | `PROJECT_PLAN.md` |
| Gap to SG-02 | CAD 4,000,000 − CAD 1,600,000 | CAD 2,400,000 remaining; requires ~6.4% CAGR over 14.75 years — at $2M in 2030, a further ~7.2% CAGR for 10 years reaches $4M | `PROJECT_PLAN.md` |
| Governance readiness | Capital-allocation, liquidity, refill, and review rules are explicit enough to govern execution | governance rules documented clearly enough for ML1 review | `LIQUIDITY_AND_CAPITAL_GUARDRAILS.md`, `NET_SAVINGS_AND_REFILL_MODEL.md`, `COMMUNICATION_PLAN.md`, `WEALTH_PLAN.md` |
| Housing budget anchor | Shared housing-budget rules exist for Toronto and Japan planning | one housing-budget policy and output standard documented clearly enough for ML1 review | `HOUSING_BUDGET_POLICY.md`, `WEALTH_PLAN.md` |
| Dependency alignment | Critical dependencies needed for execution are identified and narrowed enough to manage | no unresolved dependency that makes the path unusable for decision-making | `DEPENDENCIES.md`, `RISK_REGISTER.md` |
| ML1 gate readiness | The planning packet is complete enough for a `Planning -> Executing` decision | all required planning artifacts drafted and coherent | planning folder and `../APPROVAL_RECORD.md` |

## Business Income Vs Investment Income

The wealth model has two distinct lanes. They must be tracked separately
because they answer different planning questions.

| Lane | Current State | Planning Use |
|--------|-------------|---------------------|
| Investment income and return on capital | The existing base still needs about ~4.8% CAGR to reach SG-01 and ~6.4% CAGR to reach SG-02 | Shows how the current balance sheet compounds over time |
| Business income to Matthew | The current explicit Levine Law -> Matthew compensation target is `CAD 80,000`; no recurring `17513721 Canada Inc` -> Matthew distribution is yet assumed | Shows whether the liquid base can be refilled through owner cash flow rather than market performance |

**Current position:** business income to Matthew approximately covers living
costs, so net savings from business income are near zero. That means the
current path still depends mostly on investment income and compounding on the
existing base. This is viable for SG-01 if returns cooperate, but it leaves
less margin for return shortfalls and does not materially accelerate SG-02.

**What changes this:** If business income to Matthew rises enough to generate
net annual savings of `CAD 50,000`-`75,000` from 2027 onward, the combined
effect of savings plus compounding meaningfully reduces dependence on hitting
investment-return targets and accelerates SG-02.

**Where the business-income improvement is expected to come from:** `HBP-008`
(Levine Law 2027) and `HBP-009` (2027 Business Ideas) remain the main growth
projects. Any recurring `17513721 Canada Inc` -> Matthew distributions should
also be documented in `HBP-002_CASH_FLOW` rather than assumed informally.

**Scenario note:** `SG_01_2030_SCENARIO_MODEL.md` now shows that the strict
business-income savings requirement for SG-01 is modest in the `4%` case and
zero in the `6%` and `8%` cases. Larger savings targets still matter if ML1
wants more cushion, less market dependence, or more housing flexibility.

---

## Measurement Rule

Planning is not complete when the goal is merely restated more elegantly.
Planning is complete only when the baseline, target gap, governance rules, and
dependency picture are specific enough for ML1 to authorize controlled
execution.
