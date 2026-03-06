---
id: 02_playbooks___registry__structure_policy_md
title: Playbook Structure Policy
owner: ML1
status: draft
version: 1.0
supersedes:
created_date: 2026-02-14
last_updated: 2026-03-05
tags: [policy, structure, playbooks]
---

# Playbook Structure Policy

## Definitions

Playbook:
- A repeatable workflow.
- Must include `README.md`, `metadata.yaml`, `steps.yaml`, and `acceptance.md`.

Asset:
- A reusable noun used by playbooks (schemas, rubrics, worksheets, taxonomies, log formats, reference).
- Stored under `02_PLAYBOOKS/_ASSETS/`.

## Placement

- Workflows live in:
  - `02_PLAYBOOKS/LL_OPERATIONS/`
  - `02_PLAYBOOKS/CONTRACTS/WORKFLOWS/`
  - `02_PLAYBOOKS/CORPORATE/WORKFLOWS/`
  - `02_PLAYBOOKS/FINANCIAL_SERVICES/WORKFLOWS/`
- Non-workflow material belongs in `02_PLAYBOOKS/_ASSETS/`.
- Indexes and policy live in `02_PLAYBOOKS/_REGISTRY/`.

## Taxonomy Categories

`core`, `substantive`, `execution`, and `system` are metadata categories, not directory names.

Required encoding:
- `metadata.yaml` must include `category`.
- Category values must use: `core`, `substantive`, `execution`, or `system`.

## Naming

- Direct children of `02_PLAYBOOKS/` use uppercase/underscore naming.
- Workflow folder names under service roots use `lowercase_snake_case`.
- No numeric prefixes inside `02_PLAYBOOKS/`.
- No stage markers in playbook names.
