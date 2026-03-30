---
id: PRN-021
title: Layer Separation by Design
owner: ML1
status: active
version: 1.1
created_date: 2026-03-08
last_updated: 2026-03-28
tags: [principle, architecture, layering]
applies_to: [ML2, System, LL, HillSide]
---

# PRN-021 - Layer Separation by Design

Title: Layer Separation by Design

Statement:
Design workflows so governance decisions, enforcement logic, execution tasks, and integration transport remain separable and auditable. A change in one layer should not silently rewrite obligations in another.
Where Matter Administration and Matter File Administration both operate, they must remain distinct but linked layers; one may inform the other, but neither should silently absorb the other's role.

Rationale:
Separated layers improve auditability, reduce unintended coupling, preserve governance integrity during change, and prevent matter-state logic from being mistaken for Matter File authority.

Supersedes: None
Version: 1.1
Status: Active
