# Stage 2.2 — Integration Activation: Action Plan

## Status

- **Status:** PAUSED (Phase 2.2.1 complete; Phases 2.2.2–2.2.3 deferred pending Stage 2.3)
- **Owner:** ML1
- **Execution Owner:** Integration Steward Agent (SYS-007)
- **Dependencies:** Stage 2.1 Agent Runtime Setup (CLOSED)
- **Note:** Per ML1 directive (2026-01-28), pivoting to Stage 2.3 Inbox Intelligence Layer

---

## Purpose

Activate read-only external integrations (Gmail → SharePoint → Word) in a controlled, auditable manner, ensuring:

- No write paths exist
- Credentials are securely handled
- Audit logging is implemented
- Integrations are validated before operational use

---

## Multi-Source Intake Architecture

> **The inbox tracks uncertainty, not origin. Sources feed the inbox; they do not define it.**

All integrations in Stage 2.2 are **intake sources** that feed into `09_INBOX/_sources/`:

```
External Source (Gmail/SharePoint/OneDrive)
   ↓
09_INBOX/_sources/<source>/     ← Stage 2.2 writes here
   ↓ (normalization step)
09_INBOX/00_UNTRIAGED/          ← Stage 2.3+ reads from here
```

### Source-Specific Intake Buffers

| Integration | Intake Buffer | Purpose |
|-------------|---------------|---------|
| Gmail | `09_INBOX/_sources/gmail/` | Email metadata, message extracts |
| SharePoint | `09_INBOX/_sources/sharepoint/` | Document snapshots, metadata |
| OneDrive/Word | `09_INBOX/_sources/drive/` | Document content, read-only extracts |

### Key Principles

1. **Source ≠ Status** — All sources are treated equally after normalization
2. **No source bypasses inbox** — SharePoint, Gmail, Drive all enter through `_sources/`
3. **Mechanical buffers only** — `_sources/` folders may reflect quirks of origin systems
4. **Decisions happen after normalization** — Classification is source-agnostic

---

## Scope

### Authorized

Stage 2.2 is authorized to:

- Configure OAuth / API access for external systems
- Use read-only scopes exclusively
- Store credentials in local `.env` files (excluded from git)
- Implement and test audit logging
- Produce verification reports

### Not Authorized

Stage 2.2 is **not** authorized to:

- Enable write-back or mutation capabilities
- Access matter/client-specific data
- Automate polling or background jobs
- Modify doctrine or operating rules

---

## Binding Inputs

### Integration Specifications (Stage 1.2)

Located at: `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE1/STAGE1.2/`

| Spec | Purpose |
|------|---------|
| STAGE2_GMAIL_READ_ONLY_SPEC.md | Gmail integration requirements |
| STAGE2_SHAREPOINT_READ_ONLY_SPEC.md | SharePoint integration requirements |
| STAGE2_WORD_READ_ONLY_SPEC.md | Word/OneDrive integration requirements |
| STAGE2_AUDIT_LOGGING_EXPECTATIONS.md | Audit logging requirements |
| STAGE2_NO_WRITE_PATH_REVIEW.md | No-write-path verification criteria |

### Agent Authority

| Agent | Role |
|-------|------|
| SYS-007 Integration Steward | Primary executor |
| SYS-005 System Governance | Compliance validation |
| SYS-009 Runbook & QA | QA and schema checks |
| ML1 | Approval and escalation authority |

---

## Workstreams & Action Items

### Workstream B1 — Gmail Integration (Phase 2.2.1)

**Owner:** SYS-007 Integration Steward

**Steps:**

1. [ ] Create or select Google Cloud project
2. [ ] Configure OAuth consent screen
   - User type: internal (if applicable)
   - Scopes: Gmail read-only only
3. [ ] Generate OAuth credentials
4. [ ] Store credentials in `.env` (not committed)
5. [ ] Implement audit logging per Stage 1.2
6. [ ] Test read-only access
7. [ ] Verify no-write-path compliance
8. [ ] Produce integration status + compliance report

**Deliverables:**

- Gmail integration configuration (read-only)
- Audit logging confirmation
- No-write-path verification report

---

### Workstream B2 — SharePoint Integration (Phase 2.2.2)

**Owner:** SYS-007 Integration Steward
**Dependency:** Completion of Phase 2.2.1

**Steps:**

1. [ ] Register Azure AD application
2. [ ] Configure Microsoft Graph permissions
   - SharePoint read-only scopes only
3. [ ] Generate client credentials
4. [ ] Store credentials in `.env`
5. [ ] Implement audit logging
6. [ ] Test read-only SharePoint access
7. [ ] Verify no-write-path compliance
8. [ ] Produce integration status + compliance report

**Deliverables:**

- SharePoint integration configuration (read-only)
- Audit logging confirmation
- No-write-path verification report

---

### Workstream B3 — Word / OneDrive Integration (Phase 2.2.3)

**Owner:** SYS-007 Integration Steward
**Dependency:** Completion of Phase 2.2.2

**Steps:**

1. [ ] Enable Word / OneDrive read-only access via Graph
2. [ ] Confirm document-level read-only permissions
3. [ ] Validate no document mutation paths
4. [ ] Implement audit logging
5. [ ] Test read-only document access
6. [ ] Produce integration status + compliance report

**Deliverables:**

- Word/OneDrive integration configuration (read-only)
- Audit logging confirmation
- No-write-path verification report

---

## Governance & QA Checks (Mandatory)

### System Governance (SYS-005)

- Validate declared scopes vs specs
- Confirm no write permissions granted
- Review placement and documentation of artifacts
- Issue pass/fail compliance determination

### Runbook & QA (SYS-009)

- Validate reports against standard output format
- Confirm schema and required sections
- Flag gaps or inconsistencies

---

## Definition of Done (Stage 2.2)

Stage 2.2 is complete when:

- [ ] Gmail read-only integration active and verified
- [ ] SharePoint read-only integration active and verified
- [ ] Word/OneDrive read-only integration active and verified
- [ ] Audit logging implemented for all integrations
- [ ] No-write-path verification completed and documented
- [ ] SYS-005 compliance reports issued (pass)
- [ ] SYS-009 QA validation completed (pass)

---

## Outputs

All outputs must follow the Standard Output Format and be stored in approved locations:

| Output | Location |
|--------|----------|
| Integration configuration summaries | `03_TESTS/agent_outputs/` or designated |
| Audit logging confirmation reports | `03_TESTS/agent_outputs/` or designated |
| No-write-path verification reports | `03_TESTS/agent_outputs/` or designated |
| Governance compliance reports | `03_TESTS/agent_outputs/` or designated |
| QA validation reports | `03_TESTS/agent_outputs/` or designated |

---

## Risks & Controls

| Risk | Likelihood | Impact | Control |
|------|------------|--------|---------|
| OAuth scope creep | Low | High | Explicit scope review + SYS-005 validation |
| Credential exposure | Low | Critical | `.env` only, gitignored, safety rails |
| Undetected write path | Low | High | Explicit no-write-path testing + reports |
| Integration drift | Low | Medium | Specs are binding; changes escalated to ML1 |

---

## Execution Tracking

### Phase 2.2.1: Gmail Integration ✅ COMPLETE
| Item | Status | Date | Notes |
|------|--------|------|-------|
| Google Cloud project | ✅ done | 2026-01-28 | Project configured |
| OAuth consent screen | ✅ done | 2026-01-28 | Read-only scope only |
| Credentials generated | ✅ done | 2026-01-28 | .env populated, refresh token obtained |
| Audit logging | ✅ done | 2026-01-28 | scripts/gmail_integration.py, logs/gmail_audit.log |
| Read-only test | ✅ done | 2026-01-28 | Connected as matthew@levinelegal.ca |
| No-write-path verification | ✅ done | 2026-01-28 | GMAIL_NO_WRITE_PATH_VERIFICATION.md |
| Compliance report | ✅ done | 2026-01-28 | GMAIL_INTEGRATION_COMPLIANCE_REPORT.md |

### Phase 2.2.2: SharePoint Integration
| Item | Status | Date | Notes |
|------|--------|------|-------|
| Azure AD application | ⬜ pending | | |
| Graph permissions | ⬜ pending | | |
| Credentials generated | ⬜ pending | | |
| Audit logging | ⬜ pending | | |
| Read-only test | ⬜ pending | | |
| No-write-path verification | ⬜ pending | | |
| Compliance report | ⬜ pending | | |

### Phase 2.2.3: Word/OneDrive Integration
| Item | Status | Date | Notes |
|------|--------|------|-------|
| Graph access enabled | ⬜ pending | | |
| Document permissions | ⬜ pending | | |
| Audit logging | ⬜ pending | | |
| Read-only test | ⬜ pending | | |
| No-write-path verification | ⬜ pending | | |
| Compliance report | ⬜ pending | | |

---

## References

- Stage 2 Authorization: `01_ACTIVE_ROADMAPS/STAGE2/STAGE2_AUTHORIZATION_KICKOFF.md`
- Write-Back Policy: `00_SYSTEM/WRITE_BACK_POLICY.md`
- ML1 Approval Boundaries: `00_SYSTEM/ML1_APPROVAL_BOUNDARIES.md`
- Credential Inventory: `02_PLAYBOOKS/CREDENTIAL_INVENTORY.md`
- Agent Deployment Guide: `02_PLAYBOOKS/AGENT_DEPLOYMENT_GUIDE.md`
- **Multi-Source Inbox Architecture: `09_INBOX/README.md`**
