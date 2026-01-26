# Runbook: Runbook & QA Agent

## Purpose
Draft runbooks, validate artifact quality, and perform QA checks.

## Trigger Conditions
- New runbook draft requested
- Artifact validation requested
- Stage deliverable QA review

## Inputs
- Workflow definitions
- `00_SYSTEM/SCHEMAS.md`
- Draft artifacts for review

## Procedure

### Step 1: Schema Validation
- [ ] Load artifact to validate
- [ ] Check YAML frontmatter against SCHEMAS.md
- [ ] Document missing/invalid fields

### Step 2: Content Review
- [ ] Verify required sections present
- [ ] Check for completeness (no TBD/placeholder abuse)
- [ ] Validate internal links/paths exist

### Step 3: Runbook Drafting
- [ ] Define purpose and trigger conditions
- [ ] Document inputs and outputs
- [ ] Write step-by-step procedure
- [ ] Add authority constraints and escalation paths

### Step 4: Cross-Reference Check
- [ ] Verify referenced artifacts exist
- [ ] Check for circular references
- [ ] Validate handoff paths match Handoff Map

### Step 5: QA Report
- [ ] Document pass/fail per check
- [ ] List issues found
- [ ] Recommend approval or revision

## Outputs
- QA validation report
- Runbook drafts
- Issue lists with remediation suggestions

## Authority Constraints
- Cannot execute runbooks in production
- Cannot approve own drafts
- Cannot modify doctrine

## Escalation
- Schema conflicts → System Governance Agent
- Unclear requirements → Portfolio Planning Agent
