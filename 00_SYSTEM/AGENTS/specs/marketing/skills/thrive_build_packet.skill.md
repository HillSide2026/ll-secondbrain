---
id: mkt_skill_thrive_build_packet
title: Thrive Build Packet Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, implementation, build-packet]
---

# Skill: Thrive Build Packet

## Purpose
Produce a complete, step-by-step Thrive Architect build packet for a page that
ML1 can execute directly in WordPress without ambiguity.

## Inputs
- Approved wireframe spec (from MKT_UX_DESIGN_AGENT)
- Element mapping (from thrive_element_mapping skill)
- Responsive spec
- Brand palette (POL-049) and typography scale

## Process
For each section of the page, in order:
1. Define the outer container: Content Box element with background color / image,
   padding (top / bottom / left / right), and any border or shadow.
2. Define inner layout: Columns element with column count, width split, gap,
   vertical alignment.
3. For each column, define every element from top to bottom with full config:
   - Element name (Thrive element type)
   - Content (exact copy or asset reference)
   - All visual settings: font / size / weight / color / alignment / spacing
   - Link target (if applicable)
   - Custom CSS Class (if CSS override needed)
4. Define Symbol usage (header, footer, any global element).
5. Define any Custom CSS blocks.
6. Define responsive overrides per element.
7. Produce WordPress page setup checklist.
8. State ML1 publish step explicitly.

## Build packet format
```
PAGE SETUP
  WordPress title / slug / parent / template / publish status / menu

SECTION: [id]
  Container: Content Box
    Background: [hex or palette ref]
    Padding: [T / B / L / R]
  Columns: [count] columns, [split], gap [px], align [top/center/bottom]
    Column [n]:
      [Element type]: [config...]
      [Element type]: [config...]

SYMBOL DEFINITIONS
  [Symbol name]: [element structure and config]

CUSTOM CSS
  [Selector] { [properties] }
  @media (max-width: 768px) { [selector] { [properties] } }

RESPONSIVE SETTINGS
  [Section/element]: [change at 768px] / [change at 480px]

WORDPRESS PAGE SETUP CHECKLIST
  [ ] items...

ML1 PUBLISH STEP
  [Human action required — explicit instructions]
```

## Outputs
- Complete Thrive Architect build packet in the format above

## Constraints
- Every element must be specified. No "configure as appropriate" — that is not
  a specification.
- All colors must come from POL-049 palette.
- ML1 publish step must be clearly marked and cannot be skipped.

## Invocation
Primary output skill for MKT_THRIVE_THEMES_AGENT.
