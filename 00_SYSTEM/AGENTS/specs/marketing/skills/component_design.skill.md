---
id: mkt_skill_component_design
title: Component Design Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, components, design-system, thrive]
---

# Skill: Component Design

## Purpose
Define a reusable UI component with all states, slots, sizing, color, typography,
responsive behavior, interaction behavior, and Thrive Architect implementation
path.

## Inputs
- Component type (card / accordion / button / tab / table / hero / etc.)
- Content that will fill this component
- Platform: Thrive Architect

## Process
1. Name the component and define its type.
2. Define all slots (icon, heading, body, link, image, CTA) with config per slot.
3. Define all states: default / hover / active / expanded / collapsed / mobile.
4. Define sizing: width, min-height, aspect ratios where relevant.
5. Assign colors per slot from POL-049 palette.
6. Define typography per element: font size / weight / line-height.
7. Define border, shadow, and border-radius.
8. Define responsive behavior at 768px and 480px.
9. Define interaction behavior per state.
10. Map to Thrive Architect elements: which element(s) implement this component,
    and what configuration is required.
11. Define ARIA requirements: roles, aria-expanded, keyboard nav.
12. Assess Symbol potential: can this become a Thrive Symbol or Content Template?

## Outputs
- Complete component spec with all fields above

## Constraints
- Every component must be feasible in Thrive Architect natively or via documented
  Custom CSS.
- Prefer designs that can be made into Thrive Symbols or Content Templates for
  reuse.

## Invocation
Used when a new reusable UI component is needed for the LL design system.
