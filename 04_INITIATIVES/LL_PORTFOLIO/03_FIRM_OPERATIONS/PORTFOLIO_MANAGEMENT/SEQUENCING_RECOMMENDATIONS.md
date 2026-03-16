# Sequencing Recommendations

- Generated: 2026-03-16T18:00:00Z
- Agent: LLM-005 Portfolio Management Agent (via LLM-001 Chief of Staff)

> Advisory output. ML1 approval required before any action is taken.

## Recommended ML1 Attention Sequence

1. **`LLP-024_NDA_ESQ`** — Approve metric thresholds and make the Planning→Executing gate decision. Hard deadline: M6 milestone is 2026-03-20 (4 days). This is the most time-constrained item in the portfolio. Note: Project ID collision LLP-26-24 with LLP-011 must be resolved simultaneously — see CONTRADICTION_ALERTS.md.

2. **`LLP-011_FUNNEL1_MANAGEMENT`** — Approve metric thresholds and make the Planning→Executing gate decision. The gate packet milestone M6 (target 2026-03-14) is overdue by 2 days. Resolving the Project ID collision with LLP-024 is a prerequisite for clean governance records on this project.

3. **`LLP-006_MAINTENANCE`** — Do not advance until governance hold is resolved. LLM-006 reports Stage 3 execution artifacts exist despite no recorded initiation approval. ML1 must determine: was execution authorized informally? If yes, retroactively approve and document. If no, execution must pause until gate is properly recorded.

4. **`LLP-013_FUNNEL3_MANAGEMENT`** — Direct production of all Stage 2 planning artifacts. Initiation was approved 2026-03-15 (yesterday) but the planning stage has not started. Early action here prevents this project from accumulating the same planning lag as LLP-011.

5. **`LLP-002_CORPORATE_CLERK` + `LLP-003_ASSOCIATE_LAWYER` (batch together)** — Both are substantive initiation packets awaiting ML1 signature only. Approving these in a single session unlocks two currently stalled downstream projects (LLP-009 and LLP-010). Batching minimizes ML1 review time.

## Dependency-Driven Sequencing Constraints

- **LLP-004_ONBOARDING must advance before LLP-005_OPENING** — LLP-005 is sequentially dependent on LLP-004 being operational. Do not advance LLP-005 ahead of LLP-004.
- **LLP-002_CORPORATE_CLERK must be approved before LLP-009_CLERK_SUPERVISION can be substantively defined** — LLP-009 is currently placeholder pending this prerequisite.
- **LLP-003_ASSOCIATE_LAWYER must be approved before LLP-010_ASSOCIATE_SUPERVISION can be substantively defined** — LLP-010 is currently placeholder pending this prerequisite.
- **LLP-005_OPENING depends on LLP-004_ONBOARDING being operational** — The OPENING function receives handoff from the ONBOARDING function; sequencing is fixed.
- **LLP-006_MAINTENANCE depends on LLP-005_OPENING being operational** — The MAINTENANCE function receives handoff from OPENING; sequencing is fixed.
- **Project ID collision LLP-26-24** — LLP-024_NDA_ESQ and LLP-011_FUNNEL1_MANAGEMENT share a project ID. This must be resolved before either project can have unambiguous audit records going forward.
