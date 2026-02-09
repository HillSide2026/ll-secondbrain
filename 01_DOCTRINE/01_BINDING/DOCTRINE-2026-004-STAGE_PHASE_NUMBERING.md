---
id: 01_doctrine__01_binding__doctrine-2026-004-stage_phase_numbering_md
title: Canonical Stage & Phase Numbering Doctrine
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Canonical Stage & Phase Numbering Doctrine

**Document ID:** DOCTRINE-2026-004
**Status:** BINDING
**Effective:** 2026-01-27
**Authority:** ML1

---

## 1. Stage numbering (top level)

Stages are integers only:
- `STAGE1`
- `STAGE2`
- `STAGE3`

A stage number is globally unique and never reused.

Stage numbers are assigned once in the roadmap and never inferred later.

**Rule:**
No artifact may invent a new stage number. Stages must already exist in the roadmap.

---

## 2. Phase numbering (within a stage)

Phases are decimal expansions of the stage.

**Format:**
```
<STAGE>.<PHASE>
```

**Examples:**
- 1.1, 1.2, 1.3, 1.4
- 2.1, 2.2, 2.3

**Rules:**
- Phase numbers start at `.1`
- Phase numbers increment sequentially
- Phase numbers are never skipped
- Phases are scoped to their stage
- Phase numbers reset when the stage changes

---

## 3. Artifact naming (hard requirement)

Any artifact that references a stage or phase MUST:
- Use both stage and phase where applicable
- Match one of these formats exactly:

**Stage-only artifact:**
```
STAGE2_<NAME>.md
```

**Stage + phase artifact:**
```
STAGE2.1_<NAME>.md
```

**Invalid formats (rejected):**
- `STAGE_2.1`
- `STAGE21`
- `STAGE3_PHASE1`
- `STAGE2-1`

---

## 4. Directory structure (enforced)

Directories must reflect stage first, phase second:

```
STAGE1/
  STAGE1.1/
  STAGE1.2/
  STAGE1.3/
  STAGE1.4/

STAGE2/
  STAGE2.1/
  STAGE2.2/
  STAGE2.3/
```

**Rule:**
No directory may contain artifacts from multiple stages.

---

## 5. Agent responsibilities (to prevent drift)

### SYS-005 (System Governance)

Must:
- Reject artifacts with malformed or inconsistent stage/phase numbers
- Reject artifacts whose phase does not belong to the referenced stage
- Flag skipped or duplicate phase numbers

### SYS-009 (Runbook & QA)

Must:
- Validate naming, directory placement, and numbering consistency
- Fail QA if:
  - stage/phase format is incorrect
  - phase numbering is out of sequence
  - artifact references a non-existent stage or phase

---

## 6. Change control (critical)

Adding a new stage or new phase requires:
- Roadmap update
- Explicit ML1 approval

Agents may reference stages/phases.
Agents may **not** create new ones.

---

## Minimal enforcement checklist

- [ ] Stage number exists in roadmap
- [ ] Phase number belongs to stage
- [ ] Naming format matches `STAGE<stage>[.<phase>]_`
- [ ] Directory path matches stage/phase
- [ ] No duplicate or skipped phases
