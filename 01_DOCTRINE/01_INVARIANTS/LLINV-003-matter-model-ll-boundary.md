---
id: LLINV-003
title: 'LLINV-003: Matter Model — LL Boundary'
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
  context: First LL Invariants layer; LL-scoped view of INV-0003
tags: [invariant, ll, matters, model, boundary]
---

# LLINV-003 — Matter Model: LL Boundary

**Invariant ID:** LLINV-003
**Status:** APPROVED
**Authority:** ML1

---

## 1. Purpose

Define what is invariant about LL's relationship to the matter model. LL uses the matter model; it does not own or govern it. This invariant defines that boundary. The full structural definition of the matter model is in INV-0003.

---

## 2. LL's Relationship to the Matter Model

LL is a **consumer** of the matter model. Matters are the economic and operational containers through which LL delivers legal services.

LL does not define the matter model. Matter model structure, canonical fields, status vocabularies, and cardinality rules are owned by ML2 and governed by INV-0003.

---

## 3. Invariants

1. LL uses `matter_id`, `status`, `delivery_status`, `delivery_stage`, and `fulfillment_status` as defined by INV-0003. It does not define, extend, or rename these fields.
2. LL does not treat summaries, digests, or dashboards as authoritative matter records. Canonical structured fields govern.
3. LL does not redefine a matter's identity, status, or delivery classification through operational usage or external file mapping.
4. Every active matter that LL works on must have at least one Service (Solution or Strategy). LL does not operate on structurally incomplete matters.
5. LL generates matter-level operational signals (activity, progress, client response, billing status). These signals inform ML1 and the system but do not override canonical matter fields.
6. When LL receives a derived view of a matter (digest, action queue, dashboard), that view does not govern. The canonical MATTER.yaml governs.

---

## 4. What LL Controls

LL has operational authority within the matter delivery lifecycle:
- Moving a matter's `delivery_stage` through approved stage transitions (per POL-071 and PRO-016)
- Recording delivery activity, task completion, and billing events
- Generating signals for ML1 review

LL does not have authority to:
- Change `delivery_status` (tier) without ML1 direction
- Change `status` (open/pending/closed) without ML1 direction
- Add or remove Services without ML1 direction

---

## 5. Related Doctrine

- INV-0003 (Matter Model Structural Invariants — full definition)
- INV-0017 (Matter Identity Authority and Lifecycle)
- POL-071 (Matter Delivery Stage Policy)
- POL-043 (Clio Matter ID Structure)
