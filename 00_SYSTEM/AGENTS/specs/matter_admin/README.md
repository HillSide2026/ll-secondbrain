---
id: 00_system__agents__specs__matter_admin__readme_md
title: Matter Administration Agents
owner: ML1
status: draft
created_date: 2026-03-05
last_updated: 2026-03-05
tags: []
---

# Matter Administration Agents

This folder defines Matter Administration Agent (MAA) charters used by
the Matter Command and Control pipeline.

## Run Graphs
- `00_SYSTEM/orchestration/run_graphs/matter_admin_daily.yaml`
- `00_SYSTEM/orchestration/run_graphs/matter_admin_one.yaml`

## Runner
- `scripts/run_matter_admin.py`

## Agents In Scope
- `MAA_MATTER_INDEX`
- `MAA_INBOX_ROUTER`
- `MAA_DEADLINE_EXTRACTOR`
- `MAA_DOCUMENT_DELTA`
- `MAA_COMMS_DRAFTER`
- `MAA_MATTER_DIGEST_COMPILER`

## System-of-Record Doctrine
- Clio = matter registry authority
- Gmail = communications authority
- SharePoint = document authority
- ML2 stores derived/admin artifacts plus source pointers only
