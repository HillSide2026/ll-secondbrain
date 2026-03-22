---
id: mkt_skill_thrive_symbol_design
title: Thrive Symbol Design Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, symbols, global-elements]
---

# Skill: Thrive Symbol Design

## Purpose
Define a Thrive Symbol (global reusable element) for components that appear
across multiple pages, so changes propagate site-wide without rebuilding.

## Inputs
- Component to be globalized (nav / footer / CTA strip / disclaimer / etc.)
- Pages where this Symbol will appear
- Content and configuration for the Symbol

## Process
1. Confirm the component should be a Symbol (appears on 2+ pages, changes
   should propagate site-wide).
2. Name the Symbol precisely (e.g. "LL_Global_Footer", "LL_CTA_Strip_Inquiries").
3. Define the element structure inside the Symbol (same format as build packet).
4. Define all content slots and their configuration.
5. List every page and template region where this Symbol will be assigned.
6. Document update behavior: changes to the Symbol propagate to all instances.
7. Produce creation instructions: how to create the Symbol in Thrive > Symbols,
   and how to insert it on each page.

## Outputs
- Symbol definition document:
  - Symbol name
  - Element structure and full configuration
  - Assigned pages / template regions
  - Creation and insertion instructions
  - Update behavior note

## Constraints
- Only globalize elements that are truly shared. Do not over-globalize — a
  Symbol update affects every page it appears on.

## Invocation
Used when designing nav, footer, or any recurring CTA or disclaimer strip.
