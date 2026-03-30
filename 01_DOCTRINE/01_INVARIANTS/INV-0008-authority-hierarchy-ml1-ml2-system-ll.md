---
id: INV-0008
title: 'INV-0008: Authority Hierarchy (ML1 / ML2 / System / LL)'
owner: ML1
status: approved
version: 2.0
created_date: 2026-01-04
last_updated: 2026-03-21
tags: [authority, governance, hierarchy]

effective_date: 2026-03-21
supersedes: INV-0008 v1.0 (formerly DOCTRINE-2026-002 v1.0) (2026-01-04)

provenance:
  decided_by: ML1
  decided_on: 2026-03-21
  context: Approved amendment separating ML2 record responsibilities from System runtime responsibilities and clarifying the downstream LL execution layer
---

---

# INV-0008 — Authority Hierarchy (ML1 / ML2 / System / LL)

**Invariant ID:** INV-0008
**Status:** APPROVED
**Effective:** 2026-03-21
**Authority:** ML1

---

## Purpose

This doctrine defines the **authority hierarchy** governing:

- ML1 (Matthew Levine)
- ML2 (the Second Brain system)
- System (runtime execution and enforcement)
- LL (Levine Law and its personnel)

Its purpose is to:
- Preserve human judgment and accountability
- Prevent delegation of authority to systems, tools, or runtime layers
- Ensure execution environments do not exceed approved scope

This doctrine is binding across the entire Second Brain ecosystem.

---

## The Authority Stack

Authority flows **downward** and never upward.

### 1. ML1 — Human Authority

ML1 (Matthew Levine) is the **sole source of judgment, authority, and accountability**.

ML1:
- Makes all final decisions
- Approves doctrine
- Resolves conflicts
- Grants or withholds permission

Authority **cannot** be delegated away from ML1.

---

### 2. ML2 — System of Record (Second Brain)

ML2 is a **non-autonomous system of record**.

ML2:
- Codifies ML1-approved decisions
- Preserves doctrine, standards, and workflows
- Maintains authoritative references, provenance, and structure
- Surfaces conflicts and gaps for ML1 review

ML2:
- Does **not** make decisions
- Does **not** exercise judgment
- Does **not** invent policy
- Does **not** act independently
- Does **not** perform runtime enforcement

ML2 exists to **preserve and apply** ML1’s decisions — not replace them.

---

### 3. System — Runtime Enforcement Layer

The System is the controlled runtime layer that **applies ML2 during execution**.

The System:
- Executes agents and orchestrations
- Applies doctrine during runtime
- Performs QC validation and drift detection
- Produces diagnostics and escalation signals

The System:
- Does **not** create doctrine
- Does **not** approve exceptions
- Does **not** interpret doctrine beyond explicit rules
- Does **not** autonomously modify ML2

---

### 4. LL — Execution and Distribution Layer

LL (Levine Law) is the downstream **human execution and market-facing distribution layer**.

LL:
- Executes work based on ML1-approved doctrine
- Uses artifacts produced from ML2-governed outputs
- Delivers authorized services within explicitly defined scope
- Generates operational signals from delivery and market interaction

LL:
- Does **not** create doctrine
- Does **not** modify doctrine
- Does **not** reinterpret doctrine
- Does **not** treat runtime outputs as authority unless approved and codified

Execution without approval does not create authority.

---

## Related Boundary

External suites and collaboration platforms are **not separate authorities** in the stack.

When they are **not integrated**, they remain outside the governed operating stack.

When they are **explicitly integrated**, they become governed **execution surfaces for the System through the Execution Bridge**.

Integration does not make them canonical and does not create a new authority layer.

Where integrations are used, authority still flows:

ML1 -> ML2 -> System -> LL

---

## Prohibited Authority Inversions

The following are explicitly prohibited:

- ML2 making discretionary decisions
- System creating doctrine or approving exceptions
- LL interpreting or extending doctrine
- Agents acting as decision-makers
- External platforms being treated as canonical authorities
- Repeated usage creating implied authority
- Automation substituting for approval

If an action requires judgment, it requires **ML1**.

---

## Conflict Resolution

In the event of conflict:

1. ML1 decisions override all systems and artifacts
2. Approved doctrine recorded in ML2 overrides playbooks, templates, and runtime behavior
3. ML2 preserves the canonical record but does not resolve conflicts
4. The System flags conflicts but does not resolve them
5. LL must escalate unresolved conflicts to ML1

No system may self-resolve authority conflicts.

---

## Enforcement

Any artifact, workflow, or behavior that violates this hierarchy is invalid.

Violations must be:
- Flagged
- Corrected
- Re-approved if necessary

This doctrine governs all future system design and usage.

---

## Relationship to Other Doctrine

- This doctrine operates **in conjunction with** INV-0007 (What Qualifies as Doctrine)
- This doctrine is the canonical authority stack referenced by runtime and portfolio doctrine
- Where ambiguity exists, ML1 judgment prevails
