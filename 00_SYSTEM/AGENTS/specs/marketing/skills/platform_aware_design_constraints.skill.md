---
id: mkt_skill_platform_aware_design_constraints
title: Platform-Aware Design Constraints Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, platform, thrive, wordpress, feasibility]
---

# Skill: Platform-Aware Design Constraints

## Purpose
Validate every design decision against Thrive Architect's capabilities before
recommending it. Prevent designs that are fragile, unsupported, or create
maintenance burden in the target CMS.

## Inputs
- Proposed design elements or patterns
- Platform: Thrive Architect + WordPress (default)

## Process
For each proposed design element:
1. Identify the closest native Thrive Architect element.
2. Assess: is the desired behavior achievable natively? (YES / PARTIAL / NO)
3. If PARTIAL: what Custom CSS is required? Is it maintainable?
4. If NO: is there a JS path? Is it within scope?
5. Flag patterns that are fragile (depend on Thrive internal classes that may
   change, or require complex JS not supported by Thrive).
6. Recommend a simpler, system-friendly alternative if the primary is not feasible.
7. Prefer patterns that become reusable Symbols or Content Templates.

## Known Thrive Architect constraints
- Complex CSS animations: limited native support; use sparingly via Custom CSS
- Multi-level dropdown menus: not natively supported in Thrive nav; use
  WordPress menu with CSS
- Sticky sidebars: not natively supported; complex CSS required
- Masonry grid: not native; requires Custom CSS or JS plugin
- Infinite scroll: not native; requires plugin
- Real-time filtering / search: not native; requires plugin or custom JS
- Video backgrounds: supported but increases page weight; use sparingly
- Parallax: available in Content Box background settings; test on mobile

## Outputs
- Per-element feasibility table: element / native support / CSS path / alternative
- List of patterns avoided and why
- Recommended system-friendly alternatives

## Constraints
- No design decision proceeds to wireframe production if it is not feasible in
  the target platform and no implementation path exists.

## Invocation
Used during UI pattern selection and wireframe production for every page.
