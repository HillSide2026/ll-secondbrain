---
id: 02_playbooks__financial_services__payments__initial_screening__are_there_securities_issues_md
title: Are There Securities Issues?
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [financial-services, payments, screening, token, stablecoin, securities]
---

# Are There Securities Issues?

## Purpose

Prepared by `Muggah Securities`
(`MKT_MUGGAH_SECURITIES_AGENT`).

Internal first-pass screen for whether an intake likely raises Canadian
issuer-side, dealer-side, token-distribution, or other securities-law
perimeter issues.

This is not a final legal conclusion. It is a routing and risk-discipline tool.

## Operating Posture

- Do not assume a token, stablecoin, or platform is outside securities scope by default.
- Separate securities issues from MSB and PSP issues, but do not ignore overlap.
- Treat strong heuristics as heuristics, not as rules.
- Prefer candid routing over premature comfort.

## Core Question

Does the fact pattern suggest token issuance, distribution, solicitation,
intermediation, custody, marketplace, resale, stablecoin, dealer, or other
securities-law perimeter issues?

## Automatic Triggers For This Screen

Run this screen if the intake mentions any of the following:

- presale, prelaunch sale, SAFT-like sale, or deferred token delivery
- token, stablecoin, or value-referenced crypto asset issuance
- repeated selling, placement, or active solicitation of token interests
- redemption promises, reserve backing, stabilization, or treasury management
- staking, yield, rewards, rebates, buybacks, fee-sharing, or revenue-linked features
- custody, omnibus holding, pooled assets, or contractual claims to crypto
- platform matching, secondary trading, order routing, or exchange functionality
- tokenized exposure to equities, debt, funds, commodities, or real-world assets
- marketing that emphasizes profit, appreciation, passive upside, or managerial support

## Are They An Issuer?

### First-Pass Questions

- What exactly is being sold, transferred, or made available?
- When does the buyer actually receive it?
- What rights attach to it: redemption, fees, reserves, revenue, governance, claims, dividends, buybacks, or liquidation rights?
- What will management, affiliates, validators, operators, or foundations keep doing after the sale?
- Is there custody, control, pooled holding, or only a contractual entitlement?
- Is there a platform that brings together multiple buyers and sellers?
- Are Canadians targeted, onboarded, or permitted?
- What do the marketing materials say about value, returns, support, listings, liquidity, or treasury activity?
- What use of proceeds, build roadmap, or continuing managerial dependency exists?

### Useful But Non-Dispositive Heuristic

"No ROI from management" may be a helpful warning heuristic, but it is not a
complete Canadian token test. It does not answer custody, marketplace,
distribution, resale, or value-referenced asset issues.

### Likely Issuer Flags

- investment-contract style sale or scheme
- deferred delivery or prefunctional sale
- profit, yield, fee, buyback, reserve, or treasury-linked expectations
- tokenized interests in existing securities or investment products
- platform intermediation, custody, or matching
- resale, exemption, or secondary-market reliance

## Are They A Dealer?

### First-Pass Questions

- Is the business regularly selling, placing, arranging, or intermediating token transactions for others?
- Is there active solicitation, onboarding, marketing, or client acquisition tied to trading or distribution?
- Does the business receive compensation through spreads, fees, commissions, allocations, or transaction-based economics?
- Does the business stand between clients and market access, liquidity, counterparties, or issuers?
- Does the business hold, control, route, or facilitate client orders or client assets?
- Is the business running a platform, desk, brokerage-like channel, or other intermediation layer?
- Is the client describing repeated capital raising or token distribution as a one-off when it appears to be a business line?

### Likely Dealer Flags

- repeated intermediation or solicitation is part of the business model
- compensation is tied to placements, trades, or transaction flow
- the business helps buyers and sellers find each other or access markets
- the business handles client onboarding, order flow, or token allocation
- the business holds itself out as a route to purchase, sale, liquidity, or market access
- dealer-like activity is being framed as mere technology, community support, or introductions

## Escalation Flags

- the client insists the asset is outside securities law by default
- decentralization claims are doing most of the analytical work
- stablecoin or reserve features are underdescribed
- custody, platform, or secondary trading facts are underdescribed
- dealer-like activity is underdescribed or disguised as software-only functionality
- the model mixes issuer-side or dealer-side activity with MSB or PSP functions

## Required Output Format

Each note should state:

- `primary_regulatory_lens`
- `possible_securities_roles`
- `core_trigger_facts`
- `core_risks`
- `client_risk_rating`
- `touchability`
- `required_overlap_routing`
- `next_ml1_decision`

## Routing Rule

- Route to `Muggah Securities` whenever token issuance, distribution, dealer,
  custody, marketplace, stablecoin, resale, or investment-contract issues appear materially live.
- Add `Muggah Money Services` if virtual-currency dealing, remittance, exchange,
  or AML/reporting issues are also present.
- Add `Muggah Payment Services` if payment-function, safeguarding, or end-user
  funds issues are also present.
