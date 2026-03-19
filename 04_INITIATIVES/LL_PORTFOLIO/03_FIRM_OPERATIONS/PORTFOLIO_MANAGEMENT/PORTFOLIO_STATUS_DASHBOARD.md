# Portfolio Status Dashboard

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Portfolio Status

| Project | Stage | Health | Open Gate Gaps | Stage 2 Readiness | Approvals Present |
|---------|-------|--------|----------------|-------------------|-------------------|
| LLP-004 Onboarding (LLP-26-05) | 3 — Executing | on-track | 0 | n/a | yes |
| LLP-005 Opening (LLP-26-06) | 3 — Executing (authorized, not started) | watch | 6 | n/a | yes |
| LLP-006 Maintenance (LLP-26-07) | 3 — Executing (retroactive gate) | watch | 6 | n/a | yes (retroactive) |
| PORTFOLIO_MANAGEMENT (LLP-26-11) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| LLP-017 Strategic Risk (LLP-26-13) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| LLP-009 Clerk Supervision (LLP-26-16) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| LLP-010 Associate Supervision (LLP-26-17) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| LLP-001 Corporate Entity Mgmt (LLP-26-19) | 1 — Initiating | at-risk | 1 | n/a | no (unsigned) |
| LLP-002 Corporate Clerk (LLP-26-20) | 1 — Initiating | at-risk | 1 | n/a | no (unsigned) |
| LLP-003 Associate Lawyer (LLP-26-21) | 1 — Initiating | at-risk | 1 | n/a | no (unsigned) |
| LLP-004 Partner Supervision (LLP-26-22) | 1 — Initiating | at-risk | 1 | n/a | no (unsigned) |
| LLP-023 Matter Command & Control (LLP-26-23) | 1 — Initiating (informal scope lock) | watch | 4 | 20% (2/10 Stage 2 artifacts) | no (informal only) |
| LLP-024 NDA Esq (LLP-26-24) | 3 — Executing (authorized today, not started) | watch | 6 | n/a | yes |
| LLP-030 Firm Strategy (LLP-030) | 1 — Initiating | at-risk | 1 | n/a | no (pending) |
| LLP-011 Funnel 1 Mgmt (LLP-26-11) | 3 — Executing (authorized, not started) | watch | 6 | n/a | yes |
| LLP-012 Funnel 2 Mgmt (LLP-26-25*) | 2 — Planning | watch | 7 | 14% (1/7 Stage 2 artifacts) | yes (ID collision) |
| LLP-013 Funnel 3 Mgmt (LLP-26-26) | 2 — Planning | watch | 1 | 86% (6/7 Stage 2 artifacts) | yes (metric pending) |
| LLP-025 Marketing Strategy (LLP-26-25*) | 2 — Planning | watch | 1 | 86% (6/7 Stage 2 artifacts) | yes (metric pending) |
| 09_SERVICE_MANAGEMENT (LLP-26-28) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| 09_SVC/ESSENTIAL (LLP-26-29) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| 09_SVC/STRATEGIC (LLP-26-30) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| 09_SVC/STANDARD (LLP-26-31) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |
| 09_SVC/PARKED (LLP-26-32) | 1 — Initiating | at-risk | 6 | n/a | no (unsigned) |

*LLP-012 and LLP-025 share Project ID LLP-26-25 in their APPROVAL_RECORD.md files — collision unresolved.

---

## Summary

- Total projects: 23
- On-track: 1 | Watch: 7 | At-risk: 15
- Stage distribution: Stage 1 (Initiating): 16 | Stage 2 (Planning): 3 | Stage 3 (Executing): 4
- Stage 3 authorized-but-unstarted: 4 projects (LLP-005, LLP-006, LLP-011, LLP-024) — execution authorized but no Stage 3 artifacts exist in any of them
- Stage 2 concentration: 3 projects in Planning simultaneously (LLP-012, LLP-013, LLP-025)
- Governance integrity issue: Project ID collision between LLP-012 and LLP-025 (both carrying LLP-26-25)
- Strategic gate blocker: LLP-030 Firm Strategy initiation approval not yet recorded; 7 downstream strategic projects depend on it
- Portfolio-wide debt: 4 projects carrying retroactive or informal execution authorization without Stage 3 artifact sets
