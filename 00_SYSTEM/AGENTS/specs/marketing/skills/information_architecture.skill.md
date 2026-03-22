---
id: mkt_skill_information_architecture
title: Information Architecture Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, ia, website, structure, routing]
---

# Skill: Information Architecture

## Purpose
Define the hierarchy, relationships, and routing logic of pages within the LL
website in compliance with POL-051.

## Inputs
- Business goals for the page set
- Page level (Level 1 / Level 2 / Level 3 per POL-051)
- Existing page inventory (if auditing)
- User types / ICP

## Process
1. Read POL-051 to establish canonical page levels and role definitions.
2. Map each page to its correct level and role.
3. Define routing relationships: which Level 2 pages link to which Level 3 pages.
4. Identify gaps: Level 3 pages that do not yet exist but are needed.
5. Identify conflicts: pages doing the wrong job for their level.
6. Output IA diagram and routing rules.

## Outputs
- Text-based IA tree (Level 1 → Level 2 → Level 3)
- Routing table (source page → link text → target page)
- Gap list (missing Level 3 pages)
- Conflict list (pages violating their POL-051 role)

## Constraints
- Must comply with POL-051 hierarchy at all times.
- Level 2 pages route; Level 3 pages convert. Do not invert.

## Invocation
Used when designing or auditing any page set for LL website.
