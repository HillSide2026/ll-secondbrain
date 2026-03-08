---
id: inv-matter-model-structural
title: Matter Model Structural Invariants
owner: ML1
status: draft
version: 1.0
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [invariant, matters, model]
---

# Matter Model Structural Invariants (Binding Invariant)

## Invariant
The matter domain model is a structural contract. The following properties must remain true.

## Structural Rules
1. Matter is the economic/control container.
2. Solution is a child monetizable unit of a Matter.
3. Strategy is a child monetizable unit of a Matter.
4. Solution and Strategy are both Service types.
5. Service is an open-ended supertype; Solution and Strategy are required subtypes but do not exhaust all possible service forms.
6. `matter_id` is globally unique and immutable.
7. Every Solution must belong to exactly one valid `matter_id` (no orphan solutions).
8. Every Strategy must belong to exactly one valid `matter_id` (no orphan strategies).
9. A Matter has exactly one top-level `status`, with allowed values: `open`, `pending`, `closed`.
10. A Matter has exactly one `delivery_status`.
11. A Matter has exactly one `fulfillment_status`.
12. Canonical structured fields are source of truth; summaries and dashboards are derived views and must not override canonical fields.

## Boundary
This invariant defines structure and cardinality only. Policy documents define operational status vocabularies, transitions, and thresholds.
