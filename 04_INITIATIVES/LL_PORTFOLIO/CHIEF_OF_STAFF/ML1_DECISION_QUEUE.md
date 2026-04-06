# ML1 Decision Queue

- Generated: 2026-04-05T11:33:55+00:00
- Run ID: RUN-2026-04-05-DAILY-SWEEP-103355Z
- Source run: RUN-2026-04-05-LL-PORTFOLIO-AGENTS-110005Z (LLM-004/005/006)

> Advisory output. ML1 approval required before any action is taken.

---

## Execution Prerequisite

All inputs carry timestamps from 2026-04-05T11:00:06+00:00 under Run ID RUN-2026-04-05-LL-PORTFOLIO-AGENTS-110005Z. Inputs verified; no stale or missing files.

---

## Decision Queue

| Rank | Project | Decision Needed | Cash-Flow Impact | Urgency | Blocking | Source |
|------|---------|----------------|-----------------|---------|----------|--------|
| 1 | **LLP-011** Funnel 1 Management | Approve the canonical METRICS.md for the live F01 funnel so performance is governed by one decision-useful scorecard (lead volume, cost-per-lead, conversion rate). | Direct — active ad spend has no governed performance baseline | High | Yes — live funnel active, no auditable performance record inside second brain | LLM-006 metric schema gap; METRIC_SCHEMA_INTEGRITY_REPORT.md |
| 2 | **LLP-012** Funnel 2 Management | (a) Decide: close 6 planning gaps now or issue a written hold with reason. (b) Reconcile the packet's staging and offer architecture — README, approval record, and planning artifacts currently express different stages and entry paths. | Direct — second revenue lane (premium corporate law) cannot launch until this is resolved | High | Yes — highest priority project by score (23); cannot advance to Executing without gap closure | LLM-005 priority rank 1; SEQUENCING_RECOMMENDATIONS.md; prior COS run packet-level analysis |
| 3 | **LLP-004 + LLP-005** Onboarding / Opening | Confirm normalization stance: direct creation of canonical METRICS.md wrappers for both operating lanes and require live runtime logging in implementation logs. | Indirect — controls revenue quality through intake-to-opening discipline | Medium-High | Partial — watch flags persist; operating lanes are live but ungoverned at the measurement layer | LLM-004/005 watch status; METRIC_SCHEMA_INTEGRITY_REPORT.md |
| 4 | **LLP-025** Marketing Strategy | Confirm whether METRICS.md incompleteness is intentional (open strategy choices) or a real gap. If intentional, record a formal exception in the packet. If not, direct gap closure. LLP-025 conditions LLP-011, LLP-012, LLP-013, LLP-014, and LLP-026. | Indirect — foundational to all downstream funnel and marketing projects | Medium | Yes — five downstream projects depend on LLP-025 for positioning and measurement baseline | LLM-006 watch status; DOCTRINE_DRIFT_REPORT.md |
| 5 | **LLP-033** Associate Lawyer | Schedule the first ML1 review of the capacity and economics model. No recruitment activity should begin before this review. | Indirect — associate economics directly affect owner compensation and margin | Medium | Partial — no ML1 review on record; project may drift without a review date | LLM-004 watch status; no review date in current run |
| 6 | **Portfolio-wide SCOPE artifact** | Confirm that SCOPE_STATEMENT.md (not SCOPE_DEFINITION.md) is the canonical scope artifact under current LL doctrine, and authorize the governance toolchain to be updated accordingly. Resolves up to 10 watch flags that may be schema-mismatch artifacts rather than genuine non-compliance. | Indirect — governance noise obscures real risk signals | Medium | Yes — 10 reported stage violations may be inflated; prior COS run flagged same issue, still unresolved | DOCTRINE_DRIFT_REPORT.md; STAGE_GATE_VIOLATION_REPORT.md; prior COS brief 2026-04-04 |

---

## System Actions (Post-ML1-Decision)

1. Draft METRICS.md for LLP-011 immediately after ML1 resolves Rank 1.
2. If ML1 authorizes LLP-012 gap closure: assign capacity to draft SCOPE_STATEMENT.md and the five other missing planning artifacts; reconcile README and APPROVAL_RECORD to canonical stage and offer path.
3. Create canonical METRICS.md wrappers for LLP-004 and LLP-005; add live runtime logging requirement to implementation logs.
4. Record strategy-layer measurement exception in LLP-025 packet if ML1 confirms intentional incompleteness.
5. Add ML1 review date to LLP-033 workplan.
6. Update the deterministic governance layer to check for SCOPE_STATEMENT.md once ML1 confirms the canonical rule.
7. Re-run the full portfolio cycle after the normalization pass so health counts reflect resolved gaps.

---

## Queue Notes

This is the second consecutive daily run showing the same 10 watch projects and same dominant gap pattern. The portfolio is not deteriorating — it is stable but stalled at the planning-normalization layer. The Rank 1 and Rank 2 items are the only ones with direct revenue-signal stakes. Ranks 3–6 are real governance work but do not block revenue operations today.
