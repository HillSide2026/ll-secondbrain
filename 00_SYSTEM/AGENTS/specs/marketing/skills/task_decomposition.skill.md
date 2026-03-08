---
id: mkt_skill_task_decomposition
title: Task Decomposition Skill
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [marketing, skill, meta, orchestration]
---

# Skill: Task Decomposition

## Purpose
Break a high-level objective into a sequence of bounded tasks that can be executed using available skills.

## Inputs
- Objective
- Available skills registry
- Context information

## Process
1. Analyze the objective.
2. Identify required outcomes.
3. Decompose the objective into discrete tasks.
4. Map tasks to existing skills.
5. Define execution order.

## Outputs
- Task list
- Skill invocation plan
- Execution sequence

## Constraints
- Tasks must map to existing skills.
- Tasks must be bounded and verifiable.
- Cannot invent new skills.

## Invocation
Used by agents when planning execution of complex objectives.
