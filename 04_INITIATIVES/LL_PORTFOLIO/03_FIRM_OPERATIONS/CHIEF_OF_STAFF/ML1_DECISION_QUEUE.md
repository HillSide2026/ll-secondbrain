# ML1 Decision Queue

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-001 Chief of Staff
- Input freshness: LLM-004 run 2026-03-16T00:00:00Z, LLM-005 run 2026-03-16T18:00:00Z, LLM-006 run 2026-03-16T18:00:00Z

> Advisory output. ML1 approval required before any action is taken.

---

**Staleness note:** Management agent outputs are two days old. LLP-024_NDA_ESQ gate deadline is now 2026-03-20 (2 days away, not 4). LLP-011_FUNNEL1_MANAGEMENT gate is 4 days overdue (was 2 days at last run). All other conditions as of 2026-03-16.

---

## Decision Queue

| Rank | Project | Decision Needed | Urgency | Blocking | Source |
|------|---------|----------------|---------|----------|--------|
| 1 | LLP-024_NDA_ESQ + LLP-011_FUNNEL1 | Resolve Project ID collision LLP-26-24 — designate which project retains the ID, update all APPROVAL_RECORDs, DEPENDENCIES.md files, and cross-references | Critical | Yes — blocks clean governance records for both projects; deadline 2026-03-20 | LLM-006 |
| 2 | LLP-006_MAINTENANCE | Investigate Stage 3 artifacts with no recorded authorization — determine if execution was informally directed; if yes, retroactively document; if no, pause execution and restart at initiation gate | Critical | Yes — hard governance hold; do not advance until resolved | LLM-004, LLM-006 |
| 3 | LLP-024_NDA_ESQ | Approve metric thresholds in METRICS.md; make Planning-to-Executing gate decision | Critical | Yes — deadline 2026-03-20 (2 days); resolve ID collision first or in parallel | LLM-004, LLM-005 |
| 4 | LLP-011_FUNNEL1_MANAGEMENT | Sign ML1_METRIC_APPROVAL.md; make Planning-to-Executing gate decision | High | Yes — gate milestone overdue since 2026-03-14 (4 days overdue as of 2026-03-18) | LLM-004, LLM-005 |
| 5 | LLP-023_MATTER_COMMAND_CONTROL | Complete RISK_SCAN Go/No-Go judgment; issue formal stage authorization (retroactively approve initiation and Planning, or halt non-canonical artifacts and resume from proper gate) | High | Yes — production governance activation blocked | LLM-004, LLM-006 |
| 6 | LLP-013_FUNNEL3_MANAGEMENT | Direct production of all Stage 2 planning artifacts — initiation authorized 2026-03-15 but zero planning artifacts drafted 3 days later | High | No gate pending, but planning stalled and accruing lag | LLM-004, LLM-005 |
| 7 | LLP-004_ONBOARDING | Sign ML1_METRIC_APPROVAL.md; make Planning-to-Executing gate decision | Medium | Yes — gate blocked; prerequisite for LLP-005 | LLM-004, LLM-005 |
| 8 | LLP-005_OPENING | Sign ML1_METRIC_APPROVAL.md; make Planning-to-Executing gate decision | Medium | Yes — follows LLP-004; do not advance ahead of it | LLM-004, LLM-005 |
| 9 | LLP-012_FUNNEL2_MANAGEMENT | Make initiation gate decision: approve / hold / reject — all Stage 1 artifacts drafted | Medium | No — project is not blocking others | LLM-004 |
| 10 | LLP-001, LLP-002, LLP-003, LLP-004_PARTNER_SUPERVISION (batch) | Sign four APPROVAL_RECORDs in a single review session to authorize Planning | Medium | Partially — LLP-002 blocks LLP-009_CLERK_SUPERVISION; LLP-003 blocks LLP-010_ASSOCIATE_SUPERVISION | LLM-004 |
| 11 | LLP-009_CLERK_SUPERVISION, LLP-010_ASSOCIATE_SUPERVISION | Define substantive initiation content — currently placeholder shells; content cannot be defined until LLP-002 and LLP-003 are approved | Low | No — downstream of rank 10 | LLM-004 |
| 12 | 09_SERVICE_MANAGEMENT cluster (5 shells) | Single batch decision: park all five placeholder shells until parent project is substantively defined | Low | No | LLM-004, LLM-006 |
| 13 | PORTFOLIO_MANAGEMENT shell, LLP-017_STRATEGIC_RISK | Define scope or park — both are placeholder projects with no substantive content | Low | No | LLM-004 |
| 14 | Measurement schema doctrine correction | Issue template correction so that canonical METRICS.md replaces split schema in all future Stage 2 projects; existing Stage 2 metric files need consolidation | Low | No — but drift is propagating forward | LLM-006 |

---

## Queue Notes

- **Ranks 1 and 3 are coupled.** The ID collision fix (rank 1) must be done before or simultaneously with the LLP-024 metric approval (rank 3). The fix is fast — treat as the same session.
- **Rank 2 is independent of all other items.** The LLP-006 investigation has no dependencies and no dependencies on it. It can be handled in a separate session before or after the gate approvals.
- **Ranks 3 and 4 can be batched.** After the ID collision is resolved, LLP-024 and LLP-011 metric approvals can be reviewed in the same session. LLM-005 estimates 60-90 minutes to review all four metric approval packages (ranks 3, 4, 7, 8) at once.
- **Ranks 7 and 8 are sequentially coupled.** LLP-005_OPENING is dependent on LLP-004_ONBOARDING advancing first. Do not advance LLP-005 ahead of LLP-004.
- **Rank 10 is a batch opportunity.** All four initiation packets (LLP-001, LLP-002, LLP-003, LLP-004_PARTNER) are substantive and complete; a single 30-minute signing session handles all four.
- **Rank 12 is a single decision, not five.** "Park all five until the parent project is defined" eliminates five queue items at once.
