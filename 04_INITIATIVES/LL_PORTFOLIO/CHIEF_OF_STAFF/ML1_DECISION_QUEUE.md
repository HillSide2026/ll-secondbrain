# ML1 Decision Queue

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-16T00:00:00Z, LLM-005 run 2026-03-16T18:00:00Z, LLM-006 run 2026-03-16T18:00:00Z
- Direct file verification: 2026-03-18 (LLP-011, LLP-012 approval records read directly)

> Advisory output. ML1 approval required before any action is taken.

---

## Classification Key

- **ML1_REQUIRED** — Only ML1 can make this decision. Cannot be delegated or handled by system.
- **SYSTEM_CAN_HANDLE** — Artifact production, drafting, or schema correction that does not require ML1 judgment. Can be directed and executed without ML1 involvement beyond scope authorization.

---

## Decision Queue

| Rank | Project | Decision Needed | Classification | Urgency | Blocking | Deadline | Source |
|------|---------|----------------|----------------|---------|----------|----------|--------|
| 1 | LLP-024_NDA_ESQ | Sign metric thresholds in METRICS.md; record Planning→Executing gate decision | ML1_REQUIRED | Critical | Yes — M6 workplan milestone, execution start | 2026-03-20 | LLM-004 Rank 1, LLM-006 High |
| 2 | LLP-006_MAINTENANCE | Governance investigation: were Stage 3 execution artifacts authorized? Decide: retroactive authorization or halt | ML1_REQUIRED | Critical | Yes — governance hold on entire project | None — resolve before next cycle | LLM-006 Critical |
| 3 | LLP-023_MATTER_COMMAND_CONTROL | Decide: retroactively formalize Stage 1 + Stage 2 authorization covering existing scope lock, or require clean gate restart | ML1_REQUIRED | High | Yes — project stage is indeterminate; no authorized work can proceed | None | LLM-006 Critical, LLM-005 Rank 12 |
| 4 | LLP-013_FUNNEL3_MANAGEMENT | Direct production of all Stage 2 planning artifacts (SCOPE_DEFINITION, WORKPLAN, ASSUMPTIONS_CONSTRAINTS, DEPENDENCIES, RISK_REGISTER, COMMUNICATION_PLAN, METRICS) | SYSTEM_CAN_HANDLE (with ML1 direction) | High | Yes — Planning stage authorized but stalled; cash-flow funnel | None | LLM-004 Rank 3, LLM-005 Rank 4 |
| 5 | LLP-004_ONBOARDING | Sign ML1_METRIC_APPROVAL.md; record Planning→Executing gate decision | ML1_REQUIRED | Medium | Yes — blocks LLP-005 Opening downstream | None | LLM-004 Rank 6, LLM-006 High |
| 6 | LLP-005_OPENING | Sign ML1_METRIC_APPROVAL.md; record Planning→Executing gate decision (after LLP-004) | ML1_REQUIRED | Medium | Yes — blocks LLP-006 Maintenance downstream | Sequence: after LLP-004 | LLM-004 Rank 7, LLM-006 High |
| 7 | LLP-012_FUNNEL2_MANAGEMENT | Define Corporate Health Check pricing, delivery scope, monthly capacity ceiling, and practice area stops before launch planning can proceed | ML1_REQUIRED | Medium | Yes — these decisions gate Planning deliverables | Before launch readiness review | LLM-004 Rank 4 (now in Planning) |
| 8 | LLP-002_CORPORATE_CLERK | Sign APPROVAL_RECORD.md to authorize Planning (batch with LLP-003) | ML1_REQUIRED | Medium | Yes — prerequisite for LLP-009_CLERK_SUPERVISION | None | LLM-004 Rank 9, LLM-006 Medium |
| 9 | LLP-003_ASSOCIATE_LAWYER | Sign APPROVAL_RECORD.md to authorize Planning (batch with LLP-002) | ML1_REQUIRED | Medium | Yes — prerequisite for LLP-010_ASSOCIATE_SUPERVISION | None | LLM-004 Rank 10, LLM-006 Medium |
| 10 | LLP-001_CORPORATE_ENTITY_MANAGEMENT | Sign APPROVAL_RECORD.md to authorize Planning | ML1_REQUIRED | Medium | No downstream dependency currently | None | LLM-004 Rank 8 |
| 11 | LLP-004_PARTNER_SUPERVISION | Sign APPROVAL_RECORD.md to authorize Planning | ML1_REQUIRED | Medium | No downstream dependency currently | None | LLM-004 Rank 11 |
| 12 | Project ID collision (LLP-26-24) | Verify and resolve duplicate project ID between LLP-024 and LLP-011; LLP-011 actual record shows LLP-26-11, suggesting agents misread. Confirm canonical ID assignment. | SYSTEM_CAN_HANDLE (with ML1 confirmation) | Low | No — governance hygiene issue, not execution blocker | Before next governance audit | LLM-006 Critical |
| 13 | Placeholder shells (9 projects) | Single batch decision: park or define each of 09_SERVICE_MANAGEMENT (×5), PORTFOLIO_MANAGEMENT, LLP-017, LLP-009, LLP-010 | ML1_REQUIRED | Low | No — these are shell projects with no execution content | None | LLM-004 Rank 13–15, LLM-006 Low |
| 14 | Split metric schema correction | Update project template to use canonical METRICS.md instead of four-file split schema | SYSTEM_CAN_HANDLE | Low | No — governance debt; affects future projects | Before next Stage 2 initiation | LLM-006 Doctrine Drift |

---

## Queue Notes

**Ranking logic:**

Rank 1 is assigned on calendar deadline: NDA_ESQ M6 gate closes 2026-03-20, two days from today. This project also carries the highest direct cash-flow potential as the portfolio's only SaaS product initiative.

Rank 2 is a governance investigation, not an approval action. It is ranked ahead of all other approval items because the condition — Stage 3 execution with no authorization at any stage — is the most structurally dangerous finding in the portfolio. Until it is resolved, LLP-006 cannot be sequenced into the Firm Operations pipeline.

Rank 3 (LLP-023) is a governance-vs-momentum decision: ML1 already invested in this project via the March 4 scope lock. The question is whether to ratify that investment with formal gate documentation or require a restart. This should be resolved in the same session as Rank 2 given both involve retroactive authorization analysis.

Ranks 4, 5, 6 (LLP-013 + LLP-004 Onboarding + LLP-005 Opening) can be batched. LLP-013 requires system execution of planning artifacts; LLP-004 and LLP-005 require ML1 signatures only. Recommend a single 45-minute session for all three.

Ranks 8, 9, 10, 11 (LLP-002, LLP-003, LLP-001, LLP-004_PARTNER) are all initiation signatures on complete, substantive packets. A single batch review session of approximately 30 minutes clears all four.

Rank 7 (LLP-012 Funnel 2 ML1 decisions) is medium urgency but high strategic weight. The decisions (Corporate Health Check price, capacity ceiling, practice area stops) are foundational to the Planning workplan. Deferring these too long will cause the same stall pattern seen in LLP-013.

Rank 13 (placeholder shells) represents the single largest opportunity to clear queue depth quickly. Nine items removed in one decision, no substantive review required.

**Items resolved since last agent run (2026-03-16) — no longer in queue:**

- LLP-011_FUNNEL1_MANAGEMENT: Metric thresholds approved 2026-03-16; Planning→Executing gate authorized. Now in Executing. Baseline metrics due within 30 days.
- LLP-012_FUNNEL2_MANAGEMENT initiation decision: Approved to advance 2026-03-16. Now in Planning.
