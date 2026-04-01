# ML1 Decision Queue

- Generated: 2026-04-01T00:00:00+00:00
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-20T02:27:05+00:00, LLM-005 run 2026-03-20T02:27:05+00:00, LLM-006 run 2026-03-20T02:27:05+00:00

> Advisory output. ML1 approval required before any action is taken.

**Input staleness notice:** Management agent inputs are 12 days old (generated 2026-03-20). Git history between March 20 and April 1 shows material execution activity in LLP-024 (NDA Esq landing page) and LLP-012 (F02 blog content, linking/tagging scripts). These events are not reflected in agent outputs. A fresh LLM-004, LLM-005, LLM-006 run is recommended before acting on any queue item.

---

## Decision Queue

| Rank | Project | Decision Needed | Cash Flow Impact | ML1 or System | Urgency | Blocking | Source |
|------|---------|----------------|-----------------|---------------|---------|----------|--------|
| 1 | LLP-012 Funnel 2 Management | Confirm Planning-to-Executing gate status: was the gate formally approved after 2026-03-20? If yes, direct ML2 to record it in APPROVAL_RECORD.md. If no, confirm F02 blog content and scripts are pre-execution preparatory work and gate remains open. | direct | ML1_REQUIRED | high | yes — gate status ambiguity means F02 execution artifacts have no confirmed authorization basis | LLM-006 (APPROVAL_RECORD.md and 6 planning artifacts missing), git history 2026-03-20 to 2026-04-01 |
| 2 | LLP-012 Funnel 2 Management | Provide three F02 capacity decisions: (a) maximum active matter count ceiling, (b) minimum projected matter value floor for new corporate work, (c) practice area categories to stop accepting to protect F02 capacity | direct | ML1_REQUIRED | high | yes — six missing planning artifacts cannot be written without these inputs; GHL ICP gate cannot be confirmed as correctly configured | LLM-004 (at-risk, 6 gaps), LLM-005 (Priority Rank 1 score 23), LLP-012 PROJECT_CHARTER.md Section 5 |
| 3 | LLP-011 Funnel 1 Management | Define the F01 matter value floor (minimum acceptable fee per matter retained from F01 spend); then review and approve consolidated METRICS.md including the >2.0x ROAS hypothesis as a formal governance threshold or redirect | direct | ML1_REQUIRED | high | yes — live intake funnel has no formally approved measurement baseline; F01 investment decision has no governance trigger | LLM-006 (METRICS.md missing), LLM-005 (watch, Rank 20), LLP-025 METRIC_FRAMEWORK.md |
| 4 | LLP-024 NDA Esq | Authorize ML2 to update EXECUTION_LOG.md and DELIVERABLES_TRACKER.md to reflect execution events since 2026-03-19 (landing page completion at minimum); confirm whether May 18, 2026 MVP deadline is actively tracked | direct | ML1_REQUIRED | high | yes — executing project has no governance record of its primary post-authorization event; 60-day MVP deadline is 47 days away | LLM-004 (on-track), git history (NDA Esq landing page committed post-March 20) |
| 5 | LLP-025 Marketing Strategy | Review and approve METRIC_FRAMEWORK.md as canonical METRICS.md; decide Planning-to-Executing gate | indirect | ML1_REQUIRED | medium-high | yes — downstream intake and lead capture projects (LLP-027, LLP-028, LLP-029, LLP-026) cannot be formally scoped without LLP-025 gate closure | LLM-006 (METRICS.md missing), LLM-005 (watch, Rank 21), LLM-004 (watch) |
| 6 | LLP-030 Firm Strategy | Complete or authorize drafting of BUSINESS_CASE.md and formally close the initiation gate | indirect | ML1_REQUIRED | medium | yes — firm strategy cannot become the governing frame for downstream strategic and marketing sequencing | LLM-006 (BUSINESS_CASE.md missing), LLM-005 (at-risk), LLM-004 (at-risk) |
| 7 | LLP-004 Onboarding | Review and approve METRICS.md to clear the watch-status planning gate gap | none near-term | ML1_REQUIRED | medium | yes — planning gate cannot advance without metric approval | LLM-006 (METRICS.md missing), LLM-004 (watch) |
| 8 | LLP-007, LLP-008, LLP-016 (batch) | Sign APPROVAL_RECORD.md for each initiating project or explicitly direct park | none near-term | ML1_REQUIRED | low-medium | yes — each is frozen at initiation gate; three approval gap entries per governance cycle | LLM-006 (APPROVAL_RECORD.md missing x3), LLM-005 (at-risk Ranks 11-13) |
| 9 | LLP-031, LLP-032, LLP-033 (batch) | Complete BUSINESS_CASE.md or explicitly park each growth project placeholder | none near-term | ML1_REQUIRED | low-medium | yes — initiation gate frozen x3; inflating at-risk count | LLM-006 (BUSINESS_CASE.md missing x3), LLM-005 (at-risk Ranks 14-17) |
| 10 | LLP-015, LLP-035, LLP-036 (batch) | Formalise or park these three practice area placeholder projects (7 missing initiation artifacts each) | none near-term | ML1_REQUIRED | low | partial — 21 total missing artifact entries; no portfolio output | LLM-006 (Stage Gate Violations), LLM-005 (at-risk Ranks 2-4) |
| 11 | LLP-014, LLP-026, LLP-027, LLP-028, LLP-029, LLP-043 (batch) | Formalise or park these six unstaged marketing and governance placeholder projects (6 missing initiation artifacts each) | none near-term | ML1_REQUIRED | low | partial — 36 total missing artifact entries; largest source of governance noise | LLM-006 (APPROVAL_RECORD.md missing x6), LLM-005 (at-risk Ranks 5-10) |
| 12 | LLP-037, LLP-038, LLP-039, LLP-040, LLP-041 (batch) | Define substantive content, consolidate, or formally park the 09_SERVICE_MANAGEMENT cluster | none near-term | ML1_REQUIRED | low | no | LLM-004 (on-track x5), LLM-005 |
| 13 | Fresh agent run (LLM-004, LLM-005, LLM-006) | Trigger refresh of all management agent outputs before acting on any queue item | n/a | SYSTEM_CAN_HANDLE | high | no — staleness risk only; 12-day gap with known execution events not yet captured | LLM-001 |
| 14 | LLP-012 six planning artifact drafting | After ML1 provides capacity decisions (Rank 2), agents draft SCOPE_STATEMENT.md, PROJECT_PLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md | direct | SYSTEM_CAN_HANDLE | high (pending Rank 2) | yes — unblocked by ML1 capacity decisions | LLM-004, LLM-005 |
| 15 | LLP-011 and LLP-025 METRICS.md consolidation | Agents consolidate existing split-schema measurement files into draft canonical METRICS.md for ML1 review and approval | direct/indirect | SYSTEM_CAN_HANDLE | high (pending Ranks 3, 5) | yes — unblocked by ML1 approval | LLM-004, LLM-006 |
| 16 | LLP-024 EXECUTION_LOG and DELIVERABLES_TRACKER update | After ML1 authorization (Rank 4), agents update execution log to reflect post-March 19 events | direct | SYSTEM_CAN_HANDLE | high (pending Rank 4) | yes — unblocked by ML1 authorization | LLM-004 |

---

## Queue Notes

**Ranking logic:** Ranks 1–4 are ordered by direct cash flow impact. LLP-012 gate confirmation (Rank 1) is highest because execution may be occurring without authorization — a governance integrity issue, not just a compliance flag. LLP-012 capacity decisions (Rank 2) immediately follow because they are the input that unlocks the planning gate. LLP-011 METRICS.md (Rank 3) is the live funnel governance gap. LLP-024 (Rank 4) is an executing project with an approaching deadline that needs its record updated. Ranks 5–6 are indirect cash flow. Ranks 7–12 are governance cleanup with no near-term revenue effect. Ranks 13–16 are SYSTEM_CAN_HANDLE items included for completeness, sequenced behind the ML1_REQUIRED decisions they depend on.

**Ranks 1 and 2 can be addressed in a single ML1 session.** The gate confirmation and the capacity decisions are naturally connected — ML1 will likely resolve both simultaneously when reviewing F02 status.

**Ranks 3 and 5 are substantively linked.** The F01 matter value floor (Rank 3) is referenced as an open ML1 decision in the LLP-025 METRIC_FRAMEWORK.md (Rank 5). A single review session covering F01 performance data and the marketing strategy metrics framework resolves both.

**Ranks 8, 9, 10, 11, and 12 are all batchable.** These 15 projects require either a simple sign-off or a park decision. A single portfolio cleanup session could resolve all of them, reducing the at-risk count by up to 13 projects and eliminating approximately 75 missing artifact entries from future governance reports.

**Dependency chain for cash-flow items:**

LLP-012 capacity decisions (ML1, Rank 2) → system drafts six planning artifacts (Rank 14) → ML1 reviews and approves → planning gate closes → LLP-012 advances to authorized execution.

LLP-011 METRICS.md consolidation (system, Rank 15) → ML1 approves (Rank 3) → governance hold lifted, F01 funnel fully governed.

LLP-025 METRICS.md consolidation (system, Rank 15) → ML1 approves and decides gate (Rank 5) → downstream intake and lead capture sequencing can proceed.

LLP-024 execution log update (system, Rank 16) → authorized by ML1 (Rank 4) → governance record reflects actual delivery state.
