# System Roadmap 2026-W05 (Draft)

**Status:** DRAFT  
**Owner:** ML1  
**Date:** 2026-01-25

**Statement:** No active roadmap exists; this document is the initial draft.

## Inventory (Existing Planning Artifacts)
- 00_SYSTEM/FOLDER_MAP.md (identifies where system roadmaps live). 
- 04_INITIATIVES/SYSTEM_PORTFOLIO/00_DRAFT_ROADMAPS/README.md (draft roadmap rules). 
- 04_INITIATIVES/SYSTEM_PORTFOLIO/01_ACTIVE_ROADMAPS/README.md (active roadmap rules). 
- No other roadmap, backlog, milestone, or stage documents were found in the repository search.

---

## Stages (Milestones) + Definition of Done

### Stage 1 — System Discovery & Readiness Baseline
**Definition of Done (DoD):**
- System inventory completed for core governance + portfolio structure.
- Gaps/opportunities list created for system-level agents and read-only integrations.
- Draft architecture map for integrations and agent roles documented.
- Risks and dependencies logged for downstream stages.

### Stage 2 — Read-Only Integration Foundation
**Definition of Done (DoD):**
- Read-only integration requirements defined for Gmail, SharePoint, and Microsoft Word.
- Data access boundaries + audit expectations documented.
- Integration approach options (API, connector, export) compared with tradeoffs.
- Pilot test plan drafted (no execution authorization).

### Stage 3 — System-Level Agent Orchestration
**Definition of Done (DoD):**
- 5 active system-level agent roles defined with responsibilities + handoffs.
- Agent governance guardrails documented (no doctrine changes).
- System runbooks scoped for agent execution flows.
- Metrics for system reliability + throughput defined.

### Stage 4 — Portfolio Operating Rhythm
**Definition of Done (DoD):**
- Roadmap-to-run cadence defined (draft schedule + review triggers).
- Backlog intake and prioritization rules drafted for system portfolio.
- Active roadmap promotion criteria drafted for ML1 decision.
- Audit checklist drafted for ongoing compliance.

---

## Backlog by Stage (Items, Dependencies, Risks)

### Stage 1 Backlog
- **Inventory map:** Confirm system portfolio boundaries and related repositories.
  - **Dependencies:** None.
  - **Risks:** Overlooking informal artifacts stored outside standard folders.
- **Integration gap scan:** Identify required data sources, credentials, and access models.
  - **Dependencies:** Inventory map.
  - **Risks:** Undocumented access constraints.
- **Agent role discovery:** Define system-level roles and responsibilities at high level.
  - **Dependencies:** Inventory map.
  - **Risks:** Role overlap with matter workflows.

### Stage 2 Backlog
- **Gmail read-only spec:** Required mailbox scopes, retention expectations, audit logging.
  - **Dependencies:** Stage 1 integration gap scan.
  - **Risks:** API limits or policy constraints.
- **SharePoint read-only spec:** Site/library scopes, metadata fields, search behaviors.
  - **Dependencies:** Stage 1 integration gap scan.
  - **Risks:** Permissions complexity and tenant restrictions.
- **Microsoft Word read-only spec:** Document access patterns and extraction needs.
  - **Dependencies:** Stage 1 integration gap scan.
  - **Risks:** File format inconsistencies.
- **Integration comparison matrix:** API vs export vs connector options.
  - **Dependencies:** Gmail/SharePoint/Word specs.
  - **Risks:** Unclear operational cost or compliance impact.

### Stage 3 Backlog
- **Agent roster (5 active system-level agents):**
  - System Governance Agent
  - Portfolio Planning Agent
  - Integration Steward Agent
  - Knowledge Curation Agent
  - Runbook & QA Agent
  - **Dependencies:** Stage 1 agent role discovery.
  - **Risks:** Role ambiguity or duplicated responsibilities.
- **Agent handoff map:** Inputs/outputs per agent, with sequencing.
  - **Dependencies:** Agent roster.
  - **Risks:** Missing ownership for outputs.
- **System runbook outlines:** Draft runbooks for each agent.
  - **Dependencies:** Agent handoff map.
  - **Risks:** Overlap with doctrine or playbooks.

### Stage 4 Backlog
- **Operating cadence draft:** Weekly review, monthly portfolio check-in.
  - **Dependencies:** Stage 3 runbook outlines.
  - **Risks:** Cadence too heavy for ML1.
- **Promotion criteria draft:** Conditions to move draft → active roadmap.
  - **Dependencies:** Stage 1 inventory, Stage 3 agent map.
  - **Risks:** Insufficient clarity for ML1 decision.
- **Audit checklist draft:** Minimal compliance list for system portfolio changes.
  - **Dependencies:** Operating cadence draft.
  - **Risks:** Checklist conflicts with doctrine.

---

## 7-Day Plan (Draft)

**Workstreams:**
- **WS1: Governance + Inventory**
- **WS2: Integrations (Read-Only)**
- **WS3: Agent Orchestration**

**Day 1:**
- WS1: Confirm portfolio boundaries + structure notes.
- WS2: Draft Gmail read-only scope outline.
- WS3: Define 5 agent roles and initial responsibilities.

**Day 2:**
- WS1: Draft system-level risk register for integrations.
- WS2: Draft SharePoint read-only scope outline.
- WS3: Map agent handoffs (input/output artifacts).

**Day 3:**
- WS1: Draft system inventory summary for ML1 review.
- WS2: Draft Microsoft Word read-only scope outline.
- WS3: Draft agent governance guardrails (no doctrine changes).

**Day 4:**
- WS1: Consolidate inventory + gaps for Stage 1 DoD validation.
- WS2: Build integration comparison matrix (API vs export vs connector).
- WS3: Draft runbook outlines per agent.

**Day 5:**
- WS1: Prepare Stage 1 completion package (draft).
- WS2: Draft integration pilot test plan (read-only only).
- WS3: Define system metrics (throughput, audit, reliability).

**Day 6:**
- WS1: Draft roadmap promotion criteria for ML1 decision.
- WS2: Review integration dependencies/risks summary.
- WS3: Draft operating cadence proposal.

**Day 7:**
- WS1: Compile decision questions for ML1.
- WS2: Finalize read-only integration requirements summary.
- WS3: Finalize agent roster + handoff map.

---

## TBD (Placeholder)
- [TBD] Confirm naming conventions for agent artifacts.
- [TBD] Confirm integration logging + retention requirements.
- [TBD] Confirm allowable data extraction formats.

## Decision Questions for ML1
1. Which integration approach is preferred for Gmail/SharePoint/Word (API vs connector vs export)?
2. Are the proposed 5 system-level agents the correct set, or should roles be merged/split?
3. What cadence is acceptable for portfolio review (weekly vs biweekly vs monthly)?
4. What minimum evidence is required to promote this draft roadmap to Active?
5. Are there additional system-level dependencies to include before Stage 2?
