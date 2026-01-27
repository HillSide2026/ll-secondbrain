# System Roadmap 2026-W05

**Status:** ACTIVE
**Owner:** ML1
**Created:** 2026-01-25
**Activated:** 2026-01-26

**Statement:** This roadmap establishes the Second Brain system infrastructure — governance framework, agent orchestration, integrations, and operating rhythm.

---

## Inventory (Planning Artifacts)
- 00_SYSTEM/FOLDER_MAP.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/BACKLOG.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/00_DRAFT_ROADMAPS/README.md
- 04_INITIATIVES/SYSTEM_PORTFOLIO/01_ACTIVE_ROADMAPS/README.md

---

## Stages (Milestones) + Definition of Done

### Stage 1 — System Discovery & Readiness Baseline ✅ COMPLETE
**Definition of Done (DoD):**
- System inventory completed for core governance + portfolio structure.
- Gaps/opportunities list created for system-level agents and read-only integrations.
- Draft architecture map for integrations and agent roles documented.
- Risks and dependencies logged for downstream stages.

**Status:** Archived at `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE1/`

### Stage 2 — Read-Only Integration Foundation ✅ COMPLETE
**Definition of Done (DoD):**
- Read-only integration requirements defined for Gmail, SharePoint, and Microsoft Word.
- Data access boundaries + audit expectations documented.
- Integration approach options (API, connector, export) compared with tradeoffs.
- Pilot test plan drafted (no execution authorization).

**Status:** Archived at `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE2/`

### Stage 3 — System-Level Agent Orchestration ✅ COMPLETE
**Definition of Done (DoD):**
- 5 active system-level agent roles defined with responsibilities + handoffs.
- Agent governance guardrails documented (no doctrine changes).
- System runbooks scoped for agent execution flows.
- Metrics for system reliability + throughput defined.

**Status:** READY_FOR_CLOSURE at `01_ACTIVE_ROADMAPS/STAGE3/`

### Stage 4 — Portfolio Operating Rhythm ✅ COMPLETE
**Definition of Done (DoD):**
- Roadmap-to-run cadence defined (draft schedule + review triggers).
- Backlog intake and prioritization rules drafted for system portfolio.
- Active roadmap promotion criteria drafted for ML1 decision.
- Audit checklist drafted for ongoing compliance.

**Status:** READY_FOR_CLOSURE at `01_ACTIVE_ROADMAPS/STAGE4/`

### Stage 5 — Agent Implementation & Integration Activation 🔄 ACTIVE
**Definition of Done (DoD):**
- Agent runtime selected and configured (Claude Code, MCP, or custom)
- All 5 system-level agents deployed and operational
- Gmail read-only integration activated with audit logging
- SharePoint read-only integration activated with audit logging
- Word/OneDrive read-only integration activated with audit logging
- Integration test results documented (read-only verified, no write paths)

**Status:** KICKOFF at `01_ACTIVE_ROADMAPS/STAGE5/`

### Stage 6 — Operational Validation & Steady State 📋 PLANNED
**Definition of Done (DoD):**
- First full operating cycle completed (weekly cadence)
- All agents produce at least one artifact per runbook
- Metrics baseline established (compliance rate, triage time, etc.)
- Operating rhythm validated and adjusted if needed
- System declared operational for steady-state use

**Status:** PLANNED (pending Stage 5 completion)

---

## Backlog by Stage

### Stage 5 Backlog
- **SYS-001: Agent runtime selection** — Choose Claude Code agents, MCP servers, or custom SDK
  - **Dependencies:** Stage 3 agent roster
  - **Risks:** Wrong choice requires re-architecture
  - **Owner:** ML1
- **SYS-002: Gmail integration** — OAuth app, scopes, audit logging per Stage 2 spec
  - **Dependencies:** SYS-001
  - **Risks:** API limits, policy constraints
  - **Owner:** Integration Steward Agent
- **SYS-003: SharePoint integration** — Graph API, site scopes per Stage 2 spec
  - **Dependencies:** SYS-001
  - **Risks:** Permissions complexity, tenant restrictions
  - **Owner:** Integration Steward Agent
- **SYS-004: Word/OneDrive integration** — Document access per Stage 2 spec
  - **Dependencies:** SYS-001
  - **Risks:** File format inconsistencies
  - **Owner:** Integration Steward Agent
- **SYS-005 to SYS-009: Deploy 5 agents** — Configure and deploy each agent
  - **Dependencies:** SYS-001
  - **Risks:** Role ambiguity, missing handoffs
  - **Owner:** Runbook & QA Agent

### Stage 6 Backlog
- **SYS-010: First operating cycle** — Execute weekly cadence end-to-end
  - **Dependencies:** SYS-005 to SYS-009
  - **Risks:** Cadence too heavy, gaps in handoffs
  - **Owner:** All Agents
- **SYS-011: Archive Stage 3 + 4** — Move to 10_ARCHIVE
  - **Dependencies:** Stage closures approved
  - **Risks:** None
  - **Owner:** Knowledge Curation Agent
- **Metrics baseline** — Establish initial values for all Stage 3 metrics
  - **Dependencies:** SYS-010
  - **Risks:** Insufficient data
  - **Owner:** Portfolio Planning Agent
- **Operating rhythm adjustment** — Tune cadence based on first cycle learnings
  - **Dependencies:** Metrics baseline
  - **Risks:** Over-engineering
  - **Owner:** ML1

---

## Out of Scope (This Roadmap)
- Matter-level work or matter execution workflows
- Write-back, mutation, or automation that changes external systems (beyond read-only)
- Doctrine updates or policy changes (require separate doctrine PRs)
- LL Portfolio initiatives (separate portfolio)

## Resolved Decision Questions
1. ~~Which integration approach is preferred?~~ → **API-based (OAuth/Graph)** for Gmail and SharePoint
2. ~~Are the proposed 5 agents correct?~~ → **Yes, approved as-is**
3. ~~What cadence is acceptable?~~ → **Weekly** (with monthly health check)
4. ~~What evidence for promotion?~~ → **Checklist per STAGE4_PROMOTION_CRITERIA.md**
5. ~~Additional dependencies before Stage 2?~~ → **None identified**

## TBD (Remaining)
- [TBD] Confirm agent runtime choice (SYS-001)
- [TBD] Confirm credential storage approach for integrations
- [TBD] Confirm integration logging retention period

---

## Roadmap Promotion Record

| Date | Action | Approver | Notes |
|------|--------|----------|-------|
| 2026-01-25 | Created as DRAFT | ML1 | Initial roadmap |
| 2026-01-26 | Stage 1-4 completed | ML1 | Documentation phases done |
| 2026-01-26 | Promoted to ACTIVE | ML1 | Implementation phases begin |
