# Capacity Allocation Model (Advisory)

- Generated: 2026-04-01T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Per-Project Capacity Demand

Capacity unit method:
- Stage 1 initiation gaps: 1 unit each
- Stage 2 planning gaps: 2 units each
- Stage 2 measurement gaps: 3 units each
- Stage 3+: 0 units (monitoring mode; note any execution exceptions separately)

| Project | Stage | Estimated Units | Planning Gaps | Measurement Gaps | Notes |
|---------|-------|----------------|---------------|------------------|-------|
| LLP-014 Intake Management | 1 | 0 | 0 | 0 | Initiation complete; Planning artifacts not yet drafted (will generate demand when production begins) |
| LLP-026 Lead Capture | 1 | 0 | 0 | 0 | Initiation complete; Planning artifacts not yet drafted |
| LLP-027 Inquiries | 1 | 0 | 0 | 0 | Initiation complete; Planning artifacts not yet drafted; sequenced after LLP-014 |
| LLP-028 Consults | 0 | 6 | 0 | 0 | Unstaged stub — all 6 initiation artifacts missing; 1 unit × 6 |
| LLP-029 Onboarding | 0 | 6 | 0 | 0 | Unstaged stub — all 6 initiation artifacts missing; 1 unit × 6 |
| LLP-012 Funnel 2 Management | 2 | 15 | 6 | 1 | All 6 Stage 2 planning artifacts absent (6 × 2 = 12 units) + metric approval gap (1 × 3 = 3 units) |
| LLP-013 Funnel 3 Management | 2 | 3 | 0 | 1 | All planning artifacts present; only metric threshold approval missing (3 units) |
| LLP-023 Matter Command and Control | 2 | 2 | 1 | 0 | Formal gate closure decision only (2 units) |
| LLP-025 Marketing Strategy | 2 | 4 | 1 | 1 | Metric approval gap (3 units) + formal gate decision (2 units) — overlapping with same artifact so estimated at 4 combined |
| LLP-004 Onboarding | 2 | 0 | 0 | 0 | Planning gate approved; execution authorized — no gaps |
| LLP-011 Funnel 1 Management | 3 | 3 | 0 | 1 | Executing; metric threshold numeric lock pending (3 units; time-bound) |
| LLP-030 Firm Strategy | 1 | 1 | 0 | 0 | Initiation complete; Planning not submitted — 1 unit for Planning trigger |
| LLP-031 Corporate Entity Mgmt | 1 | 1 | 0 | 0 | APPROVAL_RECORD not recorded (1 unit) |
| LLP-032 Corporate Clerk | 1 | 1 | 0 | 0 | APPROVAL_RECORD not recorded (1 unit) |
| LLP-033 Associate Lawyer Capacity | 1 | 1 | 0 | 0 | APPROVAL_RECORD unsigned (1 unit) |
| LLP-034 Partner Supervision | 1 | 1 | 0 | 0 | APPROVAL_RECORD not recorded (1 unit) |
| LLP-007 Admin | 1 | 1 | 0 | 0 | APPROVAL_RECORD missing entirely (1 unit) |
| LLP-008 Closing | 1 | 1 | 0 | 0 | APPROVAL_RECORD missing entirely (1 unit) |
| LLP-016 Compliance | 1 | 1 | 0 | 0 | APPROVAL_RECORD missing entirely (1 unit) |
| LLP-001 Accounting | 1 | 1 | 0 | 0 | APPROVAL_RECORD unsigned (1 unit) |
| LLP-002 Budgeting | 1 | 1 | 0 | 0 | APPROVAL_RECORD unsigned (1 unit) |
| LLP-003 Weekly Report | 1 | 1 | 0 | 0 | APPROVAL_RECORD unsigned (1 unit) |
| LLP-017 Strategic Risk | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-018 Financial Risk | 1 | 1 | 0 | 0 | APPROVAL_RECORD unsigned (1 unit) |
| LLP-009 Clerk Supervision | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-010 Associate Supervision | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-037 Service Management | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-038 Service Mgmt / Essential | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-039 Service Mgmt / Strategic | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-040 Service Mgmt / Standard | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-041 Service Mgmt / Parked | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-042 Portfolio Management | 1 | 2 | 0 | 0 | Charter undefined + approval unsigned (2 units) |
| LLP-005 Opening | 3 | 0 | 0 | 0 | Executing — monitoring only |
| LLP-006 Matter Maintenance | 3 | 0 | 0 | 0 | Executing — monitoring only |
| LLP-024 NDA Esq | 3 | 0 | 0 | 0 | Executing — monitoring only |
| LLP-015, LLP-035, LLP-036 (Parked) | 1 | 0 | 0 | 0 | Parked by ML1 — no demand |

---

## Planning Demand for Newly Entered Projects (LLP-014, LLP-026, LLP-027)

These three projects currently show 0 units because their initiation is complete and Planning artifacts have not yet been produced. Once Planning production begins, each will generate approximately:
- LLP-014: 6 × 2 = 12 units (6 Stage 2 planning artifacts) + 3 units (metric framework) = ~15 units
- LLP-026: 6 × 2 = 12 units (6 Stage 2 planning artifacts) + 3 units (metric framework) = ~15 units
- LLP-027: 6 × 2 = 12 units (6 Stage 2 planning artifacts) + 3 units (metric framework) = ~15 units

**Projected additional Planning demand upon production: ~45 units**

---

## Portfolio Totals

- Stage 1 load (initiation gaps): 9 projects with gaps totaling ~35 units (dominated by undefined-charter cluster)
- Stage 2 load (planning + measurement gaps): 5 active Planning projects totaling ~27 units; 3 entering Planning imminently at ~45 projected units
- Stage 3+ load: 4 executing projects at 0 current gap units (LLP-011 has 3 time-bound metric units)
- Total estimated capacity units to close current visible gaps: **~65 units** (current state)
- Total estimated units including projected Planning production for LLP-014/026/027: **~110 units**

---

## Recommendation

Concentrate first on Stage 2 closure where the artifact is a single ML1 decision (LLP-013 metric approval = 3 units, 1 action; LLP-023 gate closure = 2 units, 1 action; LLP-025 gate + metrics = 4 units, 1 session). These close the highest-impact gates for the lowest unit cost. The LLP-014/026/027 Planning production (~45 units projected) is the largest forward demand — sequence its production deliberately to avoid all three arriving at the ML1 review queue simultaneously.
