---
id: mkt_skill_design_metadata_registration
title: Design Metadata Registration Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, governance, metadata]
---

# Skill: Design Metadata Registration

## Purpose
Capture canonical metadata and provenance for each generated design artifact.

## Inputs
- Design IDs and links
- Template references
- Run context metadata

## Process
1. Capture required metadata fields for each design.
2. Link design record to run, campaign, and template version.
3. Set governance defaults (`approval_status=draft`, `authorized=false`).
4. Persist metadata for repository governance workflows.

## Outputs
- Design metadata record
- Provenance linkage record
- Governance default-state confirmation

## Constraints
- Metadata schema must be complete.
- Missing core identifiers block artifact promotion.
- Records must remain auditable and immutable by log.

## Invocation
Used after design creation and before distribution handoff.

