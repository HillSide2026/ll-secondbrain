---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_001_wealth_management__planning__opening_balance_sheet_md
title: Wealth Management - Opening Balance Sheet
owner: ML1
status: active
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [wealth-management, planning, balance-sheet]
---

# Opening Balance Sheet

Project ID: `HBP-001`
Stage: `Planning`

## Planning Use

Use this file to document the opening consolidated balance-sheet view used by
the wealth plan. The purpose is decision usefulness, not false precision.

## Baseline Dates

- consolidated planning baseline anchor: `2026-03-23`
- current housing-planning liquidity input: `2026-04-03`

## Working Baseline Table

| Line Item | Classification | Working Value / Status | Evidence / Basis | Decision-Use Treatment |
| --- | --- | --- | --- | --- |
| High-interest savings account | `U1` unrestricted liquid | `CAD 900,000` reported by ML1 as at `2026-04-03` | ML1 direct planning input | counts toward liquid capital subject to reserve rules |
| Managed equities | `U2` market-valued near-liquid | `CAD 560,000` reported by ML1 as at `2026-04-03` | ML1 direct planning input | counts toward decision use only after valuation date, market volatility, and liquidation assumptions are acknowledged |
| `17513721 Canada Inc` bank account | `R1` entity-bound liquid | approximately `CAD 27,000` reported in the corporate bank account from YellowBricks sale proceeds | ML1 direct planning input, `HBP-002_CASH_FLOW`, and `17513721 Canada Inc` identity records | excluded from personal deployable-capital calculations unless deliberately distributed or otherwise released across the entity boundary |
| Cash and securities opening baseline | `U1/U2` liquid and near-liquid | first-pass consolidated baseline `CAD 1,600,000` as at `2026-03-23` | `METRICS.md` and `HBP-002_CASH_FLOW/README.md` | top-line planning anchor pending line-item reconciliation |
| `Levine Professional Corporation` equity (`Levine Law`) | `I1` illiquid strategic equity | valuation unresolved | internal ownership and performance records | excluded from deployable-capital calculations until valuation policy is locked |
| `17513721 Canada Inc` equity and other personally owned venture equity, excluding separately listed corporate cash | `I1` illiquid strategic equity | valuation unresolved | internal records | included in long-term wealth framing, excluded from housing budgets |
| Ontario MSB sale thesis | `C1` conditional asset | optimistic sale case exists; not realized | `HBP-002_CASH_FLOW/README.md` | carried at zero for deployable-capital decisions until realized or legally committed |
| YellowBricks residual close-out value | `C1` conditional / realized mix | slightly more than `CAD 27,000` already received into `17513721 Canada Inc`; any further value unresolved | `HBP-002_CASH_FLOW/README.md` | realized receipts count only if still liquid and uncommitted; unresolved remainder carried at zero |
| Federal MSB entity value | `I1/C1` illiquid / conditional | unresolved | internal records | carried at zero for deployable-capital decisions |
| Liabilities, taxes, and known obligations | `L1` liability | to be consolidated explicitly | accounting records and `HBP-002_CASH_FLOW` source mapping | must be deducted before any housing budget is treated as valid |

## Reconciliation Note

The current `CAD 1,460,000` personal liquid / near-liquid input as at
`2026-04-03` (`CAD 900,000` in a high-interest savings account plus
`CAD 560,000` in managed equities), plus approximately `CAD 27,000` in
`17513721 Canada Inc` from YellowBricks sale proceeds, and the `CAD 1,600,000`
opening consolidated baseline as at `2026-03-23` are not necessarily
contradictory. One is a more recent split of current holdings and the other is
a first-pass consolidated baseline that may include cash plus securities at a
different date and under a different boundary cut.

ML1 has confirmed personal ownership of `17513721 Canada Inc` and
`Levine Professional Corporation`. That ownership fact does not collapse the
entity boundaries for accounting or cash-flow treatment.

## Decision Rule

Housing budgets are not built from total baseline value. They are built from
unrestricted liquid capital after reserves, taxes, and committed obligations are
deducted.
