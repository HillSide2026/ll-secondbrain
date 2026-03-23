---
id: POL-055
title: Repository Project Policy
owner: ML1
status: draft
version: '1.1'
created_date: 2026-03-15
last_updated: 2026-03-23
tags: [doctrine, policy, projects, stage-gates]
---

# Repository Project Policy

## 1. Purpose

This policy is the repository-level canonical source for governed project
stages, stage-gate rules, and baseline project artifact requirements.

All project policies below this layer must be explicitly subsidiary to this
policy.

## 2. Scope

This policy applies to all repo-governed:

- strategic projects
- management projects
- operational projects
- decision projects

This policy does not apply to legal matter stages, which remain governed by
matter doctrine.

Project ontology and structural boundaries are defined in:

- `01_DOCTRINE/01_INVARIANTS/DOCTRINE-PROJECTS-0001-project-structural-boundaries.md`

## 3. Policy Hierarchy

Subsidiary project policies may exist for a firm, portfolio, or program, but
they must:

- explicitly declare themselves subordinate to this policy
- inherit the canonical project delivery stages from this policy
- preserve ML1 stage-gate authority from this policy
- preserve the required baseline stage artifacts from this policy unless a
  higher-order doctrine explicitly changes them

Subsidiary policies may add narrower or stronger constraints, but they may not
silently replace the repo-level stage model.

## 4. Canonical Delivery Stages

The canonical project delivery stages are:

1. `Initiating`
2. `Planning`
3. `Executing`
4. `Closing`

Rules:

- `Monitoring` is not a separate project stage.
- Monitoring and reporting artifacts belong inside `Executing`.
- `Implementation` is a deprecated project stage label and must not be used as
  the canonical stage name going forward.
- Historical references to `Implementation` or `Monitoring` should be treated
  as legacy until migrated.

## 5. Decision Lifecycle Is Separate

Delivery stages must not be confused with register-level decision tracking.

Where needed, a separate decision lifecycle may be used for project register
management, for example:

- `idea`
- `screening`
- `validating`
- `modeling`
- `deciding`
- `approved`
- `rejected`

Decision lifecycles do not replace delivery stages.

`Decision Project` is a project type, not a substitute for register-level
decision tracking.

## 6. Stage-Gate Authority

No project stage advancement is valid without explicit ML1 approval recorded in
project artifacts.

Required gate sequence:

- `Initiating -> Planning`
- `Planning -> Executing`
- `Executing -> Closing`

ML2 may draft artifacts, structure options, and prepare packets.
ML1 alone decides stage advancement.

## 6a. Project Identity Rule

Every project governed by this policy must have a globally unique Project ID.

- **Format:** `LLP-NNN` (e.g. `LLP-024`), where NNN is a zero-padded integer.
- **Project ID equals folder name.** The folder slug and the Project ID are the same string. There is no separate registry sequence.
- **Global uniqueness.** The number must be unique across the entire repository — not per portfolio area. Before creating a new project folder, verify the number is unused across all existing LLP-NNN folders.
- **Deprecated format.** The year-prefixed format `LLP-YY-NN` (e.g. `LLP-26-24`) is retired and must not appear in any new artifact. Existing occurrences must be corrected on next edit.
- `PROJECT_CHARTER.md` must declare the Project ID in the header.
- `APPROVAL_RECORD.md` must repeat the same Project ID.

## 7. Canonical Baseline Artifact Set

### Stage 1 - Initiating

Required for strategic, management, and operational projects:

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

Required (strategic projects only):

- `BUSINESS_CASE.md`

Required (decision projects only):

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

For decision projects, `PROJECT_CHARTER.md` should explicitly state:

- what exactly is being decided
- which real options are under consideration
- which criteria will be used to evaluate those options

Optional for decision projects, only if ML1 wants them:

- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`

### Stage 2 - Planning

Required for strategic and management projects:

- `SCOPE_DEFINITION.md`
- `PROJECT_PLAN.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `COMMUNICATION_PLAN.md`
- `METRICS.md`

Required for operational projects:

- `SCOPE_DEFINITION.md`
- `PROJECT_PLAN.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `METRICS.md`

Optional for operational projects, only when the project actually needs them:

- `ASSUMPTIONS_CONSTRAINTS.md`
- `COMMUNICATION_PLAN.md`

Required (decision projects only):

- `DECISION_FRAME.md`
- `PROJECT_PLAN.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `METRICS.md`

### Stage 3 - Executing

Required:

- `EXECUTION_LOG.md`
- `DECISION_LOG.md`
- `CHANGE_LOG.md`
- `ISSUE_LOG.md`
- `DELIVERABLES_TRACKER.md`
- `QA_CHECKLIST.md`
- `STATUS_REPORT.md`
- `KPI_DASHBOARD.md`
- `VARIANCE_REPORT.md`
- `RISK_UPDATES.md`
- `STAKEHOLDER_UPDATES.md`

### Stage 4 - Closing

Required:

- `DELIVERABLE_ACCEPTANCE.md`
- `LESSONS_LEARNED.md`
- `POST_EXECUTION_REVIEW.md`
- `FINAL_STATUS_REPORT.md`
- `ARCHIVE_INDEX.md`

## 8. Planning Discipline

Planning exists to support execution readiness, not planning for planning's
sake.

Rules:

- Planning artifacts must be project-specific.
- Planning artifacts must help lock scope, dependencies, controls, or gate
  readiness.
- Abstract or duplicative planning artifacts should be merged or removed.
- `PROJECT_PLAN.md` is the canonical planning-sequence artifact for strategic,
  management, operational, and decision projects. Existing `WORKPLAN.md` files
  are legacy-compatible during transition and should be normalized on next edit.
- `METRICS.md` is the single canonical measurement artifact. The split-file schema (`METRIC_DEFINITION.md`, `MEASUREMENT_METHOD.md`, `BASELINE_CAPTURE_PERIOD.md`, `VALIDATION_REVIEW.md`) is non-compliant and deprecated. Existing projects using the split schema must consolidate into `METRICS.md` before their Planning → Executing gate is closed. New projects must not use the split schema.
- `ML1_METRIC_APPROVAL.md` is deprecated and non-compliant. ML1 threshold approval belongs inside `METRICS.md`, not in a separate file.
- Decision projects should use the lightest planning packet that still supports
  the ML1 decision at hand.
- For decision projects, `PROJECT_PLAN.md` is the canonical consolidated
  planning artifact and should absorb scope, framing, and sequencing content as
  needed without creating separate `SCOPE_DEFINITION.md` or
  `COMMUNICATION_PLAN.md` files by default.

Decision projects may close after ML1 reaches a go / hold / no-go decision, or
may be reclassified into another project type before material execution begins.

## 9. Relation to Other Stage Systems

This project delivery-stage policy is distinct from:

- roadmap stage/phase numbering governed by
  `01_DOCTRINE/01_INVARIANTS/DOCTRINE-CORE-0004-stage-phase-numbering.md`
- client engagement stages governed by
  `01_DOCTRINE/03_POLICIES/POL-052_Client_Engagement_Stage_Policy.md`
- register-level decision lifecycles used for portfolio triage or screening

These systems must not be collapsed into one stage vocabulary.

## 10. Related Artifacts

- `01_DOCTRINE/01_INVARIANTS/DOCTRINE-PROJECTS-0001-project-structural-boundaries.md`
- `01_DOCTRINE/03_POLICIES/POL-056_Firm_Project_Policy.md`
- `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/PROJECT_ARTIFACT_POLICY.md`
- `01_DOCTRINE/03_POLICIES/POL-063_Project_Risk_Artifact_Lifecycle_Policy.md`
