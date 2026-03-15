---
id: 01_doctrine__03_policies__project_policy_md
title: Repository Project Policy
owner: ML1
status: draft
version: '1.0'
created_date: 2026-03-15
last_updated: 2026-03-15
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

## 6. Stage-Gate Authority

No project stage advancement is valid without explicit ML1 approval recorded in
project artifacts.

Required gate sequence:

- `Initiating -> Planning`
- `Planning -> Executing`
- `Executing -> Closing`

ML2 may draft artifacts, structure options, and prepare packets.
ML1 alone decides stage advancement.

## 7. Canonical Baseline Artifact Set

### Stage 1 - Initiating

Required (all projects):

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

Required (strategic projects only):

- `BUSINESS_CASE.md`

### Stage 2 - Planning

Required:

- `SCOPE_DEFINITION.md`
- `WORKPLAN.md`
- `ASSUMPTIONS_CONSTRAINTS.md`
- `DEPENDENCIES.md`
- `RISK_REGISTER.md`
- `COMMUNICATION_PLAN.md`
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
- `METRICS.md` is the single canonical measurement artifact.

## 9. Relation to Other Stage Systems

This project delivery-stage policy is distinct from:

- roadmap stage/phase numbering governed by
  `01_DOCTRINE/01_INVARIANTS/DOCTRINE-CORE-0004-stage-phase-numbering.md`
- matter stages governed by
  `01_DOCTRINE/03_POLICIES/DOCTRINE-MATTERS-0001-matter-stages.md`
- register-level decision lifecycles used for portfolio triage or screening

These systems must not be collapsed into one stage vocabulary.

## 10. Related Artifacts

- `01_DOCTRINE/01_INVARIANTS/DOCTRINE-PROJECTS-0001-project-structural-boundaries.md`
- `01_DOCTRINE/03_POLICIES/FIRM_PROJECT_POLICY.md`
- `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/PROJECT_ARTIFACT_POLICY.md`
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0002-project-risk-artifact-lifecycle-policy.md`
