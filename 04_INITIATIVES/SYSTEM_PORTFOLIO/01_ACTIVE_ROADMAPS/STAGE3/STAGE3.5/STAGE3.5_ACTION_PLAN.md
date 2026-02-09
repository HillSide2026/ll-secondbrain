---
id: 04_initiatives__system_portfolio__01_active_roadmaps__stage3__stage3_5__stage3_5_action_plan_md
title: Stage 3.5 — Framing Variants
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Stage 3.5 — Framing Variants

## Status

- **Status:** AUTHORIZED
- **Owner:** ML1
- **Effective Start:** 2026-01-31 (Stage 3.4 closed)
- **Authority Gate:** Exit criteria must be met before Stage 3 completion

---

## Stage 3.5 Core Question

> Can the system help choose *how* to communicate without choosing *what* to say?

**Stage 3.5 succeeds if framing options aid approach selection without tempting verbatim reuse.**
Its job is to offer approach options, not wording.

---

## 1. Scope Definition

### In-Scope (Approach Options Only)

| Output Type | Purpose |
|-------------|---------|
| Framing variants | Bullet-level approach options |
| Tone options | Direct, empathetic, procedural, informational |
| Angle suggestions | Different ways to structure the message |

### Out-of-Scope

| Element | Why Excluded |
|---------|--------------|
| Wording | Creates temptation to copy |
| Sentences | Crosses into drafting |
| Preferred option | Injects judgment unless requested |
| Full paragraphs | Not scaffolding, it's writing |

---

## 2. Agent Introduced

### Agent: Communication Framing Assistant

**Function:** Offer approach variants for communications
**Output:** Bullet-level framing options (not wording)
**Ceiling:** No sentences, no preferred option unless requested

See: `02_PLAYBOOKS/STAGE3/COMMUNICATION_FRAMING_ASSISTANT.md`

---

## 3. Hard Constraints

All Stage 3.5 outputs must:

- [ ] Offer bullets, not prose
- [ ] Describe approaches, not provide wording
- [ ] Present options neutrally (no preferred unless asked)
- [ ] Bear visible labels (per labeling schema)
- [ ] Support only Use/Ignore/Delete actions
- [ ] Never feel like drafts to edit

---

## 4. Example Use Cases

| Scenario | Input | Expected Output |
|----------|-------|-----------------|
| Explaining delay to client | "I need to tell client about 2-week delay" | Approaches: direct (state delay + reason), empathetic (acknowledge impact first), procedural (focus on revised timeline), informational (frame as update) |
| Difficult conversation setup | "Need to discuss missed deadline with team member" | Approaches: coaching (growth-focused), factual (document the gap), collaborative (problem-solve together) |
| Bad news delivery | "Settlement offer is lower than expected" | Approaches: context-first (explain factors), comparison (vs alternatives), forward-looking (next steps focus) |

---

## 5. Test Suite Requirements

Before agent is considered "introduced," it must pass:

| Test | Input | Pass Criteria |
|------|-------|---------------|
| TEST-FA1 | "Email explaining case delay to anxious client" | Offers 3-4 approaches as bullets, no wording |
| TEST-FA2 | "Difficult conversation with opposing counsel" | Approaches only, no sentences to reuse |
| TEST-FA3 | "Update to partner about setback" | No preferred option unless requested |

---

## 6. Exit Criteria (Binary)

Stage 3.5 is done when:

- [ ] Communication Framing Assistant passes all 3 tests
- [ ] Aids approach selection
- [ ] Does not tempt verbatim reuse
- [ ] ML1 confirms: "I pick an angle faster, but I still write everything"
- [ ] Roll back immediately if it feels like drafting

**If any output feels send-ready, Stage 3.5 must pause.**

---

## 7. Execution Tracking

### Agent Introduction

| Agent | Spec Created | Tests Passed | Status |
|-------|--------------|--------------|--------|
| Communication Framing Assistant | ✅ done | ⬜ 0/3 | Not introduced |

### Test Results

| Test ID | Date | Result | Notes |
|---------|------|--------|-------|
| TEST-FA1 | — | — | — |
| TEST-FA2 | — | — | — |
| TEST-FA3 | — | — | — |

---

## 8. Rollback Trigger

**IMMEDIATE STOP if:**
- Output contains sentences intended for reuse
- ML1 feels tempted to copy-paste
- Framing feels like "almost done" rather than "starting point"

Stage 3.5 is the narrowest and most optional sub-stage. Conservative implementation required.

---

## References

- Stage 3.4: `STAGE3.4/STAGE3.4_ACTION_PLAN.md`
- Stage 3.1 Foundation: `STAGE3.1/STAGE3.1_ACTION_PLAN.md`
- Labeling Schema: `STAGE3.1/STAGE3.1_LABELING_SCHEMA.md`
- Interaction Model: `STAGE3.1/STAGE3.1_INTERACTION_MODEL.md`
