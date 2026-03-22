---
id: mkt_skill_design_to_implementation_handoff
title: Design-to-Implementation Handoff Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, handoff, implementation, thrive]
---

# Skill: Design-to-Implementation Handoff

## Purpose
Produce a complete, unambiguous handoff packet for MKT_THRIVE_THEMES_AGENT
or MKT_WEBSITE_IMPLEMENTATION_AGENT to build the page without requiring
additional design decisions.

## Inputs
- All completed wireframe specs for the page
- All component definitions
- All responsive specs
- All interaction specs
- All accessibility audit results
- Platform feasibility validation

## Process
1. Verify all sections have wireframe specs.
2. Verify all components are defined with all states.
3. Verify all responsive behavior is specified.
4. Verify all interactions are specified.
5. Verify accessibility audit is complete with no open BLOCKs.
6. Compile the handoff packet in the standard format.
7. Review for completeness: flag any slot, section, or element that would require
   the implementation agent to make an undocumented design decision.

## Handoff packet format
- Page metadata: title / URL slug / level / purpose / ICP
- Section inventory: ordered list with IDs and purposes
- Per-section wireframe spec
- Component library: all reusable components
- Asset slot list: images and icons with dimensions and placeholder descriptions
- Color and typography reference from POL-049
- Responsive behavior summary
- Internal link map: all links, targets, anchor text
- CTA map: all CTAs, routing targets, button labels
- Accessibility notes and any open items
- Platform feasibility notes and Custom CSS blocks

## Outputs
- Complete design-to-implementation handoff packet document

## Constraints
- No open ambiguities allowed. If a decision has not been made, it must be
  flagged explicitly as an open item requiring ML1 resolution before build.
- Output status: draft, pending ML1 approval.

## Invocation
Used as the final step in UX design before handing off to implementation.
