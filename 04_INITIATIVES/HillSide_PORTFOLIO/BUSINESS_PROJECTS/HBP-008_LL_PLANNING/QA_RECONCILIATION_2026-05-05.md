---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_008_ll_planning__qa_reconciliation_2026_05_05_md
title: LL Planning - QA Reconciliation 2026-05-05
owner: ML1
status: draft
created_date: 2026-05-05
last_updated: 2026-05-05
tags: [hbp-008, ll-planning, qa, reconciliation, 2027, 2028, 2029, hillside]
---

# QA Reconciliation 2026-05-05

**Project:** LL Planning
**Project ID:** HBP-008

## Scope

Reviewed the HBP-008 LL Planning packet for internal consistency after:

- renaming the folder from the narrower 2027 frame to `HBP-008_LL_PLANNING`
- adding 2028 and 2029 horizon artifacts
- adding the 2027 F02 Health Check targets
- adding the LL-side tax-adjusted corporate model

Files reviewed:

- `README.md`
- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `BUSINESS_CASE.md`
- `SUCCESS_CRITERIA.md`
- `METRICS.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `RISK_SCAN.md`
- `STAKEHOLDERS.md`
- `APPROVAL_RECORD.md`
- `REVENUE_MODEL.md`
- `ASSOCIATE_MODEL.md`
- `LL_RETAINED_PROFIT_MODEL_2026_2029.md`
- `LL_TAX_ADJUSTED_CORPORATE_MODEL_2026_2029.md`
- `ANNUAL_PLAN_2028.md`
- `ANNUAL_PLAN_2029.md`

## Reconciliation Actions Taken

### Project identity

- Normalized stale frontmatter IDs from `hbp_008_levine_law_2027` to
  `hbp_008_ll_planning`.
- Normalized 2028 and 2029 annual-plan frontmatter away from `llp_030_*`
  ownership into HBP-008 LL Planning ownership.
- Preserved LLP-030 as a source/reference layer, not the owner of the horizon
  artifacts.

### F02 targets

- Updated `PROJECT_CHARTER.md` so SG-06 now explicitly states the 2027 F02 goal:
  30 paid Corporate Health Checks and CAD 90,000 direct Health Check revenue.
- Reconciled `METRICS.md` so both F02 metrics map to SG-06 rather than orphan
  SG-08 / SG-09 references.
- Confirmed `SUCCESS_CRITERIA.md`, `METRICS.md`, and `REVENUE_MODEL.md` all
  carry the same F02 target.

### Retained-profit and tax boundary

- Updated `BUSINESS_CASE.md` so the CAD 155,000-160,000 retained-profit figure is
  described as pre-tax corporate retained earnings.
- Updated `SUCCESS_CRITERIA.md` so the retained-earnings success criterion is
  explicitly pre-tax.
- Updated `REVENUE_MODEL.md` to replace the prior HBP-001 wealth-plan framing
  with an HBP-008 corporate planning interface.
- Confirmed `LL_TAX_ADJUSTED_CORPORATE_MODEL_2026_2029.md` is the LL-side
  corporate-tax adjustment and does not model ML1 personal after-tax wealth
  outcomes.

### README packet map

- Updated `README.md` from three core goals to four core goals, adding F02's
  30 / CAD 90,000 baseline.
- Updated `README.md` from "two supplementary artifacts" to four model artifacts:
  `REVENUE_MODEL.md`, `ASSOCIATE_MODEL.md`,
  `LL_RETAINED_PROFIT_MODEL_2026_2029.md`, and
  `LL_TAX_ADJUSTED_CORPORATE_MODEL_2026_2029.md`.

## Numeric Reconciliation

### 2027 revenue model

| Item | Reconciled value |
|---|---:|
| ML1 planned billings | CAD 240,000 |
| Associate floor collections | CAD 100,000 |
| Associate target collections | CAD 160,000 |
| Total firm floor collections | CAD 340,000 |
| Total firm target collections | CAD 400,000 |
| Fixed revenue to ML1 | CAD 85,000 |
| Total revenue to ML1 | CAD 90,000-95,000 |
| F02 paid Health Checks | 30 |
| F02 direct Health Check revenue | CAD 90,000 |
| F03 specialist revenue target | CAD 30,000+ |

### Retained-profit / tax model

| Case | Pre-tax retained profit | After-tax deployable capital at 12.2% |
|---|---:|---:|
| 2027 floor, 30% retained-profit case | CAD 92,000-97,000 | CAD 80,776-85,166 |
| 2027 floor, 40% retained-profit case | CAD 126,000-131,000 | CAD 110,628-115,018 |
| 2027 target, 30% retained-profit case | CAD 110,000-115,000 | CAD 96,580-100,970 |
| 2027 target, 40% retained-profit case | CAD 150,000-155,000 | CAD 131,700-136,090 |

## Remaining Validation Items

These are not defects in the packet. They are external validation items:

- Q4 2026 HBP-007 actuals must be checked before HBP-008 planning is authorized.
- LLP-033 activation gate must be confirmed before associate execution.
- HBP-002 must align definitions for collections, revenue to ML1, and cash-flow
  reporting.
- Accountant must validate the LL corporate-tax model assumptions, including
  small-business deduction eligibility, associated-corporation effects, and
  whether retained profit maps cleanly to taxable income.
- ML1 must decide whether F02 downstream conversion targets should become formal
  2027 metrics or remain channel-quality indicators.

## QA Result

The packet is internally coherent for a draft HBP-008 LL Planning project after
the reconciliation above.

The main remaining risk is not internal contradiction. It is validation timing:
the project remains an initiating-stage planning surface until HBP-007 actuals,
LLP-033 activation conditions, HBP-002 definitions, and accountant tax treatment
are confirmed.
