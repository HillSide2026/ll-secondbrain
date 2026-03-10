---
id: mkt_skill_template_slot_selection
title: Template Slot Selection Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, design, templates]
---

# Skill: Template Slot Selection

## Purpose
Select the correct approved template slot for the requested asset type and channel.

## Inputs
- Structured design brief
- Approved template registry
- Output type requirement

## Process
1. Match requested output type to approved template slots.
2. Validate template status, version, and required fields.
3. Resolve tie cases using deterministic ranking rules.
4. Return selected template reference and fallback.

## Outputs
- Selected template slot
- Template version reference
- Fallback template slot (if defined)

## Constraints
- Only approved templates may be selected.
- Deprecated templates must be rejected.
- No ad hoc template creation is allowed in this step.

## Invocation
Used before Canva design instantiation.

