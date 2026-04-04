# ML1 Decision Queue

- Generated: 2026-04-04T01:29:33Z
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-04-04T01:29:33+00:00, LLM-005 run 2026-04-04T01:29:33+00:00, LLM-006 run 2026-04-04T01:29:33+00:00

> Advisory output. ML1 approval required before any action is taken.

## Execution Prerequisite

None. The management-agent inputs were refreshed on `2026-04-04` under
`RUN-2026-04-04-LL-PORTFOLIO-AGENTS-012933Z`.

## Decision Queue

| Rank | Project | Decision Needed | Cash Flow Impact | ML1 or System | Urgency | Blocking | Source |
|------|---------|----------------|-----------------|---------------|---------|----------|--------|
| 1 | `LLP-012` Funnel 2 Management | Confirm the canonical F02 operating path and normalize the packet to match it: reconcile planning-stage docs, April 1 execution authorization, ICP gate, and the current offer architecture. | direct | ML1_REQUIRED | high | yes — highest priority project and still the main growth/control bottleneck | `LLM-005` priority rank 1; packet-level review of `README.md`, `initiation/APPROVAL_RECORD.md`, `planning/SCOPE_STATEMENT.md`, and `implementation/` |
| 2 | `LLP-011` Funnel 1 Management | Approve the canonical live-funnel scorecard and profitability lens for F01 so the active funnel is governed by one decision-useful metric surface. | direct | ML1_REQUIRED | high | yes — live funnel remains active and still lacks canonical `METRICS.md` | `LLM-006` metric schema gap; packet-level review of `planning/ML1_METRIC_APPROVAL.md` and `implementation/EXECUTION_LOG.md` |
| 3 | `LLP-004` + `LLP-005` | Confirm the intake-to-opening normalization stance: treat these as real operating lanes, create canonical measurement wrappers, and require live runtime logging rather than only packet establishment. | indirect | ML1_REQUIRED | medium-high | partial — these projects support revenue control but are not the first growth bottleneck | `LLM-004` / `LLM-005` watch status; packet-level review of onboarding/opening implementation logs |
| 4 | `LLP-025` Marketing Strategy | Confirm the strategy-layer measurement rule: keep the project active, defer a fully canonical KPI sheet until open strategy choices close, and treat current incompleteness as intentional rather than as immediate failure. | indirect | ML1_REQUIRED | medium | yes — strategy still conditions F02 and broader marketing sequencing | `planning/OPEN_QUESTIONS.md`; `planning/METRIC_FRAMEWORK.md`; `LLM-006` watch status |
| 5 | Portfolio-wide planning normalization | Confirm that the doctrine rule is controlling: `SCOPE_STATEMENT.md` is canonical, and the deterministic governance layer should be normalized accordingly rather than treating `SCOPE_DEFINITION.md` as a current requirement. | indirect | ML1_REQUIRED | medium | yes — 10 reported stage violations are still being inflated by a stale schema check | `LLM-006` / `LLM-005` reports versus current doctrine and `LLM-004` spec |

## System Actions

1. Normalize `LLP-012` so its README, approval record, planning packet, and implementation packet all express the same stage and offer architecture.
2. Draft the canonical live-funnel `METRICS.md` for `LLP-011` immediately after ML1 resolves Rank 2.
3. Create canonical measurement wrappers for `LLP-004` and `LLP-005`, then require live runtime entries in their implementation logs.
4. Record a temporary strategy-layer measurement exception for `LLP-025` pending closure of its open strategic questions.
5. Normalize the deterministic management layer so it recognizes `SCOPE_STATEMENT.md` as the canonical scope artifact, consistent with current LL doctrine.
6. Re-run the LL Chief of Staff after the scope / metrics normalization pass so the portfolio health counts stop carrying stale-schema noise.

## Queue Notes

The refreshed April 4, 2026 management run materially improves the portfolio
picture relative to the earlier Chief of Staff packet:

- current mix is `29` on-track, `10` watch, `0` at-risk
- approval gaps are now `0`
- the dominant issue is now concentrated planning and measurement normalization,
  not broad portfolio disorder

This queue therefore prioritizes:

1. `LLP-012` because it remains the top growth / sequencing item
2. live-funnel scorecard normalization because it directly affects the active funnel layer
3. intake-to-opening control normalization because those lanes directly support
   the quality of converted work

The main caution is that some governance noise is now coming from a stale tool
expectation (`SCOPE_DEFINITION.md`) rather than genuine project non-compliance.
