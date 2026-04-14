---
id: hbp-012-risk-scan
title: Risk Scan — HBP-012 — Info Product
owner: ML1
status: draft
created_date: 2026-04-14
last_updated: 2026-04-14
tags: [hillside, hbp-012, info-product]
---

# Risk Scan — HBP-012 — Info Product

## Risks

| # | Risk | Likelihood | Impact | Notes |
|---|---|---|---|---|
| R-01 | Production overrun — templates take >8 hours to clean up | Medium | High | ML1 is sole producer; no buffer. 48-hour launch window fails if production slips. |
| R-02 | No defined scalable traffic plan | High | Medium | Launch depends entirely on warm outreach (20 DMs + 2 community posts + 1 LinkedIn). After that window, there is no documented plan for continued sales. |
| R-03 | Price point untested | Medium | Medium | $197 may be above willingness-to-pay for early-stage founders who "can't afford counsel." This ICP has not been price-tested. |
| R-04 | GHL/Stripe setup friction | Medium | Medium | Multiple systems (GHL funnel, Stripe checkout, automated delivery) must work in sequence. Any failure blocks purchase or delivery. |
| R-05 | Legal positioning risk | Medium | High | Templates must be clearly sold as templates, not legal advice. If a buyer believes they are receiving personalized legal counsel, there is a professional responsibility and liability risk. Requires clear disclaimer on sales page and in product. |
| R-06 | ICP affordability mismatch | Medium | High | "Can't afford counsel" may also mean "can't afford $197." The ICP and the price point may be in tension. If conversion rate from warm outreach is low, this is the likely cause. |
| R-07 | Execution distraction | Low | Medium | 5–8 hours of production + funnel setup competes with Levine Law capacity. Tight timeline mitigates this but doesn't eliminate it. |
| R-08 | Upsell path unproven | Low | Low | Backend (contract review / retainer) is unproven and out of scope. Risk is low now but becomes relevant if a scale decision is made. |
| R-09 | Brand separation | Low | Medium | Template pack is sold under Matthew Holdings, not Levine Law. If buyers conflate the two and expect LL-level professional engagement, expectation management becomes necessary. |

## Critical Risk

**R-01 + R-02 together** are the highest combined risk: production delay collapses
the 48-hour window, and if warm outreach executes but doesn't convert, there is no
backup traffic source. These two risks together define the go/no-go condition for
the launch phase.

## Mitigations

| Risk | Mitigation |
|---|---|
| R-01 | Time-box production: if templates are not shippable in 8 hours, ship what is ready rather than delay launch |
| R-02 | Accept this constraint for Phase 1; treat it as a validation test, not a scalable launch — scale decision comes after |
| R-03 | If zero sales after full outreach, test $97 before abandoning product |
| R-04 | Test GHL + Stripe flow with a $1 test purchase before going live |
| R-05 | Add explicit disclaimer: "This product contains template documents for informational purposes only. It is not legal advice and does not create a lawyer-client relationship." |
| R-06 | Monitor conversion rate on outreach; if <5% respond and zero convert, revisit price before broader rollout |
