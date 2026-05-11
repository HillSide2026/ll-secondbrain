---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_010_rhizome_white_label__executing__workplan_md
title: Rhizome White Label - Executing Workplan
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-05-11
tags: [rhizome-white-label, executing, workplan]
---

# IMPLEMENTATION WORKPLAN

Project ID: `HBP-010`
Project Path: `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-010_RHIZOME_WHITE_LABEL`
Stage: `Executing`

## Objective

Execute the approved Rhizome services-led wrapper path (Option C: Technical Service Provider / clean perimeter model) without drifting into FinSure product work or payment services delivery execution.

## EW-01 — Commercial Structure (LOCKED 2026-04-25)

**Model:** Technical Service Provider (Option C, clean perimeter)

| Party | Role |
|---|---|
| PSP / MSB (Client) | Buys and uses compliance software |
| FinSure (us) | Commercial front-end: sell, onboard, support |
| Rhizome | Software provider: rules engine, monitoring, case management |

**Contract stack:**
- FinSure ↔ PSP: SaaS agreement
- FinSure ↔ Rhizome: white-label / OEM agreement
- No other contractual layer

**Non-negotiables:**
- No funds flow
- No onboarding decisions
- No AML decisioning
- No linkage to payment economics

## EW-02 — Control Boundary (LOCKED 2026-04-25)

| Area | Owner |
|---|---|
| PSP customer relationships | PSP |
| KYC / onboarding | PSP |
| AML decisions / reporting | PSP |
| Transaction authorization | PSP |
| Compliance tooling | Rhizome |
| Alerts / flags | Rhizome |
| Software onboarding + L1 support | FinSure |

**Rule:** FinSure provides tools only. PSP makes all decisions.

## EW-03 — Economics Guardrails (PARTIALLY RESOLVED 2026-05-11)

Rhizome OEM cost structure is now known (see below). Outstanding item is
FinSure's client-facing markup and bundling structure.

Required before contract execution:
- Minimum acceptable per-PSP fee (TBD — FinSure markup not yet set)
- No-go triggers on unit economics (TBD)

**Rhizome OEM cost to FinSure (rhizomecompliance.com/pricing — retrieved 2026-05-11):**

The published site pricing is the OEM cost basis for FinSure. FinSure is responsible
for marking up and bundling when selling to clients. All tiers listed in USD;
Canadian businesses receive a currency discount. Pricing is per-report volume,
monthly billing.

Included at all tiers: rules + AI transaction monitoring, sanctions screening,
automated STR/SAR/CTR/LVCTR reporting, unlimited user seats, audit logs,
encrypted vault, managed cloud hosting, unlimited API access.

| Rhizome Tier | Volume | OEM cost (USD/month) |
|---|---|---|
| 1 | 0–50 reports | $350 (~$7.00/report) |
| 2 | 51–100 reports | $600 (~$6.00/report) |
| 3 | 101–200 reports | $900 (~$4.50/report) |
| 4 | 201–1,000 reports | $1,750 (~$1.75/report) |
| 5 | 1,001–3,000 reports | $2,900 (~$0.96/report) |
| 6 | 3,001–5,000 reports | $4,500 (~$0.90/report) |

Enterprise self-hosting and custom development available at separate pricing.
A la carte module pricing available on request. 30-day refund guarantee.

**FinSure client-facing pricing (CAD/month — mid-market, confirmed 2026-05-11):**

Rhizome's 6 volume tiers are consolidated into 3 FinSure tiers. All prices in CAD.
Rhizome costs are in USD; FX exposure exists and should be monitored.

| FinSure Tier | Report volume | Rhizome OEM (USD/mo) | OEM in CAD (~1.38) | **FinSure price (CAD/mo)** | Gross margin |
|---|---|---|---|---|---|
| Starter | 0–50 reports | $350 | ~$485 | **$999** | ~52% |
| Growth | 51–200 reports | $600–$900 | ~$830–$1,245 | **$1,999** | ~38–60% |
| Scale | 201–1,000 reports | $1,750 | ~$2,415 | **$3,999** | ~40% |

**Onboarding fee:** An onboarding fee exists as a service line but is currently waived.
Should be defined and activated before significant volume is onboarded.

**Outstanding:** No-go triggers on unit economics not yet defined. Growth tier high-end
margin (~38%) is the tightest — watch if USD/CAD moves adversely.

## EW-04 — Dependency Protection (LOCKED 2026-04-25)

- PSP can integrate multiple tools (non-exclusive)
- FinSure supports multiple PSPs (no concentration risk)
- Data export and portability guaranteed
- No single PSP exceeds 25% of revenue

## EW-05 — Implementation Sequence (LOCKED 2026-04-25)

| Window | Tasks |
|---|---|
| Week 0–2 | Lock perimeter language in contracts; finalize PSP-facing SaaS terms |
| Week 2–6 | Integrate with 1 PSP (pilot) |
| Week 6–10 | Validate usability and alert quality |
| Week 10–12 | Roll out to additional PSPs |

## Control Notes

- `HBP-010` is about Rhizome wrapper structure and execution, not service-delivery execution.
- FinSure product work and payment services delivery remain outside this project packet.
- Any move into client-service delivery or CAMLO execution should be handled in `HBP-011` or a later delivery project.
- dominionpartners.ca is the shared public front-end for this service line.

## Change Log

- 2026-03-20 — Workplan created; execution priorities authorized
- 2026-04-25 — EW-01, EW-02, EW-04, EW-05 locked per ML1 working parameters; EW-03 flagged as outstanding
- 2026-05-11 — Rhizome OEM cost basis recorded in EW-03; FinSure client-facing pricing set (Starter $999, Growth $1,999, Scale $3,999 CAD/month); onboarding fee noted as waived; FX exposure flagged; no-go triggers remain outstanding
