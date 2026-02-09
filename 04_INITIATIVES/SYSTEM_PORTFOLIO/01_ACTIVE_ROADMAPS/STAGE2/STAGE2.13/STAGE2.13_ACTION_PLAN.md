---
id: STAGE2.13-ACTION-PLAN

title: Stage 2.13 — Gmail Matter Labeling (Backlog)
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: [stage2, roadmap, gmail, labeling, writeback]
---

# Stage 2.13 — Gmail Matter Labeling (Backlog)

## Status

- **Status:** 🟨 BACKLOG
- **Owner:** UNASSIGNED
- **Effective Start:** TBD (after Stage 2.2 + Stage 2.11)
- **Closed:** —
- **Authority Gate:** Requires ML1 approval for Gmail write-back + audit controls

---

## Stage 2.13 Core Question

> Can the system apply matter-number labels to Gmail messages without violating write-back boundaries or mislabeling client communications?

**Stage 2.13 succeeds if matter-number labeling is accurate, auditable, and strictly bounded to approved write actions.**

---

## 1. Scope Definition

### In-Scope

| Activity | Purpose |
|----------|---------|
| Define Gmail labeling policy (matter-number labels) | Ensure deterministic, approved behavior |
| Implement Gmail write-back (labels only) | Apply matter labels to messages |
| Audit logging for label writes | Traceability + rollback |
| Boundary tests (allowed/denied) | Validate no unintended writes |

### Out-of-Scope

| Element | Why Excluded |
|---------|--------------|
| Moving or deleting messages | Beyond labeling scope |
| Editing message content | Not authorized |
| Automatic labeling without approval gate | Requires explicit ML1 approval |

---

## 2. Implementation Notes (Normative Constraints)

1. Only **label add/remove** operations are permitted.
2. Labels must follow the schema: `LL/1. Delivery/1.1 - <delivery_status>/<matter_id>` (e.g., `LL/1. Delivery/1.1 - Essential/25-927-00003`).
3. Labeling must be based on deterministic attribution rules (no LLM inference).
4. Every label write must be logged with message_id, label, timestamp, and reason.
5. A human approval gate is required per run until ML1 authorizes automation.
6. **Matter attribution confidence standard:** Option B — attribution is permitted only when the message is deterministically associated to a matter via an approved structured source (e.g., pre-approved mapping table, prior authoritative linkage). Free-text inference is prohibited.
7. **Label lifecycle:** labels are created on demand at first authorized use. Label deletion is prohibited; labels may only be added to or removed from messages.

---

## Audit Log

All Gmail label write operations MUST emit an immutable audit record.

**Canonical Store:** ML2-controlled, local-first append-only log (Git-versioned).

**Required Fields:**

* message_id
* gmail_thread_id
* label_applied_or_removed
* matter_id
* operation (add | remove)
* timestamp (UTC, ISO-8601)
* approving_human (identifier)
* approval_artifact_reference
* reason

**Retention:** Indefinite unless superseded by ML1 directive.

**Access Control:** Readable by ML1; LL has no mutation rights.

---

## Human Approval Gate — Mechanism

Until explicitly automated by ML1, every labeling run requires affirmative human authorization.

**Approval Model:** Per-run batch approval.

**Mechanism:**

1. System produces a proposed action manifest (message_ids + labels).
2. Human reviewer (ML1 or delegate) signs approval via an explicit approval artifact (e.g., signed checklist file or CLI approval flag).
3. Approval artifact reference is written into the audit log for every label operation in the batch.
4. Absence of valid approval artifact hard-blocks execution.

---

## 3. Deliverables

- Gmail labeling policy + label naming conventions
- Approved label set and creation plan
- Implementation of label write-back (labels only)
- Audit logging format for label writes
- Minimal verification test (apply + remove label)

---

## 4. Acceptance Criteria

- Labels applied only when matter attribution confidence is sufficient
- No message content changes or moves
- Audit logs produced for every label write
- SYS-005 governance validation passes

---

## 5. Execution Tracking (Backlog)

### Phase 1: Policy + Boundaries (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Define labeling policy | ⬜ | ML1 approval required |
| Define label naming convention | ⬜ | `MATTER-<matter_id>` |

### Phase 2: Implementation (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Implement label write-back | ⬜ | Gmail API labels only |
| Add audit logging | ⬜ | Required for every write |

### Phase 3: Verification (Planned)
| Item | Status | Notes |
|------|--------|-------|
| Apply label to approved message | ⬜ | Must pass |
| Remove label (rollback) | ⬜ | Must pass |

---

## 6. Risks & Controls

| Risk | Likelihood | Impact | Control |
|------|------------|--------|---------|
| Mislabeling emails | Medium | High | Deterministic rules + approval gate |
| Unauthorized writes | Medium | High | Boundary enforcement + SYS-005 review |

---

## References

- Stage 2.2 Action Plan: `STAGE2.2/STAGE2.2_ACTION_PLAN.md`
- Stage 2.11 Action Plan: `STAGE2.11/STAGE2.11_ACTION_PLAN.md`
- Write-Back Policy: `00_SYSTEM/WRITE_BACK_POLICY.md`
