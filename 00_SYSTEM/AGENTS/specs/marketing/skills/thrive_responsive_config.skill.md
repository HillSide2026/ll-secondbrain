---
id: mkt_skill_thrive_responsive_config
title: Thrive Responsive Configuration Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, responsive, mobile]
---

# Skill: Thrive Responsive Configuration

## Purpose
Define per-element responsive settings in Thrive Architect to implement the
mobile-first responsive behavior specified in the wireframe spec.

## Inputs
- Responsive design spec (from MKT_UX_DESIGN_AGENT)
- Page wireframe spec with all sections and elements

## Process
For each section and element with responsive changes:
1. Identify the Thrive Architect responsive control to use:
   - Columns: set to "Stack on Mobile" checkbox in Thrive column settings
   - Padding/margin: use Responsive Padding (device icon in Thrive editor)
   - Font size: use Responsive Font Size (device icon in Thrive typography settings)
   - Visibility: use "Hide on Mobile" / "Hide on Desktop" toggle per element
   - Image width: set max-width via responsive padding or CSS override
2. Specify the exact value for each breakpoint (desktop / tablet / mobile).
3. For any responsive behavior not achievable natively: produce CSS override
   using thrive_css_override skill.

## Outputs
Per-element responsive configuration table:
- Element → Desktop value → Tablet (768px) value → Mobile (480px) value →
  Thrive control or CSS path

## Constraints
- Mobile behavior must be defined for every section.
- Do not leave responsive behavior to chance — specify it explicitly.

## Invocation
Used as part of every Thrive build packet, after wireframe spec is complete.
