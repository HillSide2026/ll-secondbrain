---
id: mkt_skill_accessibility_audit_and_remediation
title: Accessibility Audit and Remediation Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, accessibility, wcag, aria, compliance]
---

# Skill: Accessibility Audit and Remediation

## Purpose
Audit a page spec or HTML draft for WCAG 2.1 AA accessibility compliance and
produce specific remediation instructions.

## Inputs
- Page wireframe spec or HTML draft
- Color palette in use (POL-049)

## Process
Check each item:
1. **Heading hierarchy** — one H1 per page; no skipped levels (H1 → H3 without H2)
2. **Color contrast** — body text 4.5:1 minimum; large text (18pt+) 3:1 minimum;
   UI components 3:1
3. **Alt text** — all meaningful images have descriptive alt text; decorative
   images have alt=""
4. **ARIA on interactive elements** — accordions have aria-expanded and
   aria-controls; tabs have role="tab" and aria-selected; buttons have
   accessible labels
5. **Keyboard navigability** — all interactive elements reachable via Tab; focus
   order is logical; Enter/Space activate buttons
6. **Focus indicator** — visible focus ring on all interactive elements; not
   suppressed by CSS (outline: none without replacement is a failure)
7. **Form labels** — all inputs have associated <label> elements or aria-label
8. **Error announcements** — form errors announced to screen readers (aria-live
   or role="alert")
9. **Link text** — no bare "click here" or "learn more" without context; link
   text describes the destination

## Outputs
- Accessibility Audit Report: PASS / FAIL per check with specific finding
- Remediation instructions per failure
- Thrive Architect implementation notes for each fix

## Constraints
- WCAG 2.1 AA is the minimum standard.
- Failures must be remediated before the page is considered ready for ML1
  approval.

## Invocation
Used before any page handoff to MKT_THRIVE_THEMES_AGENT and before final ML1
approval.
