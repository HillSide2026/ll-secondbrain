---
id: 04_initiatives__hillside_portfolio__matthew_holdings__2b_federal_msb_17409052_canada_inc__product_software_candidates_md
title: 17409052 Canada Inc Product Software Candidates
owner: ML1
status: draft
created_date: 2026-05-15
last_updated: 2026-05-19
tags: [granville, federal-msb, product-software, mambu, toqio, crassula, sdk-finance, finlego, rhizome, formance, payments]
---

# 17409052 Canada Inc Product Software Candidates

## Purpose

This document tracks product-software candidates for `17409052 Canada Inc`.

Product software is distinct from compliance software.

For 174, product software means the platform layer that could help a buyer
understand the entity as a payments infrastructure package rather than only a
pending federal MSB shell.

## Current Candidate Status

Product-software candidates are now known at the proposed-candidate level.

No product software has been selected.

## Current Reframing Question

Both FinLego and Crassula have quoted versions of "core banking."

That may be the wrong frame for 174.

174 does not currently intend to market or operate itself as a bank, neobank,
or heavy banking platform. The existing value-stack documents point to a
lighter role:

- customer-facing application layer;
- orchestration / routing layer;
- AML / compliance control layer;
- visible EMI relationship; and
- buyer-readable product or sandbox evidence.

The live question is whether 174 can fit into a cheaper, thinner product model
that excludes the parts of "core banking" it does not actually need.

The lower-cost model to test is:

- UI or portal layer;
- fiat-account presentation, if useful;
- connector or EMI-routing layer, if real and transferable;
- sandbox or demo environment for buyer / regulator review; and
- no unnecessary cards, crypto, mobile, or full production-deployment scope.

This means vendor discussions should not ask only, "What is your core banking
price?"

They should also ask, "What is the minimum non-banking package that still makes
174 more saleable?"

## Candidate List

| Candidate | Current classification | Potential 174 role | Fit for 174 | Main diligence questions | Current status |
| --- | --- | --- | --- | --- | --- |
| Mambu Payments / Payments Hub | Payments hub / payment orchestration infrastructure | Payment processing orchestration, liquidity management, reconciliation, and managed bank connectivity evidence | Potentially strong but likely heavier and more enterprise-oriented than 174 needs at minimum sale-readiness stage | Is Mambu willing to support a pre-revenue / sale-oriented MSB asset? What minimum fees, implementation burden, bank-connectivity requirements, and contractual commitments apply? Does the current Mambu Payments product, after the Numeral acquisition, fit 174 directly or only through larger financial institutions? | Proposed candidate; not selected |
| Toqio | Embedded-finance / no-code-low-code platform | Build or demonstrate a branded embedded-finance proposition using marketplace / configurable components | Potentially useful for faster product demonstration and buyer-facing narrative; may fit a lighter sale package better than a heavy payments hub | What regulated partners are actually available to 174? Does Toqio provide product UI only, infrastructure access, partner marketplace access, or all three? Can it support the EMI path, Kwiikpay path, or both? What are the fees and transferability terms? | Proposed candidate; not selected |
| Crassula | White-label banking / BaaS / payment hub platform with software plus connectors | Product layer (UI, fiat accounts, EUR/GBP/USD) plus a broad EMI-connector layer and possible regulator-review sandbox path | More interesting than a simple software quote because the EMI connector list appears robust, but materially more expensive than FinLego and still likely broader than 174 needs | Exact final quote and currency; which EMI connectors are actually available to 174; prerequisites for regulator sandbox access; data portability and change-of-control terms | Met with ML1 week of 2026-05-18; opening pricing still pending final confirmation at roughly 20k setup and 11k/month; follow-up required |
| SDK.finance | White-label fintech platform with source-code / SaaS options | E-wallet, neobank, PSP, payment processing, ledger, reconciliation, treasury orchestration, crypto-to-fiat, back-office, and API layer | Potentially strong for technical ownership and buyer diligence because source-code licensing may support customization and portability | Is source-code access useful or overkill for 174? What is the implementation burden? Which regulated integrations are included vs client-procured? Can the platform support MSB / EMI / PSP flows without 174 holding funds? What buyer-transfer rights apply? | Proposed candidate; not selected |
| FinLego | White-label BaaS software ("core banking") — three modules: UI (desktop/phone; desktop-only available), fiat accounts, supported currencies (EUR, GBP, USD). Banking access through Kanzum, which is an MSB — not a bank or EMI | Product layer (UI, fiat accounts, EUR/GBP/USD); banking network access via Kanzum MSB | Opening pricing: setup from EUR 15k; monthly minimum from EUR 4k/month. Final offer not yet received. Kanzum does not satisfy RPAA safeguarding. ML1 gut posture: not the right path regardless of final price. | Final offer terms; whether software is separable from Kanzum | Opening figures received 2026-05-18; final offer pending; ML1 posture: likely pass; advance ClearSky first |
| Array (array.com) | US embedded finance platform — credit monitoring, identity protection, debt repayment guidance, subscription management | None — wrong product category for 174 | Not a fit. Array is a consumer financial product layer targeting US fintechs (SoFi, Dave, Brigit). No fiat accounts, no payment rails, no MSB-relevant infrastructure, no EUR/GBP/USD coverage. Not a payments infrastructure platform. | N/A | Reviewed 2026-05-18; rejected — wrong product category |
| Rhizome (founder arrangement) | White-label Rhizome software + landing page editing + Formance open-source integration — bundled founder-led arrangement | (i) white-labeled compliance/product software under Granville brand; (ii) landing page build satisfying RPAA domain requirement; (iii) Granville portal on Formance open-source repos integrated into white-labeled product | Potentially the most efficient path: bundles compliance software (already the default), product layer, public presence, and open-source infrastructure in one arrangement. Formance is auditable and transferable. Founder relationship may allow flexible terms. Key risks are founder dependency and IP/transferability clarity. | Who owns the Granville codebase? Can a buyer inherit or terminate the white-label arrangement? What are pricing and exclusivity terms? Is Rhizome's role compliance only, or does white-labeling extend into the product layer? What does the Formance integration cover (ledger, workflows, APIs)? | Proposed by ML1 2026-05-18; not yet negotiated |

## Candidate Interpretation

### Mambu

Mambu should be evaluated as a serious payments-infrastructure candidate, but
not assumed to be proportionate for 174.

Its possible value is that it may evidence a mature payments-hub path:

- payment processing orchestration;
- liquidity management;
- reconciliation; and
- managed bank connectivity.

The risk is that Mambu may be too heavy, too expensive, or too institutionally
oriented for a pre-revenue asset whose goal is sale-readiness rather than
scaled operation.

Mambu should be diligence-tested for:

- minimum implementation scope;
- pricing;
- contract term;
- buyer transferability;
- implementation timeline;
- whether 174 can use it directly;
- whether it requires an existing bank / EMI relationship first; and
- whether the newer Mambu Payments / Numeral product is the relevant offering,
  rather than the older Mambu Payment Gateway.

### Toqio

Toqio should be evaluated as a lighter embedded-finance platform candidate.

Its possible value is speed: it may support a configurable product
demonstration, marketplace-based partner access, or a branded embedded-finance
proposition without a full custom build.

The risk is that Toqio may produce a good product wrapper without solving the
real 174 infrastructure questions:

- EMI access;
- safeguarding;
- payment execution;
- regulatory responsibility split;
- Kwiikpay role; and
- buyer transferability.

Toqio should be diligence-tested for:

- whether its marketplace includes relevant regulated payment partners;
- whether 174 can use it as the customer-facing application layer;
- whether it can integrate with the EUR 12,000 EMI path;
- whether it can integrate with Kwiikpay if Kwiikpay becomes a 174
  infrastructure path;
- fees and minimums;
- no-code / low-code limits;
- data portability; and
- change-of-control or buyer-transition treatment.

### Crassula

Crassula met with ML1 week of 2026-05-18. They pitched software plus
"connectors."

#### Product Modules

The software modules discussed were:

| Module | Description | Relevance to 174 |
| --- | --- | --- |
| UI | Front-end product layer | Supports buyer-facing product narrative |
| Fiat accounts | Account infrastructure for fiat funds | Core module for the payments-infrastructure story |
| Supported currencies | EUR, GBP, USD | Matches the three-currency pattern already viewed as useful for 174 |

These modules matter because they give 174 a lightweight product-stack story
without requiring the full scope of a scaled operating build.

#### Connector Layer

Crassula's brighter point relative to FinLego is not the software layer alone.
It is the connector layer.

Crassula represented that it has a robust list of EMI connectors. That is
potentially important for 174 because it suggests multiple regulated
counterparty paths rather than one narrow quasi-banking relationship.

The key unresolved diligence question is not whether connectors exist in the
abstract. It is:

- which EMI connectors are real and live;
- which are available to 174 specifically;
- whether the relationships are direct or indirect;
- whether they help the RPAA safeguarding narrative; and
- whether a buyer can inherit or replace the connected stack cleanly.

#### Indicative Pricing

Opening pricing remains pending final confirmation, but the current indication
is roughly:

| Component | Indicative amount | Status |
| --- | --- | --- |
| Setup fee | ~20k | Pending final confirmation |
| Monthly fee | ~11k/month | Pending final confirmation |

This is more expensive than FinLego on the current numbers.

That makes Crassula hard to justify as a pure sale-readiness software purchase
unless the connector depth, transferability, or regulator utility materially
changes the value analysis.

#### Sandbox for Regulator Review

One bright spot is that Crassula indicated it may be open to making its sandbox
available for regulator review.

If that is real and practical, it could help the 174 RPAA credibility story by
making software readiness more reviewable and less abstract.

What remains unclear is what has to happen before that becomes possible:

- commercial commitment level;
- legal permissions;
- technical setup requirements;
- whether regulator review means passive viewing or active access; and
- whether the sandbox can be referenced in a buyer diligence folder.

This uncertainty is the immediate follow-up item.

#### Working Posture

Crassula remains interesting, but not because it is cheaper or lighter than
FinLego. On the current facts, it appears more expensive.

Its real value case is:

- broader EMI connector coverage; and
- possible regulator-review usefulness through sandbox access.

Crassula should now be diligence-tested for:

- exact final pricing and currency;
- minimum viable module set for sale-readiness;
- implementation timeline;
- live EMI connector availability for 174;
- sandbox prerequisites for regulator review;
- data export and portability;
- whether buyer can inherit or replace the stack; and
- whether the KYC / KYB module reduces or complicates the Rhizome / Sumsub
  compliance decision.

### SDK.finance

SDK.finance should be evaluated as a white-label fintech platform candidate.

Its possible value is that it appears to offer a broad financial-application
stack:

- e-wallet;
- neobank;
- PSP software;
- payment processing;
- ledger;
- reconciliation and settlement;
- treasury orchestration;
- crypto-to-fiat operations;
- back-office workflows; and
- source-code or SaaS pathways.

The source-code angle may be valuable if a buyer cares about portability,
customization, or control.

The risk is that source-code ownership and broad platform scope may create
implementation burden, technical due diligence questions, and a heavier build
than the 174 sale-readiness package needs.

SDK.finance should be diligence-tested for:

- whether SaaS or source-code licensing is the right posture for 174;
- minimum viable implementation scope;
- pricing and support obligations;
- regulated-provider integrations;
- whether it can sit above the EUR 12,000 EMI path or Kwiikpay path;
- whether it can support flows without 174 holding funds;
- buyer-transfer rights; and
- technical documentation needed for a buyer diligence folder.

### FinLego

FinLego met with ML1 week of 2026-05-18. They were enthusiastic about providing
software to 174 and clarified that their offer includes software plus banking.

#### Core Banking Product

FinLego's primary product offer is a white-label banking-as-a-service software
solution they call "core banking." It is a software product, not a regulated
banking licence or balance-sheet relationship.

The product has three modules:

| Module | Description | Activation note |
| --- | --- | --- |
| UI | Desktop and phone application | Desktop-only activation available; phone not required |
| Fiat accounts | Account infrastructure for holding and moving fiat funds | Core module for payments infrastructure narrative |
| Supported currencies | EUR, GBP, USD | Three major fiat currencies covered |

The ability to activate desktop only (without phone) is relevant for 174 at the
pre-revenue sale-readiness stage: it reduces scope, cost, and implementation
complexity without removing the product-layer narrative from the buyer package.

The fiat accounts module and three-currency coverage (EUR, GBP, USD) are directly
relevant to the 174 value stack. They support the buyer-facing payments
infrastructure narrative and can be documented in the diligence folder.

#### Kanzum — "Their Bank"

They referred to Kanzum (`https://www.kanzum.com/`) as "their bank."

**Kanzum is not a bank.** It is not an EMI or PSP either. It is an MSB with
apparently deep networks into developing-country markets. The characterization
of Kanzum as a "bank" is misleading or imprecise — it likely reflects how
FinLego positions the relationship commercially rather than how Kanzum is
regulated.

This has two consequences:

1. **RPAA safeguarding:** Kanzum cannot satisfy the RPAA safeguarding
   requirement. The RPAA requires a financial institution to hold end-user funds.
   An MSB does not qualify. If FinLego's "banking" access is exclusively through
   Kanzum, it does not solve 174's safeguarding problem and does not support the
   RPAA application.

2. **Separate value question:** Kanzum's developing-market networks may
   nonetheless be interesting for 174's buyer proposition if they represent
   genuine payment corridors. This should be assessed as a distinct question
   from the safeguarding and RPAA analysis — not conflated with it.

The FinLego software product should continue to be evaluated on its own terms.
If the software is sound, it retains value regardless of the Kanzum
characterization. The software scope, pricing, and transferability questions
remain open and are the priority follow-up items.

#### Pricing Received (2026-05-18) — Opening Position Only

All parts carry both a setup fee and a monthly minimum:

| Component | Setup fee | Monthly minimum | Annual run rate |
| --- | --- | --- | --- |
| Software (starting point) | EUR 15,000 | EUR 4,000/month | EUR 48,000/year |

These are opening / starting figures — not a final offer. Final pricing is
unknown.

At the opening floor, the total cost of ownership for a pre-revenue asset would
be EUR 15k upfront plus EUR 48k/year in minimums with no offsetting revenue.
That is high for a sale-readiness package, but the final offer may differ
materially.

**ML1 posture:** Gut read is that this is not the right path, regardless of
where the final offer lands. The Kanzum/safeguarding issue is structural and
independent of price. ClearSky Payments should be advanced to a formal proposal
before any further engagement with FinLego.

### ClearSky Payments (Tel Aviv)

ClearSky is not a software provider. It is an agency that sells brokered
relationships to banks. The ~2k figure previously noted was for brokerage
services, not software.

ClearSky does not belong in the product-software candidate list. It has been
removed from the candidate table.

ClearSky may be relevant to the EMI and banking access workstream — specifically
as a path to a bank or safeguarding counterparty relationship — but that
evaluation belongs in `EMI_AND_PARTNERSHIP_OPTIONS.md`, not here.

### Rhizome Founder Arrangement

ML1 has identified a potential arrangement with the founder of Rhizome comprising
three elements:

1. **White-label Rhizome software to Granville** — Rhizome, already the default
   compliance software candidate for 174, would be rebranded under the Granville
   identity. This collapses the product and compliance software decisions into one
   relationship.

2. **Edit the Granville landing page** — this directly addresses RPAA Blocker 1
   (credible domain). A live landing page describing Granville's payments business
   and regulatory status is what the Bank of Canada expects. Having the founder
   involved accelerates this.

3. **Integrate the Granville Formance codebase into the white-labeled product and
   repo** — Granville has an existing portal built on Formance open-source
   repositories. Formance (formerly Numary) is an open-source ledger and payments
   orchestration platform — providing ledger, transaction management, workflow
   automation, and APIs. Integrating it into the white-labeled product means 174
   has a codebase, not just a concept.

**Why this path is interesting:**

- It bundles four open workstreams — compliance software, product layer, landing
  page, and infrastructure codebase — into one founder-led arrangement.
- Formance is open-source: it is auditable, portable, and not dependent on a
  proprietary vendor's continued existence. A buyer can inspect, fork, or replace
  it. This is a strong transferability argument.
- The founder relationship may produce more flexible pricing and terms than a
  commercial vendor relationship.
- It produces a buyer-readable diligence artifact: a working, branded, integrated
  codebase on a known open-source stack.

**Key risks and open questions:**

- **IP ownership:** Who owns the Granville-branded codebase built on Formance?
  The open-source base is clear, but the customization layer and integration work
  must be owned by 174 (or assignable to a buyer) — not retained by the founder.
- **Founder dependency:** A buyer may flag key-person risk if the arrangement is
  personal to the founder rather than contracted to a legal entity. The arrangement
  needs to be documented as a commercial contract, not a personal favour.
- **Scope of white-label:** Does white-labeling Rhizome extend into the product
  layer (user-facing application, fiat accounts, payment flows), or is it
  compliance tooling only under a Granville skin? This determines whether it
  replaces the need for other product-software candidates.
- **Transferability:** Can a buyer inherit the white-label licence and the
  Formance integration, or must they renegotiate from scratch?
- **Exclusivity:** Does the arrangement restrict 174 or the founder from working
  with competing entities?

**EMI layer:** The Rhizome founder arrangement addresses software, compliance,
and infrastructure. It does not provide payment rails or safeguarding. The EMI
layer remains a separate requirement. Airwallex and Modulr are the current
identified candidates in `EMI_AND_PARTNERSHIP_OPTIONS.md`, but no EMI has been
selected and no decision has been made. Which EMI pairs with this stack is
an open question.

**ML1 posture:** This is the most promising path identified to date. It should
be advanced to a term-sheet conversation with the founder before committing to
any other product-software vendor.

## Relationship to Compliance Software

The current compliance-software candidates remain:

- Rhizome, as default; and
- Sumsub, only if EMI, bank, or safeguarding counterparties require it.

Mambu and Toqio do not replace the Rhizome / Sumsub compliance decision unless
their offerings include compliance modules that satisfy the buyer-review
standard.

## Relationship to Kwiikpay

Kwiikpay remains an infrastructure / partnership path, not a product-software
candidate, unless its role is defined in writing as a product or platform layer
for 174.

If Kwiikpay becomes the relevant infrastructure path, Mambu and Toqio should be
tested for whether they can integrate with, complement, or replace Kwiikpay.
The same test applies to Crassula and SDK.finance.

## Minimum Gate Effect

The 174 minimum sale-readiness gate requires that product-software candidates
are known.

This document satisfies the candidate-identification part of that requirement
only at a preliminary level.

The gate is not stronger than that until ML1 decides whether either candidate
is suitable enough to remain in the buyer-facing diligence package.

## Sources To Verify In Diligence

- Mambu Payments Hub: `https://mambu.com/en/payments-hub`
- Mambu Payments documentation: `https://docs.mambu.com/docs/mambu-payments/`
- Toqio: `https://toqio.co/`
- Crassula: `https://crassula.io/`
- SDK.finance: `https://sdk.finance/`
- Kanzum (FinLego-referenced MSB, not a bank): `https://www.kanzum.com/`
