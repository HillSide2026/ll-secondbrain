---
id: 04_initiatives__ll_portfolio__06_financial_portfolio__readme_md
title: 06_FINANCIAL_PORTFOLIO — Finance
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-05-13
tags: []
---

# 06_FINANCIAL_PORTFOLIO — Finance

## Current Direction

ML1 has determined that **Accounting** and **Finance** are separate domains.

Accounting includes:

- bookkeeping;
- management accounting;
- budgeting;
- financial risk;
- cash / collections.

Finance includes:

- external financing, including shareholder funding;
- debt facilities, including credit cards and credit lines;
- tax-planning interfaces, including pension and health insurance;
- major asset/liability decisions, including leases;
- strategic banking relationships;
- investment / reserve policy;
- corporate finance decisions, including acquiring property through LawCo;
- M&A or acquisition financing, including buying a book of business;
- partner/shareholder distributions, including recruiting a lawyer with a book of business.

## Purpose

Govern Levine Law finance matters that are about capital, liabilities, strategic banking, tax-planning interfaces, major asset/liability decisions, investment/reserve policy, corporate finance, acquisition financing, and partner/shareholder economics.

## Scope

**Characteristics:** Strategic finance, advisory unless ML1 approves a decision.

### In Scope

- External financing, including shareholder funding
- Debt facilities, including credit cards and credit lines
- Tax-planning interfaces, including pension and health insurance
- Major asset/liability decisions, including leases
- Strategic banking relationships
- Investment / reserve policy
- Corporate finance decisions, including property acquisition through LawCo
- M&A or acquisition financing, including buying a book of business
- Partner/shareholder distributions, including recruiting a lawyer with a book of business
- Advisory finance modeling outputs produced by `LLM-003_CFO_AGENT`

### Out of Scope

- Bookkeeping records
- Management accounting revenue classification
- Budgeting control unless expressly cross-referenced
- Operating cash/collections workflow
- Matter-level WIP conversion analysis
- Auto-feeding outputs into operations/sales
- Treating models as decisions

## Critical Boundary

- **Accounting = operating money system**
- **Finance = capital, liability, strategic banking, tax interface, and major transaction system**
- **They may connect, but they must not be collapsed into each other**

## ML1 Authority Statement

ML1 is the sole authority for finance decisions, including external financing, debt facilities, strategic banking, major asset/liability commitments, investment/reserve policy, corporate finance, acquisition financing, and partner/shareholder distributions. The System may model scenarios against ML2 canon, but all outputs are advisory only.

## Explicit Prohibitions

The System must NOT:

- Set prices
- Approve discounts
- Declare profitability
- Auto-feed outputs into operations or sales systems
- Treat models as decisions
- Mix accounting records with finance decisions without labelling the layer
- Execute based on model outputs

## Approval State

**DRAFT / ACTIVE BOUNDARY** — Finance scope has been clarified by ML1. Existing budgeting artifacts in this folder are legacy placement and should be migrated or cross-referenced only with ML1 approval.

## Core Finance Artifacts

- `LL_FINANCE_PRINCIPLES.md` — finance concepts relevant to Levine Law
- `LL_FINANCE_INVARIANTS.md` — durable finance truths and constraints
- `LL_FINANCE_POLICIES.md` — ML1-approved or draft finance decision rules

## Existing Homes / Legacy Notes

- `LLP-002_BUDGETING/` — legacy placement; budgeting belongs to Accounting under the clarified architecture
- `CFO/` — advisory output home for `LLM-003_CFO_AGENT`

## Last ML1 Review Date

*Not yet reviewed*
