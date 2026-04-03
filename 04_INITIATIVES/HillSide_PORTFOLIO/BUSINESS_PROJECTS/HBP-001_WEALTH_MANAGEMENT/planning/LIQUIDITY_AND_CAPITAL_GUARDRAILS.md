---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_001_wealth_management__planning__liquidity_and_capital_guardrails_md
title: Wealth Management - Liquidity and Capital Guardrails
owner: ML1
status: active
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [wealth-management, planning, liquidity, guardrails]
---

# Liquidity And Capital Guardrails

Project ID: `HBP-001`
Stage: `Planning`

## Planning Use

Use this file to separate wealth from spendable capital and to prevent large
commitments from weakening resilience.

## Capital Buckets

| Bucket | Purpose | Rule |
| --- | --- | --- |
| Core personal liquidity reserve | Protect personal stability and housing continuity | Hold enough liquid capital for at least 24 months of personal living costs, taxes, debt service, insurance, and unavoidable fixed commitments |
| Operating and tax reserve | Protect business support and irregular obligations | Hold enough liquid capital for known business support needs, unresolved taxes, and expected irregular obligations identified through `HBP-002_CASH_FLOW` |
| Strategic optionality reserve | Preserve room for real opportunities and surprises | Keep an explicit reserve that is not pre-committed to housing while the wealth plan is still in planning |
| Transaction buffer | Protect against execution friction | Include closing costs, legal fees, furnishing, moving, repairs, and first-year variance before a housing budget is considered valid |
| Deployable capital | Defines what can actually be committed | unrestricted liquid capital less all reserves and the transaction buffer |

## Guardrail Rules

- No housing decision is approvable if post-close unrestricted liquidity falls
  below the core personal reserve, operating and tax reserve, and transaction
  buffer.
- No major decision may count illiquid business equity or unrealized sale
  proceeds as housing funding.
- No major decision may rely on future revenue growth unless it is already
  visible in `HBP-002_CASH_FLOW` as a credible net-savings line.
- No second major housing commitment may reserve capital that is already needed
  by another unresolved housing path.
- Any exception requires explicit written ML1 approval and should be treated as
  an exception rather than the new normal.

## Current Planning Standard

Because current net savings are near zero, major housing commitments should be
evaluated as a reduction of the existing liquid base, not as a budget that will
quickly refill itself.

## Required Outputs For Any Major Housing Budget

- maximum acquisition price
- maximum upfront cash deployment
- maximum monthly carrying cost
- minimum post-close unrestricted liquidity
- financing assumption
- transaction buffer
- explicit no-go triggers

## No-Go Triggers

- reserve breach
- forced sale of strategic or illiquid assets
- dependence on optimistic income growth not yet visible in `HBP-002_CASH_FLOW`
- unresolved tax, legal, or close-cost exposure large enough to make the budget misleading
