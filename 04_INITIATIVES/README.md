---
id: 04_initiatives__readme_md
title: 04_INITIATIVES — Strategic Initiatives & Projects
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# 04_INITIATIVES — Strategic Initiatives & Projects

## Purpose

This directory contains all strategic initiatives and projects, organized by portfolio based on primary beneficiary.

---

## Portfolio Structure

```
04_INITIATIVES/
├── HillSide_PORTFOLIO/     # HillSide portfolio initiatives
├── SYSTEM_PORTFOLIO/       # ML2 system development
│   ├── 00_DRAFT_ROADMAPS/
│   ├── 01_ACTIVE_ROADMAPS/
│   └── BACKLOG.md
└── LL_PORTFOLIO/           # Levine Law operational support
    ├── 01_ACCOUNTING/
    ├── 02_PRACTICE_AREAS/
    ├── 03_FIRM_OPERATIONS/
    ├── 04_RISK/
    ├── 05_MATTER_DOCKETING/
    ├── 06_FINANCIAL_PORTFOLIO/
    ├── 07_STRATEGIC_PROJECTS/
    ├── 08_MARKETING/
    └── 09_SERVICE_MANAGEMENT/
```

---

## SYSTEM_PORTFOLIO

**Purpose:** Initiatives that improve the Second Brain system itself (ML2).

**Beneficiary:** The system's ability to support ML1 and LL.

**Examples:**
- Agent runtime setup
- Integration activation
- Cognitive scaffolding development
- System governance improvements

**Governance:** Follows stage-based roadmap model with explicit authorization gates.

---

## LL_PORTFOLIO

**Purpose:** Initiatives whose primary purpose is to improve how Levine Law (LL) operates.

**Beneficiary:** Levine Law as an operating firm.

**Core Principle:**
> ML1 defines intent and priority. ML2 preserves scope, constraints, and state. LL consumes ONLY ML1-approved outputs, never raw reasoning.

**Governance:** Follows controlled registry model with explicit ML2 function authorization.

**Work Type Taxonomy (Canonical):**
- Strategic projects
- Management projects
- Operational projects
- Client matters (aka client projects)

Strategic, management, and operational projects follow the project stage-gate artifact lifecycle.
Client matters/client projects follow matter doctrine and matter-stage artifacts.

See: `LL_PORTFOLIO/README.md` for detailed governance rules.

---

## HillSide_PORTFOLIO

**Purpose:** Initiatives whose primary beneficiary is HillSide and related entities.

**Beneficiary:** HillSide portfolio operations and governance.

---

## Boundary Rules

### SYSTEM_PORTFOLIO → LL_PORTFOLIO

- System capabilities may enable LL capabilities
- System outputs may be consumed by LL workflows
- System doctrine applies to LL operations

### LL_PORTFOLIO → SYSTEM_PORTFOLIO

- LL requirements may drive system priorities
- LL feedback may trigger system improvements
- LL operations never modify system governance

---

## References

- Folder Map: `00_SYSTEM/architecture/FOLDER_MAP.md`
- System Portfolio: `SYSTEM_PORTFOLIO/README.md`
- LL Portfolio: `LL_PORTFOLIO/README.md`
