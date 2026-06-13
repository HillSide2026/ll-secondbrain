---
id: llp-012_funnel2_fractional_counsel_pricing
title: Fractional Counsel Pricing Model — Funnel 2
owner: ML1
status: draft
created_date: 2026-04-02
last_updated: 2026-06-11
tags: [funnel-02, fractional-counsel, pricing, retainer]
---

# Fractional Counsel Pricing Model — Funnel 2

## Adopted Model

| Tier | Name | Price | Monthly Scope | Response | Target Client |
| --- | --- | --- | --- | --- | --- |
| V1 | Foundations | `CAD 1,500/month` | 2 hours — contract reviews, governance questions, employment basics, ad hoc advice calls | 48h | Stable SMB with low transaction volume |
| V2 | Active | `CAD 2,750/month` | 4 hours — ongoing contracts, shareholder matters, employment issues, corporate housekeeping, 1 priority matter/month | 24h | Growing business with regular legal needs |
| V3 | Growth | `CAD 4,500/month` | 7 hours — complex commercial contracts, equity arrangements, multi-party matters, active M&A or financing support | 24h | Business in active transition |

## Notes

- This file now adopts the tier structure already defined in
  `LLP-030/BUSINESS_PLAN.md` as the canonical downstream F02
  retainer model.
- Retainer pricing reflects the F02 ICP: Ontario businesses with at least
  CAD 5M annual cash flow, aligned with approved industry lanes,
  accountant/referral-sourced where possible, and willing to pay for an
  ongoing commercial legal relationship. Below-CAD-5M prospects should be
  routed toward monetizable information products where possible.
- Overage on all tiers is billed at the applicable hourly rate.
- Unused hours do not roll over.
- Minimum commitment is `3` months on all tiers.
- Stripe products for fractional counsel retainer tiers are not yet created.
  Configuration remains pending, but the pricing model itself is no longer
  treated as open.

## Relationship to F02-T01 Entry Offers

The F02-T01 (Corporate Health Check) tactical funnel has three distinct offers
at different price points. These are not tier variants of the same product —
they are structurally distinct offers. ML1 confirmed this distinction
2026-06-11.

| Offer | Price | Description |
| --- | --- | --- |
| Diagnostic | `~CAD 600` | Diagnostic product — default entry offer; ML1-confirmed 2026-06-11 |
| Consultation | TBC | Consultation offer — price to be confirmed |
| Implementation | TBC | Implementation offer — price to be confirmed |

Each offer requires its own Stripe product. Scope and deliverable definition
for each offer is an open item — see `TACTICAL_FUNNEL_MAP.md`.

## Relationship to Entry Offer

The fractional counsel retainer is the downstream revenue product that the
F02-T01 entry offers feed. A client who completes the Diagnostic or
Consultation and has identified remediation needs is a natural candidate
for an ongoing retainer relationship.

Immediate post-engagement conversion should prefer remediation work first.
Fractional counsel is a downstream relationship offer after trust is
established through findings and follow-on work.
