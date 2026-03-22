---
id: mkt_skill_ui_pattern_selection
title: UI Pattern Selection Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, ui-patterns, components, thrive]
---

# Skill: UI Pattern Selection

## Purpose
Select the correct UI pattern for each content type, validated against Thrive
Architect platform feasibility and LL design system rules.

## Inputs
- Content type (list of issues / industry cards / comparison / FAQ / CTA / etc.)
- Number of items
- ICP and reading context (scanning vs. reading)
- Platform: Thrive Architect

## Process
1. Identify the content type and how users will consume it.
2. List candidate UI patterns for that content type.
3. Evaluate each candidate:
   - Clarity and hierarchy fit
   - Thrive Architect native support (YES / PARTIAL / NO)
   - Reusability (Symbol / Content Template potential)
   - Mobile behavior
4. Select the best pattern.
5. If primary is PARTIAL or NO in Thrive: define Custom CSS path or select
   alternative.
6. Document rationale.

## Outputs
- Selected pattern with rationale
- Thrive feasibility assessment
- Alternative if primary is not feasible
- Mobile behavior spec

## Constraints
- Do not recommend patterns that are fragile or unsupported in Thrive Architect
  without a clear Custom CSS path.
- Prefer patterns that can be made into reusable Thrive Symbols or Content
  Templates.

## Invocation
Used during wireframe production and component design for any new section or
content block.
