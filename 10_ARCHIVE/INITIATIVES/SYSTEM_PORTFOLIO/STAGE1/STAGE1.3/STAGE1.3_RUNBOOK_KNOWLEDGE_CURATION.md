# Runbook: Knowledge Curation Agent

## Purpose
Organize, index, and maintain system knowledge artifacts.

## Trigger Conditions
- New artifact in INBOX
- Periodic index refresh
- Staleness review requested

## Inputs
- `09_INBOX/` contents
- `00_SYSTEM/FOLDER_MAP.md`
- Repository file tree

## Procedure

### Step 1: Scan INBOX
- [ ] List all items in `09_INBOX/`
- [ ] Check age (>7 days = overdue for triage)
- [ ] Classify each item by target folder

### Step 2: Propose Placement
- [ ] Match artifact type to FOLDER_MAP
- [ ] Document proposed destination path
- [ ] Flag items requiring ML1 decision (doctrine candidates)

### Step 3: Index Update
- [ ] Update any index files affected
- [ ] Cross-reference related artifacts
- [ ] Note dependencies

### Step 4: Staleness Check
- [ ] Identify artifacts not updated in >90 days
- [ ] Check for orphaned references
- [ ] Propose archive or refresh actions

### Step 5: Promotion Proposal
- [ ] For items ready for promotion, document:
  - Current path
  - Proposed path
  - Rationale
- [ ] Submit to System Governance for validation

## Outputs
- INBOX triage report
- Promotion proposals
- Staleness report
- Updated indexes

## Authority Constraints
- Cannot promote to doctrine without ML1
- Cannot delete artifacts
- Cannot modify binding content

## Escalation
- Doctrine promotion → ML1
- Placement disputes → System Governance Agent
