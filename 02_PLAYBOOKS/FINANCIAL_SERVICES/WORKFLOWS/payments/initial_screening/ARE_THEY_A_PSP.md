---
id: 02_playbooks__financial_services__payments__initial_screening__are_they_a_psp_md
title: Are They A PSP?
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [financial-services, payments, screening, psp, rpaa]
---

# Are They A PSP?

Prepared by `Muggah Payment Services`
(`MKT_MUGGAH_PAYMENT_SERVICES_AGENT`).

## Purpose

Internal first-pass screen for whether an intake likely raises Canadian
payment-services or RPAA perimeter issues.

This is not a final legal conclusion. It is a routing and risk-discipline tool.

## Operating Posture

- Do not assume the business is outside PSP scope by default.
- Separate PSP issues from MSB and securities issues, but do not ignore overlap.
- Prefer candid routing over premature comfort.

## Core Question

Does the fact pattern suggest that the client is performing payment functions,
handling end-user funds, safeguarding value, or otherwise operating inside a
Canadian payment-services / RPAA frame?

## Automatic Triggers For This Screen

Run this screen if the intake mentions any of the following:

- wallet, stored-value, payout, merchant-settlement, or payment-orchestration flows
- movement, holding, or safeguarding of end-user funds
- facilitation of payments for merchants, platforms, or marketplaces
- PayFac, program-manager, wallet, or processor language
- token or stablecoin products framed as payment rails or settlement tools
- operational control over payment flow or customer funds
- statements that RPAA does not apply because the business is "just technology"

## First-Pass Questions

- What payment function is the business actually performing?
- Does it hold, settle, transmit, or safeguard end-user funds?
- Who are the end users, merchants, or counterparties?
- Is the client merely a software vendor, or part of the payment flow itself?
- Are funds handled directly, indirectly, contractually, or through partners?
- What role do outsourcing, banking, custody, or sponsor relationships play?
- Is the product really a payments business with token features, rather than the reverse?

## Initial Flags

### Likely PSP / RPAA Flags

- payment-function activity appears operationally real, not incidental
- end-user funds are handled, controlled, or safeguarded
- the client sits inside the flow of funds rather than outside it
- merchant, wallet, payout, stored-value, or settlement language is central
- operational-risk architecture matters to how the business works

### Escalation Flags

- safeguarding is underdescribed or hand-waved away
- the client treats operational controls as incidental
- the model mixes PSP-like activity with MSB or securities functions
- a token or stablecoin narrative may be obscuring a payments business

## Output Format

Each note should state:

- `primary_regulatory_lens`: `payment_services | overlap | unclear`
- `core_trigger_facts`
- `core_risks`
- `client_risk_rating`
- `touchability`
- `required_overlap_routing`
- `next_ml1_decision`

## Routing Rule

- Route to `Muggah Payment Services` whenever PSP, payment-function,
  safeguarding, operational-risk, or end-user-funds issues appear materially live.
- Add `Muggah Money Services` if MSB, foreign-MSB, virtual-currency dealing,
  exchange, remittance, or AML/reporting issues are also present.
- Add `Muggah Securities` if token issuance, custody, marketplace, resale, or
  investment-contract issues are also present.

