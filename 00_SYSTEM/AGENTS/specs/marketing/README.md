---
id: 00_system__agents__specs__marketing__readme_md
title: Marketing Agents
owner: ML1
status: active
created_date: 2026-03-08
last_updated: 2026-03-21
tags: [marketing, agents, orchestration]
---

# Marketing Agents

This folder defines the LL Marketing Agent Suite for governed campaign strategy,
content production, website implementation, quality control, distribution
preparation, market-signal capture, and repository governance.

## Activation Status
- Core suite activated by ML1 on `2026-03-21` for governed internal execution, draft generation, QA, implementation, and release preparation.
- Optional specialist agents remain separately gated and are not activated by default.
- Final outward publishing still remains subject to `INV-0002` and explicit ML1 action.

## Core Agents
- `MKT_CHIEF_MARKETING_OFFICER_AGENT`
- `MKT_MARKETING_STRATEGY_AGENT`
- `MKT_CONTENT_PRODUCTION_AGENT`
- `MKT_DESIGN_PRODUCTION_AGENT`
- `MKT_EDITORIAL_QA_AGENT`
- `MKT_WEBSITE_IMPLEMENTATION_AGENT`
- `MKT_UX_DESIGN_AGENT`
- `MKT_THRIVE_THEMES_AGENT`
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
6. UX Design agent translates approved content into wireframes, component specs,
   interaction patterns, and implementation handoff packets.
7. Thrive Themes agent translates wireframe specs into Thrive Architect build
   packets for ML1 execution in WordPress.
8. Website Implementation agent assembles approved website changes, local patch
   sets, and WIP deployment packets.
9. Distribution orchestration agent prepares channel handoff and deployment packages.
10. Market signal agent reports market feedback as operational signals.
11. Repository governance agent stores assets with lifecycle and provenance controls.

## Website Build Chain (page production)
```
MKT_CONTENT_PRODUCTION_AGENT     (approved copy)
MKT_MARKETING_STRATEGY_AGENT     (page purpose, ICP, funnel context)
MKT_DESIGN_PRODUCTION_AGENT      (brand assets, palette)
        ↓
MKT_UX_DESIGN_AGENT              (wireframe spec, component definitions, handoff packet)
        ↓
MKT_THRIVE_THEMES_AGENT          (Thrive Architect build packet)
        ↓
ML1                              (executes build in WordPress; approves; publishes)
```

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
