---
id: 00_system_integrations_plane_readme
title: Plane Integration
owner: ML1
status: draft
created_date: 2026-06-05
last_updated: 2026-06-05
tags: [plane, integration, tickets, sync]
---

# Plane Integration

Plane is the source of truth for ticket status, assignee, priority, labels,
cycle, and project. This repository stores Git-versioned Markdown snapshots of
Plane tickets inside mapped project folders.

## Mapping Rule

The sync never creates project folders from Plane. Each Plane project must be
explicitly mapped in `project-map.json`.

If a Plane project is unmapped, the sync skips it and logs a warning.

Each mapping must provide:

- `plane_project_id`, `plane_project_slug`, `plane_project_name`, or
  `plane_project`
- `project_path`: an existing detected project folder in this repository
- `ticket_dir`: a repo-project-relative output directory for Plane snapshots

The `ticket_dir` may be created inside the mapped project, but only because it
is explicitly configured.

Example:

```json
{
  "projects": [
    {
      "plane_project_id": "replace-with-plane-project-id",
      "plane_project_name": "Granville",
      "project_path": "04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-013_SALE_OF_GRANVILLE",
      "ticket_dir": "executing/plane"
    }
  ]
}
```
