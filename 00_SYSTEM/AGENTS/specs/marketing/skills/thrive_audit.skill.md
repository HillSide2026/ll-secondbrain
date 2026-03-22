---
id: mkt_skill_thrive_audit
title: Thrive Audit Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, audit, compliance]
---

# Skill: Thrive Audit

## Purpose
Evaluate an existing Thrive-built page for compliance, correctness, and
implementation quality.

## Inputs
- Page URL or Thrive Architect export / screenshot
- Page level per POL-051

## Process
Evaluate per dimension:
1. **POL-051 compliance**: is the page doing the correct job for its level?
2. **POL-050 brand signal compliance**: judgment authority, systemized precision,
   calm competence present?
3. **POL-049 color compliance**: are all colors from the active palette?
4. **Layout and hierarchy**: is the visual hierarchy clear and correct?
5. **CTA and link routing**: do all CTAs and links go to correct targets?
6. **Responsive behavior**: does the page behave correctly on mobile? (check
   in Thrive responsive preview or browser DevTools)
7. **Symbol usage**: are shared elements implemented as Symbols or rebuilt
   redundantly?
8. **WordPress page settings**: correct slug, parent, template, menu assignment,
   SEO settings?
9. **Thrive element quality**: are elements configured correctly, or are there
   inline style overrides, leftover placeholder text, or misconfigured elements?

## Outputs
- Thrive Audit Report: PASS / ISSUE / BLOCK per dimension
- Specific finding and remediation instruction per issue
- Priority ranking for fixes (BLOCK → ISSUE order)

## Constraints
- BLOCK if POL-051 page role is violated or INV-0002 is at risk.
- ISSUE for quality or compliance problems that do not block publication.
- PASS only if all dimensions clear.

## Invocation
Used when auditing existing Thrive-built pages or reviewing a completed build
before ML1 approval.
