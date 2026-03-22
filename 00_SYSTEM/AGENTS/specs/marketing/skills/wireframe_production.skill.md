---
id: mkt_skill_wireframe_production
title: Wireframe Production Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, wireframe, layout, design]
---

# Skill: Wireframe Production

## Purpose
Produce annotated, section-by-section wireframe specs for LL website pages
precise enough for MKT_THRIVE_THEMES_AGENT to build without ambiguity.

## Inputs
- Approved copy for the page
- Page type and level (POL-051)
- ICP and business goal
- Platform: Thrive Architect (default)
- Brand palette (POL-049) and signals (POL-050)

## Process
1. Read approved copy and identify sections.
2. Assign a layout type to each section (full-width / 2-col / card grid /
   accordion / table / etc.).
3. Define background, padding, and column structure for each section.
4. Map each content item to a named slot with element type, content, typography,
   color, sizing, and alignment.
5. Validate every element against platform feasibility (Thrive Architect).
6. Add responsive notes for each section (how it stacks / resizes at 768px).
7. Output the full annotated wireframe spec.

## Outputs
- Annotated wireframe spec: section-by-section with all slot definitions

## Constraints
- Every design decision must be feasible in Thrive Architect natively or via
  documented Custom CSS.
- Mobile-first: define mobile layout before desktop.
- No ambiguity allowed — every element must be specified.

## Invocation
Used for every new page build or redesign task.
