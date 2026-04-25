---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_010_rhizome_white_label__executing__workplan_md
title: Rhizome White Label - Executing Workplan
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-04-25
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

## EW-03 — Economics Guardrails (OUTSTANDING)

Minimum acceptable commercial terms and effort assumptions not yet defined.

Required before contract execution:
- Minimum acceptable per-PSP fee
- Rhizome OEM cost structure and margin floor
- No-go triggers on unit economics

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
