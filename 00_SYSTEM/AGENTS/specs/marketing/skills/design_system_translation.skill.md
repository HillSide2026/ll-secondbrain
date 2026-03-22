---
id: mkt_skill_design_system_translation
title: Design System Translation Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, design-system, brand, thrive, tokens]
---

# Skill: Design System Translation

## Purpose
Translate POL-049 (color palette) and POL-050 (brand identity) into a working
design system for the LL website in Thrive Architect.

## Inputs
- POL-049 (active color palette with hex values)
- POL-050 (brand signals: judgment authority, systemized precision, calm competence)
- Thrive Color Manager and font system

## Process
1. Define color tokens: map each POL-049 palette color to a named token
   (primary-dark / primary-mid / accent / surface / text-primary / text-secondary
   / border / etc.).
2. Define typography scale: H1–H6, body, caption — size / weight / line-height
   for desktop and mobile.
3. Define spacing scale: consistent set of padding/margin values across the
   system (e.g. 8 / 16 / 24 / 32 / 48 / 64 / 96px).
4. Define border and shadow tokens (border-radius, box-shadow values).
5. Define component baseline rules (all cards share: border-radius 8px,
   box-shadow [token], padding 32px, etc.).
6. Produce Thrive Color Manager setup instructions (how to enter palette colors).
7. Produce Thrive font setup instructions (font family, fallback stack).
8. Document where each token maps to POL-049 / POL-050 — traceable.

## Outputs
- Color token table (name → palette ref → hex)
- Typography scale (desktop and mobile)
- Spacing scale
- Border and shadow tokens
- Component baseline rules
- Thrive Color Manager setup instructions
- Thrive font setup instructions

## Constraints
- All colors must come from the active POL-049 palette. No ad hoc colors.
- Typography must support the brand signals defined in POL-050.

## Invocation
Used once when setting up the LL website design system, and revisited when
POL-049 or POL-050 is updated.
