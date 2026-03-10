---
id: mkt_skill_design_handoff_packet
title: Design Handoff Packet Skill
owner: ML1
status: draft
created_date: 2026-03-10
last_updated: 2026-03-10
tags: [marketing, skill, handoff, design]
---

# Skill: Design Handoff Packet

## Purpose
Assemble a complete handoff package for Editorial QA and Distribution Orchestration.

## Inputs
- Preflight-approved design artifacts
- Metadata records
- Design brief and variant matrix

## Process
1. Bundle design links, IDs, and variant labels.
2. Attach compliance and preflight reports.
3. Attach source brief and content provenance.
4. Emit structured handoff manifest for downstream agents.

## Outputs
- Design handoff manifest
- QA handoff packet
- Distribution-ready artifact references

## Constraints
- Handoff packet must include complete provenance chain.
- Incomplete packets cannot advance stages.
- Handoff does not confer publication authorization.

## Invocation
Used at the end of design production before downstream agent execution.

