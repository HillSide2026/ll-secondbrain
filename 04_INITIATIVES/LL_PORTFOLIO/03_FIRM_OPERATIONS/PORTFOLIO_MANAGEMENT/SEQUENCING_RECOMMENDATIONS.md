# Sequencing Recommendations

- Generated: 2026-04-01T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Recommended ML1 Attention Sequence

### First tier — unblock the intake and capture cluster

1. **LLP-014 Intake Management** — Planning artifacts must be produced first within the intake cluster. The LLP-014 APPROVAL_RECORD explicitly records that LLP-027/028/029 Planning artifacts depend on LLP-014's stage-gate definitions and handoff protocols. Producing SCOPE_DEFINITION.md and WORKPLAN.md here is the critical path prerequisite for all three subprojects. Advancing LLP-014 into active Planning unlocks LLP-027's triage logic and surfaces the handoff requirements LLP-028 needs for scope definition.

2. **LLP-026 Lead Capture** — Run Planning in parallel with LLP-014 (per the LLP-014 APPROVAL_RECORD: "LLP-026 Planning should run in parallel to ensure lead routing into the pipeline is defined before LLP-027 builds its inquiry receipt system"). LLP-026 Planning does not depend on LLP-014 outputs to begin, but its routing configuration must be finalized against LLP-014's routing decisions before LLP-027 can lock down inquiry format. Starting LLP-026 Planning concurrent with LLP-014 is the correct sequencing.

3. **LLP-027 Inquiries** — Planning can begin in parallel but cannot be finalized until: (a) LLP-014 Planning has defined the pipeline stage structure and handoff protocol, and (b) LLP-026 Planning has established the inquiry format entering the pipeline. LLP-027's triage logic and SLA targets are the outputs that in turn define the handoff gate LLP-028 depends on.

4. **LLP-028 Consults** — Cannot enter Planning until LLP-027 defines its handoff protocol AND LLP-028 has a complete initiation packet (currently a stub — no Stage 1 artifacts exist). Sequencing: initiate LLP-028 first, then begin Planning only after LLP-027 Planning is sufficiently advanced to specify what a "qualified handoff" looks like.

5. **LLP-029 Onboarding** — Last in the intake sequence. Depends on LLP-028 defining what a retained client looks like at handoff. Also requires coordination with LLP-004 (operational onboarding counterpart) to confirm scope boundary before Planning begins. Must be initiated first (stub only currently).

---

### Second tier — close the funnel planning gates that feed LLP-026

6. **LLP-013 Funnel 3 Management** — Only one outstanding gap: ML1 metric threshold approval. All planning artifacts are present. Closing this gate is a single ML1 decision and immediately converts LLP-013 from Planning to Executing. This matters for LLP-026 because F3 is one of three funnels feeding lead capture — LLP-026 Planning needs to know the F3 CTA and routing configuration before it can design capture for that channel. Close this gate as early as possible.

7. **LLP-012 Funnel 2 Management** — Highest planning debt in the marketing cluster: all six canonical Stage 2 artifacts are absent. LLP-026 Planning will need F2 CTA specifications before F2 lead capture can be configured. This is not a blocker for starting LLP-026 Planning, but it is a blocker for finalizing LLP-026's F2 capture scope. ML1 capacity decisions (max matters, value floor, category stop-accepts) are required before the Planning gate can close here.

8. **LLP-011 Funnel 1 Management** — Executing, but metric thresholds not yet locked (due within 30 days of execution start per approval terms). F1 is the current revenue funnel; its baseline data will inform LLP-026 Planning on F1 capture volume and conversion rates. Lock thresholds once the 4-week baseline window closes.

---

### Third tier — strategic frame and governance

9. **LLP-030 Firm Strategy** — Governing frame for the entire cluster. Capacity ceiling and matter value floor decisions required for LLP-012 Planning, F02 launch capacity modeling, and LLP-013's demand projections (explicitly referenced in LLP-013 DEPENDENCIES.md: "F3 demand projections must stay within 20 billable hour/week ceiling and 12–18 active matter ceiling"). Initiating Planning here is high leverage even if LLP-030 is not a blocker for the intake cluster specifically.

10. **LLP-025 Marketing Strategy** — Metric approval and Planning gate decision pending. This project governs the F01-to-F02 transition plan and accountant referral program (IMP-01), which is also the gate for SPE-01 activation in LLP-013. Closing this gate has downstream effects on LLP-012 (F2 channel strategy) and LLP-013 (accountant referral source).

11. **LLP-023 Matter Command and Control** — Planning artifacts complete and ready for execution. Formal gate closure is a documentation action only. Advance this as soon as bandwidth allows — it provides the morning visibility layer on matters that will become more critical as F2/F3 intake volume grows.

---

### Deferred tier — initiation approvals for at-risk cluster

12. Batch process initiation approvals for the unsigned/missing-approval cluster: LLP-031, LLP-032, LLP-034, LLP-033, LLP-007, LLP-008, LLP-016 — these are all single-action items (sign or create APPROVAL_RECORD.md) and can be processed as a batch in one ML1 session.

13. Placeholder/undefined-charter cluster (LLP-017, LLP-009, LLP-010, LLP-037–041, LLP-042) — ML1 must decide whether to define, defer, or park each; these are not blocking any active work and can be addressed in a dedicated governance session.

---

## Dependency-Driven Sequencing Constraints

- **LLP-014 must advance into Planning before LLP-027 Planning artifacts can be finalized** — recorded in LLP-014 APPROVAL_RECORD.md: "Planning must sequence LLP-014 before finalizing subproject (LLP-027, LLP-028, LLP-029) Planning artifacts, since the parent protocol governs the handoff logic each subproject depends on."

- **LLP-026 Planning must run parallel to LLP-014 Planning, not after it** — recorded in LLP-014 APPROVAL_RECORD.md: "LLP-026 Planning should run in parallel to ensure lead routing into the pipeline is defined before LLP-027 builds its inquiry receipt system." LLP-026 routing decisions feed into LLP-027 scope.

- **LLP-027 Planning cannot be finalized until LLP-026 establishes inquiry format** — recorded in LLP-027 APPROVAL_RECORD.md: "Planning must coordinate with LLP-026 (on inquiry format) and LLP-028 (on handoff requirements) before triage and handoff logic is finalized."

- **LLP-028 Planning cannot begin until LLP-027 Planning has defined the handoff protocol** — LLP-028 is the receiving stage; it cannot define its own intake scope until LLP-027 specifies what a qualified handoff looks like. LLP-028 must also be initiated first (no Stage 1 artifacts yet).

- **LLP-029 Planning cannot begin until LLP-028 defines what a retained client looks like at handoff** — LLP-029 is the final intake stage; it requires LLP-028's output definition and must coordinate scope boundaries with LLP-004 (operational counterpart). LLP-029 must also be initiated first.

- **LLP-026 Planning requires funnel CTA specifications from LLP-011, LLP-012, LLP-013** — LLP-026 governs capture across all three funnels; finalizing F2 and F3 capture configuration depends on LLP-012 and LLP-013 reaching sufficient planning maturity to specify their CTAs. LLP-011 is already executing and its capture configuration is established.

- **LLP-013 channel activation depends on LLP-012 F02 website being live** — recorded in LLP-013 DEPENDENCIES.md: BSE-01 (blog/SEO for F3) is blocked until levine-law.ca traffic baseline is established via F02 website live gate. This means LLP-012 Executing is a soft prerequisite for LLP-013 reaching full channel activation.

- **LLP-030 Firm Strategy capacity decisions are required inputs for LLP-012 Planning** — LLP-013 DEPENDENCIES.md explicitly requires F3 demand projections to stay within the capacity ceiling defined in FIRM_STRATEGY.md / BUSINESS_PLAN.md. LLP-012 Planning similarly requires ML1 to provide the maximum active matter count and value floor before its Planning gate can close.

---

## Intake Cluster Sequencing — Summary Map

```
LLP-014 Planning (produce stage-gate definitions + handoff protocol)
     |
     +-- LLP-026 Planning [parallel] (produce routing + CTA configuration scope)
     |        |
     |        +-- feeds inquiry format into LLP-027
     |
     +-- LLP-027 Planning (finalize after LLP-014 stage structure + LLP-026 inquiry format)
              |
              +-- LLP-028 Initiation then Planning (depends on LLP-027 handoff spec)
                       |
                       +-- LLP-029 Initiation then Planning (depends on LLP-028 handoff + LLP-004 coordination)
```
