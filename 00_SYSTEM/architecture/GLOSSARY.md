---
id: 00_system__glossary_md
title: System Glossary
owner: ML1
status: draft
created_date: 2026-01-25
last_updated: 2026-03-23
tags: []
---

# System Glossary
Canonical system-level definitions for terms used across the Second Brain.

Scope boundary:
- This document defines system and architecture terms.
- LL portfolio/domain terms are defined in `04_INITIATIVES/LL_PORTFOLIO/LL_GLOSSARY.md`.

## Doctrine
An artifact qualifies as doctrine when all criteria are met:
- States normative guidance (for example: must/should/rules/standards/policies).
- Applies beyond a single case.
- Is explicitly approved by ML1.
- Resides in `01_DOCTRINE`.
- Has `status: approved` or `status: active`.
- Is classified as one of the doctrine classes listed below.

## Doctrine Classes
The only doctrine classes are:
- Invariant
- Principle
- Policy
- Capability Profile
- Protocol

## Invariant
Constitution-level structural truth that must remain true for system validity. If violated, the system design is invalid until corrected or formally amended.

## Principle
Decision heuristic used to guide interpretation where rules are incomplete or ambiguous. Principles guide judgment; they are not direct enforcement routines.

## Policy
Binding governance constraint that defines required or prohibited behavior. Policies are enforceable and are implemented operationally through protocols.

## Capability Profile
Scoped permission boundary describing what a component is allowed and not allowed to do.

## Protocol
Operational interaction contract that implements policy in executable process form (gates, checks, choreography, and escalation paths).

## Layer
An architectural responsibility boundary in the system model. A layer defines what kind of function is performed, not who performs it. A layer may contain one or more components.

## Component
A concrete actor or subsystem that operates within a layer and executes specific responsibilities.

## Agent
A component that may orchestrate governed workflows, apply doctrine gates, and invoke workers and tools within assigned capability boundaries.

## Orchestrating Agent
The agent assigned primary responsibility for a governed run. The orchestrating agent coordinates workers, tools, and any participating agents, and is the only runtime component permitted to issue the run's final output.

## Final Output
An artifact issued by the run's orchestrating agent as the terminal output of a governed run. Final-output issuance is distinct from ML1 approval, publication, distribution, or external delivery.

## Worker
A scoped task executor invoked by an orchestrating agent for bounded work (for example: classification, extraction, drafting, QA checks, formatting, and structured analysis). A worker does not orchestrate runs and may not issue final outputs.

## Subagent
Synonym for Worker. The canonical doctrine term is Worker.

## Tool
A callable capability exposed by an integration adapter for governed runtime use.

## Integration Adapter (MCP)
A component that connects the runtime to external systems and exposes approved tools for external I/O.

## Run
An execution container that records governed runtime activity, including orchestration, worker invocations, tool calls, artifacts, and outputs.

## Artifact
A recorded intermediate or final output produced during execution.

## Contact
An identity record that may exist independently of matter creation. A contact is not automatically a client.

## Client
A matter-bound role designation for a contact serving as client-of-record on at least one matter. Without a matter, there is no client designation.

## Supporting Artifacts (Non-Doctrine)
These may exist under `01_DOCTRINE` for governance support but are not doctrine classes:
- Procedural
- Rules
- Tests

## ML1
Human authority component (Matthew Levine) in the authority layer. Sole source of final judgment, approval, and exceptions. ML1 governs the Second Brain but is not a component within it.

## ML2
Canonical, versioned system-of-record component in the record layer for governed knowledge artifacts. ML2 preserves durable memory and operating rules. It is not the storage container.

## System
Operational reasoning and runtime component in the execution layer that reads and executes ML2, applies doctrine, enforces controls, detects drift, and produces diagnostics. It does not originate doctrine and does not include ML1.

## Second Brain
Umbrella architecture composed of ML2 and the System. It is governed by ML1 but does not include ML1 as a component.

## Repository
Current transport and storage container for ML2 artifacts, system implementation components, tooling, and configuration. The repository is not identical to ML2, the System, or the Second Brain as a conceptual model.

## LL
Human distribution component (Levine Law personnel) in the distribution layer. Delivers market-facing services from final outputs and provides operational signals.

## Canonical
Authoritative artifact state in ML2 that governs all downstream copies.

## Published
Distributed operational copy in external tools/suites. Published artifacts do not supersede canonical ML2 artifacts.

## Services / Legal Services
An open-ended service category used for market-facing delivery.
It includes, but is not limited to, Solutions and Strategies.
Additional service forms may exist where permitted by approved doctrine and capability profiles.

## Conversion (Marketing Stage)
The terminal stage of the marketing lifecycle. It is the marketing-language label used when objective conversion evidence is satisfied and recorded.

## Onboarding (Fulfillment Stage)
The first stage of the fulfillment lifecycle. It is the fulfillment-language label for the post-conversion handoff event and subsequent gate-controlled setup.
