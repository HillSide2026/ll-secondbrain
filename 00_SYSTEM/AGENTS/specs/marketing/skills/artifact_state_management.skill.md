---
id: mkt_skill_artifact_state_management
title: Artifact State Management Skill
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [marketing, skill, repository, lifecycle]
---

# Skill: Artifact State Management

## Purpose
Control lifecycle state of marketing artifacts.

## Inputs
- Artifact identifier
- State transition request

## Process
1. Validate transition rules.
2. Update artifact lifecycle state.

Possible states:
- draft
- approved
- published
- retired

## Outputs
- Updated artifact state record

## Constraints
- Unauthorized transitions must be rejected.

## Invocation
Used by Repository Governance Agent for lifecycle enforcement.
