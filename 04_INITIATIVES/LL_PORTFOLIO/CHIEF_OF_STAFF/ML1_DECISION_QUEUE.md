# ML1 Decision Queue

- Generated: 2026-03-18T12:00:00Z
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-18T00:00:00Z, LLM-005 run 2026-03-18T00:00:00Z, LLM-006 run 2026-03-18T00:00:00Z

> Advisory output. ML1 approval required before any action is taken.

---

## Decision Queue

| Rank | Project | Decision Needed | Urgency | Blocking | Source |
|------|---------|----------------|---------|----------|--------|
| 1 | LLP-030 Firm Strategy | Sign initiation APPROVAL_RECORD.md — governing frame for entire strategic portfolio; 7 projects cannot advance to Planning until this is done | high | yes — LLP-001, LLP-002, LLP-003, LLP-011, LLP-012, LLP-013, LLP-025 all hold on this | LLM-004, LLM-005 |
| 2 | LLP-013 Funnel 3 (cross-agent conflict) | Resolve approval record integrity issue: locate or produce the 6 Stage 2 artifacts that APPROVAL_RECORD.md claims are drafted but do not exist on disk; then decide Planning→Executing gate | high | yes — RPAA content window closes 2026-03-31; external deadline | LLM-005, LLM-006 |
| 3 | LLP-024 NDA Esq | Direct immediate creation of all 6 Stage 3 execution artifacts; confirm Product, Growth, and Operations workstream lead assignments | high | yes — three-workstream launch has zero governance artifacts; execution authorized today | LLM-004, LLM-005 |
| 4 | LLP-025 Marketing Strategy (cross-agent conflict) | Consolidate non-canonical metric schema into METRICS.md; sign ML1 metric approval; decide Planning→Executing gate | high | yes — LLM-005 recommends advancing before LLP-012 and LLP-013 execute; metric schema gap blocks clean gate closure | LLM-005, LLM-006 |
| 5 | LLP-012 / LLP-025 Project ID Collision (LLP-26-25) | Assign LLP-012 a new unique project ID; update PROJECT_CHARTER.md and APPROVAL_RECORD.md for LLP-012; update any LLP-025 cross-references | high | yes — both projects are ungovernable as a pair until resolved; audit trail ambiguity | LLM-006, LLM-004 |
| 6 | LLP-012 Funnel 2 (after ID collision resolved) | Update LLP-012 charter stage field to "Planning"; direct creation of 6 missing Stage 2 planning artifacts; provide 3 ML1 capacity decisions: active matter ceiling, matter value floor, practice area exclusions | medium | yes — F02 launch planning cannot close without these decisions | LLM-004, LLM-005 |
| 7 | LLP-023 Matter Command and Control | Issue a canonical Initiating stage gate decision to replace the informal 2026-03-04 scope lock; complete RISK_SCAN.md Go/No-Go judgment | medium | yes — project stage is indeterminate; no authorized work can proceed until formalized | LLM-006, LLM-004 |
| 8 | LLP-006 Matter Maintenance | Locate or direct creation of execution artifacts in implementation/; confirm whether the matter maintenance cycle is actually running and where its outputs are | medium | yes — execution authorized retroactively but ungoverned at artifact level | LLM-004, LLM-005 |
| 9 | LLP-011 Funnel 1 Management | Direct creation of all 6 Stage 3 execution artifacts; confirm 30-day metric baseline window start date | medium | yes — funnel is live; execution authorized 2026-03-16; zero governance artifacts | LLM-004, LLM-005 |
| 10 | LLP-005 Opening | Confirm whether execution is intentionally deferred or should be active; if active, direct creation of all Stage 3 execution artifacts | medium | yes — execution authorized 2026-03-16; handoff from LLP-004 must be confirmed active first | LLM-004, LLM-005 |
| 11 | LLP-001, LLP-002, LLP-003, LLP-004 Partner Supervision (batch) | Add BUSINESS_CASE.md to each (required for Strategic Project type per PROJECT_POLICY.md §7); then sign APPROVAL_RECORD.md for each. Hold Planning advancement pending LLP-030 approval. | low | partial — LLP-002 blocks LLP-009; LLP-003 blocks LLP-010; LLP-001 and LLP-004 Partner have no immediate downstream dependency | LLM-004, LLM-006 |
| 12 | Project ID collision LLP-26-11 (PORTFOLIO_MANAGEMENT vs. LLP-011) | Assign PORTFOLIO_MANAGEMENT a new unique project ID; update its APPROVAL_RECORD.md and PROJECT_CHARTER.md | low | no — LLP-011 is active and retains LLP-26-11; PORTFOLIO_MANAGEMENT is a shell | LLM-006 |
| 13 | 09_SERVICE_MANAGEMENT cluster (5 shell projects) | Single batch decision: define with substantive charter content, collapse into one service management governance project, or formally park all five | low | no — placeholder shells with no execution content | LLM-004, LLM-005, LLM-006 |
| 14 | PORTFOLIO_MANAGEMENT shell, LLP-017 Strategic Risk | Define charter content or formally park; both are ungovernable shells | low | no | LLM-004, LLM-006 |

---

## Queue Notes

**Ranking logic:**

Rank 1 (LLP-030) is the master lock for the strategic cluster. A single signature removes the strategic dependency block from seven projects simultaneously. There is no deadline but the compounding cost of deferral is high — the longer it waits, the more Planning-stage work proceeds without confirmed strategic direction.

Rank 2 (LLP-013) is ranked second because of the hard external RPAA deadline (2026-03-31) and because it is the sharpest cross-agent conflict in this cycle. The approval record integrity violation discovered by LLM-006 means the gate cannot be cleanly authorized until the artifact discrepancy is resolved. Time available before the deadline narrows with each day deferred.

Ranks 3–5 (LLP-024, LLP-025, ID collision) are all high urgency. LLP-024 is the primary cash-flow vehicle and was authorized today — it needs governance artifacts immediately. LLP-025 and the ID collision are linked: LLM-005 recommends advancing LLP-025 before LLP-012 and LLP-013, so LLP-025 gate and ID collision resolution should be handled in the same session.

Rank 6 (LLP-012) follows resolution of Rank 5. LLP-012 cannot be properly governed until it has a clean ID, and its planning workplan cannot be completed until ML1 provides the three capacity decisions.

Ranks 7–10 (LLP-023, LLP-006, LLP-011, LLP-005) are execution governance items. They can be handled as a focused batch in a single 45-minute session. LLP-006 and LLP-011 should be prioritized within this batch because the matter maintenance cycle and Funnel 1 are both operationally live without audit trails.

Rank 11 (LLP-001/002/003/004 Partner batch) is a batch signing session. Each project needs BUSINESS_CASE.md added before the signature is clean. Recommend handling as one session after LLP-030 is approved, since LLP-030 approval is a prerequisite for advancing any of these to Planning.

Ranks 12–14 are queue hygiene items with no execution blockers. Deferred.

**Items resolved since prior cycle (2026-03-16) — no longer in queue:**

- LLP-006 Maintenance unauthorized execution: RESOLVED. ML1 retroactively authorized Planning→Executing gate on 2026-03-18.
- LLP-024 NDA Esq metric approval: RESOLVED. ML1 approved Planning→Executing gate 2026-03-18.
- LLP-011 Funnel 1 metric approval: RESOLVED. ML1_METRIC_APPROVAL.md approved 2026-03-16.
- LLP-004 Onboarding metric approval: RESOLVED. ML1_METRIC_APPROVAL.md approved 2026-03-16.
- LLP-005 Opening metric approval: RESOLVED. ML1_METRIC_APPROVAL.md approved 2026-03-16.
- LLP-012 Funnel 2 initiation gate: RESOLVED. ML1 approved Initiating→Planning on 2026-03-16.
- LLP-025 Marketing Strategy initiation gate: RESOLVED. Approved 2026-03-17.
