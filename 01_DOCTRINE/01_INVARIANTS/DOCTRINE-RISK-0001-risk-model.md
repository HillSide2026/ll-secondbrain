---
id: DOCTRINE-RISK_MODEL-0001
title: Risk Model Doctrine (Economic, Execution, Operational, Financial, Strategic)
owner: ML1
status: draft
version: 1.0
created_date: 2026-02-24
last_updated: 2026-03-15
tags: [doctrine, risk]

effective_date:
supersedes:

provenance:
  decided_by: ML1
  decided_on:
  context:
---

# Risk Model Doctrine (Economic, Execution, Operational, Financial, Strategic)

**Document ID:** DOCTRINE-RISK_MODEL-0001  
**Status:** DRAFT  
**Effective:** TBD  
**Authority:** ML1

---

## 1. Purpose

Define a firm-wide risk model that:
- is computable from deterministic fields where possible
- separates economic instability from execution complexity and relationship degradation
- supports portfolio-level monitoring and matter-level prioritization
- avoids a single subjective risk number

## 2. Risk Axes

Risk is decomposed into five axes. Not all axes apply to all work types — see Section 6 for the mapping.

### A. Economic Risk (Derived — Portfolio Level)

Economic risk is computed from portfolio ratios. It is not manually scored.

Components (portfolio-level):
- Top-3 Client Concentration Ratio
- A/R Over-Threshold Ratio
- Decision-Constrained Revenue Ratio
- Low-Probability Pipeline Ratio
- Single-Matter Dependency Ratio

Economic Risk Score rules:
- weighted function of the above ratios
- weighting is explicit and stored as configuration
- ratios are normalized to 0-1
- score is stored as 0-100

Economic Risk is evaluated at:
- firm level (primary)
- optionally client level (same ratios within client portfolio)

### B. Execution Risk (Bounded, Partly Judgment-Based)

Execution risk is derived from solution-level fields that are bounded and auditable. Relationship signals are included here rather than as a separate axis.

Required solution fields:
- complexity_level (1-5)
- regulatory_exposure (low|med|high)
- external_dependency_count (integer >= 0)
- novelty_flag (boolean)

Relationship signals (per matter or per client):
- days_since_client_response
- open_invoice_days_outstanding
- discount_frequency_90d
- scope_disputes_90d
- expansion_rejections_180d

Execution Risk at Matter Level:
- matter execution risk equals the maximum execution risk score across active solutions within the matter
- active solution definition: solution_stage in {approved, in_production, client_review, awaiting_external}
- relationship signals are flagged when any signal breaches its threshold; they contribute to execution risk, not a separate score

### C. Operational Risk (Scope / Schedule / Budget)

Operational risk tracks delivery-level threats to bounded work. Applies to all project types and legal matters.

Components:
- Scope creep or undefined scope
- Schedule slippage or deadline pressure
- Budget overrun or cost uncertainty
- External dependency failures (vendors, integrations, counterparties)

### D. Financial Risk (Project Investment Level)

Financial risk tracks the firm's capital exposure to a specific project or initiative. Applies to strategic, management, and decision projects only.

Components:
- Project cost overrun vs approved budget
- ROI uncertainty or benefit realization risk
- Opportunity cost of resource allocation

### E. Strategic Risk (Direction and Positioning)

Strategic risk tracks whether the initiative remains aligned with firm direction and whether execution could create structural problems. Applies to strategic, management, and decision projects only.

Components:
- Strategy drift (project no longer serves original intent)
- Precedent risk (creating unintended firm-wide commitments)
- Dependency risk (project creates lock-in or cascading failure points)
- Competitive or market positioning exposure

## 3. Thresholds and Configuration

All thresholds are explicit, versioned, and adjustable:

Economic Risk (Axis A):
- AR_THRESHOLD_DAYS (e.g., 60)
- LOW_PROB_THRESHOLD (e.g., 0.4)
- DECISION_AGING_DAYS (e.g., 7/14)

Execution Risk — Relationship Signals (Axis B):
- CLIENT_RESPONSE_DAYS (e.g., 7)
- DISCOUNT_FREQ_LIMIT_90D (integer)
- SCOPE_DISPUTES_LIMIT_90D (integer)
- EXPANSION_REJECTION_LIMIT_180D (integer)

## 4. Governance Rules

- Economic Risk must be reproducible from stored data. No manual overrides.
- Execution Risk inputs may be human-entered but must be bounded and attributable to an owner and timestamp.
- Relationship Risk begins as signals and threshold flags; scoring is deferred until signals have sufficient history.
- All risk metrics must retain traceability: which matters and solutions contributed, and which thresholds and weights were used.

## 5. Outputs (Canonical)

The system produces:
- Firm Economic Risk Score (0-100)
- Firm Economic Risk Component Ratios (0-1)
- Matter Execution Risk Score (0-100) plus contributing solution_id
- Relationship Risk Flags (per signal, per matter or client)

---

## 6. Risk Axes by Work Type

This section defines which risk axes apply to each work type.

### Work Type Definitions

| Type | Description | Examples |
|---|---|---|
| Strategic Project | Long-horizon firm capability build. Novel, multi-stage, full governance. | LLP-001 through LLP-005 |
| Management Project | Internal firm ops and portfolio governance. Process/recurring. | Portfolio Management, Governance Audit |
| Operational Project | Bounded technical or integration build. Specific deliverable, time-limited. | SharePoint-Clio integration, Gmail governance |
| Decision Project | Bounded option-framing work intended to support a go / hold / no-go or reclassification decision. | Rhizome white-label evaluation, agency go/no-go framing |
| Legal Matter | Client delivery work. Governed by matter doctrine, not project doctrine. | All active matters in Clio |

### Risk Axes by Type

| Risk Axis | Strategic Project | Management Project | Operational Project | Decision Project | Legal Matter |
|---|:---:|:---:|:---:|:---:|:---:|
| A. Economic Risk | | | | | ✓ |
| B. Execution Risk (incl. Relationship) | | | | | ✓ |
| C. Operational Risk (scope/schedule/budget) | ✓ | ✓ | ✓ | ✓ | ✓ |
| D. Financial Risk | ✓ | ✓ | | ✓ | |
| E. Strategic Risk | ✓ | ✓ | | ✓ | |

## 7. Lifecycle Risk Artifacts and Gate Review (Policy Boundary)

Required lifecycle artifact schemas and stage-gate review requirements are defined in:
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0002-project-risk-artifact-lifecycle-policy.md`

This invariant remains limited to the risk model structure (axes, scoring boundaries, and output definitions).
