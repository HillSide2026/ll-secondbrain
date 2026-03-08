---
id: mkt_skill_skill_selection
title: Skill Selection Skill
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [marketing, skill, meta, orchestration]
---

# Skill: Skill Selection

## Purpose
Select the most appropriate skill for executing a defined task.

## Inputs
- Task description
- Available skill registry

## Process
1. Identify task requirements.
2. Match task requirements to skill capabilities.
3. Select best-fit skill.
4. Validate that skill constraints are satisfied.

## Outputs
- Selected skill
- Skill invocation parameters

## Constraints
- Must use registered skills.
- Cannot select skills outside agent authority.

## Invocation
Used after task decomposition to determine execution capability.
