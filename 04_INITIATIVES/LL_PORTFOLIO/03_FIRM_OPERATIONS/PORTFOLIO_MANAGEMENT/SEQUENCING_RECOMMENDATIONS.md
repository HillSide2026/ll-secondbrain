# Sequencing Recommendations

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Recommended ML1 Attention Sequence

1. **LLP-030 Firm Strategy** — Approve initiation before any other strategic project is advanced to Planning. This is the governing frame for LLP-001, LLP-002, LLP-003, LLP-011, LLP-012, LLP-013, and LLP-025. Without it, Planning stage work for those seven projects may produce direction inconsistent with the firm's 3-year strategy. A single ML1 signature here removes the strategic lock from the entire portfolio.

2. **Project ID Collision (LLP-012 / LLP-025)** — Resolve the LLP-26-25 collision before either project advances to Executing. Both LLP-012 Funnel 2 Management and LLP-025 Marketing Strategy carry this ID; audit records are ambiguous. This is a 5-minute administrative action with material governance consequences if deferred.

3. **LLP-024 NDA Esq** — Create all 6 Stage 3 execution artifacts (EXECUTION_LOG.md, DECISION_LOG.md, CHANGE_LOG.md, ISSUE_LOG.md, DELIVERABLES_TRACKER.md, QA_CHECKLIST.md) and confirm Product, Growth, and Operations lead assignments. Execution was authorized today; the three-workstream structure means that without artifacts, progress across all workstreams is invisible to governance.

4. **LLP-013 Funnel 3 Mgmt** — Review and approve METRICS.md; approve the Planning->Executing gate. RPAA registration deadline is 2026-03-31 — the first execution milestone (organic RPAA content) has a hard external calendar dependency. Advancing this gate now preserves the ability to publish time-sensitive content within the deadline window.

5. **LLP-025 Marketing Strategy** — Review METRIC_FRAMEWORK.md (non-canonical naming: should be METRICS.md) and approve or hold the Planning->Executing gate. LLP-025 governs the strategy for all three funnels and unblocks F02 launch architecture, F01 wind-down framework, and agent activation. Advancing LLP-025 to Executing before advancing LLP-012 and LLP-013 is the correct sequence — the strategy layer should be authorized before its sub-projects execute.

6. **LLP-006 Matter Maintenance** — Locate or create execution artifacts in implementation/ before the next maintenance cycle. The execution cycle has retroactive approval (2026-03-18) but is ungoverned at the artifact level. This is an operational risk, not a planning risk — the function may be running without audit trail.

7. **LLP-011 Funnel 1 Mgmt** — Create Stage 3 execution artifacts and confirm the 30-day metric baseline window start date. The funnel is live and generating leads, but the governance layer is absent. This is a lower-urgency item than LLP-024 only because F01 is an established channel rather than a new launch.

8. **LLP-005 Opening** — Confirm whether execution is intentionally deferred or should be active. If active, direct creation of all Stage 3 execution artifacts. LLP-005 depends on LLP-004 Onboarding handoff being operational — verify that cadence is running before directing execution artifact creation.

9. **LLP-002 + LLP-003 (batch together)** — Sign APPROVAL_RECORD.md for Corporate Clerk and Associate Lawyer in a single session. Both are substantive initiation packets. Approving them unblocks LLP-009 and LLP-010 from being substantively defined. Hold Planning advancement for both until LLP-030 is approved.

10. **09_SERVICE_MANAGEMENT cluster** — Make a single batch decision on the 5 placeholder shells (LLP-26-28 through LLP-26-32): define individually, collapse into one service management governance project, or formally park. This removes between 5 and 30 phantom WIP items from the portfolio with one decision.

11. **LLP-012 Funnel 2 Mgmt** — Once LLP-025 has advanced to Executing and the Project ID collision is resolved, direct creation of the 6 missing Stage 2 planning artifacts and provide the 3 ML1 capacity decisions (active matter ceiling, matter value floor, practice area exclusions). LLP-025 must advance first because LLP-025 governs F02 launch strategy; LLP-012 executes it.

12. **LLP-023 Matter Command & Control** — Issue a canonical stage gate decision to formalize the 2026-03-04 scope lock. Decide whether Slice 1 production governance is authorized or whether a full Stage 2 artifact set is required first.

---

## Dependency-Driven Sequencing Constraints

- **LLP-030 must be approved before LLP-001, LLP-002, LLP-003, LLP-011, LLP-012, LLP-013, and LLP-025 advance to Planning** — all seven projects have a documented strategic dependency on an approved Firm Strategy before their own planning directions can be confirmed as correct.

- **LLP-025 Marketing Strategy should advance to Executing before LLP-012 Funnel 2 and LLP-013 Funnel 3 execute** — LLP-025 DEPENDENCIES.md confirms that LLP-025 governs the strategic layer; LLP-012 and LLP-013 execute within that governing frame. Authorizing execution at the sub-funnel level before the strategy layer is authorized inverts the governance hierarchy.

- **LLP-004 Onboarding must be confirmed operational before LLP-005 Opening is activated** — LLP-005 DEPENDENCIES.md records a hard dependency on a Gate 2-authorized packet from LLP-004. LLP-005 cannot receive matters that LLP-004 has not processed. LLP-004 is currently on-track and in Executing; the handoff cadence must be confirmed active before directing LLP-005 execution.

- **LLP-005 Opening must be operational before LLP-006 Maintenance is expected to govern opened matters** — LLP-006 DEPENDENCIES.md confirms that the maintenance function governs matters that have been opened. Running maintenance cycles on matters that have not gone through a formal Opening function creates reconciliation anomalies.

- **LLP-002 Corporate Clerk must produce an approved role definition before LLP-009 Clerk Supervision can be substantively scoped** — LLP-009 is a supervision framework that has no content to supervise until the Clerk role is defined.

- **LLP-003 Associate Lawyer must produce an approved role definition before LLP-010 Associate Supervision can be substantively scoped** — same logic as LLP-002/LLP-009.

- **LLP-013 Funnel 3 channel activation (WS-3) depends on LLP-025 IMP-01 (3+ accountant referral relationships)** — per LLP-013 DEPENDENCIES.md, SPE-01 activation (which drives F3 authority hooks at scale) is gated on LLP-025 reaching the accountant referral milestone. F3 organic content at scale requires LLP-025 to be executing.

- **LLP-013 Funnel 3 SEO content depends on LLP-012 Funnel 2 website going live** — per LLP-013 DEPENDENCIES.md, BSE-01 (Blog/SEO Engine) is blocked until the levine-law.ca traffic baseline is established, which requires the F02 website to be live. F3 SEO is a Phase 2 activity, not a near-term gate.

- **Project ID collision must be resolved before LLP-012 or LLP-025 can be considered fully governed** — both carry LLP-26-25; whichever receives the new canonical ID will need its APPROVAL_RECORD.md corrected before the record can be relied on for gate decisions.
