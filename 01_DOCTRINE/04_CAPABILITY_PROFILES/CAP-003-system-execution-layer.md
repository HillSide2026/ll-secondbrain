---
id: CAP-003
title: Capability Profile: System (Execution Layer)
owner: ML1
status: active
version: 1.0
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [capability, system, execution]
---
# Capability Profile: System (Execution Layer)

## Purpose
Define runtime permissions and limits for the System execution component.

## Allowed
- Execute agents and orchestrations
- Apply doctrine during runtime
- Perform QC validation
- Detect drift and inconsistencies
- Produce diagnostics and escalation signals

## Not Allowed
- Create doctrine
- Interpret doctrine beyond explicit rules
- Approve exceptions
