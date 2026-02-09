---
id: 00_system__agents__agent_typology_md
title: Agent Typology
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Agent Typology

Classification of agents operating within the Second Brain system.

---

## Purpose

Define the distinct categories of agents, their roles, authority boundaries, and relationships to system resources. This typology governs how agents are instantiated, configured, and constrained.

This document reflects the current state of the system and explicitly identifies planned but not yet implemented agent types.

---

## Agents Index (Derived from AGENTS.md)

### System Agents
- 00_SYSTEM/AGENTS/SYS-005_SYSTEM_GOVERNANCE.md
- 00_SYSTEM/AGENTS/SYS-006_PORTFOLIO_PLANNING.md
- 00_SYSTEM/AGENTS/SYS-007_INTEGRATION_STEWARD.md
- 00_SYSTEM/AGENTS/SYS-008_KNOWLEDGE_CURATION.md
- 00_SYSTEM/AGENTS/SYS-009_RUNBOOK_QA.md

### Proto-Agents (Draft)
- 00_SYSTEM/AGENTS/PROTO-REPO-LINTER.md
- 00_SYSTEM/AGENTS/PROTO-FOLDER-MAP-DRIFT.md

---

## Type 1: System Agents

### Definition

System Agents perform **infrastructure, operational, and coordination functions** across the Second Brain system. They do not exercise domain-specific professional judgment.

### Characteristics

| Attribute | Value |
|-----------|-------|
| Domain expertise | None (domain-agnostic) |
| Judgment authority | Operational only |
| Output type | System artifacts, logs, indices, reports |
| Solution access | None |
| Escalation target | System administrator / ML1 |

### Constraints

- May not interpret legal, business, or domain-specific facts
- Outputs are operational, not advisory

### Governing Doctrine

- [DOCTRINE-AGENTS-0001](../../01_DOCTRINE/01_BINDING/DOCTRINE-AGENTS-0001-SECOND-BRAIN_AGENT_AUTHORITY.md)
- [AGENT-CAPABILITY-PROFILE-0001](../../01_DOCTRINE/03_CAPABILITY_PROFILES/AGENT-CAPABILITY-PROFILE-0001-DRAFT_WRITE_ACCESS.md)

---

## Type 2: Practice Area Master Agents (Current State)

### Definition

Practice Area Master Agents are **practice-area-scoped coordinating agents** responsible for:

- Intake interpretation within a practice area
- Routing matters to appropriate Solutions
- Ensuring outputs conform to Solution structure and constraints
- Escalating to ML1 when Solution boundaries are exceeded

They are **not** delivery systems.

They currently combine:
- Some system-level coordination
- Some domain awareness
- Some provisional delivery logic

**This role is explicitly transitional.**

### Characteristics (Current)

| Attribute | Value |
|-----------|-------|
| Domain expertise | Practice-area contextual understanding |
| Judgment authority | Solution selection + bounded expert reasoning |
| Output type | Matter framing, solution selection, escalation questions |
| Solution access | Full access to practice area Solutions |
| Escalation target | ML1 / human authority |

### Constraints

- May not act outside approved Solutions
- May not override Solution scope without escalation
- Must use mandatory output schema
- May not assume firm-wide delivery authority

### Examples

| Agent | Practice Area |
|-------|---------------|
| CORPORATE_LAW_MASTER_AGENT | Corporate |
| CONTRACTS_MASTER_AGENT | Contracts |
| PAYMENTSERVICES_MASTER_AGENT | Payments |
| TRANSACTIONS_MASTER_AGENT | Transactions |

### Governing Specification

- [PRACTICE_AREA_MASTER_AGENT_SPEC.md](PRACTICE_AREA_MASTER_AGENT_SPEC.md)

---

## Type 3: Solution-Area Specialist Agents (To Be Implemented)

### Definition

Solution-Area Specialist Agents are **narrow, bounded expert agents** instantiated to operate inside a single Solution packet.

They provide **solution-local advisory signal only**.

They do not manage engagements, escalation, or delivery relationships.

### Characteristics

| Attribute | Value |
|-----------|-------|
| Domain expertise | Deep, solution-specific |
| Judgment authority | None (advisory only) |
| Output type | Flags, observations, artifact references |
| Solution access | Single Solution only |
| Escalation authority | None |
| Escalation target | Practice Area Master Agent |

### Constraints

- May not select or change Solutions
- May not escalate directly to ML1
- May not reinterpret system doctrine
- All outputs are advisory and non-binding

---

## Relationship Between Agent Types (Target State)

```
┌─────────────────────────────────────────────────────────────┐
│                     ML1 / Human Authority                    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ escalates to
┌─────────────────────────────────────────────────────────────┐
│              Type 2: Practice Area Master Agents             │
│                                                              │
│  • Solution routing                                          │
│  • Practice-area framing                                     │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ request analysis and production from
┌─────────────────────────────────────────────────────────────┐
│            Type 3: Solution-Area Specialist Agents            │
│                                                              │
│  • Advisory only                                             │
│  • Single Solution scope                                     │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ supported by
┌─────────────────────────────────────────────────────────────┐
│                  Type 1: System Agents                        │
│                                                              │
│  • Operational functions                                     │
│  • No domain judgment                                        │
│  • Infrastructure, routing, reporting                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Invariant (System Rule)

> Practice areas coordinate work via one or more solution. Solutions confirm scope and generate signal. Human retains authority.

---

## Key Distinctions

| Dimension | Type 1 (System) | Type 2 (Practice Area Master) | Type 3 (Solution Specialist) |
|-----------|-----------------|-------------------------------|------------------------------|
| Expertise | None | Practice-area contextual | Deep, solution-specific |
| Judgment | Operational | Solution selection + bounded reasoning | None (advisory only) |
| Solutions | Not used | Full practice area access | Single Solution only |
| Output schema | Flexible | Mandatory | Flags + observations |
| Confidence scoring | Optional | Required | N/A |
| Assumption budget | N/A | Max 3 | N/A |
| Escalation target | ML1 / system admin | ML1 | Practice Area Master Agent |
| Escalation authority | Operational issues | Domain judgment + constraints | None |

---

## Implication (Important)

Until Type 4 (Delivery System) is implemented:

- Practice Area Master Agents are operating in a **hybrid role**
- Delivery logic is necessarily **incomplete**
- Escalation risk is mitigated only by **human review**

---

## Instantiation

### Type 1 Agents
Instantiated by system configuration. No practice-area-specific parameters required.

### Type 2 Agents
Instantiated per practice area by:
1. Applying the generic [PRACTICE_AREA_MASTER_AGENT_SPEC.md](PRACTICE_AREA_MASTER_AGENT_SPEC.md)
2. Binding to the practice area's Solution library
3. Configuring practice-area-specific:
   - Decision registry (named decision points)
   - Known-safe defaults
   - Intake question packs
   - Collision matrix (if multi-solution)

### Type 3 Agents
To be implemented. Instantiation pattern TBD — expected to require:
1. Binding to a single Solution packet
2. Defining advisory output format (flags, observations, artifact references)
3. Registering under the parent Practice Area Master Agent

---

## Index

### Type 1 Agents

| Agent | Location | Status |
|-------|----------|--------|
| todo-rollup | scripts/todo_rollup.py | Active |
| system-governance | TBD | Planned |
| project-manager | TBD | Planned |

### Type 2 Agents

| Agent | Practice Area | Location | Status |
|-------|---------------|----------|--------|
| CORPORATE_LAW_MASTER_AGENT | Corporate (Ontario) | 02_PLAYBOOKS/CORPORATE/AGENTS/ | Active |
| CONTRACTS_MASTER_AGENT | Contracts | 02_PLAYBOOKS/CONTRACTS/AGENTS/ | Active |
| PAYMENTSERVICES_MASTER_AGENT | Payments | 02_PLAYBOOKS/FINANCIAL_SERVICES/PAYMENTS/AGENTS/ | Active |

### Type 3 Agents

No Type 3 agents have been instantiated. This type is planned.

---

## Adding New Agents

### Type 1
1. Define operational function
2. Specify inputs/outputs
3. Grant capability profile if write access needed
4. No Solution binding required

### Type 2
1. Apply PRACTICE_AREA_MASTER_AGENT_SPEC.md
2. Define practice-area Solutions
3. Configure decision registry, defaults, intake packs
4. Grant capability profile
5. Register in typology index

### Type 3
1. Bind to single Solution packet
2. Define advisory output format
3. Register under parent Practice Area Master Agent
4. No escalation authority granted
