---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_011_payments_regulatory_compliance_agency__executing__workplan_md
title: Payment Services Consulting Line - Executing Workplan
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-05-11
tags: [payment-services-consulting-line, executing, workplan]
---

# IMPLEMENTATION WORKPLAN

Project ID: `HBP-011`
Project Path: `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-011_PAYMENTS_REGULATORY_COMPLIANCE_AGENCY`
Stage: `Executing`

## Objective

Operationalize the Payment Services Consulting Line under
`17513721 Canada Inc` with two entry points:

1. FinSure STR report
2. FINTRAC effectiveness review readiness lead magnet with paid consultation offer

Business model: agency model. 175 owns the offer, coordinates delivery, and may
use outsourced providers for CAMS operational consulting, licensing support, and
CAMLO sourcing.

Relationship to `HBP-014`: HBP-011 is the execution packet for the
payment-services service line inside the 175 / Dominion / Andersen strategy.

Buyer profile: same PSP / MSB profile as HBP-010.

## EW-01 — Service Packaging (updated 2026-05-23)

Approved six-tier 175 service ladder:

| Tier | Description | Entity | Price |
|---|---|---|---|
| 1 | FinSure STR report, consulting only | 17513721 Canada Inc. | $297 |
| 2 | Rhizome white label | 17513721 Canada Inc. / HBP-010 | TBD |
| 3 | Managed compliance, no CAMLO provision | 17513721 Canada Inc. | TBD |
| 4 | CAMS operational consulting, outsourced operations track | 17513721 Canada Inc. | TBD |
| 5 | Licensing support, outsourced high-ticket track | 17513721 Canada Inc. | TBD |
| 6 | CAMLO sourcing, 1-year contract minimum | 17513721 Canada Inc. | $3,000 CAD/month reference price, flagged as possibly too low |

Levine Law monthly / quarterly review and fractional counsel are separate
referral pathways, not part of the 175 service ladder.

Entry architecture:

| Entry Point | Purpose | Conversion Path |
|---|---|---|
| FinSure STR report | Productized STR drafting / suspicious-activity workflow entry point | Qualifies clients into managed compliance, CAMS operational consulting, or broader compliance support |
| FINTRAC effectiveness review readiness checklist | Demand-generation checklist for existing MSBs before independent effectiveness review | Converts into paid AML Effectiveness Review Readiness Assessment / remediation session |

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
| CAMS operational consulting (value ladder tier 4) | Fixed fee / retainer | TBD (outsourced delivery possible; 30% floor applies) |
| Licensing support (value ladder tier 5) | Fixed fee / milestone fee | TBD (high-ticket; outsourced delivery possible; 30% floor applies) |
| CAMLO sourcing (value ladder tier 6) | Monthly, 1-year contract min | $3,000 CAD/month reference price may be too low; cost to 17513721: $18,000/year; gross margin ~50% before coordination burden |

**Onboarding fee:** An onboarding fee exists as an agency offering but is currently waived.
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

**Business name:** FinSure (confirmed product brand for the STR report entry point).

**Public front-end:** finsure.dominionpartners.ca (within the Dominion Platform).

**Dominion relationship:** `dominionpartners.ca` is the parent 175 / Dominion
enterprise site. `finsure.dominionpartners.ca` is the focused FinSure subdomain
for the HBP-011 Payment Services Consulting Line.

Required FinSure web structure:

| Route / Surface | Role |
|---|---|
| `finsure.dominionpartners.ca` | FinSure home page / product overview |
| STR report landing page | Explains and routes to the FinSure STR report product |
| Portal access | Authenticated client area; the STR product lives inside the portal |
| FINTRAC readiness landing page | Hosts the effectiveness review readiness checklist and converts to paid consultation |

**Second entry point / lead magnet:** `LEAD_MAGNET_FINTRAC_EFFECTIVENESS_REVIEW_READINESS.md`.

Current lead magnet:

**Is Your MSB Ready for FINTRAC Effectiveness Review?**

A practical readiness checklist for Canadian Money Services Businesses. The
paid consultation path is the **AML Effectiveness Review Readiness Assessment**:
a pre-review readiness assessment / remediation session for existing MSBs,
compliance officers, AML compliance managers, fintech operators, payment
companies, and growing payment businesses.

## Entry Point 1 — FinSure STR Report (updated 2026-05-03)

FinSure is being built out as a landing page leading to a portal where clients access
the STR report product. The STR product lives inside the authenticated portal,
with an opt-in path to higher-ticket services.

**Funnel:**

```
finsure.dominionpartners.ca (landing page)
   ↓
Portal (authenticated client area)
   ↓
FinSure STR report product
   ↓
Opt-in to higher-ticket services
```

**Infrastructure:**
- Prior build: `https://finsure-w321.onrender.com`
- Target domain: `https://finsure.dominionpartners.ca` (Vercel; DNS via CNAME to cname.vercel-dns.com)
- DNS authority: single Vercel team / account per Dominion Platform architecture
- Prior HostGator DNS blocker is superseded by the Dominion Platform Vercel deployment model

**Value ladder (updated 2026-05-23):**

| Tier | Description | Entity | Price |
|---|---|---|---|
| 1 | FinSure STR report, consulting only | 17513721 Canada Inc. | $297 |
| 2 | Rhizome white label | 17513721 Canada Inc. / HBP-010 | TBD |
| 3 | Managed compliance, no CAMLO provision | 17513721 Canada Inc. | TBD |
| 4 | CAMS operational consulting, outsourced operations track | 17513721 Canada Inc. | TBD |
| 5 | Licensing support, outsourced high-ticket track | 17513721 Canada Inc. | TBD |
| 6 | CAMLO sourcing, 1-year contract minimum | 17513721 Canada Inc. | $3,000 CAD/month reference price, flagged as possibly too low |
| 7 | Levine Law monthly or quarterly review | Levine Law | TBD |
| 8 | Levine Law fractional counsel | Levine Law | $8,000/month minimum |

Tiers 1–6 are non-legal services delivered by 17513721 Canada Inc. (FinSure brand).
Tiers 7–8 are Levine Law services. They are a separate entity. Tiers 7–8 are
referral pathways only — not part of 17513721's service offering — and each
cross-entity referral requires ML1 authorization per engagement.

HBP-011 governs tiers 1, 3, 4, 5, and 6. HBP-010 governs tier 2.

**Tier 1–4 operating model:**

| Tier | Commercial Role | Core Deliverable | Buyer Trigger | Boundary / Escalation |
|---|---|---|---|---|
| 1 | Low-friction entry product that qualifies demand and creates a client record | FinSure compliance assessment / tool, issue-spotting output, and recommendation path | Client wants a quick read on PSP / fintech compliance posture without committing to an advisory mandate | Consulting only; no filings, no legal opinion, no CAMLO role; output should identify whether tier 3, 4, 5, 6, or Levine Law referral is appropriate |
| 2 | Product / partner implementation layer through HBP-010 | Rhizome white-label implementation or adjacent partner work | Client needs tooling or implementation support beyond the FinSure entry assessment | Governed by HBP-010, not HBP-011; must not smuggle Rhizome or partner work into the FinSure compliance packet |
| 3 | Managed compliance infrastructure without CAMLO provision | Compliance program build / refresh, policy set-up, workflow design, monitoring cadence, evidence discipline, and operating calendar | Client needs recurring compliance operating support but retains its own responsible officer and decision-making | No CAMLO provision, no delegated decision-making, no regulator representation; may ladder into tier 4 CAMS operational consulting or tier 5 licensing support when specialist delivery is required |
| 4 | CAMS operational consulting | AML/KYC operations, compliance workflow, policy implementation support, operational readiness, and evidence discipline | Client needs practical compliance operations support from a specialist delivery bench but is not asking 175 to provide the CAMLO function | Outsourced CAMS / AML specialist support under 175 coordination; no CAMLO provision, no delegated decision-making, no regulator representation |

**CAMLO sourcing model (tier 6):**
- 17513721 Canada Inc. sources (places) a CAMLO for the client — it does not itself
  provide the CAMLO function
- This is a consulting/placement service, not a legal service; Levine Law has no role
- Minimum commitment: 1-year contract required from the client before sourcing begins
- Cost to 17513721: $18,000/year for the placed CAMLO
- Current client-facing reference price: $3,000 CAD/month (billed monthly; $36,000/year); gross margin ~50% before coordination, diligence, replacement, escalation, and account-management cost
- Pricing caution: $3,000 CAD/month may be too low for a 1-year CAMLO sourcing arrangement if 175 is expected to carry provider diligence, replacement risk, client-management burden, or escalation support
- Currency: all client pricing in CAD; CAMLO cost denominated in CAD

**Tier 3 scope clarification:** Managed compliance does not include CAMLO provision.
CAMLO sourcing is a distinct, higher-commitment service available only at tier 6.

Tier 3 may ladder into two separately priced outsourced delivery tracks:

| Track | Description | Delivery posture | Pricing posture |
|---|---|---|---|
| CAMS operational consulting | AML/KYC operations, compliance workflow, policy implementation support, and operational readiness | Outsourced CAMS / AML specialist support; no CAMLO provision and no delegated decision-making | Fixed fee or retainer; price TBD |
| Licensing | High-ticket licensing / registration support for payment-services clients | Outsourced specialist support under 175 coordination; legal/regulatory boundary to be checked before offer | High-ticket fixed fee or milestone fee; price TBD |

Rödl Latvia is a candidate outsourced provider for the CAMS / AML operational
consulting track. Public source check: Rödl Latvia describes an
interdisciplinary legal, tax, audit, and accounting team, and lists Arsenijs
Korabelskis as a Certified Anti-Money Laundering Specialist (CAMS) with AML and
KYC compliance experience.

Spridzans is the candidate outsourced provider for the licensing track. Public
source check: Spridzans presents Latvian banking, finance and capital markets,
regulatory, corporate / commercial, and international advisory capability. ML1
identified Spridzans as able to support licensing.

**Confirmed build decisions:**
- Portal authentication: shared via Dominion `packages/auth` module across FinSure and dominionpartners.ca (confirmed 2026-05-03)

**Open build questions:**
- Whether the existing finsure-w321.onrender.com build migrates to Vercel or is rebuilt — TBD

See `MATTHEW_HOLDINGS_17513721_CANADA_INC/DOMINION_PLATFORM/PLATFORM_ARCHITECTURE.md`
for the full Dominion deployment and DNS model.

## Control Notes

- The approved path is narrower than the original broad agency concept.
- HBP-011 has two entry points: the FinSure STR report and the FINTRAC
  effectiveness review readiness lead magnet.
- The FINTRAC effectiveness review readiness checklist is the current
  lead-magnet concept for qualifying existing MSBs into a paid readiness
  assessment / remediation session.
- Rhizome white-label or partner implementation work is outside `HBP-011` and belongs in `HBP-010`.
- Higher-ticket opt-in services require a separate scoped decision before activation.

## Change Log

- 2026-03-20 — Workplan created; execution priorities authorized
- 2026-04-25 — All five workstreams locked per ML1 working parameters; CAMLO scope removal recorded; FinSure positioning confirmed
- 2026-05-03 — Product model updated: landing page → portal → entry-level product → higher-ticket opt-in; Dominion Platform architecture adopted; DNS model updated to Vercel
- 2026-05-11 — Value ladder restructured to 6 tiers; CAMLO model clarified as sourcing/placement (not provision, not legal service); 1-year contract minimum added; Levine Law confirmed as referral pathway (separate entity); Tier 1 price set at $297; CAMLO cost to 17513721 recorded at $18,000/year (annual); EW-02 updated with dollar amounts; Tiers 2, 3, and 5 client pricing TBD
- 2026-05-23 — Tier 3 managed compliance split into two possible outsourced tracks: high-ticket licensing and CAMS operational consulting; Rödl Latvia recorded as candidate outsourced CAMS / AML operational provider
- 2026-05-23 — Value ladder expanded to 8 tiers: outsourced operational and licensing tracks added before Levine Law referral pathways, which were renumbered to tiers 7–8
- 2026-05-23 — CAMS operational consulting corrected to tier 4; licensing retained as tier 5; CAMLO sourcing moved to tier 6 with $3,000 CAD/month reference price flagged as potentially too low
- 2026-05-23 — Spridzans recorded as candidate outsourced licensing provider for tier 5
- 2026-05-24 — HBP-011 wired to HBP-014 as the payment-services service-line execution packet; FINTRAC effectiveness review readiness checklist recorded as the current lead magnet
