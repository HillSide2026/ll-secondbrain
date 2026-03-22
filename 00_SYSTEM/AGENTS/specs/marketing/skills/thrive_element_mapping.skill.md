---
id: mkt_skill_thrive_element_mapping
title: Thrive Element Mapping Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, implementation, elements]
---

# Skill: Thrive Element Mapping

## Purpose
Map every content block from a wireframe spec or HTML draft to the precise
Thrive Architect element that implements it.

## Inputs
- Wireframe spec or HTML draft
- Thrive Architect element library (known set)

## Process
For each content block or component:
1. Identify the content type (heading, text, image, button, list, card, accordion,
   table, form, icon, etc.).
2. Select the correct Thrive element:
   - Heading → Heading element (configure tag, font, size, color)
   - Body text → Text element
   - Image → Image element
   - CTA button → Button element
   - Bulleted list → Styled List element
   - Card → Content Box + Columns (nested)
   - Card grid → Columns element with n columns
   - Accordion → Toggle element
   - Tabs → Thrive Tabs element
   - Comparison table → Custom HTML or Styled Table
   - Contact form → Lead Generation element or Custom HTML (GHL embed)
   - Icon → Icon element
   - Divider/spacer → Divider element
   - Global header/footer → Symbol
3. For each element, define the required configuration (see thrive_build_packet).
4. Flag any content type not achievable natively — recommend Custom HTML or CSS.

## Outputs
- Element mapping table: content block → Thrive element → configuration notes
- List of non-native patterns requiring Custom HTML or CSS

## Constraints
- Use only known Thrive Architect elements.
- Do not invent elements that do not exist in Thrive.

## Invocation
First step in any Thrive build packet task.
