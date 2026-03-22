---
id: mkt_skill_ux_audit
title: UX Audit Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, audit, website, layout, conversion]
---

# Skill: UX Audit

## Purpose
Evaluate an existing page or wireframe against POL-051 hierarchy compliance,
layout quality, CTA logic, mobile behavior, content-to-layout fit, and brand
signal compliance.

## Inputs
- Page URL (for live site) or wireframe spec / HTML draft
- Page level (Level 1 / Level 2 / Level 3 per POL-051)

## Process
Evaluate per dimension:
1. POL-051 compliance: is the page doing the right job for its level?
2. Layout clarity: is hierarchy immediately scannable? Is there a clear primary,
   secondary, tertiary sequence?
3. CTA placement and routing: does the user know where to go next? Is the CTA
   correctly sized for the page level?
4. Mobile experience: does the layout degrade correctly on mobile?
5. Content-to-layout fit: too much text? Wrong container for content type?
6. Brand signal compliance: POL-050 signals present (judgment authority,
   systemized precision, calm competence)?
7. Accessibility: heading hierarchy, contrast, alt text, keyboard nav (summary;
   full check uses accessibility_audit_and_remediation skill).

## Outputs
- UX Audit Report: PASS / ISSUE / BLOCK per dimension
- Specific finding and recommended correction per issue
- Overall assessment: PASS / REVISE / BLOCK

## Constraints
- BLOCK if the page is violating POL-051 page role rules.
- ISSUE if the page is degrading UX without violating doctrine.
- PASS only if all dimensions clear.

## Invocation
Used when evaluating any existing or draft page before handoff or approval.
