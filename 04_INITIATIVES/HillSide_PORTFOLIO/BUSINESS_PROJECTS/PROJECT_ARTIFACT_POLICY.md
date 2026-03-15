---
id: 04_initiatives__hillside_portfolio__business_projects__project_artifact_policy_md
title: HillSide Business Project Artifact Policy
owner: ML1
status: draft
created_date: 2026-03-15
last_updated: 2026-03-15
tags: [hillside, business-projects, stage-gates, artifacts]
---

# HillSide Business Project Artifact Policy

## Purpose

Define the HillSide-specific project artifact requirements for HillSide
business projects.

This policy is explicitly subsidiary to
`01_DOCTRINE/03_POLICIES/PROJECT_POLICY.md`.

It applies the repository-level project policy to HillSide business-project
packets and adds HillSide-specific packet rules where needed.

## Policy Hierarchy

`01_DOCTRINE/03_POLICIES/PROJECT_POLICY.md` is the repository-level canonical
project policy.

This HillSide policy may add narrower portfolio-specific rules, but it may not
replace the canonical project delivery stages, ML1 stage-gate authority, or
baseline artifact requirements defined at the repo level.

## Scope

This policy applies to:

- `04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-*`

This policy does not govern:

- entity folders outside `BUSINESS_PROJECTS`
- LL client matters
- non-project reference material

## Pre-Initiation Shells

A HillSide project may exist as a folder shell with only:

- `README.md`
- a project-register entry

This is acceptable while the project remains at `idea` or `screening`.

Once a project packet is started or a project is described as `Initiating`, the
required initiation artifact set must be represented explicitly. Missing items
should be shown as pending, not implied complete.

## Stage 1 - Initiating

Required stage-gate artifacts for all HillSide business projects in
`Initiating`:

- `PROJECT_CHARTER.md`
- `PROBLEM_STATEMENT.md`
- `SUCCESS_CRITERIA.md`
- `STAKEHOLDERS.md`
- `RISK_SCAN.md`
- `APPROVAL_RECORD.md`

Required for strategic projects only:

- `BUSINESS_CASE.md`

Supporting but non-gate artifacts:

- `README.md`
- working-capture files such as `IDEA_BACKLOG.md`

Supporting artifacts may coexist with the initiation packet, but they do not
replace required stage-gate artifacts.

## Stage-Gate Rule

Planning may begin only after ML1 records `Initiating -> Planning` approval in
`APPROVAL_RECORD.md`.

## Consistency Rule

If a project README lists initiation artifacts, that list should match this
policy.

If a project approval record tracks initiation progress, it should reflect this
policy's required artifact set rather than a shortened local variant.
