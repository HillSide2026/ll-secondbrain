---
id: mkt_skill_integration_workflow_execution
title: Integration Workflow Execution Skill
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [marketing, skill, distribution, integrations]
---

# Skill: Integration Workflow Execution

## Purpose
Prepare structured instructions for external publishing tools and integration adapters.

## Inputs
- Channel-ready asset package
- Distribution schedule
- Integration configuration

## Process
1. Prepare upload payloads for each platform.
2. Map assets to integration endpoints.
3. Generate structured publishing instructions.
4. Pass instructions to integration adapters.

## Outputs
- Integration execution payload
- Publishing workflow instructions

## Constraints
- Cannot directly execute publishing without authorization.
- Must preserve approved content integrity.

## Invocation
Used by Distribution Orchestration Agent when coordinating publishing workflows.
