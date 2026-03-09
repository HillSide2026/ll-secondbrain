---
id: POL-034
title: Fulfillment Lifecycle Definition and Authority Boundary
owner: ML1
status: draft
version: 0.2
created_date: 2026-03-09
last_updated: 2026-03-09
tags: [policy, fulfillment, lifecycle, authority, gates]
---

# POL-034 — Fulfillment Lifecycle Definition and Authority Boundary

Policy Statement: Fulfillment is the governed administrative system that begins at Onboarding and ends at Closing. Fulfillment is not legal delivery and must operate within explicit gate, scope, and authority boundaries.

Terminology rule:
- `onboarding` is the canonical fulfillment-stage label.
- `conversion` is a marketing-stage label and is not a fulfillment stage.

Canonical fulfillment lifecycle:
1. Onboarding (`LLP-004`) — Fulfillment start (pre-signature setup and engagement packet control)
2. Opening (`LLP-005`) — Authorization-to-operational-readiness control
3. Maintenance (`LLP-006`) — Ongoing post-open administrative operations
4. Closing (`LLP-008`) — Fulfillment end-state (financial and record closure)

Cross-cutting fulfillment functions:
- Accounts (cross-cutting across `LLP-004`/`LLP-005`/`LLP-006`): money setup, billing controls, collections, trust/retainer controls
- Admin (`LLP-007`): fulfillment risk-management controls

Gate and status transition rules:
- Gate 1 (Qualified Lead) authorizes entry into Onboarding.
- Before signed engagement agreement: matter status must be `Pending`.
- Gate 2 (Engagement Signed) authorizes transition from Onboarding to Opening.
- Upon signed engagement agreement: matter status must transition to `Open`.
- Gate 3 (Matter Open) requires completion and approval of Opening controls before transition to Maintenance.
- No stage skipping is allowed.

Boundary rules:
- Fulfillment governs administrative execution only; it must not perform legal judgment, legal strategy, or substantive delivery decisions.
- Marketing ends at the end of Conversion per `POL-032` and `POL-033`; fulfillment begins at Onboarding.
- Maintenance outputs do not authorize doctrine changes or gate overrides.
- Closing may occur only after fulfillment closure preconditions are satisfied and explicitly approved under ML1 authority.

Authority rules:
- ML1 is the sole authority for gate advancement, exceptions, and boundary overrides.
- System/agent layers may enforce controls and produce diagnostics but may not self-authorize stage promotion.

Authority (Principles referenced): PRN-020, PRN-021, PRN-027, PRN-028
Enforcement expectation: Any run, artifact, or workflow that misclassifies fulfillment stages, skips gates, or performs out-of-scope legal-delivery actions is non-compliant and must be blocked or escalated to ML1.
Supersedes: None
Version: 0.2
Status: Draft
