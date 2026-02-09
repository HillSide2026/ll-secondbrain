---
id: 02_playbooks__agent_deployment_guide_md
title: Agent Deployment Guide
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Agent Deployment Guide

**Version:** 2.0
**Last Updated:** 2026-01-27
**Status:** Active

---

## Overview

This guide documents how to deploy and invoke the system-level agents in the Levine Law Second Brain system. It defines *how agents are used*, *what they are allowed to do*, and *where human authority intervenes*.

**Runtime:** Claude Code agents
**Stage:** 2.1 (Agent Runtime Setup)

This document is an operational artifact. Agent Definitions remain the source of truth for permissions and constraints.

---

## Agent Inventory

| Agent ID | Name                | Purpose                                            |
| -------- | ------------------- | -------------------------------------------------- |
| SYS-005  | System Governance   | Validate compliance, review changes, enforce rules |
| SYS-006  | Portfolio Planning  | Manage roadmaps, backlog, stage transitions        |
| SYS-007  | Integration Steward | Govern integration specs (read-only)               |
| SYS-008  | Knowledge Curation  | Organize, index, maintain knowledge artifacts      |
| SYS-009  | Runbook & QA        | Draft runbooks, validate artifact quality          |

---

## Agent Definition vs Playbook

### Agent Definition

* Located in `00_SYSTEM/AGENTS/`
* Defines agent capabilities, permissions, and constraints
* Machine-readable contract for agent behavior
* Includes:

  * Authority scope
  * Allowed inputs
  * Allowed outputs
  * Explicit non-authority
  * Refusal conditions

### Playbook

* Located in `02_PLAYBOOKS/`
* Human-readable operational guide
* Explains how to invoke and use agents correctly
* Includes:

  * Invocation patterns
  * Examples
  * Troubleshooting

**Rule:** Playbooks may *never* expand authority beyond what is defined in Agent Definitions.

---

## Invocation Patterns

### General Pattern

```
Invoke agent [AGENT_ID] to [ACTION].

Inputs:
- [Input 1]: [path or value]
- [Input 2]: [path or value]

Scope: [explicit, bounded scope]
Context: [relevant context]

Produce: [expected output type]
```

**Scope is normative.** Agents must refuse to act outside the declared scope.

---

## Agent Invocation Guides

### SYS-005 — System Governance

**Use when:** Validating PR compliance, checking folder placement, reviewing doctrine alignment

```
Review PR changeset for governance compliance.

Inputs:
- PR diff or artifact paths: [paths]
- Folder map: 00_SYSTEM/FOLDER_MAP.md
- Schemas: 00_SYSTEM/SCHEMAS.md
- Doctrine: 01_DOCTRINE/

Scope: full governance review
Context: PR review for [PR description]

Produce: Governance compliance report with pass/fail and recommendations.
```

---

### SYS-006 — Portfolio Planning

**Use when:** Reviewing backlog, preparing stage closure, sequencing roadmap items

```
Review backlog and prepare stage closure recommendation.

Inputs:
- Backlog: 04_INITIATIVES/SYSTEM_PORTFOLIO/BACKLOG.md
- Stage artifacts: 04_INITIATIVES/SYSTEM_PORTFOLIO/01_ACTIVE_ROADMAPS/STAGE2/STAGE2.1/
- DoD checklist: STAGE2_AUTHORIZATION_KICKOFF.md

Scope: Stage 2.1 closure review
Context: Weekly cycle 2026-W05

Produce: Stage closure recommendation with DoD evidence.
```

---

### SYS-007 — Integration Steward

**Role:** Read-only integration governance agent

**Use when:** Reviewing integration specs, verifying read-only constraints, preparing capability matrices

```
Review integration spec for no-write-path compliance.

Inputs:
- Integration spec: [path]
- Write-back policy: 00_SYSTEM/WRITE_BACK_POLICY.md

Scope: Specified integration only
Context: Stage 2.1 read-only validation

Produce: No-write-path verification report and capability matrix.
```

**Note:** SYS-007 has no execution or external write authority.

---

### SYS-008 — Knowledge Curation

**Use when:** Triaging INBOX, identifying stale artifacts, proposing placements

```
Triage INBOX and propose artifact placements.

Inputs:
- INBOX: 09_INBOX/
- Folder map: 00_SYSTEM/FOLDER_MAP.md

Scope: INBOX-only
Context: Weekly cycle 2026-W05

Produce: INBOX triage report with promotion proposals.
```

---

### SYS-009 — Runbook & QA

**Use when:** Validating artifact quality, checking schemas, reviewing runbook drafts

```
Validate artifact for schema compliance.

Inputs:
- Artifact: [path]
- Schemas: 00_SYSTEM/SCHEMAS.md
- Handoff map: 01_ACTIVE_ROADMAPS/STAGE1/STAGE1.3/STAGE1.3_HANDOFF_MAP.md

Scope: Full QA validation
Context: Artifact review request

Produce: QA validation report with pass/fail and issue list.
```

---

## Standard Output Format

All agents must produce outputs using this structure:

```markdown
## Summary
- (3–5 bullets)

## Findings
1. ...
2. ...

## Recommendations
1. ...
2. ...

## Actions
- [ ] ...
- [ ] ...

## Escalations Required (if any)
- ML1 approval required because: ...

## Evidence
- file_path:line_number

## Assumptions / Confidence
- ...
```

---

## Write-Back Policy

All agents operate under `00_SYSTEM/WRITE_BACK_POLICY.md`:

1. **Local-first:** All work lands in repo first
2. **No external writes:** External tool writes are disallowed in Stage 2.1
3. **ML1 approval required:** External writes require explicit ML1 approval

### Allowed Write Locations by Agent

| Agent   | Allowed Locations                                  |
| ------- | -------------------------------------------------- |
| SYS-005 | Compliance reports, governance review notes        |
| SYS-006 | BACKLOG.md (within scope), planning reports        |
| SYS-007 | Integration specs (versioned), capability matrices |
| SYS-008 | Index files, triage reports                        |
| SYS-009 | QA reports, runbook drafts                         |

---

## ML1 Approval Boundaries

ML1 approval is required when:

* An action would modify schemas or doctrine
* An action would enable external writes
* An action would change agent authority or scope
* An agent escalates uncertainty beyond defined rules

Canonical reference: `00_SYSTEM/ML1_APPROVAL_BOUNDARIES.md`

---

## Agent Versioning and Status

### Version Format

* `v<major>.<minor>`
* Major: Breaking changes to permissions or outputs
* Minor: Non-breaking enhancements

### Status Definitions

* **Draft:** Safe for analysis and reporting; write-back requires review
* **Active:** Approved for operation within defined constraints

### Current Versions

| Agent   | Version | Status |
| ------- | ------- | ------ |
| SYS-005 | v1.0    | Active |
| SYS-006 | v1.0    | Active |
| SYS-007 | v1.0    | Active |
| SYS-008 | v1.0    | Active |
| SYS-009 | v1.0    | Active |

---

## Troubleshooting

### Agent Refuses to Execute

**Cause:** Scope violation, refusal condition, or approval boundary reached

**Resolution:**

1. Check agent definition
2. Verify scope and inputs
3. Determine if ML1 approval is required
4. Escalate per governance process

### Output Format Non-Compliant

**Resolution:**

1. Re-invoke with explicit format requirement
2. Validate against standard output format
3. Request SYS-009 QA validation

### Prohibited Write Attempt

**Resolution:**

1. Stop execution
2. Review invocation context
3. Run safety rails script
4. Report to SYS-005

---

## Weekly Operating Cycle

1. Run SYS-008 INBOX scan
2. Run SYS-006 backlog update
3. Run SYS-005 compliance check (if PRs pending)
4. Run SYS-007 integration review (if applicable)
5. Run SYS-009 QA validation (if artifacts submitted)
6. Review outputs for format compliance
7. Document cycle results

---

## Known Gaps (Intentional)

* No autonomous cross-agent chaining
* No external writes
* No self-modifying schemas or doctrine
* No implicit authority expansion

---

## Related Documents

* Agent Definitions: `00_SYSTEM/AGENTS/`
* Write-Back Policy: `00_SYSTEM/WRITE_BACK_POLICY.md`
* ML1 Approval Boundaries: `00_SYSTEM/ML1_APPROVAL_BOUNDARIES.md`
* Folder Map: `00_SYSTEM/FOLDER_MAP.md`
* Schemas: `00_SYSTEM/SCHEMAS.md`
* Test Fixtures: `03_TESTS/fixtures/`
* Golden Outputs: `03_TESTS/golden_outputs/`
