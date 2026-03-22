---
id: mkt_skill_forms_and_conversion_ux
title: Forms and Conversion UX Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [ux, forms, conversion, lead-generation, thrive-leads]
---

# Skill: Forms and Conversion UX

## Purpose
Design form layout and conversion flow for inquiry and opt-in pages, optimized
for ICP-01 and ICP-02 and implementable in Thrive Lead Generation or GHL forms.

## Inputs
- Conversion goal (inquiry / lead magnet / consultation request)
- ICP
- Fields required
- Platform: Thrive Lead Generation element or GHL embedded form

## Process
1. Define the minimum viable field set (fewer fields = higher conversion; only
   ask what is needed to qualify the lead).
2. Order fields from lowest to highest friction.
3. Define field types, labels, placeholders, and validation rules.
4. Define button label (specific > generic: "Send my inquiry" > "Submit").
5. Define error state styling.
6. Define success state (thank-you message or redirect URL).
7. Define mobile layout (fields full-width and stacked; button full-width).
8. Map to Thrive Lead Generation element configuration or GHL embed.
9. Note any ARIA requirements (label association, error announcements).

## Outputs
- Field list with type / label / placeholder / validation / required
- Button label and placement
- Error state spec
- Success state / redirect spec
- Mobile layout spec
- Thrive Lead Generation or GHL configuration notes

## Constraints
- Do not ask for more fields than needed to qualify the lead — each additional
  field reduces conversion rate.
- Marketing must not accept or reject work autonomously (Marketing README).
- No legal advice must be implied by form framing.

## Invocation
Used for any page with a contact form, lead capture, or opt-in element.
