# Reference vs Research — Movement Rules

## Core Distinction

| Aspect | 07_REFERENCE | 08_RESEARCH |
|--------|--------------|-------------|
| Purpose | Consulted | Worked on |
| Nature | Stable, non-speculative | Active, iterative |
| Churn | Low | High |
| Authority | Cited as truth | Not authoritative |
| Metaphor | Library | Lab |

---

## The Tests

### Test 1: Breakage Test
> "If this were wrong tomorrow, would anything break?"

| Answer | Implication |
|--------|-------------|
| Yes | Does NOT belong in Reference |
| No | Might belong in Reference |
| Not sure | Goes in Research |

### Test 2: Consultation Test
> "Is this something we consult or something we're figuring out?"

| Answer | Implication |
|--------|-------------|
| Consult | Reference |
| Figuring out | Research |

---

## Movement: Reference → Research

**Common and encouraged.**

| What | Example |
|------|---------|
| Copy excerpts | OAuth spec into integration notes |
| Cite while analyzing | Vendor doc in tradeoff analysis |

This is **consumption**.

---

## Movement: Research → Reference

**Rare, explicit, and gated.**

### Requirements

| Requirement | Meaning |
|-------------|---------|
| Stabilization | No longer speculative |
| Source clarity | Attribution complete |
| ML1 approval | Implicit or explicit |

### Method

Usually a **rewrite**, not a move.

This is **promotion**, not cleanup.

### Example

A research memo becomes a canonical definition after:
1. Speculation removed
2. Sources attributed
3. ML1 confirms stability

---

## Movement: Research → Trash

**Also a valid outcome.**

Dead research is not failure; it's evidence of exploration.

Options:
- Move to `08_RESEARCH/EXPERIMENTS/abandoned/`
- Delete entirely

---

## Movement: Research → Doctrine

Via formal promotion path.

Research → Synthesis → Recommendation → Doctrine (via 01_DOCTRINE process)

Research never directly becomes doctrine without explicit promotion.

---

## Agent Behavior by Directory

### SYS-008 (Knowledge Curation)

| Directory | Allowed | Not Allowed |
|-----------|---------|-------------|
| Reference | Index, flag staleness | Rewrite, summarize as truth |
| Research | Organize, suggest synthesis, flag for promotion | — |

### SYS-009 (QA)

| Directory | Checks |
|-----------|--------|
| Reference | Attribution, formatting, completeness |
| Research | Clarity, internal consistency only |

**Never "fails" research for being speculative.**

### SYS-005 (Governance)

| Directory | Standard |
|-----------|----------|
| Reference | Stricter |
| Research | Mostly hands-off |

---

## Key Principle

> **Reference supports research. Research never lives in reference.**
