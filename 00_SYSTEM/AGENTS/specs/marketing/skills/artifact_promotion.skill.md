---
id: mkt_skill_artifact_promotion
title: Artifact Promotion Skill
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [marketing, skill, meta, lifecycle]
---

# Skill: Artifact Promotion

## Purpose
Promote validated artifacts to the appropriate lifecycle state within the repository.

## Inputs
- Artifact
- Validation result
- Target lifecycle state

## Process
1. Confirm artifact validation status.
2. Verify state transition rules.
3. Update artifact lifecycle state.
4. Record provenance and promotion event.

Possible states:
- draft
- reviewed
- approved
- published
- archived

## Outputs
- Updated artifact record
- Promotion log

## Constraints
- Only validated artifacts may be promoted.
- Promotion must follow lifecycle rules.

## Invocation
Used when artifacts move between lifecycle stages.
