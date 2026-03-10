---
id: mkt_skill_canva_design_instantiation
title: Canva Design Instantiation Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, design, canva, mcp]
---

# Skill: Canva Design Instantiation

## Purpose
Create draft Canva designs from approved template slots through governed integration adapters.

## Inputs
- Selected template slot
- Design brief
- Integration adapter configuration

## Process
1. Validate adapter availability and permission scope.
2. Invoke Canva create-design workflow via approved tool interface.
3. Bind initial template and create draft design object.
4. Capture returned design identifiers and links.

## Outputs
- Draft Canva design record
- Design ID and URLs
- Initial creation log

## Constraints
- No direct external API calls outside approved adapters.
- Created asset must default to draft status.
- Failure must surface as structured error output.

## Invocation
Used when creating first-pass design artifacts in Canva.

