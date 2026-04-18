---
id: POL-054
title: Matter Summary Policy
owner: ML1
status: approved
approved_by: ML1
approved_date: 2026-04-18
version: 1.0
created_date: 2026-02-24
last_updated: 2026-03-28
tags: [policy, matters]

effective_date:
supersedes:

provenance:
  decided_by: ML1
  decided_on:
  context:
---

# Matter Summary Policy

**Document ID:** POL-054  
**Status:** DRAFT  
**Effective:** TBD  
**Authority:** ML1

---

## 1. Purpose

The Matter Summary is the canonical, compressed representation of a matter's current economic, status, delivery, fulfillment, risk, strategic, and ML1-decision state.

It exists to answer, in under 60 seconds:
- What is this matter?
- Why does it matter economically?
- What should remain visible to ML1?
- What, if anything, requires ML1 action now?
- Where is the risk?
- What tension does it create for the firm?

The Matter Summary is not a narrative memo. It is a structured state snapshot.

This policy consumes:
- `01_DOCTRINE/01_INVARIANTS/INV-0003-matter-model-structural-invariants.md`

## 2. Role in ML2

The Matter Summary:
- aggregates data from Matter, Solution, and Risk layers
- is the primary object consumed by dashboards
- is the primary briefing artifact for ML1
- is regenerated from canonical fields (not manually composed free-text)
- must be reproducible from structured state

It is the matter-level cognitive interface.

The Matter Summary must distinguish between:

- **ML1 visibility** — the facts ML1 should continue to see because the matter
  remains important, active, strategic, risky, or otherwise relevant
- **ML1 action** — the narrower set of matters where ML1 judgment, approval, or
  intervention is actually required now

Ordinary fulfillment handling must not be treated as ML1 action. Only
**fulfillment escalation** belongs in the ML1-action layer.

## 3. Design Principles

Deterministic Where Possible
- Revenue, state, aging, and ratios must be derived.

Opinionated but Bounded
- Limited short-form human judgment allowed (e.g., strategic significance).

No Redundant Narrative
- It references structured fields; it does not duplicate them.

Time-Stamped
- Every summary must have a generated_at timestamp.

Override Transparency
- If any matter status, delivery status, fulfillment status, or risk is manually overridden, that must appear in the summary.

## 4. Required Sections (Canonical Order)

### A. Identity Block
- matter_id
- matter_name
- client_name
- owner
- engagement_date
- matter_status
- delivery_status
- fulfillment_status

### B. Economic Snapshot
- est_total_value
- est_remaining_revenue
- amount_billed_to_date
- amount_collected_to_date
- ar_balance
- ar_age_bucket
- probability_weighted_pipeline_value (if pipeline present)

Purpose: show economic exposure and cash status.

### C. Solution Snapshot
- total_solutions
- active_solutions_count
- pipeline_solutions_count
- highest_value_solution_id
- next_solution_milestone

Purpose: show monetization structure.

### D. Control Snapshot
- matter_status
- engagement_stage
- delivery_status
- fulfillment_status
- days_in_engagement_stage
- next_ML1_decision_required
- decision_due_date
- decision_age_days
- blocking_actor (if any)
- inactivity_days

Purpose: show flow friction, decision pressure, and the difference between
visibility and action.

### D1. Control Snapshot Definitions

- `next_ML1_decision_required`
  - The next decision that actually requires ML1 judgment.
  - This is not the next task, next email, or next operational step.
  - If no ML1 decision is presently required, this field should be null.

- `decision_due_date`
  - The date by which the ML1 decision should be made under the applicable
    operational expectation or SLA.
  - This is the primary timeliness anchor for ML1 action.

- `decision_age_days`
  - How long the unresolved ML1 decision has been pending.
  - Useful for aging and breach detection, but secondary to
    `decision_due_date`.

- `blocking_actor`
  - The actor presently preventing material forward movement.
  - Examples: `ML1`, `client`, `counterparty`, `regulator`, `fulfillment`,
    `unknown`.

- `inactivity_days`
  - Days since the matter last had meaningful movement.
  - This is a drift signal only. It must not by itself imply that ML1 action is
    required.

### E. Risk Snapshot

Economic Risk:
- economic_risk_score_0_100
- economic_primary_driver (largest ratio driver)

Execution Risk:
- execution_risk_score_0_100
- execution_driver_solution_id

Relationship Risk:
- relationship_risk_flags (array)

Purpose: show instability concentration.

### F. Capacity Impact
- production_owner_load_ratio
- review_dependency (boolean)
- estimated_hours_remaining
- solutions_per_owner

Purpose: show human system load.

### G. Strategic Alignment
- client_strategic_tier
- matter_strategic_weight
- margin_band (if available)
- strategic_drift_flags

Purpose: show direction fit.

### H. Tension Summary (Short Text, Max 500 chars)

One structured sentence:

Format:
"This matter is [economic significance] and currently [ML1 visibility + action posture]. Primary tension: [risk/control/capacity driver]. Next leverage point: [decision/action]."

This is the only narrative field allowed.

## 5. Regeneration Rules

The Matter Summary must be recomputed on:
- matter_status change
- delivery_status change
- engagement_stage change
- fulfillment_status change
- solution_stage change
- billing update
- A/R aging update
- risk threshold breach
- daily snapshot run
- change to `next_ML1_decision_required`
- change to `decision_due_date`
- change to `blocking_actor`

Stored as:
- 05_MATTERS/<matter_id>/matter_summary.json, or
- central derived snapshot in `06_RUNS/state/`

Compatibility note:
- Current scaffolds also produce matter_summary.md in run outputs (see new_matter_scaffold).

Snapshotted in 06_RUNS during periodic firm-state runs.

## 6. Governance Rules

- No free-text editing of derived fields.
- Manual overrides must appear in override_reason and override_timestamp.
- Matter Summary is authoritative for dashboard display.
- If structured fields conflict with summary content, structured fields win.
- The Matter Summary must not collapse ML1 visibility into ML1 action.
- Fulfillment issues appear in the ML1-action layer only when they qualify as
  fulfillment escalation.
