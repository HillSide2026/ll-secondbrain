# ML1 Decision Queue

- Generated: 2026-03-19T06:14:19+00:00
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-19T06:14:19+00:00, LLM-005 run 2026-03-19T06:14:19+00:00, LLM-006 run 2026-03-19T06:14:19+00:00

> Advisory output. ML1 approval required before any action is taken.

---

## Decision Queue

| Rank | Project | Decision Needed | Urgency | Blocking | Source |
|------|---------|----------------|---------|----------|--------|
| 1 | LLP-030 Firm Strategy | Sign initiation APPROVAL_RECORD.md and lock the strategic frame for downstream strategic and marketing work | high | yes — governing frame for strategic portfolio direction and marketing sequencing | LLM-004, LLM-005 |
| 2 | LLP-025 Marketing Strategy | Consolidate planning measurement artifacts into canonical METRICS.md, record ML1 metric approval, and decide Planning -> Executing gate | high | yes — strategy layer remains the cleanest upstream marketing gate still open | LLM-004, LLM-005, LLM-006 |
| 3 | LLP-012 Funnel 2 Management | Complete the 6 missing Stage 2 planning artifacts and provide the 3 ML1 capacity decisions (matter ceiling, value floor, practice area exclusions) | high | yes — F02 planning cannot close cleanly without these decisions | LLM-004, LLM-005 |
| 4 | LLP-005 Opening | Confirm whether execution should now be active and, if yes, direct creation of the canonical Stage 3 execution packet | medium | yes — opening is the operational bridge from onboarding to maintenance | LLM-004, LLM-005 |
| 5 | LLP-011 Funnel 1 Management | Consolidate split-schema planning measurement artifacts into METRICS.md and formalize the live execution packet location | medium | yes — funnel is active, but governance packaging still needs cleanup | LLM-004, LLM-006 |
| 6 | LLP-023 Matter Command and Control | Record one canonical stage decision and complete ML1 go / no-go posture so the project stops reading differently across reports | medium | yes — stage ambiguity still weakens sequencing and governance interpretation | LLM-004, LLM-005, LLM-006 |
| 7 | LLP-031 / LLP-032 / LLP-033 / LLP-034 (batch) | Decide whether to complete the missing planning packets now or hold these projects in controlled planning pending broader strategic timing | medium | partial — these projects are defined enough to stay visible but not ready to advance cleanly | LLM-004, LLM-005 |
| 8 | 09_SERVICE_MANAGEMENT cluster | Make a single define / consolidate / park decision for LLP-037 through LLP-041 | low | no — packets are structurally valid but still placeholder-heavy | LLM-004, LLM-005, LLM-006 |
| 9 | LLP-026 / LLP-027 / LLP-028 / LLP-029 / LLP-043 (batch) | Decide whether to formalize initiation packets for the unstaged marketing and governance stubs or explicitly park them | low | no — current risk is inventory drag, not execution risk | LLM-004, LLM-005 |
| 10 | LLP-042 PORTFOLIO_MANAGEMENT and LLP-017 Strategic Risk | Either define substantive initiation content or formally park both shells | low | no | LLM-004, LLM-006 |

---

## Queue Notes

**Ranking logic:**

Rank 1 remains LLP-030 because it is the cleanest high-leverage signature in the portfolio. It is still the best single decision for reducing strategic ambiguity across downstream work.

Ranks 2 and 3 are the real marketing control layer now. The previously reported LLP-012 / LLP-025 ID collision has been cleared in source artifacts, so the remaining work is ordinary planning-gate closure: LLP-025 needs canonical measurement packaging and LLP-012 needs the rest of its planning packet.

Ranks 4 through 6 are operational governance cleanup items. They matter because they affect real work already in motion, but they are no longer mixed with stale collision or false missing-artifact claims.

Ranks 7 through 10 are queue-shaping decisions. They matter mainly because the refreshed portfolio inventory now includes 39 governed packets, and a meaningful share of the at-risk count is driven by unstaged or placeholder shells rather than active delivery failures.

**Items resolved since prior cycle (2026-03-18) — no longer in queue:**

- LLP-012 / LLP-025 Project ID collision: RESOLVED in source approval artifacts. Both projects now carry canonical IDs in their current approvals.
- LLP-013 Funnel 3 approval-record integrity conflict: RESOLVED as a reporting issue. The planning artifacts are present on disk and no longer support the prior conflict claim.
- LLP-024 NDA Esq zero-Stage-3-artifact emergency: RESOLVED. Execution artifacts now exist in `implementation/`.
- PORTFOLIO_MANAGEMENT canonical ID collision with LLP-011: RESOLVED. PORTFOLIO_MANAGEMENT now uses LLP-042 in source artifacts.
