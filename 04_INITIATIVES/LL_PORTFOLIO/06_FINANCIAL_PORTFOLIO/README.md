---
id: 04_initiatives__ll_portfolio__06_financial_portfolio__readme_md
title: 06_FINANCIAL_PORTFOLIO — Models & Constraints
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-03-23
tags: []
---

# 06_FINANCIAL_PORTFOLIO — Models & Constraints

## Purpose

Financial visibility and modeling WITHOUT decision authority.

## Scope

**Characteristics:** Analytical, assumption-bound, advisory only

### In Scope

- Revenue and pricing frameworks
- Unit economics
- Cost models
- Scenario and sensitivity analysis
- Financial constraints (e.g., margin floors)
- Advisory financial-modeling outputs produced by `LLM-003_CFO_AGENT`

### Out of Scope

- Setting prices
- Approving discounts
- Declaring profitability
- Auto-feeding outputs into operations/sales
- Treating models as decisions

## Critical Boundary

- **Accounting = facts** (01_ACCOUNTING)
- **Financial Portfolio = models** (this folder)
- **They must never be mixed.**

## ML1 Authority Statement

ML1 is the sole authority for pricing decisions, discount approvals, and profitability declarations. The System may model scenarios against ML2 canon, but all outputs are advisory only.

## Explicit Prohibitions

The System must NOT:

- Set prices
- Approve discounts
- Declare profitability
- Auto-feed outputs into operations or sales systems
- Treat models as decisions
- Mix accounting facts with financial models
- Execute based on model outputs

## Approval State

**ACTIVE** — Budget modeling artifacts exist and the governed packet formalization is underway.

## Active Financial Modeling Homes

- `LLP-002_BUDGETING/` — canonical Levine Law budgeting and scenario packet
- `CFO/` — advisory output home for `LLM-003_CFO_AGENT`

## Last ML1 Review Date

*Not yet reviewed*
