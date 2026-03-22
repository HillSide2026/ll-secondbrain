---
id: mkt_skill_thrive_css_override
title: Thrive CSS Override Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, css, custom-styling]
---

# Skill: Thrive CSS Override

## Purpose
Produce Custom CSS for Thrive Architect elements when native Thrive controls
cannot achieve the required visual result.

## Inputs
- Element requiring CSS override (with description of the gap between native
  Thrive output and required result)
- Target selector (Thrive CSS class or Custom CSS Class added to element)
- Required visual properties

## Process
1. Identify the correct CSS selector:
   - Add a Custom CSS Class to the element in Thrive Architect (e.g. `ll-industry-card`)
   - Use `.ll-industry-card` as the selector
   - Or use Thrive's native `.tve_` class if stable (note: may change across
     Thrive updates — prefer Custom CSS Classes for stability)
2. Write the CSS properties to achieve the required result.
3. Write responsive overrides (`@media (max-width: 768px)`) where needed.
4. Specify where to enter the CSS:
   - Per-element: Thrive Architect element > Advanced > Custom CSS tab
   - Global: Thrive Dashboard > Global CSS or WordPress Customizer > Additional CSS
5. Note any Thrive-specific quirks that affect the CSS (e.g. specificity issues,
   inline style overrides).

## Outputs
- CSS block with selector, properties, and responsive overrides
- Entry location instructions (per-element or global)
- Notes on specificity or Thrive quirks

## Constraints
- Prefer Custom CSS Classes over Thrive internal selectors for stability.
- Test CSS on mobile before finalizing.
- Document all overrides so they can be maintained.

## Invocation
Used whenever a required visual result is not achievable with native Thrive
Architect controls.
