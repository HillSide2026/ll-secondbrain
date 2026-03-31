# Purpose
Draft a single action proposal for ML1 review using the approved execution schema.

# Canonical Inputs (MUST USE)
- 02_PLAYBOOKS/EXECUTION/ACTION_PROPOSAL_SCHEMA.md (current)
- 01_DOCTRINE/03_POLICIES/POL-001_Output_Labeling_Requirement.md (POL-001)
- 01_DOCTRINE/03_POLICIES/POL-002_Provenance_Requirement.md (POL-002)
- 01_DOCTRINE/03_POLICIES/POL-003_Novel_Policy_Prohibition.md (POL-003)
- 01_DOCTRINE/03_POLICIES/POL-004_External_Output_Approval_Requirement.md (POL-004)
- 01_DOCTRINE/03_POLICIES/POL-005_Low_Confidence_Escalation.md (POL-005)
- 01_DOCTRINE/03_POLICIES/POL-010_Maintainability_Versioning_Requirement.md (POL-010)
- 01_DOCTRINE/03_POLICIES/POL-011_Discoverability_Requirement.md (POL-011)
- 01_DOCTRINE/03_POLICIES/DOCTRINE-CORE-0005-no-fictional-execution-constructs.md (DOCTRINE-2026-005)

# Run ID Convention
Format: `RUN-YYYY-MM-DD-<SLUG>` where SLUG is a short kebab-case descriptor.
See `.claude/run_id_convention.md` for full specification.

# Steps
1. Create or confirm the run folder `06_RUNS/<run_id>/` and record the run id.
2. Collect the source item and any existing context; if matter-related, pull `05_MATTERS/<matter_id>/context.md` (or note missing context).
3. Draft the proposal using `02_PLAYBOOKS/EXECUTION/ACTION_PROPOSAL_SCHEMA.md`, filling all required fields.
4. Cite referenced canon artifacts inline (include the exact repo path) where they govern content.
5. If confidence is low or policy novelty is detected, stop and escalate per POL-005 and POL-003.
6. Ensure output labeling and provenance are present per POL-001 and POL-002.
7. Save the draft to the run folder using the naming convention below.

# Error Handling
- **Schema file missing** (`02_PLAYBOOKS/EXECUTION/ACTION_PROPOSAL_SCHEMA.md` not found): halt. Surface the missing path. Do not draft a proposal without the schema.
- **Matter context missing**: note the gap in the proposal frontmatter (`context_source: missing`). Do not fabricate context.
- **Policy novelty detected** (POL-003): halt immediately. Surface the novel policy claim and the specific statement triggering it. Do not continue without ML1 direction.
- **Low confidence on any material claim** (POL-005): halt. Surface the claim and ask ML1 before proceeding.
- **Run folder cannot be created**: halt and surface the path error.

# Output Requirements
- Output file: `06_RUNS/<run_id>/proposal__<short_slug>.md`
- Include `status: draft` in frontmatter where applicable.
- Include an explicit output label and provenance footer.
- Do not mark as approved without an ML1 approval artifact.

# Provenance Footer (MANDATORY)
Derived from: <list of canon paths>
Doctrine refs: <list of policy/protocol ids>
Run id: <run folder name>
Date: <YYYY-MM-DD>
Status: DRAFT (unless ML1-approved artifact exists)
