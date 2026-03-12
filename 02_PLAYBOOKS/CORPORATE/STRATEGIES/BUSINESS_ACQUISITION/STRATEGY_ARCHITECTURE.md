---
id: 02_playbooks__corporate__strategies__business_acquisition__strategy_architecture_md
title: Strategy Architecture: Business Acquisition
owner: ML1
status: draft
created_date: 2026-03-12
last_updated: 2026-03-12
tags: [business-acquisition, strategy-architecture]
---

# Strategy Architecture: Business Acquisition

---

## Architecture Summary

The Business Acquisition Strategy is a sequenced engagement architecture built around three invariant phases — LOI, Diligence, APA — with a fourth phase (Closing / Post-Closing) that is uniform across all S-Levels. Complexity and advisory depth scale with S-Level. The BUSINESS_ACQUISITION Tier 2 Solution (Levels 1 and 2) governs sub-$1M transactions and is a component reference at S-Level 1.

## S-Level Sequence Files

Detailed engagement sequences by S-Level are maintained in dedicated files:

| File | S-Level | Status |
|------|---------|--------|
| [S_LEVEL_1_SEQUENCE.md](S_LEVEL_1_SEQUENCE.md) | S-Level 1 ($1M–$2.5M, brokered) | Draft |
| S_LEVEL_2_SEQUENCE.md | S-Level 2 ($2.5M–$5M) | Not yet built |
| S_LEVEL_3_SEQUENCE.md | S-Level 3 ($5M–$7.5M) | Not yet built |
| S_LEVEL_4_SEQUENCE.md | S-Level 4 ($7.5M–$10M) | Not yet built |

---

## Invariant Phase Sequence

All S-Levels follow this phase order. No phase may be skipped.

```
Intake & Classification
       ↓
    LOI Phase
       ↓
  Diligence Phase
       ↓
   APA Phase
       ↓
Conditions & Closing
       ↓
   Post-Closing
```

---

## Phase Detail by S-Level

### Phase 1 — Intake & Classification

| Task | All S-Levels |
|------|-------------|
| Confirm deal size and engagement trigger (both conditions met) | ✓ |
| Classify S-Level | ✓ |
| Complete Required Inputs (see Solution Assembly reference) | ✓ |
| Flag all escalation conditions before proceeding | ✓ |
| Confirm advisory team composition for S-Level | ✓ |

---

### Phase 2 — LOI

| Element | S-Level 1 | S-Level 2 | S-Level 3 | S-Level 4 |
|---------|-----------|-----------|-----------|-----------|
| Non-binding status explicit | ✓ | ✓ | ✓ | ✓ |
| Key commercial terms (price, structure, payment) | ✓ | ✓ | ✓ | ✓ |
| Exclusivity period | Optional | ✓ | ✓ | ✓ |
| Conditions to closing (headline) | ✓ | ✓ | ✓ | ✓ |
| Binding provisions (confidentiality, exclusivity, costs) | Identified | ✓ | ✓ | ✓ |
| Diligence access provision | ✓ | ✓ | ✓ | ✓ |
| Break fee / cost provisions | — | Optional | ✓ | ✓ |
| Working capital reference | — | ✓ | ✓ | ✓ |
| Earnout framework (if applicable) | Optional | ✓ | ✓ | ✓ |

---

### Phase 3 — Diligence

| Diligence Area | S-Level 1 | S-Level 2 | S-Level 3 | S-Level 4 |
|----------------|-----------|-----------|-----------|-----------|
| PPSA searches | ✓ | ✓ | ✓ | ✓ |
| Corporate/title searches | ✓ | ✓ | ✓ | ✓ |
| Material contracts review | ✓ | ✓ | ✓ | ✓ |
| Lease review | ✓ | ✓ | ✓ | ✓ |
| Licence and permit inventory | ✓ | ✓ | ✓ | ✓ |
| Employee schedule review | ✓ | ✓ | ✓ | ✓ |
| Financial statements (3 years) — accountant | Instructed | ✓ | ✓ | ✓ |
| Tax status / CRA review | Basic | ✓ | ✓ | ✓ |
| Formal diligence request list | ✓ | ✓ | ✓ | ✓ |
| Diligence summary memo | Optional | ✓ | ✓ | ✓ |
| Operational / management review | — | — | ✓ | ✓ |
| IT / systems review | — | — | Optional | ✓ |
| Formal data room | — | — | — | ✓ |

---

### Phase 4 — APA

| APA Element | S-Level 1 | S-Level 2 | S-Level 3 | S-Level 4 |
|-------------|-----------|-----------|-----------|-----------|
| Lawyer-prepared APA | ✓ | ✓ | ✓ | ✓ |
| Standard reps and warranties | ✓ | ✓ | ✓ | ✓ |
| Survival period | 12–18 months | Negotiated | Negotiated | Negotiated |
| Indemnity | Standard | Basket + cap | Fully negotiated | Fully negotiated |
| Disclosure schedules | Basic | ✓ | ✓ | ✓ |
| Working capital adjustment | — | ✓ | ✓ | ✓ |
| Earnout schedule / agreement | If applicable | If applicable | If applicable | If applicable |
| VTB security instrument | If applicable | If applicable | If applicable | If applicable |
| Non-competition / non-solicitation | ✓ | ✓ | ✓ | ✓ |
| Transition services agreement | Optional | Optional | ✓ | ✓ |
| Management / consulting agreements | — | — | Optional | ✓ |
| Rep & warranty insurance | — | Consider | ✓ | ✓ |
| Tax and accounting covenants | — | ✓ | ✓ | ✓ |

---

### Phase 5 — Conditions & Closing

Standard across all S-Levels. Conditions tracked against closing checklist.

| Item | All S-Levels |
|------|-------------|
| Conditions satisfaction confirmation | ✓ |
| Closing agenda | ✓ |
| Authorizing resolutions (buyer and seller) | ✓ |
| Closing certificates | ✓ |
| Funds flow / closing statement | ✓ |
| PPSA discharges confirmed | ✓ |

---

### Phase 6 — Post-Closing

| Item | All S-Levels |
|------|-------------|
| Post-closing checklist | ✓ |
| Business licence (if required) | ✓ |
| Lease assignment confirmation | If applicable |
| CRA registrations | ✓ |
| Closing binder / file index | ✓ |
| Earnout monitoring (if applicable) | If applicable |

---

## Orchestration Logic

- The LOI phase is mandatory and must be completed before diligence commences
- Diligence findings may require LOI terms to be renegotiated — document any such reopening with a written amendment or side letter to the LOI
- The APA is drafted after diligence is substantively complete; no drafting before diligence at S-Levels 3–4
- Tax counsel must be engaged before APA is finalized at S-Levels 3–4
- At S-Level 4, assess co-counsel requirement before accepting the mandate

---

## Advisory Team by S-Level

| Advisor | S-Level 1 | S-Level 2 | S-Level 3 | S-Level 4 |
|---------|-----------|-----------|-----------|-----------|
| LL (corporate counsel) | ✓ | ✓ | ✓ | ✓ |
| Accountant / financial diligence | Client-led (LL advises to obtain) | ✓ | ✓ | ✓ |
| Tax counsel | — | Refer if flagged | ✓ (standard) | ✓ (standard) |
| Business broker / M&A advisor | Possible | Likely | ✓ | ✓ |
| Co-counsel (M&A specialist) | — | — | Assess | Assess |

---

## Entry → Core Progression

**Standard entry:** Client instructs on a target business. Intake confirms S-Level. LOI phase commences.

**Alternate entry — pre-signed LOI:** Client arrives with LOI already signed. Confirm LOI adequacy for the S-Level. If LOI is materially deficient for the deal size, advise client on gaps before proceeding to diligence.

**Alternate entry — existing client (additional service):** Client has completed a prior acquisition (e.g., BUSINESS_ACQUISITION Tier 2 Solution) and is now pursuing a second deal at Strategy level. Prior matter context is informative for conflict check and advisory continuity; each acquisition is a discrete engagement.
