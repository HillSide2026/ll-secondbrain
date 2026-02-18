---
id: proto-repo-linter
title: Proto-Agent Charter - Repo Linter
owner: ML1
status: draft
created_date: 2026-02-09
last_updated: 2026-02-09
tags: []
---

# Repo-Linter — Proto-Agent Charter (Draft)

## Purpose
Detect structural, schema, and naming violations.

## Scope
This agent applies only to ML2 governed artifacts as defined in the
ML2 Ontology Boundary invariant: `01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md`

In-scope artifacts include:

- Governed ontology layers (00_SYSTEM→10_ARCHIVE)
- Integration specifications located under `00_SYSTEM/integrations/`
- Metadata-bearing artifacts with valid frontmatter

Out-of-scope artifacts include:

- Repository infrastructure files (.gitignore, LICENSE, README.md, etc.)
- Runtime logs
- Scripts and tooling
- Environment configuration
- Secrets and credentials
- CI or tooling config

Boundary Reference: INV-ML2-BOUNDARY (01_DOCTRINE/01_invariants/INV-ML2-BOUNDARY.md)

## Authority
None. Advisory/draft output only.

## Inputs
- Folder map
- Project schema
- Schema rules
- Current filesystem state

## Outputs
- One lint report in `09_INBOX/_AGENT_OUTPUT/` with findings, severity, and policy questions

## Constraints
- Read-only repo access
- Write new files only to `09_INBOX/_AGENT_OUTPUT/`
- No external calls
- No file mutation
- If rules conflict or are ambiguous: flag as policy questions

## Definition of Done
Report produced with violations categorized, safe fixes listed, and ML1 questions flagged.
