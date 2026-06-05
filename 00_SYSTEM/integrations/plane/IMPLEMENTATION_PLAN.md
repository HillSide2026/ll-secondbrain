---
id: 00_system_integrations_plane_implementation_plan
title: Plane Integration Implementation Plan
owner: ML1
status: draft
created_date: 2026-06-05
last_updated: 2026-06-05
tags: [plane, integration, implementation-plan]
---

# Plane Integration Implementation Plan

## Existing Repo Conventions

Projects are stored as project packets, primarily under `04_INITIATIVES`.
Typical project folders include frontmatter-bearing Markdown artifacts such as:

- `README.md`
- `PROJECT_CHARTER.md`
- `PROJECT_PLAN.md`
- `APPROVAL_RECORD.md`
- `METRICS.md`
- `RISK_REGISTER.md`
- phase folders such as `planning/` and `executing/`

Matter-like work lives under `05_MATTERS` and uses matter files such as
`MATTER.yaml`, `MATTER_BRIEF.md`, `ISSUES_AND_POSITIONS.md`, and
`NOTES_TO_FILE.md`.

There is no universal ticket folder convention across projects. Therefore the
Plane integration must use explicit project-local mappings.

## Smallest Fitting Integration

1. Keep Plane as the source of truth for ticket state, assignee, priority,
   labels, cycle, and project.
2. Store only Markdown snapshots in this repo.
3. Require an explicit mapping from Plane project to repo project folder.
4. Write snapshots into a configured ticket directory inside the mapped project.
5. Skip unmapped Plane projects with clear warnings.
6. Never create repo project folders from Plane.
7. Preserve manual sections starting at `## Links`.

## Current Implementation

- Mapping file: `00_SYSTEM/integrations/plane/project-map.json`
- Sync script: `scripts/sync-plane-tickets.ts`
- NPM command: `npm run sync:plane`
- Workflow: `.github/workflows/sync-plane.yml`

Each mapping supplies:

- Plane project key: `plane_project_id`, `plane_project_slug`,
  `plane_project_name`, or `plane_project`
- Repo project folder: `project_path`
- Project-relative ticket output folder: `ticket_dir`

Configured `ticket_dir` folders may be created inside existing mapped projects.
That is intentional and explicit. Unmapped Plane projects are not written.

