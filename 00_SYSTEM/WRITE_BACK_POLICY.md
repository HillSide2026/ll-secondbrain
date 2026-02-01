# System Write-Back Policy

**Version:** v1.0
**Status:** ACTIVE
**Effective:** Stage 2.1 onwards

---

## Purpose

Define rules governing how agents write data to the repository and external systems.

---

## Core Principles

### 1. Local-First
All agent work lands in the repository first. The repo is the system of record.

### 2. Read-Only External Access (Stage 2.1)
During Stage 2.1, all external integrations are **read-only**:
- Gmail: Read emails only
- SharePoint: Read documents only
- Word/OneDrive: Read documents only

No agent may write, create, update, or delete data in external systems during this stage.

### 3. Explicit Authorization Required
Any future write-back capabilities require:
- ML1 explicit approval
- Change summary documenting what will be written
- Rollback plan documenting how to undo changes
- Audit logging of all write operations

---

## Agent Write Permissions

### Allowed Write Locations (Repository)

| Agent | Allowed Write Locations |
|-------|------------------------|
| SYS-005 System Governance | Compliance reports, governance audit outputs |
| SYS-006 Portfolio Planning | Backlog updates, stage closure recommendations, roadmap proposals |
| SYS-007 Integration Steward | Integration specs (versioned), capability matrices, verification reports |
| SYS-008 Knowledge Curation | Triage recommendations, artifact promotion proposals, index updates |
| SYS-009 Runbook & QA | QA validation reports, runbook drafts |

### Prohibited Actions (All Agents)

- Writing to external systems (Gmail, SharePoint, Word, etc.)
- Modifying credentials or secrets
- Changing doctrine without ML1 approval
- Writing outside designated output folders
- Deleting artifacts without governance review

---

## Enforcement

### Pre-Commit Checks
Safety rails validate:
- `.env` is not tracked
- Agent outputs only in allowed folders
- Required frontmatter present for artifact types

### Governance Review
System Governance Agent (SYS-005) validates:
- Output placement compliance
- Write permission boundaries
- Escalation when violations detected

---

## Future Stages

When external write-back is authorized (Stage 3+), the following additional requirements apply:

1. **Change Summary Required**
   - What will be written
   - Target system and location
   - Expected outcome

2. **Rollback Plan Required**
   - How to undo the change
   - Who can execute rollback
   - Time window for rollback

3. **Audit Trail Required**
   - Timestamp of write
   - Agent identifier
   - Exact data written
   - Success/failure status

---

## References

- Agent definitions: `00_SYSTEM/AGENTS/`
- Stage 2.1 Action Plan: `01_ACTIVE_ROADMAPS/STAGE2/STAGE2.1_ACTION_PLAN.md`
- Stage 2 Authorization: `01_ACTIVE_ROADMAPS/STAGE2/STAGE5_AUTHORIZATION_KICKOFF.md`
