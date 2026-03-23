---
id: POL-056
title: Firm Project Policy
owner: ML1
status: draft
version: '1.1'
created_date: 2026-03-14
last_updated: 2026-03-23
tags: [doctrine, policy, projects, stage-gates]
---

# Firm Project Policy

## 1. Purpose

This policy is the Levine Law subsidiary project policy.

Canonical repository-level project stages, stage-gate rules, and baseline
artifact requirements are defined in
`01_DOCTRINE/03_POLICIES/POL-055_Repository_Project_Policy.md`.

This policy applies that repository-level project policy to Levine Law project
governance and defines the Levine Law-specific scope for its use.

## 2. Policy Hierarchy

`01_DOCTRINE/03_POLICIES/POL-055_Repository_Project_Policy.md` is the top-level project policy for
the repository.

This policy is explicitly subordinate to that repo-level project policy.

This policy may add Levine Law-specific application rules, but it may not
replace the canonical delivery stages, ML1 stage-gate authority, or baseline
artifact requirements defined at the repo level.

## 3. Scope

This policy applies directly to Levine Law strategic, management, and
operational projects.

This policy does not apply to HillSide project packets, which require their own
subsidiary portfolio-specific policy under the repo-level project policy.

This policy does not apply to legal matter stages, which are governed by
matter doctrine.

## 4. Adoption of Repo-Level Project Rules

Levine Law projects adopt the canonical repository-level project rules defined
in `01_DOCTRINE/03_POLICIES/POL-055_Repository_Project_Policy.md`, including:

- delivery stages: `Initiating`, `Planning`, `Executing`, `Closing`
- separation of delivery stages from register-level decision lifecycles
- ML1-only stage-gate advancement authority
- baseline stage artifact requirements
- planning-discipline rules

## 4a. Project Identity — Levine Law Application

Levine Law projects apply the repo-level Project Identity Rule (§6a of `POL-055_Repository_Project_Policy.md`) as follows:

- All LL Portfolio projects use the `LLP-NNN` format (e.g. `LLP-024`).
- The number is unique across the entire `04_INITIATIVES/LL_PORTFOLIO/` tree — not per portfolio area (not per `03_FIRM_OPERATIONS/`, `08_MARKETING/`, etc.).
- Before creating any new LL project folder, check the full list of existing `LLP-NNN` folders under `04_INITIATIVES/LL_PORTFOLIO/` to confirm the chosen number is unused.
- The deprecated `LLP-26-XX` year-prefixed format must not be used in any LL project artifact.

## 5. Levine Law Application Rules

For Levine Law specifically:

- project governance under this policy applies to Levine Law project packets and
  project-management structures under `04_INITIATIVES/LL_PORTFOLIO`
- LL client matters remain governed by matter doctrine, not project doctrine
- Levine Law project templates, summaries, and agent specifications must conform
  first to the repo-level project policy, then to this Levine Law subsidiary
  policy

## 6. Drift Control

If a Levine Law template, agent specification, README, or portfolio summary
conflicts with the repo-level project policy, the repo-level project policy
governs.

If a Levine Law-specific project artifact conflicts with this subsidiary policy,
this policy governs, subject always to the repo-level project policy.

## 7. Related Artifacts

- `01_DOCTRINE/03_POLICIES/POL-055_Repository_Project_Policy.md`
- `04_INITIATIVES/LL_PORTFOLIO/03_FIRM_OPERATIONS/PROJECT_MANAGEMENT/PROJECT_ARTIFACT_TEMPLATE.md`
- `00_SYSTEM/AGENTS/LLM-004_PROJECT_MANAGEMENT_AGENT.md`
- `01_DOCTRINE/03_POLICIES/POL-063_Project_Risk_Artifact_Lifecycle_Policy.md`
