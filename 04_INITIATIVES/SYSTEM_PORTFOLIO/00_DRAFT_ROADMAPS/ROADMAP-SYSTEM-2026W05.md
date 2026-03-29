---
id: 04_initiatives__system_portfolio__00_draft_roadmaps__roadmap-system-2026w05_md
title: System Roadmap 2026-W05
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-11
tags: []
---

# System Roadmap 2026-W05

**Status:** ACTIVE
**Owner:** ML1
**Created:** 2026-01-25
**Activated:** 2026-01-26

**Statement:** This roadmap establishes the Second Brain system infrastructure — governance framework, agent orchestration, integrations, and operating rhythm.

---

## Inventory (Planning Artifacts)
- 00_SYSTEM/architecture/FOLDER_MAP.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/BACKLOG.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/00_DRAFT_ROADMAPS/README.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/01_ACTIVE_ROADMAPS/README.md

---

## Stage Structure

```
ROADMAP-SYSTEM-2026W05
├── Stage 1 — Foundation & Governance ✅ COMPLETE
│   ├── 1.1 System Discovery & Readiness
│   ├── 1.2 Integration Specifications
│   ├── 1.3 Agent Orchestration Design
│   └── 1.4 Operating Rhythm Rules
│
└── Stage 2 — Implementation & Operations 🔄 ACTIVE
    ├── 2.1 Agent Runtime Setup
    ├── 2.2 Integration Activation
    ├── 2.3 Operational Validation
    ├── 2.9 Drive Integration Setup
    ├── 2.10 Move Authoritative Ledger to Drive
    ├── 2.11 Matter Management Agent
    ├── 2.12 Calendar Scheduling
    └── 2.13 Gmail Matter Labeling
```

---

## Stage 1 — Foundation & Governance ✅ COMPLETE

**Purpose:** Establish governance framework, design agents, specify integrations, define operating rules.
**Status:** All sub-stages complete. Artifacts archived or ready for archive.

### 1.1 System Discovery & Readiness Baseline ✅
**DoD:**
- System inventory completed for core governance + portfolio structure
- Gaps/opportunities list created for agents and integrations
- Architecture map for integrations and agent roles documented
- Risks and dependencies logged

**Artifacts:** `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE1/STAGE1.1/`

### 1.2 Read-Only Integration Foundation ✅
**DoD:**
- Integration requirements defined for Gmail, SharePoint, Word
- Data access boundaries + audit expectations documented
- Integration approach options compared with tradeoffs
- Pilot test plan drafted

**Artifacts:** `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE1/STAGE1.2/`

### 1.3 System-Level Agent Orchestration ✅
**DoD:**
- 5 system-level agent roles defined with responsibilities + handoffs
- Agent governance guardrails documented
- Runbooks scoped for agent execution flows
- Metrics for reliability + throughput defined

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE1/STAGE1.3/` (ready for archive)

### 1.4 Portfolio Operating Rhythm ✅
**DoD:**
- Roadmap-to-run cadence defined
- Backlog intake and prioritization rules drafted
- Promotion criteria drafted for ML1 decision
- Audit checklist drafted

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE1/STAGE1.4/` (ready for archive)

---

## Stage 2 — Implementation & Operations 🔄 ACTIVE

**Purpose:** Build and deploy actual agents and integrations; validate operational readiness.
**Status:** Kickoff approved. Sub-stages in progress.

### 2.1 Agent Runtime Setup 🔄 IN PROGRESS
**DoD:**
- Agent runtime selected and configured: **Claude Code agents**
- Credential storage configured: **Environment variables** (`.env` excluded from git)
- All 5 agents deployed and tested against runbooks

**Decisions Resolved:**
- Runtime: Claude Code agents (subprocess model)
- Credentials: Environment variables (upgrade to secrets manager later if needed)

**Backlog Items:** SYS-001, SMA-001 to SMA-005

### 2.2 Integration Activation 🔄 ACTIVE / NORMALIZING
**DoD:**
- Gmail integration active with audit logging
- SharePoint integration active with audit logging
- Word/OneDrive read-only integration active with audit logging
- Planning packets opened for SYS-002, SYS-003, and SYS-004

**Sequence:** Gmail → SharePoint → Word (per ML1 decision)

**Backlog Items:** SYS-002, SYS-003, SYS-004

### 2.3 Operational Validation 📋 PLANNED
**DoD:**
- First full operating cycle completed (weekly cadence)
- All agents produce at least one artifact per runbook
- Metrics baseline established
- System declared operational for steady-state use

**Deliverable Complexity Ladder (D1–D4):**
- **D1:** Email labeling (deterministic, bounded)
- **D2:** Case summaries (neutral, source-bound)
- **D3:** Multi-artifact packets with cross-references
- **D4:** Controlled propagation outputs (Stage 4 protocol)

**Backlog Items:** SYS-010, SYS-011, metrics baseline, rhythm adjustment

### 2.9 Drive Integration Setup 🟨 BACKLOG
**DoD:**
- Drive access limited to approved folder boundary
- Read/write test passes inside boundary; fails outside
- Auth model + scopes documented

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.9/`

### 2.10 Authoritative Ledger in Drive 🟨 BACKLOG
**DoD:**
- Ledger persists in Drive and survives daily regeneration
- Human status edits respected
- Daily report is ledger-first

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.10/`

### 2.11 Matter Management Agent 🟨 BACKLOG
**DoD:**
- Hourly Matter Dashboard runs (9–5, Mon–Fri)
- Repo-local outputs only (no write-back)
- Governance validation passes

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.11/`

### 2.12 Calendar Scheduling 🟨 BACKLOG
**DoD:**
- Top-priority tasks scheduled to approved calendar
- Human approval gate enforced
- Audit logs for each calendar write

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.12/`

### 2.13 Gmail Matter Labeling 🟨 BACKLOG
**DoD:**
- Deterministic matter-number labeling policy approved
- Gmail labels applied via write-back (labels only)
- Audit logging for each label write

**Artifacts:** `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.13/`

---

## Backlog Summary

### Stage 2.1 — Agent Runtime
| ID | Description | Owner | Status |
|----|-------------|-------|--------|
| SYS-001 | Agent runtime selection | ML1 | **RESOLVED: Claude Code** |
| SMA-001 | Deploy System Governance Agent | Runbook & QA | pending |
| SMA-002 | Deploy Portfolio Planning Agent | Runbook & QA | pending |
| SMA-003 | Deploy Integration Steward Agent | Runbook & QA | pending |
| SMA-004 | Deploy Knowledge Curation Agent | Runbook & QA | pending |
| SMA-005 | Deploy Runbook & QA Agent | Runbook & QA | pending |

### Stage 2.2 — Integrations
| ID | Description | Owner | Status |
|----|-------------|-------|--------|
| SYS-002 | Gmail integration surface | Integration Steward | planning |
| SYS-003 | SharePoint integration surface | Integration Steward | planning |
| SYS-004 | Word/OneDrive integration | Integration Steward | planning |

### Stage 2.3 — Validation
| ID | Description | Owner | Status |
|----|-------------|-------|--------|
| SYS-010 | First operating cycle | All Agents | pending |
| SYS-011 | Archive Stage 1 artifacts | Knowledge Curation | pending |

---

## Out of Scope (This Roadmap)
- Matter-level work or matter execution workflows
- Write-back, mutation, or automation that changes external systems
- Doctrine updates or policy changes
- LL Portfolio initiatives

## Resolved Decisions

| # | Question | Decision | Date |
|---|----------|----------|------|
| 1 | Integration approach | API-based (OAuth/Graph) | 2026-01-26 |
| 2 | Agent roster | 5 agents approved as-is | 2026-01-26 |
| 3 | Review cadence | Weekly (monthly health check) | 2026-01-26 |
| 4 | Promotion evidence | Per 01_ACTIVE_ROADMAPS/STAGE4/STAGE4_PROMOTION_CRITERIA.md | 2026-01-26 |
| 5 | Agent runtime | **Claude Code agents** | 2026-01-26 |
| 6 | Credential storage | **Environment variables** | 2026-01-26 |
| 7 | Integration order | **Gmail → SharePoint → Word** | 2026-01-26 |

## TBD (Remaining)
- [TBD] Integration logging retention period

---

## Roadmap Record

| Date | Action | Approver | Notes |
|------|--------|----------|-------|
| 2026-01-25 | Created as DRAFT | ML1 | Initial roadmap |
| 2026-01-26 | Stage 1 completed | ML1 | Foundation phases done |
| 2026-01-26 | Promoted to ACTIVE | ML1 | Implementation begins |
| 2026-01-26 | Stage 2 decisions | ML1 | Runtime, credentials, order resolved |
