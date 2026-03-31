---
id: sla-002
title: Integrity Compliance Standards
owner: ML1
status: draft
version: 1.0
created_date: 2026-03-31
last_updated: 2026-03-31
applies_to: [ML2, System]
tags: [doctrine, sla, integrity, compliance, measurement]
---

# SLA-002: Integrity Compliance Standards

Measurable compliance thresholds for ML2 structural health. These are non-negotiable floors, not aspirational targets.

---

## Artifact Consistency Rate

**Definition:** % of playbooks and templates with no internal or cross-artifact conflicts.

**Standard:** No conflicting artifact pair may remain unresolved once detected. Detection triggers escalation under SLA-001 (Conflict Detection SLA).

---

## Version Traceability

**Definition:** % of outputs traceable to a versioned artifact.

**Standard:** 100%. Any output that cannot be traced to a versioned artifact is non-compliant regardless of output quality.

---

## Schema Compliance

**Definition:** % of new artifacts following approved naming and metadata rules.

**Standard:** All artifacts entering the system must pass schema validation before use. Non-compliant artifacts are not active artifacts.

---

## Drift Rate

**Definition:** % of LL outputs deviating from approved artifacts.

**Standard:** Drift must be detectable and flagged. Drift that is not flagged is a system failure — the output itself is a secondary concern.

---

> **Note:** These standards are measurable expressions of SLA-001. Measurement thresholds and reporting cadence are defined in `08_KPIs/`.
