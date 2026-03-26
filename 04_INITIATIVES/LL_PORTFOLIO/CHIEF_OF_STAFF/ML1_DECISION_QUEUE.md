# ML1 Decision Queue

- Generated: 2026-03-25T00:00:00+00:00
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-20T02:27:05+00:00, LLM-005 run 2026-03-20T02:27:05+00:00, LLM-006 run 2026-03-20T02:27:05+00:00

> Advisory output. ML1 approval required before any action is taken.

**Input staleness notice:** Management agent inputs are 5 days old (generated 2026-03-20). A fresh agent run is recommended before acting on any item whose status may have changed.

---

## Decision Queue

| Rank | Project | Decision Needed | Cash Flow Impact | ML1 or System | Urgency | Blocking | Source |
|------|---------|----------------|-----------------|---------------|---------|----------|--------|
| 1 | LLP-012 Funnel 2 Management | Provide three capacity decisions: (a) matter ceiling, (b) value floor, (c) practice area exclusions for F02, then approve six missing planning artifacts | direct | ML1_REQUIRED | high | yes — F02 planning gate cannot close; execution cannot begin | LLM-004, LLM-005, LLM-006 |
| 2 | LLP-011 Funnel 1 Management | Approve consolidated METRICS.md for live F01 intake funnel; record ML1 metric approval | direct | ML1_REQUIRED | high | yes — live funnel is ungoverned at the measurement layer | LLM-004, LLM-005, LLM-006 |
| 3 | LLP-025 Marketing Strategy | Approve canonical METRICS.md and decide Planning-to-Executing gate | indirect | ML1_REQUIRED | high | yes — upstream marketing gate blocks downstream funnel sequencing | LLM-004, LLM-005, LLM-006 |
| 4 | LLP-030 Firm Strategy | Sign initiation APPROVAL_RECORD.md and lock strategic frame (BUSINESS_CASE.md required) | indirect | ML1_REQUIRED | high | yes — strategic frame blocks clean sequencing of strategic and marketing downstream work | LLM-004, LLM-005, LLM-006 |
| 5 | LLP-015, LLP-035, LLP-036 (batch) | Formalise or park decision for three unstaged projects each missing all 7 initiation artifacts | none near-term | ML1_REQUIRED | medium | partial — inflating at-risk count and consuming governance cycle; no direct delivery block | LLM-004, LLM-005, LLM-006 |
| 6 | LLP-014, LLP-026, LLP-027, LLP-028, LLP-029, LLP-043 (batch) | Formalise or park decision for six unstaged projects each missing 6 initiation artifacts | none near-term | ML1_REQUIRED | medium | partial — same as above; largest single source of governance noise in the portfolio | LLM-004, LLM-005, LLM-006 |
| 7 | LLP-007, LLP-008, LLP-016 (batch) | Sign APPROVAL_RECORD.md or formally park each of the three initiating projects | none near-term | ML1_REQUIRED | medium | yes — each is blocked at initiation gate | LLM-004, LLM-006 |
| 8 | LLP-031, LLP-032, LLP-033 (batch) | Complete BUSINESS_CASE.md or formally defer initiation for each project | none near-term | ML1_REQUIRED | medium | yes — blocked at initiation gate | LLM-004, LLM-006 |
| 9 | LLP-004 Planning | Approve METRICS.md to close measurement gap and unblock planning gate advancement | none near-term | ML1_REQUIRED | low | yes — cannot advance planning stage without metric approval | LLM-004, LLM-006 |
| 10 | LLP-023 Matter Command and Control | Record one canonical stage decision and confirm go/no-go posture | none near-term | ML1_REQUIRED | low | no — stage ambiguity is a governance reporting issue, not an execution block | LLM-004, LLM-005, LLM-006 |
| 11 | LLP-005 Opening | Confirm whether execution is active; if yes, direct creation of canonical Stage 3 execution packet | none near-term | ML1_REQUIRED | low | no — watch status reflects governance packaging gap | LLM-004, LLM-005 |
| 12 | Fresh agent run (LLM-004, LLM-005, LLM-006) | Trigger refresh of all management agent outputs before acting on queue items | n/a | SYSTEM_CAN_HANDLE | high | no — staleness risk only | LLM-001 |
| 13 | LLP-012 six planning artifact drafting | After ML1 provides capacity decisions, agents draft SCOPE_STATEMENT.md, PROJECT_PLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md | direct | SYSTEM_CAN_HANDLE | high (pending Rank 1) | yes — unblocked by ML1 capacity decisions | LLM-004, LLM-005 |
| 14 | LLP-011 and LLP-025 METRICS.md consolidation | Agents consolidate split-schema measurement files into draft canonical METRICS.md for ML1 review | direct/indirect | SYSTEM_CAN_HANDLE | high (pending Ranks 1-2) | yes — unblocked by ML1 approval | LLM-004, LLM-006 |
| 15 | LLP-037 through LLP-041 service cluster | Single define/consolidate/park decision across all five initiating shells | none near-term | ML1_REQUIRED | low | no | LLM-004, LLM-005 |

---

## Queue Notes

**Ranking logic:**

Ranks 1 through 4 are ordered by direct cash flow impact. LLP-012 (F02, Rank 1) is ranked above LLP-011 (F01, Rank 2) because LLP-012 is completely blocked at the planning gate — nothing can advance — while LLP-011 is in live execution and the governance gap is a compliance issue rather than an execution stop. LLP-025 (Rank 3) is the highest-leverage indirect cash flow item because it governs the downstream marketing sequence. LLP-030 (Rank 4) is the cleanest single-decision unlock for strategic portfolio clarity.

Ranks 5 and 6 are batched formalise/park decisions. The nine projects in these two rows are the largest single source of governance noise and at-risk inflation in the portfolio. Resolving them as a batch — even with a simple park decision — would materially reduce the compliance load on every future cycle.

Ranks 7 and 8 are initiation gate holds. All six projects (LLP-007, LLP-008, LLP-016, LLP-031, LLP-032, LLP-033) require a single artifact each; they can be reviewed and signed off in one batch session.

Ranks 9 through 11 are watch-status cleanup items. They matter but do not carry time-sensitive execution pressure.

Ranks 12 through 14 are SYSTEM_CAN_HANDLE items included in the queue for completeness. They are sequenced behind the ML1_REQUIRED decisions they depend on.

Rank 15 is a low-urgency portfolio shaping decision that can be deferred until higher-priority items are resolved.

**Dependency chain for cash-flow items:**

LLP-012 capacity decisions (ML1, Rank 1) → system drafts six planning artifacts (Rank 13) → ML1 reviews and approves → planning gate closes → LLP-012 advances to execution.

LLP-011 METRICS.md consolidation (system, Rank 14) → ML1 approves (Rank 2) → governance hold lifted, funnel fully governed.

LLP-025 METRICS.md consolidation (system, Rank 14) → ML1 approves and decides gate (Rank 3) → downstream marketing sequencing can proceed.
