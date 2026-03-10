---
id: 00_system__agents__specs__marketing__readme_md
title: Marketing Agents
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-10
tags: [marketing, agents, orchestration]
---

# Marketing Agents

This folder defines the LL Marketing Agent Suite for governed campaign strategy,
content production, quality control, distribution preparation, market-signal
capture, and repository governance.

## Core Agents
- `MKT_CHIEF_MARKETING_OFFICER_AGENT`
- `MKT_MARKETING_STRATEGY_AGENT`
- `MKT_CONTENT_PRODUCTION_AGENT`
- `MKT_DESIGN_PRODUCTION_AGENT`
- `MKT_EDITORIAL_QA_AGENT`
- `MKT_DISTRIBUTION_ORCHESTRATION_AGENT`
- `MKT_MARKET_SIGNAL_AGENT`
- `MKT_REPOSITORY_ASSET_GOVERNANCE_AGENT`

## Skill Mapping
- Canonical map: `00_SYSTEM/AGENTS/specs/marketing/MARKETING_AGENT_SKILL_MAP.md`
- Agent-level bindings are listed in each charter under `Relevant Skills`.
- Skill files location: `00_SYSTEM/AGENTS/specs/marketing/skills/`

## Optional Specialized Agents
- `MKT_SEO_DISCOVERABILITY_AGENT`
- `MKT_SOCIAL_NARRATIVE_AGENT`
- `MKT_OFFER_FUNNEL_AGENT`
- `MKT_COMPETITIVE_POSITIONING_AGENT`

## Reference Workflow
1. Chief Marketing Officer agent decomposes objective and sequences skills.
2. Strategy agent defines campaign and funnel requirements.
3. Content agent produces draft artifacts.
4. Design Production agent creates governed design drafts from approved templates.
5. Editorial QA agent validates strategy, doctrine, and policy alignment.
6. Distribution orchestration agent prepares channel handoff and deployment packages.
7. Market signal agent reports market feedback as operational signals.
8. Repository governance agent stores assets with lifecycle and provenance controls.

## Meta-Execution Chain
1. Objective
2. `task_decomposition.skill.md`
3. `skill_selection.skill.md`
4. `context_assembly.skill.md`
5. `operational_skill`
6. `execution_validation.skill.md`
7. `artifact_promotion.skill.md`

Operational skills (marketing, content, SEO, and competitive skills) plug into the `operational_skill` stage.

## Runtime and Authority Boundaries
- Runtime actions must remain within ML2 doctrine and assigned capabilities.
- Agents, workers, tools, integration adapters, and run containers do not create doctrine.
- Workers and subagents do not issue Authorized Outputs.
- Authorized Output status requires the authorized issuance layer under governed workflow controls.
- Ambiguity, scope uncertainty, or boundary failure requires escalation.

## Integration Surface
External I/O is mediated through approved integration adapters only (for example:
CMS, email platform, social platform, analytics stack). No direct external calls
outside governed adapter pathways.
