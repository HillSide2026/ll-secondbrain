# Runbook: Portfolio Planning Agent

## Purpose
Manage roadmap sequencing, backlog prioritization, and stage transitions.

## Trigger Conditions
- New backlog item proposed
- Stage DoD review requested
- Roadmap update needed

## Inputs
- `04_INITIATIVES/SYSTEM_PORTFOLIO/BACKLOG.md`
- Active roadmap (e.g., `ROADMAP-SYSTEM-2026W05.md`)
- Stage artifacts and DoD checklists

## Procedure

### Step 1: Backlog Triage
- [ ] Review new items in INBOX or proposed additions
- [ ] Classify by stage relevance
- [ ] Assign preliminary priority

### Step 2: Dependency Analysis
- [ ] Map dependencies between backlog items
- [ ] Identify blockers
- [ ] Flag items waiting on ML1 decision

### Step 3: Stage DoD Review
- [ ] Compare stage artifacts against DoD checklist
- [ ] Document evidence for each DoD item
- [ ] Determine if stage is ready for closure

### Step 4: Prepare Closure Package
- [ ] List all stage deliverables with paths
- [ ] Document DoD compliance
- [ ] Prepare closure recommendation for ML1

### Step 5: Update Backlog
- [ ] Mark completed items
- [ ] Add new items from stage work
- [ ] Update priorities based on ML1 input

## Outputs
- Updated `BACKLOG.md`
- Stage closure recommendation
- Sequencing proposals

## Authority Constraints
- Cannot promote roadmaps (ML1 only)
- Cannot authorize execution
- Cannot skip DoD requirements

## Escalation
- Roadmap promotion → ML1
- DoD disputes → System Governance Agent
