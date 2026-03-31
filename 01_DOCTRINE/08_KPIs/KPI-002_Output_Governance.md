---
id: kpi-002
title: Output Governance KPIs
owner: ML1
status: draft
version: 1.0
created_date: 2026-03-31
last_updated: 2026-03-31
applies_to: [ML2, System, LL]
tags: [doctrine, kpi, governance, output, safety]
---

# KPI-002: Output Governance KPIs

These protect the boundary between ML2 and LL. If these rise, the system is losing control.

---

## Unauthorized Output Rate

**Definition:** Outputs used by LL without ML1 approval.

**Signal:** Any non-zero value is a governance failure. This is not a metric to optimize toward a target — it is a binary compliance indicator. Rising trend requires immediate escalation.

---

## Template Fidelity Score

**Definition:** Degree to which outputs match approved templates.

**Signal:** Declining fidelity means outputs are drifting from the approved artifact layer. Correlate with Drift Rate (SLA-002) to distinguish system error from template gaps.

---

## Exception Frequency

**Definition:** How often LL needs to escalate beyond system rules.

**Signal:** Rising frequency signals either (a) doctrine has gaps the system cannot resolve, or (b) the system is not surfacing relevant doctrine. Both require ML1 intervention — the cause determines the fix.
