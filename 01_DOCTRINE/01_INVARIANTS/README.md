---
id: 01_doctrine__01_invariants__readme_md
title: Invariants (Level 1)
owner: ML1
status: draft
version: 1.0
created_date: 2026-02-13
last_updated: 2026-03-08
tags: [doctrine, invariants]
---

# Invariants (Level 1)

Definition:
An Invariant is a structural property that must remain true for the system to remain coherent and valid.
This is the system constitution layer.

Characteristics:
- Architectural, not interpretive.
- Rarely changed.
- Violation breaks system integrity.
- Requires formal amendment to modify.
- Higher than Policies.
- If something conflicts with an invariant, the other thing is wrong.

Boundary:
Invariants do NOT:
- Govern behavior within workflows.
- Describe quality posture.
- Define enforcement routines.
- Replace Policies.

Classification:
- If a rule governs behavior, it belongs in Policies.
- If it defines enforcement logic, it belongs in Protocols.
- If it defines interpretive posture, it belongs in Principles.

Typical examples in the ML1/ML2/LL model:
- ML1 retains final judgment authority.
- ML2 is a system of record, not an autonomous actor.
- LL consumes only ML1-approved outputs.
- System decisions and changes must be auditable.
