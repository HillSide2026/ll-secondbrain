---
id: LLPRO-005
title: Client Economics Audit Protocol
owner: ML1
status: draft
version: 1.0
effective_date: 2026-06-08
policy: LLPOL-001, LLPOL-004
supersedes:
provenance:
  decided_by: ML1
  decided_on: 2026-06-08
  context: Implements periodic per-client realized contribution assessment implied by LLPRN-019 and LLPRN-021
created_date: 2026-06-08
last_updated: 2026-06-08
tags: [protocol, ll, client, economics, audit, quarterly, portfolio]
---

# LLPRO-005 — Client Economics Audit Protocol

**Trigger:** Quarterly.

---

## Purpose

Assesses each active client's realized contribution to identify high-return, low-return, and negative-return relationships. Feeds portfolio selectivity decisions and intake filter adjustments.

---

## Steps

**Step 1 — Pull per-client data for the review period.**

For each active client, compile:

| Dimension | What to assess |
|---|---|
| Realization rate | Billed vs. collected over the quarter |
| Collections velocity | Average days to collect |
| Scope discipline | Number of scope expansions; number absorbed without additional retainer |
| Customization burden | Degree of bespoke work vs. standard scope delivery |
| Concentration | Client's share of total firm revenue |

**Step 2 — Classify each client.**

| Classification | Criteria |
|---|---|
| Retain and invest | High realization, fast collections, clean scope, standard delivery |
| Retain and monitor | Adequate economics; one or more flags requiring attention |
| Price correction required | Scope or realization degrading; reprice at next renewal or matter opening |
| Exit or refer | Below-ICP economics confirmed; transition plan required |

**Step 3 — Generate portfolio-level view.**
Count clients in each classification. Note any concentration risk. Assess whether the portfolio distribution is moving toward or away from the operating model target.

**Step 4 — Record decisions.**
For each client classified as price correction or exit, document the planned action and timeline. For retain-and-monitor clients, document the specific flags and review triggers.

---

## Outputs

- Per-client economics summary with classification
- Portfolio-level distribution (how many clients in each tier)
- Decisions: price corrections, exit or referral plans, intake filter adjustments

---

## Related Doctrine

- LLPRN-019 (Client-Level Earnings Variability)
- LLPRN-021 (Portfolio Selectivity Over Client Count)
- LLPRN-023 (Collections Are Economic Discipline)
- LLPOL-001 (Firm Self-Interest)
- LLPOL-004 (Below-ICP Exception — exit decisions may trigger review of prior exceptions)
- LLPRO-004 (KPI Dashboard Review Protocol — monthly complement to this quarterly audit)
