---
id: 04_initiatives__ll_portfolio__05_matter_docketing__specs__matters_field_model_md
title: Matters Field Model
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Matters Field Model

## Core Rule

Each matter is represented using **THREE canonical fields**. These fields are
orthogonal and must not be conflated.

---

## The Three Fields

### 1. status (Clio Matter Status) — METADATA

| Attribute | Value |
|-----------|-------|
| Source of truth | Clio |
| Allowed values | `Open` \| `Pending` \| `Closed` |
| Meaning | The matter's canonical status in Clio |
| Storage | Metadata field in 00_META.md |

### 2. delivery_status (Lawyer Attention Priority) — DIRECTORY

| Attribute | Value |
|-----------|-------|
| Source of truth | ML1 / lawyer |
| Allowed values | `Essential` \| `Strategic` \| `Standard` \| `Parked` |
| Meaning | How much lawyer attention the matter deserves |
| Directory implication | Determines folder in 05_MATTERS/ |

### 3. fulfillment_status (Admin Workload State) — METADATA

| Attribute | Value |
|-----------|-------|
| Source of truth | Admin team / ops |
| Allowed values | `urgent` \| `active` \| `keep in view` \| `dormant` \| `closing` |
| Meaning | Admin workload state for the matter |
| Storage | Metadata field in 00_META.md |

---

## Secondary Operational Field

### fulfillment_stage (Operational Workflow Guide) — SECONDARY

| Attribute | Value |
|-----------|-------|
| Source of truth | Team workflow / governed operational handling |
| Typical values | `onboarding` \| `opening` \| `maintenance` \| `pending_close` \| `closed` |
| Meaning | Guides how the team should handle the matter operationally |
| Canonical standing | Secondary — useful operationally, but not one of the core canonical matter fields |

`fulfillment_stage` is allowed and useful for workflow guidance, handoffs, and
team coordination, but it must not be presented as a peer to the three
canonical matter fields.

---

## Directory Rule

05_MATTERS/ is organized by **delivery_status** only:

```
05_MATTERS/
├── ESSENTIAL/
├── STRATEGIC/
├── STANDARD/
└── PARKED/
```

status (Clio) and fulfillment_status (admin) are metadata fields within each
matter's `00_META.md`.

---

## Non-Inference Rule (Hard Constraint)

**You MUST NOT infer any field from any other.**

| Incorrect Inference | Why Wrong |
|---------------------|-----------|
| Parked → Pending or Closed | Parked is delivery priority, not Clio status |
| urgent → Essential | Admin workload ≠ lawyer priority |
| Closed → dormant | Clio status ≠ admin workload |
| Essential → urgent | Lawyer priority ≠ admin workload |
| fulfillment_stage → fulfillment_status | Workflow position ≠ admin workload state |

---

## Handling Missing Fields

If a field is missing:
1. Mark as `unknown`
2. Request ML1/admin input
3. **Do not guess**

---

## Output Format

When listing matters, present three fields separately:

```yaml
status: Open|Pending|Closed
delivery_status: Essential|Strategic|Standard|Parked
fulfillment_status: urgent|active|keep in view|dormant|closing
```

Secondary operational field when needed:

```yaml
fulfillment_stage: onboarding|opening|maintenance|pending_close|closed
```

Do not merge or rename the canonical fields. Do not treat `fulfillment_stage`
as a fourth canonical field.
