---
id: 04_initiatives__ll_portfolio__08_marketing__agent_roster_md
title: Marketing Portfolio — Agent Roster
owner: ML1
status: active
created_date: 2026-02-08
last_updated: 2026-03-18
tags: [agents, marketing, roster]
---

# Marketing Portfolio — Agent Roster

**Location**: `LL_PORTFOLIO/08_MARKETING/06_AGENTS/`
**Last ML1 Review**: 2026-03-18

---

## Activation Status Summary

| Agent ID | Name | Spec | Activation Status | Blocker |
|---|---|---|---|---|
| SE-01 | Strategic Editor | V2 | **Active** — lightweight mode | None |
| SEO-01 | SEO Metrics Master | V2 | **Active** — keyword research only (IMP-05) | None |
| SPE-01 | Selective Provocation Engine | V2 | **Blocked** | ≥3 active accountant referral relationships (IMP-01) |
| BSE-01 | Blog & SEO Engine | V2 | **Blocked** | Health Check landing page live (F02) |
| CA-01 | Conversion Architect | V1 (pending V2 spec) | **Blocked** | F02 live + traffic baseline + conversion data |

---

## Agent Descriptions

### SE-01 — Strategic Editor

**Role**: Coherence gate — system-wide governance layer
**Spec**: [AGENT_SPEC-STRATEGIC_EDITOR_V2.md](06_AGENTS/STRATEGIC_EDITOR/AGENT_SPEC-STRATEGIC_EDITOR_V2.md)
**Activated**: 2026-03-18

Runs post-generation, pre-output on all externally facing artifacts. Override authority over all downstream agents. Positioning > optimization — if an output improves metrics but weakens positioning, it is rejected.

Scores outputs against: Positioning Integrity (0.35), ICP Precision (0.20), Offer Clarity (0.20), Non-Generic Language (0.15), Internal Consistency (0.10). Thresholds: ≥0.85 approved, 0.60–0.84 revision required, <0.60 rejected.

Current mode: manual invocation per output. No automation or batch processing.

---

### SEO-01 — SEO Metrics Master

**Role**: Keyword discovery and traffic/conversion analytics
**Spec**: [AGENT_SPEC-SEO_METRICS_MASTER_V2.md](06_AGENTS/SEO_METRICS_MASTER/AGENT_SPEC-SEO_METRICS_MASTER_V2.md)
**Activated**: 2026-03-18 (limited scope)

Current activation: IMP-05 only — produce Structuring keyword shortlist for ML1 approval. Scores candidates by intent alignment, commercial value, and difficulty. Does not choose keywords for use — outputs require ML1 approval before any content production or Google Ads activation.

Full activation (performance monitoring, funnel leak detection, content briefs) requires F02 landing page live.

---

### SPE-01 — Selective Provocation Engine

**Role**: Top-of-funnel authority hooks for LinkedIn and outreach
**Spec**: [AGENT_SPEC-SELECTIVE_PROVOCATION_ENGINE_V2.md](06_AGENTS/SELECTIVE_PROVOCATION_ENGINE/AGENT_SPEC-SELECTIVE_PROVOCATION_ENGINE_V2.md)
**Status**: Blocked

**Blocker**: ≥3 active accountant referral relationships (IMP-01 in LLP-025). Distribution channel must exist before hook generation begins.

Generates contrarian insights, pattern interrupts, and authority hooks at operator-level tone. All outputs reviewed by SE-01 before use. High risk-level outputs require SE-01 review before ML1 queue.

---

### BSE-01 — Blog & SEO Engine

**Role**: SEO content production for Structuring keyword cluster
**Spec**: [AGENT_SPEC-BLOG_SEO_ENGINE_V2.md](06_AGENTS/BLOG_SEO_ENGINE/AGENT_SPEC-BLOG_SEO_ENGINE_V2.md)
**Status**: Blocked

**Blockers** (both required):
1. Health Check landing page live on levine-law.ca
2. ML1-approved keyword list from SEO-01

Produces structured SEO articles mapped to approved keywords. 60% F02 (Health Check), 30% F03 (Payments/MSB), 10% F01 support. All outputs default to Draft; require SE-01 review then ML1 approval before publishing.

---

### CA-01 — Conversion Architect

**Role**: Health Check purchase rate and diagnostic-to-retainer conversion optimization
**Spec**: V2 spec pending
**Status**: Blocked

**Blockers**: F02 live, traffic baseline established, conversion data available. Last agent to activate — needs real data to optimize against.

---

## Agent Hierarchy

```
SE-01 (Strategic Editor) — governance gate across all agents
│
├── SEO-01 (SEO Metrics Master) — analytics and keyword research
│     └── feeds keyword list → BSE-01
│
├── SPE-01 (Selective Provocation Engine) — top-of-funnel hooks
│     └── high-performing hooks → BSE-01 (long-form expansion)
│
├── BSE-01 (Blog & SEO Engine) — SEO content production
│     └── performance data → SEO-01
│
└── CA-01 (Conversion Architect) — conversion optimization
      └── copy variants → SE-01 for review
```

All agent outputs pass through SE-01 before ML1 approval queue.

---

## ML1 Authority Statement

ML1 is the sole authority for:
- Agent activation and deactivation
- Approval of all agent outputs before external use
- Keyword list approval (SEO-01)
- Positioning doctrine definition
- Stage advancement decisions

## Explicit Prohibitions (All Agents)

- Cannot accept or reject client work autonomously
- Cannot open matters in Clio
- Cannot provide legal advice
- Cannot score or rank leads
- Cannot merge funnel data with delivery metrics
- Cannot publish or distribute content without ML1 approval
