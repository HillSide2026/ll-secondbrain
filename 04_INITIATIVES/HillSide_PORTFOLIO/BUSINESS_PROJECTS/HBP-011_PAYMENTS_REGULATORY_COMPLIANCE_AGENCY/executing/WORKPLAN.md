---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_011_payments_regulatory_compliance_agency__executing__workplan_md
title: Payments Regulatory & Compliance Consulting Agency - Executing Workplan
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-05-11
tags: [payments-regulatory-compliance-agency, executing, workplan]
---

# IMPLEMENTATION WORKPLAN

Project ID: `HBP-011`
Project Path: `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-011_PAYMENTS_REGULATORY_COMPLIANCE_AGENCY`
Stage: `Executing`

## Objective

Operationalize a narrow payment services compliance service under
`17513721 Canada Inc` with FinSure as the initial entry offer.

Buyer profile: same PSP / MSB profile as HBP-010.

## EW-01 — Service Packaging (LOCKED 2026-04-25)

Three service tiers:

| Tier | Name | Description |
|---|---|---|
| 1 | Readiness | RPAA / MSB compliance assessment |
| 2 | Build | AML and compliance program build |
| 3 | Ongoing | Advisory (recurring) |

## EW-02 — Pricing Design (updated 2026-05-11)

- Model: fixed fee plus retainer
- Margin floor: 30% minimum
- Hourly billing is not the core model

All prices in CAD.

| Service | Type | Price |
|---|---|---|
| Entry product (value ladder tier 1) | Fixed fee | $297 CAD |
| Managed compliance — Build (value ladder tier 3) | Fixed fee | TBD (30% floor applies) |
| Managed compliance — Ongoing (value ladder tier 3) | Retainer | TBD (30% floor applies) |
| CAMLO sourcing (value ladder tier 4) | Monthly, 1-year contract min | $3,000 CAD/month ($36,000/year); cost to 17513721: $18,000/year; gross margin ~50% |

**Onboarding fee:** An onboarding fee exists as a service line but is currently waived.
This should be defined and activated before any significant volume is onboarded.

## EW-03 — Scope Control (LOCKED 2026-04-25)

**In scope:** compliance infrastructure and advisory to Canadian PSPs and fintechs.

**Explicitly excluded:**
- No CAMLO role
- No regulatory filings
- No regulator representation
- No decision-making delegation

**Scope narrowing note (2026-04-25):** Prior approval record (2026-03-20) listed "CAMLO services" as part of the initial service model. This has been removed. FinSure provides tools and advisory only; CAMLO responsibility stays with the client.

## EW-04 — Second-Model Decision (LOCKED 2026-04-25)

**Decision: NO.** Infrastructure-focused CAMLO-support model (client supplies in-house CAMLO) is deferred. Not part of the current service set.

## EW-05 — FinSure Positioning (LOCKED 2026-04-25)

**Positioning statement:** "We provide compliance infrastructure and advisory to Canadian PSPs and fintechs."

**Business name:** FinSure (confirmed entry offer and brand).

**Public front-end:** finsure.dominionpartners.ca (within the Dominion Platform).

## FinSure Product Model (updated 2026-05-03)

FinSure is being built out as a landing page leading to a portal where clients access
the entry-level product, with an opt-in path to higher-ticket services.

**Funnel:**

```
finsure.dominionpartners.ca (landing page)
   ↓
Portal (authenticated client area)
   ↓
Entry-level product (compliance tool / assessment)
   ↓
Opt-in to higher-ticket services
```

**Infrastructure:**
- Prior build: `https://finsure-w321.onrender.com`
- Target domain: `https://finsure.dominionpartners.ca` (Vercel; DNS via CNAME to cname.vercel-dns.com)
- DNS authority: single Vercel team / account per Dominion Platform architecture
- Prior HostGator DNS blocker is superseded by the Dominion Platform Vercel deployment model

**Value ladder (updated 2026-05-11):**

| Tier | Description | Entity | Price |
|---|---|---|---|
| 1 | FinSure entry product — consulting only | 17513721 Canada Inc. | $297 |
| 2 | + Rhizome white label | 17513721 Canada Inc. (HBP-010) | TBD |
| 3 | + Managed compliance (no CAMLO provision) | 17513721 Canada Inc. | TBD |
| 4 | + CAMLO sourcing — 1-year contract minimum | 17513721 Canada Inc. | $3,000 CAD/month (billed monthly; cost to 17513721: $18,000/year; ~50% gross margin) |
| 5 | Levine Law monthly or quarterly review | Levine Law | TBD |
| 6 | Levine Law fractional counsel | Levine Law | $8,000/month minimum |

Tiers 1–4 are non-legal services delivered by 17513721 Canada Inc. (FinSure brand).
Tiers 5–6 are Levine Law services. They are a separate entity. Tiers 5–6 are
referral pathways only — not part of 17513721's service offering — and each
cross-entity referral requires ML1 authorization per engagement.

HBP-011 governs tiers 1, 3, and 4. HBP-010 governs tier 2.

**CAMLO sourcing model (tier 4):**
- 17513721 Canada Inc. sources (places) a CAMLO for the client — it does not itself
  provide the CAMLO function
- This is a consulting/placement service, not a legal service; Levine Law has no role
- Minimum commitment: 1-year contract required from the client before sourcing begins
- Cost to 17513721: $18,000/year for the placed CAMLO
- Client-facing price: $3,000 CAD/month (billed monthly; $36,000/year); gross margin ~50%
- Currency: all client pricing in CAD; CAMLO cost denominated in CAD

**Tier 3 scope clarification:** Managed compliance does not include CAMLO provision.
CAMLO sourcing is a distinct, higher-commitment service available only at tier 4.

**Confirmed build decisions:**
- Portal authentication: shared via Dominion `packages/auth` module across FinSure and dominionpartners.ca (confirmed 2026-05-03)

**Open build questions:**
- Whether the existing finsure-w321.onrender.com build migrates to Vercel or is rebuilt — TBD

See `MATTHEW_HOLDINGS_17513721_CANADA_INC/DOMINION_PLATFORM/PLATFORM_ARCHITECTURE.md`
for the full Dominion deployment and DNS model.

## Control Notes

- The approved path is narrower than the original broad agency concept.
- FinSure is the entry offer; the landing page and portal extend this into a product funnel.
- Rhizome white-label or partner implementation work is outside `HBP-011` and belongs in `HBP-010`.
- Higher-ticket opt-in services require a separate scoped decision before activation.

## Change Log

- 2026-03-20 — Workplan created; execution priorities authorized
- 2026-04-25 — All five workstreams locked per ML1 working parameters; CAMLO scope removal recorded; FinSure positioning confirmed
- 2026-05-03 — Product model updated: landing page → portal → entry-level product → higher-ticket opt-in; Dominion Platform architecture adopted; DNS model updated to Vercel
- 2026-05-11 — Value ladder restructured to 6 tiers; CAMLO model clarified as sourcing/placement (not provision, not legal service); 1-year contract minimum added for tier 4; Levine Law confirmed as tiers 5–6 referral pathway (separate entity); Tier 1 price set at $297; Tier 4 CAMLO cost to 17513721 recorded at $18,000/year (annual); EW-02 updated with dollar amounts; Tiers 2, 3, 5 client pricing TBD
