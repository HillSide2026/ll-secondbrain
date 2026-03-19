# Capacity Allocation Model (Advisory)

- Generated: 2026-03-18T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Per-Project Capacity Demand

Scoring method: Stage 1 initiation gaps x1 unit each | Stage 2 planning gaps x2 units, measurement gaps x3 units | Stage 3: execution artifact gaps x2 units each

| Project | Est. Units | Planning Gaps | Measurement Gaps | Notes |
|---------|-----------|---------------|------------------|-------|
| LLP-004 Onboarding | 0 | 0 | 0 | Fully governed in Executing; no current gap |
| LLP-005 Opening | 12 | 0 | 0 | 6 Stage 3 artifacts missing x2 units each; execution authorized but not started |
| LLP-006 Maintenance | 12 | 0 | 0 | 6 Stage 3 artifacts missing x2 units each; retroactive gate, no implementation artifacts |
| LLP-011 Funnel 1 Mgmt | 12 | 0 | 0 | 6 Stage 3 artifacts missing x2 units each; funnel operationally live but ungoverned |
| LLP-024 NDA Esq | 12 | 0 | 0 | 6 Stage 3 artifacts missing x2 units each; authorized today; 3 workstream leads TBD |
| LLP-025 Marketing Strategy | 3 | 0 | 1 | Stage 2 artifacts complete; 1 metric approval outstanding (x3) plus non-canonical schema |
| LLP-013 Funnel 3 Mgmt | 3 | 0 | 1 | Stage 2 artifacts complete; 1 metric approval outstanding (x3); RPAA time pressure |
| LLP-012 Funnel 2 Mgmt | 18 | 6 | 1 | 6 planning artifacts absent (x2 each = 12) + metric approval (x3) + 3 ML1 decisions |
| LLP-023 Matter Command & Control | 14 | 4 | 1 | 4 canonical Stage 2 artifacts missing (x2 each = 8) + measurement framework absent (x3) + formalization decision (x3) |
| LLP-030 Firm Strategy | 1 | 0 | 0 | Single initiation gate decision; content is substantive; only ML1 signature needed |
| LLP-001 Corporate Entity Mgmt | 1 | 0 | 0 | Signature only; hold Planning pending LLP-030 |
| LLP-002 Corporate Clerk | 1 | 0 | 0 | Signature only; hold Planning pending LLP-030 |
| LLP-003 Associate Lawyer | 1 | 0 | 0 | Signature only; hold Planning pending LLP-030 |
| LLP-004 Partner Supervision | 1 | 0 | 0 | Signature only |
| PORTFOLIO_MANAGEMENT shell | 6 | 6 | 0 | All charter fields placeholder; 6 initiation content gaps (x1 each) |
| LLP-017 Strategic Risk | 6 | 6 | 0 | All charter fields placeholder; 6 initiation content gaps (x1 each) |
| LLP-009 Clerk Supervision | 0 | 0 | 0 | Blocked; do not consume capacity until LLP-002 produces role definition |
| LLP-010 Associate Supervision | 0 | 0 | 0 | Blocked; do not consume capacity until LLP-003 produces role definition |
| 09_SVC_MGMT cluster (x5) | 2 | 0 | 0 | 1 batch decision unit + 1 implementation unit if consolidated; individual definition would be ~30 units (not recommended) |

---

## Portfolio Totals

- Stage 1 load: 16 projects actively in Initiating
- Stage 2 load: 3 projects in Planning (LLP-012, LLP-013, LLP-025)
- Stage 3+ load: 5 projects in Executing (1 governed, 4 ungoverned)
- Total estimated capacity units to close current gaps: ~105 units

### Load by Category

| Category | Units | Notes |
|----------|-------|-------|
| Stage 3 execution artifact creation (4 ungoverned projects) | 48 | Highest absolute load; production work, not ML1 review |
| LLP-012 Stage 2 artifact production | 15 | Second-highest; all artifacts need to be created |
| LLP-023 Stage 2 formalization | 14 | Third-highest; governance formalization + artifact creation |
| PORTFOLIO_MANAGEMENT + LLP-017 placeholder content | 12 | Define or park; if park, cost drops to ~2 units each |
| Metric approval decisions (LLP-013, LLP-025) | 6 | ML1 review time only; no production required |
| Initiation signatures (LLP-030, LLP-001, LLP-002, LLP-003, LLP-004_PARTNER) | 5 | Decision time only |
| 09_SERVICE_MANAGEMENT batch decision | 2 | Lowest-cost path is a single park decision |

---

## Recommendation

Concentrate immediate ML1 decision capacity on LLP-030 initiation (1 unit, highest leverage) and the two Planning gate approvals for LLP-013 and LLP-025 (6 units combined, clears the Stage 2 frontier). Then direct production capacity to closing the four Stage 3 execution artifact sets (48 units) — this work does not require ML1 to produce, only a directive to create. The largest avoidable capacity sink is the PORTFOLIO_MANAGEMENT and LLP-017 placeholder content (12 units) — parking both removes 12 units from the active queue at zero production cost.
