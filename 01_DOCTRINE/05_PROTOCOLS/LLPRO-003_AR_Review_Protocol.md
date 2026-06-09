---
id: LLPRO-003
title: A/R Review Protocol
owner: ML1
status: draft
version: 1.0
effective_date: 2026-06-08
policy: LLPOL-005, LLPOL-001
supersedes:
provenance:
  decided_by: ML1
  decided_on: 2026-06-08
  context: Implements the monthly collections review obligation; enforces LLPOL-005 aging thresholds
created_date: 2026-06-08
last_updated: 2026-06-08
tags: [protocol, ll, collections, ar, receivables, monthly]
---

# LLPRO-003 — A/R Review Protocol

**Trigger:** Monthly — first week of each month.

---

## Purpose

Implements the monthly A/R review obligation. Ensures aging thresholds defined in LLPOL-005 are checked and acted on before receivables drift past recovery.

---

## Steps

**Step 1 — Pull and age all open receivables.**
List every open invoice by client and matter. Calculate days outstanding from invoice date.

**Step 2 — Apply LLPOL-005 thresholds.**

| Age | Required action |
|---|---|
| 30+ days | Issue payment reminder |
| 45–60 days | ML1 direct client contact; assess collectability |
| 60+ days | ML1 decision: demand letter, payment arrangement, or write-off |

**Step 3 — Process write-off or arrangement approvals.**
Any write-off or payment arrangement identified in Step 2 requires ML1 approval per LLPOL-005. Document outcome at the matter level.

**Step 4 — Calculate firm-level aging metrics.**
Compute average A/R days across all open receivables. Compare to target (under 45 days). Note any KPI breach for the monthly dashboard review (LLPRO-004).

---

## Outputs

- Monthly A/R aging report (client, matter, age, status)
- Escalation actions taken
- Write-off or arrangement approvals documented at the matter level
- Aging metric for KPI dashboard

---

## Related Doctrine

- LLPOL-005 (A/R Aging Policy)
- LLPOL-001 (Firm Self-Interest)
- LLPRN-023 (Collections Are Economic Discipline)
- LLPRN-024 (KPI-Governed Scaling — A/R days target)
- LLPRO-004 (KPI Dashboard Review Protocol — receives aging metric)
