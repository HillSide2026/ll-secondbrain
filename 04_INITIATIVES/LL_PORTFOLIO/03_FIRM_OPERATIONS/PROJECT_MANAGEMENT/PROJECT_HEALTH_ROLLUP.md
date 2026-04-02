# Project Health Rollup

- Generated: 2026-04-01T00:00:00Z
- Agent: LLM-004 Project Management Agent
- Projects reviewed: 36

> Advisory output. ML1 approval required before any action is taken.

---

## Portfolio Health Summary

- On-track: 12
- Watch: 8
- At-risk: 16

---

## Project Assessments

### LLP-014 — Intake Management

**Stage:** Initiating
**Stage source:** approval_record
**Health:** on-track
**Project type:** Management (Marketing Operations)

**What this project is:** Governs the full client intake pipeline from first inquiry through onboarding, coordinating pipeline integrity across three subprojects: LLP-027 (Inquiries), LLP-028 (Consults), and LLP-029 (Onboarding).

**Artifact gaps (current stage):**
- None — all six Stage 1 artifacts present and complete

**Blockers for ML1:**
- None — initiation approved 2026-04-01; advance to Planning authorized

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not yet required (Initiating stage)

**Recommended ML1 action:** Authorize Planning stage by approving Planning artifacts when drafted, starting with SCOPE_DEFINITION.md and WORKPLAN.md; note that LLP-014 planning must sequence before finalizing LLP-027/028/029 planning artifacts.

---

### LLP-026 — Lead Capture

**Stage:** Initiating
**Stage source:** approval_record
**Health:** on-track
**Project type:** Management (Marketing Operations)

**What this project is:** Governs lead capture operations across all marketing funnels — landing pages, lead magnets, opt-ins, and top-of-funnel conversion assets — bridging funnel traffic from LLP-011/012/013 into the intake pipeline (LLP-014).

**Artifact gaps (current stage):**
- None — all six Stage 1 artifacts present and complete

**Blockers for ML1:**
- None — initiation approved 2026-04-01; advance to Planning authorized

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not yet required (Initiating stage)

**Recommended ML1 action:** Authorize Planning stage; Planning must coordinate with LLP-014 on routing requirements before CTA and capture configuration is finalized.

---

### LLP-027 — Inquiries

**Stage:** Initiating
**Stage source:** approval_record
**Health:** on-track
**Project type:** Management (Intake Operations)

**What this project is:** Governs the first stage of the client intake pipeline — receipt, triage, and initial response to incoming inquiries across all channels, with handoff to the consultation stage (LLP-028).

**Artifact gaps (current stage):**
- None — all six Stage 1 artifacts present and complete

**Blockers for ML1:**
- None — initiation approved 2026-04-01; advance to Planning authorized

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not yet required (Initiating stage)

**Recommended ML1 action:** Authorize Planning stage; Planning must coordinate with LLP-026 on inquiry format and LLP-028 on handoff requirements before triage and handoff logic is finalized.

---

### LLP-004 — Onboarding

**Stage:** Planning
**Stage source:** approval_record
**Health:** on-track
**Project type:** Operational

**What this project is:** Establishes a repeatable onboarding function controlling the path from qualified lead to signed engagement authorization, producing a Clio matter, engagement agreement, and Gate 2 authorization packet for each qualified lead.

**Artifact gaps (current stage):**
- Stage 2 planning artifacts are present (SCOPE_STATEMENT.md, WORKPLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md, ML1_METRIC_APPROVAL.md)
- Planning -> Executing gate has been approved by ML1 (2026-03-16); execution artifacts are present in implementation/
- Minor: WORKPLAN.md uses split metric schema (METRIC_DEFINITION.md, MEASUREMENT_METHOD.md, etc.) rather than consolidated METRICS.md — flagged for future cleanup

**Blockers for ML1:**
- None — Planning gate approved; implementation artifacts established

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: yes (2026-03-16)

**Recommended ML1 action:** Begin logging execution activity in implementation/EXECUTION_LOG.md; this project has all gates approved and is ready for active execution.

---

### LLP-005 — Opening

**Stage:** Executing
**Stage source:** approval_record
**Health:** on-track
**Project type:** Operational

**What this project is:** Establishes a repeatable opening function that converts engagement-authorized matters into operationally ready open matters, producing an opening task log, financial readiness status, and Gate 3 approval packet.

**Artifact gaps (current stage):**
- Execution logs present: EXECUTION_LOG.md, DECISION_LOG.md, CHANGE_LOG.md, ISSUE_LOG.md, DELIVERABLES_TRACKER.md, QA_CHECKLIST.md
- None identified

**Blockers for ML1:**
- None

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: yes (2026-03-16)

**Recommended ML1 action:** Monitor execution logs; no gate action required at this time.

---

### LLP-006 — Matter Maintenance

**Stage:** Executing
**Stage source:** approval_record
**Health:** on-track
**Project type:** Operational

**What this project is:** Establishes a repeatable matter maintenance function keeping open matter records accurate across Clio, SharePoint, and Gmail, producing an exception list and ML1 action queue on each maintenance cycle.

**Artifact gaps (current stage):**
- Execution logs present: EXECUTION_LOG.md, DECISION_LOG.md, CHANGE_LOG.md, ISSUE_LOG.md, QA_CHECKLIST.md, DELIVERABLES_TRACKER.md
- Minor: split metric schema in planning/ not yet consolidated into single METRICS.md — flagged for cleanup, does not block execution

**Blockers for ML1:**
- None

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: yes (2026-03-18, retroactive)

**Recommended ML1 action:** Monitor execution logs; plan a future cleanup pass to consolidate the split metric schema.

---

### LLP-007 — Admin

**Stage:** Initiating
**Stage source:** inferred from artifacts
**Health:** at-risk
**Project type:** Operational

**What this project is:** Governs the cross-cutting admin control layer for fulfillment operations, making operational risk-management controls explicit, bounded, and ML1-reviewable.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: missing (no file in initiation/)

**Blockers for ML1:**
- No ML1 approval on record — project is unstaged without a signed APPROVAL_RECORD

**Approval status:** APPROVAL_RECORD.md present: no | ML1 metric approval: not yet required

**Recommended ML1 action:** Create and sign APPROVAL_RECORD.md to formally record the initiation decision and authorize advancement to Planning.

---

### LLP-008 — Closing

**Stage:** Initiating
**Stage source:** inferred from artifacts
**Health:** at-risk
**Project type:** Operational

**What this project is:** Governs fulfillment closing as the administrative end-state for financial and record closure, with explicit preconditions and ML1 approval boundaries for matter closeout.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: missing (no file in initiation/)

**Blockers for ML1:**
- No ML1 approval on record — project is unstaged without a signed APPROVAL_RECORD

**Approval status:** APPROVAL_RECORD.md present: no | ML1 metric approval: not yet required

**Recommended ML1 action:** Create and sign APPROVAL_RECORD.md to formally record the initiation decision and authorize advancement to Planning.

---

### LLP-016 — Compliance

**Stage:** Initiating
**Stage source:** inferred from artifacts
**Health:** at-risk
**Project type:** Operational

**What this project is:** Governs the operational compliance control layer for recurring firm obligations, making compliance work explicit, reviewable, and bounded by ML1 authority.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: missing (no file in initiation/)

**Blockers for ML1:**
- No ML1 approval on record — project is unstaged without a signed APPROVAL_RECORD

**Approval status:** APPROVAL_RECORD.md present: no | ML1 metric approval: not yet required

**Recommended ML1 action:** Create and sign APPROVAL_RECORD.md to formally record the initiation decision and authorize advancement to Planning.

---

### LLP-011 — Funnel 1 Management

**Stage:** Executing
**Stage source:** approval_record
**Health:** on-track
**Project type:** Management

**What this project is:** Establishes controlled execution governance for Funnel 01 as the current-state acquisition funnel, maintaining campaign governance, asset control, and signal/reporting structure while F02 is built.

**Artifact gaps (current stage):**
- Execution logs present: EXECUTION_LOG.md, DECISION_LOG.md, CHANGE_LOG.md, ISSUE_LOG.md, DELIVERABLES_TRACKER.md, QA_CHECKLIST.md
- Note: metric thresholds in planning/ML1_METRIC_APPROVAL.md are pending numeric lock from first 4-week baseline (per approval terms)

**Blockers for ML1:**
- Metric numeric thresholds not yet locked — due within 30 days of execution start (per 2026-03-16 approval terms)

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: conditional (framework approved; numeric thresholds pending baseline)

**Recommended ML1 action:** Lock metric thresholds in ML1_METRIC_APPROVAL.md once first 4-week baseline is complete.

---

### LLP-012 — Funnel 2 Management

**Stage:** Planning
**Stage source:** approval_record
**Health:** watch
**Project type:** Management

**What this project is:** Plans the execution of Funnel 02 as the corporate-law services funnel targeting Ontario operating companies with $1M+ annual revenue, including the accountant referral network as primary acquisition channel and Corporate Health Check as the entry offer.

**Artifact gaps (current stage):**
- Stage 2 canonical planning artifacts: SCOPE_DEFINITION.md/SCOPE_STATEMENT.md, WORKPLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md are all absent from planning/
- Only research notes and draft METRICS.md/ML1_METRIC_APPROVAL.md (placeholder, no thresholds) are present in planning/
- ML1 capacity decisions required before F02 launch: maximum active matter count, minimum matter value floor, practice area categories to stop accepting

**Blockers for ML1:**
- Full set of canonical Stage 2 planning artifacts not yet drafted
- ML1 capacity decisions outstanding (max active matters, value floor, categories to stop accepting)
- ML1_METRIC_APPROVAL.md is a placeholder with no approved thresholds

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: no (placeholder only)

**Recommended ML1 action:** Direct production of SCOPE_STATEMENT.md, WORKPLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md; provide capacity decisions required before Planning gate can close.

---

### LLP-013 — Funnel 3 Management

**Stage:** Planning
**Stage source:** approval_record
**Health:** watch
**Project type:** Management

**What this project is:** Plans the execution and optimization of Funnel 03 for payments/MSB/PSP regulatory counsel, including networking as a controlled business development channel, and makes the full F03 offer stack explicit as a governed acquisition system.

**Artifact gaps (current stage):**
- All six canonical Stage 2 planning artifacts are drafted (SCOPE_STATEMENT.md, WORKPLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md)
- METRICS.md present with 7 KPIs and proposed thresholds but ML1 numeric threshold approval not yet recorded
- ML1_METRIC_APPROVAL.md is a placeholder

**Blockers for ML1:**
- ML1 must approve numeric metric thresholds in METRICS.md before Planning -> Executing gate can close

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: no (placeholder only)

**Recommended ML1 action:** Review and approve metric thresholds in planning/METRICS.md to close the Planning gate and authorize Executing.

---

### LLP-023 — Matter Command and Control

**Stage:** Planning
**Stage source:** inferred from artifacts (approval_record does not formally close gates)
**Health:** watch
**Project type:** Strategic

**What this project is:** Builds a single command and control layer for matters providing deterministic morning visibility on movement, stalls, and exceptions using read-only connectors to Clio, SharePoint, and Gmail without overriding any source of truth.

**Artifact gaps (current stage):**
- Planning artifacts present: SCOPE_STATEMENT.md, PROJECT_PLAN.md, MILESTONE_PLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md, METRICS.md, IMPLEMENTATION_SPEC.md
- APPROVAL_RECORD.md does not record a formal ML1 gate decision for Initiating -> Planning or Planning -> Executing
- Initiating artifacts: PROJECT_CHARTER.md, RISK_SCAN.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md present; PROBLEM_STATEMENT.md and APPROVAL_RECORD.md (formal ML1 gate) not confirmed

**Blockers for ML1:**
- No formal ML1 gate closure recorded for Initiating -> Planning in APPROVAL_RECORD.md
- Planning -> Executing gate not submitted or approved

**Approval status:** APPROVAL_RECORD.md present: yes (but gates not formally closed) | ML1 metric approval: not confirmed

**Recommended ML1 action:** Record formal gate decisions in APPROVAL_RECORD.md for both Initiating -> Planning and Planning -> Executing to convert the drafted planning packet into authorized execution.

---

### LLP-024 — NDA Esq

**Stage:** Executing
**Stage source:** approval_record
**Health:** on-track
**Project type:** Strategic

**What this project is:** Builds and launches an AI-powered NDA review SaaS with three workstreams — product development, customer acquisition, and operations — enabling users to upload NDAs for AI risk analysis with an optional human lawyer review tier.

**Artifact gaps (current stage):**
- Execution logs present: EXECUTION_LOG.md, DECISION_LOG.md, CHANGE_LOG.md, ISSUE_LOG.md, DELIVERABLES_TRACKER.md, QA_CHECKLIST.md
- Minor: RISK_SCAN.md and BUSINESS_CASE.md added 2026-03-15 to align with policy; no separate ML1 approval recorded for these two artifacts (noted in APPROVAL_RECORD.md)

**Blockers for ML1:**
- None

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: yes (2026-03-18)

**Recommended ML1 action:** Monitor execution logs; optionally record acknowledgment of the two retroactively added initiation artifacts.

---

### LLP-025 — Marketing Strategy

**Stage:** Planning
**Stage source:** approval_record
**Health:** watch
**Project type:** Management

**What this project is:** Governs Levine Law's marketing strategy as a managed project, maintaining positioning, objectives, ICP definitions, funnel portfolio governance, and the F01-to-F02 transition plan.

**Artifact gaps (current stage):**
- Stage 2 planning artifacts present: SCOPE_STATEMENT.md, WORKPLAN.md, ASSUMPTIONS_CONSTRAINTS.md, DEPENDENCIES.md, RISK_REGISTER.md, COMMUNICATION_PLAN.md
- METRIC_FRAMEWORK.md drafted (KPI definitions and threshold placeholders) but no ML1_METRIC_APPROVAL.md with approved thresholds
- Planning gate decision recorded as "Pending ML1 review"

**Blockers for ML1:**
- ML1 must approve metric thresholds and record formal Planning gate decision before Executing is authorized

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: no (METRIC_FRAMEWORK.md placeholder only)

**Recommended ML1 action:** Review planning artifacts and approve metric thresholds in METRIC_FRAMEWORK.md; record Planning -> Executing gate decision in APPROVAL_RECORD.md.

---

### LLP-030 — Firm Strategy

**Stage:** Initiating
**Stage source:** approval_record
**Health:** watch
**Project type:** Strategic

**What this project is:** Produces a governing Firm Strategy document (positioning, ICP, service model, 3-year direction) and a Business Plan document (revenue model, acquisition architecture, capacity model, financial milestones) to anchor all active marketing and operations projects.

**Artifact gaps (current stage):**
- All Stage 1 initiation artifacts present and approved
- Planning stage not yet submitted; FIRM_STRATEGY.md, BUSINESS_PLAN.md, FINANCIAL_MODEL.md are stubs only
- No Planning artifacts exist yet

**Blockers for ML1:**
- Planning artifacts have not been drafted; Firm Strategy content itself is stub only

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not yet required (Initiating stage)

**Recommended ML1 action:** Initiate Planning stage by directing production of SCOPE_DEFINITION.md and WORKPLAN.md, and begin substantive work on FIRM_STRATEGY.md; this project is the governing frame for the strategic cluster.

---

### LLP-031 — Corporate Entity Management

**Stage:** Initiating
**Stage source:** approval_record (draft — ML1 approval not yet recorded)
**Health:** at-risk
**Project type:** Strategic

**What this project is:** A build-vs-buy capability decision project determining whether Levine Law should procure entity management software, build internally, or defer, producing an ML1 decision packet covering requirements, options, and tradeoffs.

**Artifact gaps (current stage):**
- All six Stage 1 artifacts are drafted
- APPROVAL_RECORD.md explicitly states: "Initiation Approved By: Not yet approved"
- ML1 initiation approval not recorded

**Blockers for ML1:**
- No ML1 initiation approval on record

**Approval status:** APPROVAL_RECORD.md present: yes (draft) | ML1 metric approval: not yet required

**Recommended ML1 action:** Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md.

---

### LLP-032 — Corporate Clerk

**Stage:** Initiating
**Stage source:** approval_record (draft — ML1 approval not yet recorded)
**Health:** at-risk
**Project type:** Strategic

**What this project is:** A staffing and timing decision project determining how and when Levine Law should hire a corporate clerk, producing an ML1 decision packet covering role purpose, task taxonomy, supervision dependencies, and activation conditions.

**Artifact gaps (current stage):**
- All six Stage 1 artifacts are drafted
- APPROVAL_RECORD.md explicitly states: "Initiation Approved By: Not yet approved"
- ML1 initiation approval not recorded

**Blockers for ML1:**
- No ML1 initiation approval on record

**Approval status:** APPROVAL_RECORD.md present: yes (draft) | ML1 metric approval: not yet required

**Recommended ML1 action:** Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md.

---

### LLP-033 — Associate Lawyer Capacity Expansion

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Strategic

**What this project is:** Designs and implements an Associate Lawyer role that expands firm legal capacity while preserving quality, supervision standards, and risk controls, producing a formally defined associate lawyer framework.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md, PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md present
- APPROVAL_RECORD.md exists but is unsigned placeholder ("Initiation Approved By: ______")
- No ML1 approval recorded

**Blockers for ML1:**
- APPROVAL_RECORD.md is a blank placeholder — no ML1 signature or gate decision

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Sign APPROVAL_RECORD.md to formally record the initiation decision.

---

### LLP-034 — Partner Supervision

**Stage:** Initiating
**Stage source:** approval_record (draft — ML1 approval not yet recorded)
**Health:** at-risk
**Project type:** Strategic

**What this project is:** Defines the supervision and capacity-control framework Levine Law needs before adding delegated work or additional delivery roles, producing a partner-supervision model with review/escalation boundaries and measurable supervision indicators.

**Artifact gaps (current stage):**
- All six Stage 1 artifacts are drafted
- APPROVAL_RECORD.md explicitly states: "Initiation Approved By: Not yet approved"
- ML1 initiation approval not recorded

**Blockers for ML1:**
- No ML1 initiation approval on record

**Approval status:** APPROVAL_RECORD.md present: yes (draft) | ML1 metric approval: not yet required

**Recommended ML1 action:** Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md.

---

### LLP-015 — Corporate Practice Area Initiative

**Stage:** Initiating (Parked)
**Stage source:** approval_record
**Health:** on-track
**Project type:** Strategic

**What this project is:** A governed placeholder for a possible future corporate practice area packet; currently parked by ML1 decision pending future reactivation.

**Artifact gaps (current stage):**
- None — all Stage 1 artifacts complete; parked decision recorded with ML1 approval 2026-04-01

**Blockers for ML1:**
- None — parked state is the intended outcome

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not applicable (parked)

**Recommended ML1 action:** No action required; reactivate only when and if ML1 directs.

---

### LLP-035 — Contracts Practice Area Initiative

**Stage:** Initiating (Parked)
**Stage source:** approval_record
**Health:** on-track
**Project type:** Strategic

**What this project is:** A governed placeholder for a possible future contracts practice area packet; currently parked by ML1 decision pending future reactivation.

**Artifact gaps (current stage):**
- None — all Stage 1 artifacts complete; parked decision recorded with ML1 approval 2026-04-01

**Blockers for ML1:**
- None — parked state is the intended outcome

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not applicable (parked)

**Recommended ML1 action:** No action required; reactivate only when and if ML1 directs.

---

### LLP-036 — Financial Services Practice Area Initiative

**Stage:** Initiating (Parked)
**Stage source:** approval_record
**Health:** on-track
**Project type:** Strategic

**What this project is:** A governed placeholder for a possible future financial services practice area packet; currently parked by ML1 decision pending future reactivation.

**Artifact gaps (current stage):**
- None — all Stage 1 artifacts complete; parked decision recorded with ML1 approval 2026-04-01

**Blockers for ML1:**
- None — parked state is the intended outcome

**Approval status:** APPROVAL_RECORD.md present: yes | ML1 metric approval: not applicable (parked)

**Recommended ML1 action:** No action required; reactivate only when and if ML1 directs.

---

### LLP-017 — Strategic Risk

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" across all sections — no substantive purpose statement has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md: content is placeholder ("To be defined by ML1")
- APPROVAL_RECORD.md: unsigned placeholder
- Note: PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md are present in initiation/ but charter itself is unsubstantiated

**Blockers for ML1:**
- Charter content is undefined — ML1 must define the project purpose before initiation artifacts are meaningful
- APPROVAL_RECORD.md is unsigned

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or direct a deferred/park decision.

---

### LLP-018 — Financial Risk

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** Governs financial risk visibility and escalation for Levine Law, covering major financial exposures, thresholds, and escalation logic as the firm's financial operations mature.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: unsigned placeholder
- All other Stage 1 artifacts present (PROJECT_CHARTER.md, PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md)

**Blockers for ML1:**
- APPROVAL_RECORD.md is unsigned — no ML1 gate decision recorded

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Sign APPROVAL_RECORD.md to formally record the initiation decision.

---

### LLP-001 — Accounting

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Operational

**What this project is:** Governs Levine Law's accounting fact layer so historical financial records are captured, reconciled, and reviewable without crossing into modeling or decision authority.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: unsigned placeholder
- All other Stage 1 artifacts present (PROJECT_CHARTER.md, PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md)

**Blockers for ML1:**
- APPROVAL_RECORD.md is unsigned — no ML1 gate decision recorded

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Sign APPROVAL_RECORD.md to formally record the initiation decision.

---

### LLP-002 — Budgeting

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** Governs Levine Law's budgeting and financial scenario management, anchoring budget assumptions and model outputs as advisory and bounded, linking existing budget content to explicit scope and authority.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: unsigned placeholder
- All other Stage 1 artifacts present (PROJECT_CHARTER.md, PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md)

**Blockers for ML1:**
- APPROVAL_RECORD.md is unsigned — no ML1 gate decision recorded

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Sign APPROVAL_RECORD.md to formally record the initiation decision.

---

### LLP-003 — Weekly Report

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Operational

**What this project is:** Governs the weekly matter-docketing report so ML1 receives a reliable delivery-facing operating summary of matter state, activity periods, blockers, and next actions without changing systems of record.

**Artifact gaps (current stage):**
- APPROVAL_RECORD.md: unsigned placeholder
- All other Stage 1 artifacts present (PROJECT_CHARTER.md, PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md)

**Blockers for ML1:**
- APPROVAL_RECORD.md is unsigned — no ML1 gate decision recorded

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Sign APPROVAL_RECORD.md to formally record the initiation decision.

---

### LLP-009 — Clerk Supervision

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Operational

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" across all sections — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Note: PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md are present but charter is undefined

**Blockers for ML1:**
- Charter content is undefined; ML1 must define the project purpose
- APPROVAL_RECORD.md is unsigned

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or direct a deferred/park decision.

---

### LLP-010 — Associate Supervision

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Operational

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" across all sections — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Note: PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md are present but charter is undefined

**Blockers for ML1:**
- Charter content is undefined; ML1 must define the project purpose
- APPROVAL_RECORD.md is unsigned

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose in PROJECT_CHARTER.md, then sign APPROVAL_RECORD.md or direct a deferred/park decision.

---

### LLP-042 — Portfolio Management

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" across all sections — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts (PROBLEM_STATEMENT.md, SUCCESS_CRITERIA.md, STAKEHOLDERS.md, RISK_SCAN.md) not confirmed present

**Blockers for ML1:**
- Charter content is undefined; all substantive initiation content is missing
- APPROVAL_RECORD.md is unsigned

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md.

---

### LLP-037 — Service Management

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts not confirmed present

**Blockers for ML1:**
- Charter content is undefined; all substantive initiation content is missing

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md or direct a park decision.

---

### LLP-038 — Service Management / Essential

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts not confirmed present

**Blockers for ML1:**
- Charter content is undefined

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md or direct a park decision.

---

### LLP-039 — Service Management / Strategic

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts not confirmed present

**Blockers for ML1:**
- Charter content is undefined

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md or direct a park decision.

---

### LLP-040 — Service Management / Standard

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts not confirmed present

**Blockers for ML1:**
- Charter content is undefined

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md or direct a park decision.

---

### LLP-041 — Service Management / Parked

**Stage:** Initiating
**Stage source:** inferred from artifacts (APPROVAL_RECORD is unsigned placeholder)
**Health:** at-risk
**Project type:** Management

**What this project is:** PROJECT_CHARTER.md content is "To be defined by ML1" — no substantive project purpose has been authored.

**Artifact gaps (current stage):**
- PROJECT_CHARTER.md content is placeholder
- APPROVAL_RECORD.md: unsigned placeholder
- Stage 1 supporting artifacts not confirmed present

**Blockers for ML1:**
- Charter content is undefined

**Approval status:** APPROVAL_RECORD.md present: yes (unsigned placeholder) | ML1 metric approval: not yet required

**Recommended ML1 action:** Define the project purpose and author Stage 1 artifacts, then sign APPROVAL_RECORD.md or direct a park decision.

---

## ML1 Action Queue

Ranked by urgency (most blocking first):

| Rank | Project | Action | Urgency |
|------|---------|--------|---------|
| 1 | LLP-030 Firm Strategy | Begin substantive FIRM_STRATEGY.md and BUSINESS_PLAN.md drafts; initiate Planning stage — this is the governing frame for the entire strategic cluster | high |
| 2 | LLP-023 Matter Command and Control | Record formal ML1 gate decisions for Initiating -> Planning and Planning -> Executing in APPROVAL_RECORD.md; planning artifacts are drafted and waiting | high |
| 3 | LLP-012 Funnel 2 Management | Draft canonical Stage 2 planning artifacts (SCOPE_STATEMENT, WORKPLAN, etc.) and provide ML1 capacity decisions required before F02 launch | high |
| 4 | LLP-013 Funnel 3 Management | Approve numeric metric thresholds in planning/METRICS.md to close the Planning gate | high |
| 5 | LLP-025 Marketing Strategy | Approve metric thresholds and record Planning -> Executing gate decision in APPROVAL_RECORD.md | high |
| 6 | LLP-011 Funnel 1 Management | Lock numeric metric thresholds in planning/ML1_METRIC_APPROVAL.md once 4-week baseline is complete | medium |
| 7 | LLP-031 Corporate Entity Management | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md | medium |
| 8 | LLP-032 Corporate Clerk | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md | medium |
| 9 | LLP-034 Partner Supervision | Review initiation packet and record ML1 approval decision in APPROVAL_RECORD.md | medium |
| 10 | LLP-033 Associate Lawyer | Sign APPROVAL_RECORD.md to record initiation decision | medium |
| 11 | LLP-007 Admin | Create and sign APPROVAL_RECORD.md | medium |
| 12 | LLP-008 Closing | Create and sign APPROVAL_RECORD.md | medium |
| 13 | LLP-016 Compliance | Create and sign APPROVAL_RECORD.md | medium |
| 14 | LLP-001 Accounting | Sign APPROVAL_RECORD.md | low |
| 15 | LLP-002 Budgeting | Sign APPROVAL_RECORD.md | low |
| 16 | LLP-003 Weekly Report | Sign APPROVAL_RECORD.md | low |
| 17 | LLP-018 Financial Risk | Sign APPROVAL_RECORD.md | low |
| 18 | LLP-017 Strategic Risk | Define charter content and sign APPROVAL_RECORD.md or park | low |
| 19 | LLP-009 Clerk Supervision | Define charter content and sign APPROVAL_RECORD.md or park | low |
| 20 | LLP-010 Associate Supervision | Define charter content and sign APPROVAL_RECORD.md or park | low |
| 21 | LLP-037–041 Service Management cluster | Define charter content and sign APPROVAL_RECORD.md or park each | low |
| 22 | LLP-042 Portfolio Management | Define charter content and sign APPROVAL_RECORD.md | low |
| 23 | LLP-014, LLP-026, LLP-027 | Begin Planning artifacts per approval terms from 2026-04-01 | low |

---

## Rule

Do not advance a project gate without explicit ML1 approval.
