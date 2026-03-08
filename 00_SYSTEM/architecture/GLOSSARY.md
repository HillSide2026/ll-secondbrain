---
id: 00_system__glossary_md
title: Glossary
owner: ML1
status: draft
created_date: 2026-01-25
last_updated: 2026-03-08
tags: []
---

# Glossary
Canonical definitions for terms used across the Second Brain.

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

## Supporting Artifacts (Non-Doctrine)
These may exist under `01_DOCTRINE` for governance support but are not doctrine classes:
- Procedural
- Rules
- Tests

## ML1
Human authority component (Matthew Levine) in the authority layer. Sole source of final judgment, approval, and exceptions.

## ML2
Canonical, versioned system-of-record component in the record layer for governed knowledge artifacts.

## System
Operational reasoning and runtime component in the execution layer that applies doctrine, enforces controls, detects drift, and produces diagnostics. It does not originate doctrine.

## LL
Human distribution component (Levine Law personnel) in the distribution layer. Delivers authorized services from approved outputs and provides operational signals.

## Canonical
Authoritative artifact state in ML2 that governs all downstream copies.

## Published
Distributed operational copy in external tools/suites. Published artifacts do not supersede canonical ML2 artifacts.

## Services / Legal Services
An open-ended service category used for market-facing delivery.
It includes, but is not limited to, Solutions and Strategies.
Additional service forms may exist where permitted by approved doctrine and capability profiles.
