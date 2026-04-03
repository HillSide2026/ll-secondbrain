---
id: trm_citt_update_scanner
title: CITT Update Scanner Agent Charter
owner: ML1
status: draft
created_date: 2026-04-02
last_updated: 2026-04-02
tags: [trade-remedies, citt, monitoring, scanner]
---

# CITT Update Scanner Agent Charter

## Agent
`TRM_CITT_UPDATE_SCANNER`

## Purpose
Scan official Canadian International Trade Tribunal surfaces for updates
relevant to trade-remedies pipeline monitoring.

The current operating use case is the Andersen trade-remedies sales pipeline in
[`05_MATTERS/ESSENTIAL/26-1639-00002/`](../../../../05_MATTERS/ESSENTIAL/26-1639-00002/).

## Action Bindings
- `agent_citt_update_scan` (matter-scoped scheduled or ad hoc run)

## Inputs
- Matter-local watchlist YAML
- Prior scanner state
- Official CITT source pages only

## Current Official Source Scope
- CITT home page / What's new
- Active dumping and subsidizing cases
- Measures in force and expiry time lines
- Active safeguard inquiries
- List of Tribunal decisions not yet published

## Responsibilities
- Detect source-page changes on official CITT pages
- Surface newly observed case captions, news items, and trade-remedy signals
- Flag approaching expiry-review / sunset-review timelines from the official measures-in-force page
- Match observed signals against matter-specific watch terms
- Produce a matter-local report for ML1 review
- Separate direct observation from downstream inference

## Outputs
- Matter-local CITT signal report
- Scanner state snapshot

## Runner
- `00_SYSTEM/scripts/scan_citt_updates.py`
- Default matter watchlist: `05_MATTERS/ESSENTIAL/26-1639-00002/CITT_WATCHLIST.yaml`

## Current Operating Cadence
- Daily trade-remedies scheduler: `00_SYSTEM/scripts/run_trade_remedies_daily.py`
- Local machine installer: `00_SYSTEM/scripts/install_trade_remedies_citt_launch_agent.py`
- Schedule contract: `00_SYSTEM/CONFIG/run_schedule.yml`

## Does Not
- Contact target organizations automatically
- Advance pipeline stages automatically
- Treat every CITT update as a business-development opportunity
- Make legal judgments about merits, jurisdiction, standing, or filing strategy

## Definition of Done
- Every surfaced signal is attributable to an official CITT URL
- Source changes are distinguished from unchanged sources
- Matter-specific matches are distinguished from general market awareness items
- Any recommendation is clearly labeled as recommendation rather than
  observation
