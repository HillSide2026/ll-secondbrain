# Project Priority Matrix

- Generated: 2026-04-01T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Priority Rankings

Priority basis applied in order:
1. Health = at-risk AND missing approvals
2. Health = at-risk for other reason
3. Health = watch, Stage 2 measurement gaps
4. Health = watch, Stage 2 planning gaps
5. On-track but has cross-project dependencies blocking others

| Rank | Project | Health | Priority Basis | Recommended Focus |
|------|---------|--------|----------------|-------------------|
| 1 | LLP-030 Firm Strategy | watch | Watch; governing frame for entire strategic and marketing cluster — no downstream project can finalize capacity or positioning constraints without it | Begin substantive FIRM_STRATEGY.md and BUSINESS_PLAN.md drafts; this unlocks capacity ceiling inputs required by LLP-012, LLP-013, and LLP-025. |
| 2 | LLP-012 Funnel 2 Management | watch | Watch; Stage 2 planning gap — all 6 canonical planning artifacts absent, metric approval placeholder only; upstream of LLP-026 capture configuration | Direct production of all six Stage 2 planning artifacts and provide ML1 capacity decisions (max active matters, value floor, category stop-accepts) required before the Planning gate can close. |
| 3 | LLP-023 Matter Command and Control | watch | Watch; planning artifacts complete but formal gate decisions not recorded in APPROVAL_RECORD — blocks executing authorization | Record formal ML1 gate decisions for Initiating-to-Planning and Planning-to-Executing in APPROVAL_RECORD.md to convert drafted artifacts into authorized execution. |
| 4 | LLP-013 Funnel 3 Management | watch | Watch; Stage 2 measurement gap only — all planning artifacts present, only metric threshold approval is outstanding; upstream of LLP-026 | Approve numeric metric thresholds in planning/METRICS.md to close the Planning gate and authorize Executing. |
| 5 | LLP-025 Marketing Strategy | watch | Watch; metric approval and Planning gate decision both outstanding; governs F01-to-F02 transition plan which affects LLP-011 and LLP-012 | Approve metric thresholds in METRIC_FRAMEWORK.md and record the Planning-to-Executing gate decision in APPROVAL_RECORD.md. |
| 6 | LLP-014 Intake Management | on-track | On-track but has cross-project dependencies: LLP-014 Planning artifacts must be completed before LLP-027, LLP-028, and LLP-029 can finalize their own planning logic | Initiate Planning stage: direct production of SCOPE_DEFINITION.md and WORKPLAN.md, including stage-gate definitions and handoff protocols that LLP-027/028/029 depend on. |
| 7 | LLP-026 Lead Capture | on-track | On-track but cross-project dependency: LLP-026 Planning must coordinate with LLP-014 on routing requirements before CTA and capture configuration is finalized; bridges all three funnels to intake | Run Planning in parallel with LLP-014; draft SCOPE_DEFINITION.md and WORKPLAN.md covering CTA configuration scope, opt-in mechanics, and lead routing logic per funnel. |
| 8 | LLP-027 Inquiries | on-track | On-track; Planning authorized; sequencing constraint: cannot finalize triage and handoff logic until LLP-014 pipeline stage definitions and LLP-026 inquiry format are established | Hold Planning artifact drafting until LLP-014 planning is sufficiently advanced to define handoff protocol; begin by scoping inquiry channels and response SLA framework. |
| 9 | LLP-011 Funnel 1 Management | watch (conditional) | Executing but metric thresholds not yet locked; time-bound: due within 30 days of execution start; upstream of LLP-026 lead capture | Lock numeric metric thresholds in ML1_METRIC_APPROVAL.md once first 4-week baseline is complete. |
| 10 | LLP-031 Corporate Entity Mgmt | at-risk | At-risk; initiation approval not recorded | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md. |
| 11 | LLP-032 Corporate Clerk | at-risk | At-risk; initiation approval not recorded | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md. |
| 12 | LLP-034 Partner Supervision | at-risk | At-risk; initiation approval not recorded | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md. |
| 13 | LLP-033 Associate Lawyer Capacity | at-risk | At-risk; approval unsigned placeholder | Sign APPROVAL_RECORD.md to formally record the initiation decision. |
| 14 | LLP-007 Admin | at-risk | At-risk; APPROVAL_RECORD missing entirely | Create and sign APPROVAL_RECORD.md for initiation. |
| 15 | LLP-008 Closing | at-risk | At-risk; APPROVAL_RECORD missing entirely | Create and sign APPROVAL_RECORD.md for initiation. |
| 16 | LLP-016 Compliance | at-risk | At-risk; APPROVAL_RECORD missing entirely | Create and sign APPROVAL_RECORD.md for initiation. |
| 17 | LLP-028 Consults | at-risk | Unstaged stub; no initiation packet; downstream of LLP-027, cannot plan until LLP-014 defines handoff protocol | Direct initiation: produce PROJECT_CHARTER.md and full Stage 1 packet, then sign APPROVAL_RECORD.md. |
| 18 | LLP-029 Onboarding | at-risk | Unstaged stub; no initiation packet; downstream of LLP-028; has coordination dependency with LLP-004 (operational counterpart) | Direct initiation: produce PROJECT_CHARTER.md and full Stage 1 packet; coordinate scope boundary with LLP-004. |
| 19 | LLP-001 Accounting | at-risk | At-risk; approval unsigned | Sign APPROVAL_RECORD.md. |
| 20 | LLP-002 Budgeting | at-risk | At-risk; approval unsigned | Sign APPROVAL_RECORD.md. |
| 21 | LLP-003 Weekly Report | at-risk | At-risk; approval unsigned | Sign APPROVAL_RECORD.md. |
| 22 | LLP-018 Financial Risk | at-risk | At-risk; approval unsigned | Sign APPROVAL_RECORD.md. |
| 23 | LLP-017 Strategic Risk | at-risk | At-risk; charter undefined and approval unsigned | Define project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or park. |
| 24 | LLP-009 Clerk Supervision | at-risk | At-risk; charter undefined and approval unsigned | Define project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or park. |
| 25 | LLP-010 Associate Supervision | at-risk | At-risk; charter undefined and approval unsigned | Define project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or park. |
| 26 | LLP-037–041 Service Mgmt cluster | at-risk | At-risk; all five charters undefined, approvals unsigned | Define project purposes and sign APPROVAL_RECORD.md or direct a park decision for each. |
| 27 | LLP-042 Portfolio Management | at-risk | At-risk; charter undefined, approval unsigned | Define project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md. |
| 28 | LLP-004 Onboarding | on-track | On-track; Planning gate approved; execution in progress | Begin logging execution activity in implementation/EXECUTION_LOG.md; no gate action required. |
| 29 | LLP-005 Opening | on-track | On-track; executing | Monitor execution logs; no gate action required. |
| 30 | LLP-006 Matter Maintenance | on-track | On-track; executing | Monitor execution logs; plan future cleanup of split metric schema. |
| 31 | LLP-024 NDA Esq | on-track | On-track; executing | Monitor execution logs; optionally record acknowledgment of retroactively added initiation artifacts. |
| 32 | LLP-015, LLP-035, LLP-036 (Parked) | on-track | Parked by ML1 decision | No action required; reactivate only on ML1 direction. |
