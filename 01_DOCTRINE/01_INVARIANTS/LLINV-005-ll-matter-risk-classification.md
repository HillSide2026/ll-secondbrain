---
id: LLINV-005
title: 'LLINV-005: LL Matter Risk Classification'
owner: ML1
status: approved
approved_by: ML1
approved_date: 2026-05-30
version: 1.0
created_date: 2026-05-30
last_updated: 2026-05-30
effective_date: 2026-05-30
supersedes:
provenance:
  decided_by: ML1
  decided_on: 2026-05-30
  context: First LL Invariants layer; LL-scoped view of INV-0014
tags: [invariant, ll, risk, matters, classification]
---

# LLINV-005 — LL Matter Risk Classification

**Invariant ID:** LLINV-005
**Status:** APPROVED
**Authority:** ML1

---

## 1. Purpose

Define the invariant rules for how risk is classified at the matter level for Levine Law. This is the LL-scoped application of INV-0013 (risk axes) and INV-0014 (classification rules) to legal matters specifically.

LL initiative risk is governed by POL-064 at the policy layer. This invariant defines the structural classification rules that POL-064 operationalizes.

---

## 2. Risk Axes That Apply to LL Matters

From INV-0013, two axes apply to legal matters:

| Axis | Applies to LL Matters | Definition |
|---|:---:|---|
| A. Economic Risk | Yes | Portfolio-level ratios: client concentration, A/R aging, decision-constrained revenue |
| B. Execution Risk (incl. Relationship) | Yes | Matter-level: complexity, regulatory exposure, external dependencies, novelty, client relationship signals |
| C. Operational Risk | Yes | Scope, schedule, delivery deadline pressure |
| D. Financial Risk | No | Project investment exposure — does not apply to legal matters |
| E. Strategic Risk | No | Firm direction and positioning — does not apply to individual legal matters |

---

## 3. Invariants

1. Every active LL matter must be assessable on Axes A, B, and C. No axis may be omitted.
2. Economic Risk (Axis A) is assessed at the portfolio level, not per matter. Its output informs matter prioritization but is not a matter-level score.
3. Execution Risk (Axis B) is assessed at the matter level. The matter's execution risk equals the maximum execution risk score across its active solutions.
4. Relationship signals are part of Execution Risk (Axis B). They are not a separate risk category for matters.
5. Every canonical risk statement for a matter must assign exactly one canonical category: `Scope`, `Schedule`, `Budget`, `Financial`, or `Strategic` (per INV-0014). Legacy labels are not permitted.
6. A risk statement must describe the exposure, not the mitigation. If a statement describes both, it must be split.
7. `Budget` risk at the matter level applies only where an explicit fee cap, fixed fee, or budget ceiling exists. Open-ended retainer matters do not carry Budget risk by default.

---

## 4. Matter Risk Traceability

Every matter risk artifact must answer:
- What is the risk
- Which category it belongs to
- Why that category applies
- Which matter it belongs to (by `matter_id`)

Risk statements without a traceable `matter_id` are not canonical.

---

## 5. LL Initiative Risk

LL initiatives (projects in the LL Portfolio) are governed by POL-064, which applies all five risk axes per INV-0013. LL initiatives are not legal matters and are not governed by this invariant.

---

## 6. Related Doctrine

- INV-0013 (Risk Model — full five-axis definition)
- INV-0014 (Risk Classification Invariants — labeling and decomposition rules)
- LLINV-004 (LL Business Risk — firm-level categories)
- POL-064 (Levine Law Initiative Risk Policy)
- POL-063 (Project Risk Artifact Lifecycle Policy)
