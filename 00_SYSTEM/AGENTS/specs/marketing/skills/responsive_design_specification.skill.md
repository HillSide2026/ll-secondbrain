---
id: mkt_skill_responsive_design_specification
title: Responsive Design Specification Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, responsive, mobile, breakpoints, thrive]
---

# Skill: Responsive Design Specification

## Purpose
Define mobile-first responsive behavior for every section and component, in
terms that Thrive Architect's responsive controls can implement directly.

## Inputs
- Desktop wireframe spec (section and component definitions)
- Breakpoints: 768px (tablet/mobile), 480px (small mobile)
- Platform: Thrive Architect

## Process
1. Start from 375px mobile layout.
2. Define what changes at each breakpoint:
   - Column stacking (2-col → 1-col, etc.)
   - Font size scaling
   - Padding/margin reduction
   - Image sizing or reordering
   - Visibility toggles (show desktop-only / mobile-only elements)
   - Navigation collapse (hamburger)
   - Card grid reflow (2×3 → 1×6, etc.)
3. Map each responsive change to a Thrive Architect control (Responsive Padding,
   Responsive Font Size, Responsive Visibility, etc.).
4. Flag any responsive behavior not achievable natively — provide Custom CSS.

## Outputs
- Per-section responsive spec with all changes at 768px and 480px
- Thrive Architect control mapping for each change
- Custom CSS for any non-native responsive behavior

## Constraints
- Mobile-first: 375px is the baseline. Desktop is enhancement.
- Every responsive change must be achievable in Thrive's responsive system or
  via documented Custom CSS.

## Invocation
Used after wireframe production, before handoff to MKT_THRIVE_THEMES_AGENT.
