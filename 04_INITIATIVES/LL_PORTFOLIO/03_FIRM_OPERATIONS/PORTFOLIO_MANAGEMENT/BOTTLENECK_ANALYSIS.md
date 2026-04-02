# Bottleneck Analysis

- Generated: 2026-04-01T00:00:00Z
- Agent: LLM-005 Portfolio Management Agent

> Advisory output. ML1 approval required before any action is taken.

---

## Portfolio Bottlenecks

- Planning bottleneck candidates (projects with outstanding planning artifacts): 5 (LLP-012, LLP-013, LLP-023, LLP-025, LLP-014/026/027 entering imminently)
- Measurement bottleneck candidates (projects missing metric threshold approvals): 3 (LLP-011, LLP-012, LLP-013)

---

## Top Bottlenecks

| Artifact / Approval | Missing In N Projects | Impact |
|---------------------|----------------------|--------|
| ML1 metric threshold approval (ML1_METRIC_APPROVAL.md signed with numeric thresholds) | 3 projects (LLP-011, LLP-012, LLP-013) | Blocks Planning-to-Executing gate for LLP-012 and LLP-013; blocks execution quality signal lock for LLP-011. All three are upstream funnels feeding LLP-026 lead capture. |
| SCOPE_DEFINITION.md / SCOPE_STATEMENT.md (canonical Stage 2 artifact) | 4+ projects (LLP-012 missing all 6; LLP-014, LLP-026, LLP-027 entering Planning without this artifact yet drafted) | The most widespread missing artifact type. Indicates that the Stage 2 planning packet template is the structural gap — agents and ML1 need to produce this artifact across the most active Planning projects simultaneously. |
| APPROVAL_RECORD.md (signed ML1 gate decision) | 13+ projects at Stage 1 (LLP-007, LLP-008, LLP-016, LLP-001, LLP-002, LLP-003, LLP-009, LLP-010, LLP-017, LLP-018, LLP-031, LLP-032, LLP-033, LLP-034, LLP-037–042) | The single highest-volume gap type across the portfolio. All are unsigned or missing; none can advance stages without a recorded ML1 decision. Represents the largest approval load item. |
| WORKPLAN.md | 4 projects entering or in Planning (LLP-012, LLP-014, LLP-026, LLP-027) | Required before any execution mobilization; without it, milestone sequencing and resource allocation for the intake/capture cluster cannot be locked. |
| Formal gate closure in APPROVAL_RECORD.md for Planning-to-Executing | 2 projects (LLP-023, LLP-025) | Both have planning artifacts substantially complete but cannot authorize execution without a recorded ML1 gate decision. Low-effort action with high unlock value. |
| Initiation packet (all Stage 1 artifacts) | 2 projects (LLP-028, LLP-029) | Both remain stubs; they cannot enter formal planning until initiated. These are the last two stages of the intake pipeline — without initiation they are structural gaps in the intake chain. |

---

## Assessment

The dominant bottleneck pattern in this portfolio is the **ML1 approval signature** — specifically the absence of signed APPROVAL_RECORD.md entries across the largest segment of the portfolio (Stage 1 projects). This is not a drafting problem; most of those projects have artifacts present. The bottleneck is a single point of human decision authority, and the volume (13+ projects awaiting a signature) is not sustainable to process one-at-a-time. A batch session addressing the unsigned APPROVAL_RECORD cluster in one pass would clear the most numerically significant bottleneck.

The second distinct bottleneck is at the **Stage 2 planning artifact layer** for the marketing and intake cluster: LLP-012 has zero Stage 2 artifacts, while LLP-014, LLP-026, and LLP-027 are entering Planning with no artifacts yet drafted. Without SCOPE_DEFINITION.md and WORKPLAN.md produced and approved for each, the intake pipeline cannot be sequenced. The intake cluster Planning bottleneck is particularly acute because projects cannot finalize their own planning until upstream projects have produced their artifacts first (see SEQUENCING_RECOMMENDATIONS.md).

The third bottleneck is **metric threshold approval**: three executing or near-executing projects (LLP-011, LLP-012, LLP-013) are missing ML1-approved numeric thresholds. Without these, execution quality monitoring cannot operate. For LLP-011 this is time-bound (due within 30 days of execution start); for LLP-012 and LLP-013 it is a hard Planning gate requirement.
