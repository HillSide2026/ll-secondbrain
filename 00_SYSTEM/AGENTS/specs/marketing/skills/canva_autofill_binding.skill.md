---
id: mkt_skill_canva_autofill_binding
title: Canva Autofill Binding Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, design, canva, autofill]
---

# Skill: Canva Autofill Binding

## Purpose
Bind approved content fields into Canva template fields deterministically.

## Inputs
- Draft Canva design
- Required fields matrix
- Approved copy blocks

## Process
1. Validate required template fields are present.
2. Map source content blocks to target template fields.
3. Apply autofill bindings through approved tool calls.
4. Confirm field population and record unresolved fields.

## Outputs
- Populated design draft
- Field mapping record
- Missing-field exceptions (if any)

## Constraints
- Do not generate new claims to fill missing content.
- Unresolved required fields must block promotion.
- Field mappings must be logged.

## Invocation
Used after design instantiation and before design QA.

