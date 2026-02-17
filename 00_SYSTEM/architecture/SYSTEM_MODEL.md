---
id: 00_system__architecture__system_model_md
title: System Model
owner: ML1
status: draft
version: 1.0
created_date: 2026-02-14
last_updated: 2026-02-14
tags: [architecture, system, boundary, ontology]
---

# System Model

## Purpose

This document defines the architectural model of the LL Second Brain environment.

It clarifies the distinction between:

- ML1 (human authority)
- ML2 (governed ontology)
- The System (execution environment)
- The Repository (transport container)

This document is architectural and interpretive.  
Binding constraints on ML2 are defined in:

`01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md`

---

# Core Definitions

## ML1 - Human Authority

ML1 (Matthew Levine) is the sole source of:

- Judgment
- Approval
- Strategic direction
- Exception handling

ML1 is accountable for all system outputs and doctrinal changes.

ML1 is not automated.

---

## ML2 - Governed Ontology

ML2 is the system-of-record for durable knowledge and its operating rules.

ML2 consists exclusively of governed artifacts defined by the ML2 Ontology Boundary invariant.

### ML2 Includes

- Constitution
- Principles
- Policies
- Protocols
- Playbooks
- Templates
- Runs (evidence)
- Integration specifications (non-secret)

ML2 is conceptual.  
It is not defined by its storage medium.

If the execution engine changes, ML2 artifacts remain authoritative.

---

## The System - Execution of ML2

The System is the operational environment that executes, enforces, and maintains ML2.

It consists of:

- ML1 (authority)
- ML2 (ontology)
- Agents (system-management and domain agents)
- Orchestration logic
- Retrieval mechanisms
- Integration adapters
- Runtime infrastructure
- Validation and QA processes

The System enforces ML2.  
It is not itself ML2.

If the execution engine changes, the System may change.  
ML2 must remain intact.

---

## The Repository - Transport Container

The repository is the current storage and execution container for:

- ML2 artifacts
- System implementation components
- Tooling and configuration

The repository is not ML2.

The repository may contain:

- Repo infrastructure (.gitignore, LICENSE, etc.)
- Execution telemetry (logs/)
- Scripts and tooling
- Local configuration
- CI configuration

These are container artifacts and are not governed ontology.

---

# Boundary Principles

## Ontology vs Mechanism

ML2 defines truth and rules.

The System defines how those rules are executed.

Mechanisms may change without altering ontology.

---

## Durable vs Ephemeral

If an artifact would survive migration to a different execution engine as authoritative knowledge, it belongs to ML2.

If it would not survive that migration, it belongs to the System or repository layer.

---

# Integration Model

Integrations have two components:

1. Integration Specifications (ML2)
   - Governed, non-secret
   - Define authority, classification, ingestion rules
   - Located under `00_SYSTEM/integrations/`

2. Integration Mechanisms (System)
   - Adapters, retrieval logic, credentials
   - Runtime-bound
   - May change without altering ontology

Secrets and credentials are never ML2.

---

# Enforcement Implications

- System Admin Agents enforce ML2 boundaries only where defined by invariant.
- Drift detection applies to ML2 layers, not container artifacts.
- Metadata enforcement applies only to governed ontology artifacts.
- Reference validation applies only within ML2 cross-references unless explicitly configured.

---

# Layer Model (Stable Form)

ML1 -> Authority  
ML2 -> Ontology  
System -> Execution of ontology  
Repository -> Transport container

This layering is stable across tooling changes.

---

# Change Control

Changes to this document require explicit ML1 review.

Changes to ML2 boundaries must reference:

`INV-ML2-BOUNDARY.md`
