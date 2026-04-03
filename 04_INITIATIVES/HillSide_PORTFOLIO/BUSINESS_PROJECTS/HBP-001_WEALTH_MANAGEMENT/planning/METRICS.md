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
| Gap to SG-01 | CAD 2,000,000 − CAD 1,600,000 | CAD 400,000 remaining; requires ~4.8% CAGR on existing base over 4.75 years — path is primarily investment returns, not savings from income | `PROJECT_PLAN.md` |
| Gap to SG-02 | CAD 4,000,000 − CAD 1,600,000 | CAD 2,400,000 remaining; requires ~6.4% CAGR over 14.75 years — at $2M in 2030, a further ~7.2% CAGR for 10 years reaches $4M | `PROJECT_PLAN.md` |
| Governance readiness | Capital-allocation, liquidity, refill, and review rules are explicit enough to govern execution | governance rules documented clearly enough for ML1 review | `LIQUIDITY_AND_CAPITAL_GUARDRAILS.md`, `NET_SAVINGS_AND_REFILL_MODEL.md`, `COMMUNICATION_PLAN.md`, `WEALTH_PLAN.md` |
| Housing budget anchor | Shared housing-budget rules exist for Toronto and Japan planning | one housing-budget policy and output standard documented clearly enough for ML1 review | `HOUSING_BUDGET_POLICY.md`, `WEALTH_PLAN.md` |
| Dependency alignment | Critical dependencies needed for execution are identified and narrowed enough to manage | no unresolved dependency that makes the path unusable for decision-making | `DEPENDENCIES.md`, `RISK_REGISTER.md` |
| ML1 gate readiness | The planning packet is complete enough for a `Planning -> Executing` decision | all required planning artifacts drafted and coherent | planning folder and `../APPROVAL_RECORD.md` |

## Wealth Accumulation Model

Net worth grows from two sources. Both must be tracked and modelled
explicitly — neither alone is sufficient.

| Source | Current State | What Needs to Change |
|--------|-------------|---------------------|
| Investment returns on base | $1.6M base requires ~4.8% CAGR to reach SG-01; ~6.4% CAGR for SG-02 | Return assumption must be fixed and reviewed annually against actuals |
| Net savings from income | ML revenue ~$80K/year ≈ living costs → net savings ~$0 | To generate meaningful net savings, ML revenue must reach ~$130–150K+ (requires LL or other venture revenue growth from 2027 onward) |

**Current position:** wealth accumulation is entirely dependent on investment
returns. Professional income covers living costs but does not contribute
materially to the base. This is a viable path to SG-01 but leaves no margin
for return shortfalls and does not meaningfully accelerate SG-02.

**What changes this:** If net annual savings reach CAD 50,000–75,000 from
2027 onward (requiring ML gross revenue of ~$130–160K), the combined effect
of savings plus compounding meaningfully reduces dependence on hitting return
targets and accelerates SG-02.

**Where revenue growth is planned:** `HBP-008` (Levine Law 2027) and
`HBP-009` (2027 Business Ideas) are the projects responsible for closing
the gap between current ML revenue and the level required to generate net
savings.

---

## Measurement Rule

Planning is not complete when the goal is merely restated more elegantly.
Planning is complete only when the baseline, target gap, governance rules, and
dependency picture are specific enough for ML1 to authorize controlled
execution.
