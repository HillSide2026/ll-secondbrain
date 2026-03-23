---
id: 01_doctrine__01_invariants__doctrine-projects-0001-project-structural-boundaries_md
title: Project Structural Boundaries
owner: ML1
status: draft
version: '1.0'
created_date: 2026-03-15
last_updated: 2026-03-15
tags: [doctrine, invariants, projects, structure]
---

# Project Structural Boundaries

## Purpose

Define the structural ontology for projects and adjacent work containers so the
repository does not blur projects with matters, workflows, modules, solutions,
programs, or portfolios.

This invariant defines what these containers are, how they relate, and what
they are not.

Artifact requirements, stage-gate packets, and lifecycle controls remain at the
policy layer.

## Structural Rule

The repository recognizes the following distinct structural units:

- portfolio
- program
- project
- matter
- solution
- module
- workflow

These are not interchangeable labels.

No artifact, folder, register, or policy may silently collapse one unit into
another.

## Canonical Definitions

### 1. Portfolio

A portfolio is the highest governed grouping of related work organized by
primary beneficiary, operating domain, or ownership branch.

The current repository has three canonical portfolios under `04_INITIATIVES`:

- `SYSTEM_PORTFOLIO`
- `LL_PORTFOLIO`
- `HillSide_PORTFOLIO`

A portfolio:

- groups one or more programs and related governance structures
- sets broad scope and boundary for included work
- is not itself a project, workflow, or matter

### 2. Program

A program is a governed grouping of related projects or ongoing governance lines
within a portfolio that share a common operating aim, domain, or coordination
need.

A program:

- contains one or more projects
- coordinates related projects
- may hold a shared register, policy overlay, or decision frame
- is not itself a single project deliverable
- is not a matter, solution, or workflow

### 3. Project

A project is a bounded change initiative governed by the project delivery-stage
system.

A project:

- has a defined purpose, scope boundary, and owner
- uses one canonical project type
- advances, when authorized, through project delivery stages
- may consume solutions, modules, workflows, and templates
- may affect a portfolio or program

A project is not:

- a portfolio
- a program
- a solution architecture unit
- a workflow definition
- a doctrine artifact

### 4. Project Types

The canonical project types are:

- `Strategic`
- `Management`
- `Operational`
- `Decision`

#### Strategic Project

A strategic project is a change initiative that defines or materially changes
long-horizon direction, capability, ownership posture, or structural operating
position.

#### Management Project

A management project is a change initiative focused on governance, control,
coordination, monitoring, or optimization of existing systems or operating
domains.

#### Operational Project

An operational project is a bounded execution-focused initiative that improves,
implements, or stabilizes how defined work is carried out.

#### Decision Project

A decision project is a bounded option-framing initiative used to structure,
compare, and decide whether a proposed build, partnership, divestiture, or new
venture path should advance, be reclassified, or be closed.

A decision project:

- is evaluation-first, not execution-first
- exists to produce a clear ML1 go / hold / no-go or reclassification decision
- may conclude by closing or by being reclassified into another project type

Each project must use one canonical project type for governance purposes.

### 5. Matter

A matter is a client-specific legal work unit governed by matter doctrine, not
project doctrine.

A matter:

- is tied to a client engagement
- follows matter lifecycle and matter-stage rules
- may use solutions, modules, or workflows in delivery
- may depend on projects that improve firm capability

Whether a matter is a type of project is not resolved by current doctrine and
remains an open question.

Current rule:

- matter governance is separate from project governance
- the matter/project relationship must not be inferred beyond what doctrine
  explicitly states

### 6. Solution

A solution is the canonical offering boundary for reusable operational design
and delivery.

A solution:

- defines what offering or outcome is being delivered
- is decomposed into modules
- may be used across multiple matters or operating contexts

A solution is not a project, matter, or workflow.

### 7. Module

A module is a bounded reusable functional component within a solution.

A module:

- groups operational artifacts required for a defined function
- may contain workflows, templates, checklists, and supporting references
- remains subordinate to its parent solution

A module is not a project, matter, or full solution.

### 8. Workflow

A workflow is the canonical procedural execution unit.

A workflow:

- defines how work is performed
- operates within a bounded solution/module or other approved operational scope
- consumes governed inputs and produces governed outputs

A workflow is not a project, matter, solution, or doctrine artifact.

## Structural Relationships

The canonical relationships are:

```text
Portfolio
-> Program
-> Project

Practice Area
-> Solution
-> Module
-> Workflow
```

Cross-system relationship rules:

- Projects may create, change, govern, or improve solutions, modules, and workflows.
- Workflows may execute work that supports a project or a matter.
- Matters may consume solutions, modules, and workflows.
- Portfolios contain programs.
- Programs contain projects.

Containment must not be inferred where doctrine does not define it.

## Stage-System Separation

Project delivery stages are a distinct system from:

- roadmap `STAGE<n>[.<phase>]` numbering
- register decision lifecycles such as `idea`, `screening`, or `approved`
- matter delivery-status states

These systems must not be collapsed into one vocabulary.

`Decision Project` is a canonical project type inside the project system. It is
not the same thing as a register-level decision lifecycle.

## Identity Rule

Project identity and storage location are not the same thing.

- `Project ID` is canonical identity.
- project path is a location key.
- folder slugs are not authoritative identity fields.

## Boundary Rule

If classification is ambiguous, the system must escalate rather than guess.

No artifact may:

- resolve the matter/project relationship by inference when doctrine has not
  resolved it
- classify a workflow, module, or solution as a project
- treat a portfolio or program as if it were a single project

## Related Doctrine

- `01_DOCTRINE/03_POLICIES/POL-055_Repository_Project_Policy.md`
- `01_DOCTRINE/03_POLICIES/POL-052_Client_Engagement_Stage_Policy.md`
- `01_DOCTRINE/03_POLICIES/POL-038_Module_Policy.md`
- `01_DOCTRINE/03_POLICIES/POL-039_Solution_Policy.md`
- `01_DOCTRINE/03_POLICIES/POL-040_Workflow_Policy.md`
- `01_DOCTRINE/01_INVARIANTS/DOCTRINE-RISK-0001-risk-model.md`
