---
id: mkt_skill_interaction_and_state_specification
title: Interaction and State Specification Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, interaction, states, animation, aria, thrive]
---

# Skill: Interaction and State Specification

## Purpose
Define precisely how every interactive UI element behaves across all states,
with ARIA requirements and Thrive Architect implementation path.

## Inputs
- List of interactive elements on the page (accordion, tabs, buttons, cards,
  nav, forms, hover effects)
- Platform: Thrive Architect

## Process
For each interactive element:
1. Define trigger (click / hover / scroll / focus / page load).
2. Define before state (visual and ARIA attributes).
3. Define transition (duration, easing, what changes).
4. Define after state (visual and ARIA attributes).
5. Define mobile / touch equivalent.
6. Define keyboard nav path (Tab order, Enter/Space behavior, Escape behavior).
7. Map to Thrive Architect implementation (native / Custom CSS / Custom HTML).
8. Flag any interaction not achievable in Thrive without JS — provide solution.

## Outputs
- Per-element interaction spec: trigger / before / transition / after / mobile /
  keyboard / ARIA / Thrive implementation

## Constraints
- ARIA attributes must be correct and complete (aria-expanded, aria-controls,
  role, aria-hidden as appropriate).
- Avoid animations that create accessibility barriers (respect prefers-reduced-motion).
- Only recommend JS-dependent interactions if a JS implementation path is
  provided.

## Invocation
Used for any page with interactive components: accordions, tabs, hover cards,
sticky nav, modals.
