# ML1 Decision Queue

- Generated: 2026-04-04T00:32:32Z
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-04-04T00:30:07+00:00, LLM-005 run 2026-04-04T00:30:07+00:00, LLM-006 run 2026-04-04T00:30:07+00:00

> Advisory output. ML1 approval required before any action is taken.

## Execution Prerequisite

None. The management-agent inputs were refreshed on `2026-04-04` under
`RUN-2026-04-04-LL-PORTFOLIO-AGENTS-003007Z`.

## Decision Queue

| Rank | Project | Decision Needed | Cash Flow Impact | ML1 or System | Urgency | Blocking | Source |
|------|---------|----------------|-----------------|---------------|---------|----------|--------|
| 1 | `LLP-012` Funnel 2 Management | Confirm the operating rule for F02 while six planning artifacts remain open: should adjacent build work pause behind planning closure, or is limited preparatory work allowed while the packet is completed? | direct | ML1_REQUIRED | high | yes — highest priority project and largest remaining planning packet gap | `LLM-005` priority rank 1; `LLM-004` and `LLM-006` both show 6 open gaps |
| 2 | `LLP-011` + `LLP-025` | Confirm the measurement stance: prioritize a canonical live-funnel scorecard for `LLP-011`, defer a canonical KPI sheet for `LLP-025` until open strategy questions are resolved, and accept temporary document messiness in the strategy layer meanwhile. | direct / indirect | ML1_REQUIRED | high | yes — the live funnel still needs a canonical scorecard, while the strategy layer remains intentionally unfinished | `LLM-006` metric schema gaps; `LLM-004` / `LLM-005` watch status |
| 3 | `LLP-030` Firm Strategy | Complete or authorize drafting of `BUSINESS_CASE.md` so the strategy packet can close initiation cleanly. | indirect | ML1_REQUIRED | medium-high | yes — leaves the governing strategy packet formally incomplete | `LLM-006` stage violation; `LLM-004` / `LLM-005` at-risk |
| 4 | `LLP-007`, `LLP-008`, `LLP-016`, `LLP-043` | Sign `APPROVAL_RECORD.md` or explicitly park each project. | none near-term | ML1_REQUIRED | medium | yes — this is now the core residual approval-gap set in the portfolio | `LLM-006` approval gap report |
| 5 | Portfolio-wide planning normalization | Confirm that the doctrine rule is controlling: `SCOPE_STATEMENT.md` is canonical, and the deterministic governance layer should be normalized accordingly rather than treating `SCOPE_DEFINITION.md` as a current requirement. | indirect | ML1_REQUIRED | medium | yes — 10 reported stage violations are being inflated by a stale schema check | `LLM-006` / `LLM-005` reports versus current doctrine and `LLM-004` spec |
| 6 | `LLP-004` + `LLP-005` | Decide whether to batch these two operating projects into the same one-time planning / metrics normalization pass as the funnel layer, rather than treating them as isolated watch items. | indirect | ML1_REQUIRED | medium | partial — both remain watch because of planning / measurement cleanup, not broad execution failure | `LLM-004` / `LLM-005` watch status |

## System Actions

1. Draft or normalize the six `LLP-012` stage-2 planning artifacts immediately after ML1 resolves Rank 1.
2. Draft the canonical live-funnel `METRICS.md` for `LLP-011` immediately after ML1 resolves Rank 2, and record a temporary strategy-layer exception for `LLP-025` pending closure of its open strategic questions.
3. Normalize the deterministic management layer so it recognizes `SCOPE_STATEMENT.md` as the canonical scope artifact, consistent with current LL doctrine.
4. Re-run the LL Chief of Staff after the scope / metrics normalization pass so the portfolio health counts stop carrying stale-schema noise.

## Queue Notes

The refreshed April 4, 2026 management run materially improves the portfolio
picture relative to the stale April 1 Chief of Staff packet:

- current mix is `24` on-track, `10` watch, `5` at-risk
- approval gaps are down to `4`
- the dominant issue is now concentrated planning normalization, not broad
  portfolio disorder

This queue therefore prioritizes:

1. `LLP-012` because it remains the top growth / sequencing item
2. live-funnel scorecard normalization because it directly affects the active funnel layer
3. strategic / approval cleanup in the small residual true at-risk set

The main caution is that some governance noise is now coming from a stale tool
expectation (`SCOPE_DEFINITION.md`) rather than genuine project non-compliance.
