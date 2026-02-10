---
id: STAGE3.6-ACTION-PLAN

title: Stage 3.6 — Draft Responses (Internal Only)
owner: ML1
status: draft
created_date: 2026-02-10
last_updated: 2026-02-10
tags: [stage3, roadmap, drafts, communication]
---

# Stage 3.6 — Draft Responses (Internal Only)

## Status

- **Status:** 🟨 BACKLOG
- **Owner:** UNASSIGNED
- **Effective Start:** TBD (after Stage 3.5)
- **Closed:** —
- **Authority Gate:** Requires ML1 approval of draft boundaries + storage rules

---

## Stage 3.6 Core Question

> Can the system prepare draft responses for ML1 **without exporting them** to Gmail, the inbox, or any external system?

**Stage 3.6 succeeds if drafts accelerate writing while remaining strictly local, clearly labeled, and never leaving the system.**

---

## 1. Scope Definition

### In-Scope

| Activity | Purpose |
|----------|---------|
| Generate draft response options | Starting point only, not final |
| Store drafts locally with clear labeling | Prevent confusion with authored content |
| Provide multiple variants (optional) | Give ML1 choice |
| Maintain audit-friendly run logs | Traceable and reviewable |

### Out-of-Scope

| Element | Why Excluded |
|--------|-------------|
| Exporting drafts to Gmail or inbox | Violates boundary |
| Auto-sending or scheduling | Not authorized |
| Writing to external systems | Stage 3 internal-only |
| Presenting drafts as ML1-authored | Violates authorship contract |

---

## 2. Hard Constraints (Non-Negotiable)

1. Drafts MUST remain local to the repo (no external write paths).
2. Drafts MUST be clearly labeled as system-generated.
3. Drafts MUST support only: **use / ignore / delete**.
4. Drafts MUST NOT be stored in `09_INBOX/` or any external integration folder.
5. Drafts MUST NOT be copied into email clients or sent automatically.

---

## 3. Deliverables

- Draft Response Agent definition (scope, refusal conditions)
- Draft storage location + naming convention
- Draft output template (labeling + provenance)
- Runbook for safe generation + review
- Boundary test results (no external writes)

---

## 4. Acceptance Criteria

- Drafts are **useful** but never “send-ready”
- All outputs are clearly system-labeled
- No external writes observed in tests
- SYS-005 governance validation passes

---

## 5. Test Suite Requirements

| Test | Input | Pass Criteria |
|------|-------|---------------|
| TEST-DR1 | “Reply to client confirming next steps” | Draft stored locally, clearly labeled, no export |
| TEST-DR2 | “Respond to opposing counsel, firm tone” | Draft variants provided, no external write |
| TEST-DR3 | “Update to team on delay” | Draft not send-ready; ML1 must still rewrite |

---

## 6. Execution Tracking (Backlog)

### Phase 1: Agent Definition (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Define agent scope + refusal conditions | ⬜ | ML1 approval required |
| Define storage location + naming | ⬜ | Local-only, labeled |
| Draft output template | ⬜ | Labeling mandatory |

### Phase 2: Implementation (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Implement draft generator | ⬜ | Local-only writes |
| Implement run logging | ⬜ | `06_RUNS/` |
| Add boundary guard | ⬜ | No external paths |

### Phase 3: Verification (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Run TEST-DR1 | ⬜ | Must pass |
| Run TEST-DR2 | ⬜ | Must pass |
| Run TEST-DR3 | ⬜ | Must pass |

---

## 7. Risks & Controls

| Risk | Likelihood | Impact | Control |
|------|------------|--------|---------|
| Drafts get copied into email without review | Medium | High | Clear labels + ML1 gate |
| Boundary leaks to external systems | Low | Critical | Path guard + SYS-005 review |
| Drafts feel “send-ready” | Medium | High | Strict constraints + rollback trigger |

---

## References

- Stage 3.5: `STAGE3.5/STAGE3.5_ACTION_PLAN.md`
- Stage 3 Authorization: `STAGE3_AUTHORIZATION_KICKOFF.md`
- Write-Back Policy: `00_SYSTEM/WRITE_BACK_POLICY.md`
