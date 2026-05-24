---
id: 04_initiatives__hillside_portfolio__matthew_holdings_17513721_canada_inc__dominion_platform__platform_architecture_md
title: Dominion Platform Architecture
owner: ML1
status: draft
created_date: 2026-05-03
last_updated: 2026-05-03
tags: [dominion, platform, architecture, 17513721, payments, flowsignal, d-airpay]
---

# Dominion Platform Architecture

**Entity owner:** 17513721 Canada Inc, to be registered as Dominion Partners
**Internal portfolio label:** Matthew Holdings
**Last updated:** 2026-05-03

---

## 1. Core Structure

### Corporate Role

17513721 Canada Inc / Dominion Partners is primarily the vehicle for the
Andersen Consulting collaborating firm agreement. The Dominion Platform should
be assessed as part of 175's enterprise-value strategy, not only as a marketing
or delivery wrapper.

The Andersen relationship is tied to Sidera, an Andersen member firm, and is
dependent on the Sidera relationship. Dominion Partners should seek additional
Andersen allies without damaging that relationship, including through other
Canadian Andersen member or collaborating firms and Andersen growth segments
such as energy or pharma.

Sidera wants Dominion Partners to do trade remedies work on North American
files. That lane is acceptable in principle, but Sidera does not currently have
North American files and 175 / ML1 does not yet have deep trade remedies
experience. The relationship is valuable because the Sidera principal is a
former ML1 classmate who has become highly successful in Brazil.

Sidera is owned by the Saldanha family. It was founded by Mr. Saldanha and has
been grown by his daughter. Ms. Saldanha is married to Mr. Ures. Mr. Saldanha,
Ms. Saldanha, and Mr. Ures are wealthy, highly skilled, and formidable
collaborators.

They have extensive C-suite relationships with Brazilian industry, especially
agri-food, as well as European and, to some extent, North American investors
and traders into Brazil.

Dominion Partners needs to identify an offering that is repeatable for 175,
linked to Canada, seen as valuable by Sidera, and within international trade,
because Sidera's relationship to Andersen hinges on developing an International
Trade Services Line.

The five Dominion / 175 service lines are:

- trade remedies
- market access
- data centers
- mining
- payment services

Each service line should be positioned clearly before being advanced.

Current offering work:

- `CANADA_TRADE_READINESS_MARKET_DIAGNOSTIC.md` — product for foreign
  manufacturers, exporters, investors, distributors, and industry groups
  evaluating or expanding Canadian trade activity.
- `GLOBAL_TRADE_DIVERSIFICATION_MARKET_ACCESS_DIAGNOSTIC.md` — companion
  product for Canadian manufacturers, distributors, exporters, investors, and
  industrial groups evaluating international expansion, sourcing
  diversification, or non-U.S. market development.

Current platform-level work includes improving `dominionpartners.ca` and
developing Dominion Partners branding to maximize credibility and Andersen
synergy, subject to what the collaborating firm agreement permits and the risk
of overreliance on the Andersen brand. 175 is also considering whether renting
or leasing space for Dominion Partners would increase brand value.

### Commercial Infrastructure Requirements

**Per-offer pipeline and coverage:**
Each offering (Canada market entry; Canadian trade diversification away from
US) requires its own pipeline, SDR function, and account manager. These are
not shared across offers — each audience, channel, and Andersen relationship
lane is sufficiently distinct to require dedicated commercial coverage.

**Rates schedule:**
175 requires a rates schedule. A rates schedule is a prerequisite for serious
client and partner conversations, for the Andersen collaborating firm
relationship, and for any SDR or account manager to operate credibly. The
rates schedule should cover both offers and should reflect 175's positioning
as an advisory firm, not a commodity provider.

### Entity Ownership

All assets owned and controlled by 17513721 Canada Inc, to be registered as
Dominion Partners.

### Brand and Domain Hierarchy

| Brand | Domain | Role |
|---|---|---|
| Dominion | dominionpartners.ca | Branding and intake for enterprise clients |
| FlowSignal | flowsignal.dominionpartners.ca | Intelligence layer |
| D-AirPay | d-airpay.dominionpartners.ca | Monetization / payments execution |
| FinSure | finsure.dominionpartners.ca | Payment Services Consulting Line subdomain: home page, STR report landing page, FINTRAC readiness lead-magnet landing page, and portal access to the STR product |

---

## 2. Functional Layering (System View)

```
Dominion (Root)
   ↓
FlowSignal (Intelligence / Distribution Layer)
   ↓
D-AirPay (Execution / Payments Layer)
```

### Layer Roles

**Dominion**
- Narrative and positioning layer
- Intake for enterprise clients

**FlowSignal**
- Market intelligence
- Partner and introducer interface

**D-AirPay**
- Payments execution layer
- Rails abstraction (fiat and stablecoin)

---

## 3. Repository Architecture

```
repos/
├── dominion
├── flowsignal
├── d-airpay
└── finsure
```

### Rules

- Each repo is an independent deployable unit
- No uncontrolled code duplication across repos
- Shared logic must be explicitly modularized:

```
packages/
├── ui
├── auth
└── types
```

---

## 4. Deployment Architecture (Vercel)

Each repo is deployed as a separate Vercel project.

| Repo | Vercel Project | Domain |
|---|---|---|
| dominion | dominion | dominionpartners.ca |
| flowsignal | flowsignal | flowsignal.dominionpartners.ca |
| d-airpay | d-airpay | d-airpay.dominionpartners.ca |
| finsure | finsure | finsure.dominionpartners.ca |

### DNS Configuration

| Record | Type | Value |
|---|---|---|
| @ | A | 76.76.21.21 |
| www | CNAME | cname.vercel-dns.com |
| flowsignal | CNAME | cname.vercel-dns.com |
| d-airpay | CNAME | cname.vercel-dns.com |
| finsure | CNAME | cname.vercel-dns.com |

---

## 5. Control Layer Requirements

To avoid system drift:

- Single DNS authority
- Single Vercel team / account
- Consistent environment variable naming
- Centralized secret management

---

## 6. Platform Decision

**Option A — Independent Apps (current direction)**

- No shared authentication
- No shared data layer
- Simple linking between products

---

## 7. Operational Principles

- Treat Dominion as intake for enterprise clients, not just a website
- Treat FlowSignal as distribution engine
- Treat D-AirPay as monetization infrastructure
- Avoid mixing responsibilities across repos
- Maintain clear separation between:
  - narrative (Dominion)
  - intelligence (FlowSignal)
  - execution (D-AirPay)

---

## 8. FinSure Web / Product Model

FinSure is the product / demand-generation subdomain for the HBP-011 Payment
Services Consulting Line, operated under 17513721 Canada Inc.

FinSure sits under the Dominion Platform as a subdomain:
`finsure.dominionpartners.ca`. The root Dominion site (`dominionpartners.ca`)
remains the 175 / Dominion enterprise brand and service-line gateway; FinSure is
the focused payment-services compliance product surface.

**Required subdomain structure:**

```
finsure.dominionpartners.ca
   ├── home page / product overview
   ├── STR report landing page
   │      ↓
   │   portal access
   │      ↓
   │   STR product inside authenticated portal
   └── FINTRAC effectiveness review readiness landing page
          ↓
       lead magnet
          ↓
       paid AML Effectiveness Review Readiness Assessment
```

**Product layers:**
- Home page: explains FinSure and routes users to the two entry points
- STR report landing page: explains and routes to the paid FinSure STR report product
- Portal access: authenticated client area; the STR product lives inside the portal
- Lead-magnet landing page: hosts **Is Your MSB Ready for FINTRAC Effectiveness
  Review?** and converts to a paid consultation offer
- Paid consultation: AML Effectiveness Review Readiness Assessment

**HBP-011 service ladder:**

```
Entry point 1 — FinSure STR report
Entry point 2 — FINTRAC readiness lead magnet / paid consultation offer
   ↓
Tier 1 — FinSure STR report, consulting only
   ↓
Tier 2 — Rhizome white label (HBP-010)
   ↓
Tier 3 — Managed compliance, no CAMLO provision
   ↓
Tier 4 — CAMS operational consulting
   ↓
Tier 5 — Licensing support
   ↓
Tier 6 — CAMLO sourcing
```

**Governance note:** HBP-011 tiers 1-6 are non-legal 17513721 Canada Inc
services. Levine Law monthly / quarterly review and fractional counsel are
separate referral pathways, not part of the 175 service ladder. Any
cross-entity referral requires ML1 authorization per engagement.

**Confirmed decisions:**
- Portal authentication: shared via Dominion `packages/auth` module across FinSure and dominionpartners.ca (confirmed 2026-05-03)
- DNS target: `finsure.dominionpartners.ca` as a Vercel-hosted subdomain using
  CNAME to `cname.vercel-dns.com`

**Open questions:**
- Whether the existing finsure-w321.onrender.com build migrates directly or is rebuilt — TBD
- Whether the STR report landing page and FINTRAC readiness lead-magnet landing
  page live in one FinSure app as routes or as separate Vercel projects under
  the same subdomain — TBD

**Governing project:** HBP-011 (Payment Services Consulting Line)

---

## Relationship to Prior Structure

The prior recorded structure (as of 2026-04-25) had a two-lane model:
- Lane 1: referral introductions to providers (Interpolitan, KwiikPay)
- Lane 2: FinSure as entry product at `finsure.dominionpartners.ca`

The three-tier Dominion / FlowSignal / D-AirPay architecture supersedes that model.
FinSure is now retained as the HBP-011 payment-services subdomain inside the
Dominion Platform, with two entry points: FinSure STR report and FINTRAC
effectiveness review readiness lead magnet / paid consultation offer.
