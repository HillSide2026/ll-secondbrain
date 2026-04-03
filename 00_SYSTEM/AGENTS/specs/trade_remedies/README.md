---
id: 00_system__agents__specs__trade_remedies__readme_md
title: Trade Remedies Agents
owner: ML1
status: draft
created_date: 2026-04-02
last_updated: 2026-04-02
tags: [trade-remedies, agents]
---

# Trade Remedies Agents

This folder defines trade-remedies-specific agent charters used to monitor,
interpret, and support the Andersen trade-remedies lane and any later LL trade
remedies matters.

## Run Graphs
- `00_SYSTEM/orchestration/run_graphs/trade_remedies_citt_daily.yaml`

## Agents In Scope
- `TRM_CITT_UPDATE_SCANNER`

## Runners
- `00_SYSTEM/scripts/run_trade_remedies_daily.py`
- `00_SYSTEM/scripts/scan_citt_updates.py`

## Current Matter Configuration
- `05_MATTERS/ESSENTIAL/26-1639-00002/CITT_WATCHLIST.yaml`

## Local Scheduler
- `00_SYSTEM/scripts/install_trade_remedies_citt_launch_agent.py`
- Schedule config: `00_SYSTEM/CONFIG/run_schedule.yml`

## Authority Boundary
- Official-source monitoring and reporting only
- No automatic outreach
- No automatic matter-stage changes
- No legal conclusions or filing decisions without ML1 review
