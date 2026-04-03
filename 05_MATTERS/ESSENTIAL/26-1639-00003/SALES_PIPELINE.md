---
id: MATTER-26-1639-00003-SALES_PIPELINE
title: Sales Pipeline — 26-1639-00003 — Andersen (Market Access)
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [matter, sales-pipeline, 26-1639-00003]
practice_areas: [market_access, trade, customs]
---

# Sales Pipeline — 26-1639-00003 — Andersen (Market Access)

## Purpose

This file breaks the Andersen market-access matter into prospective end-client
files inside the Andersen relationship.

Andersen is the LL client. The pipeline here is about prospecting and
advancing end-client files through Andersen.

This is similar to LL Onboarding in that it moves opportunities toward close
and usable work, but it is not the same process. It does not treat the end
client as automatically being the LL client of record.

## Stage Model

- `identified` — a proceeding, transaction, or file opportunity has surfaced; we are identifying relevant parties, jurisdictions, and issues, and initiating outreach where appropriate, but have not yet established live contact
- `contacted` — we have established contact with a real live human being at the target organization
- `qualified` — there is enough substance to treat the file as a real target
- `closing` — active effort is underway to convert the opportunity into instructed work through Andersen
- `active_file` — instructions are in and the file is now live inside the Andersen market-access lane

## Industry Segment Model

Initial target segments for the Andersen market-access lane:

- `agriculture_and_agri_food`
- `mining_and_minerals`
- `manufacturing`
- `dual_use_manufacturing`
- `data_and_data_centres`

Current visible tracks sit inside `agriculture_and_agri_food`. Additional
tracks should be tagged to one of the above segments when first recorded.

## Active Tracks

| Track ID | End-client file | Segment | Stage | Current signal | Next step |
|----------|-----------------|---------|-------|----------------|-----------|
| `MA-001` | Pecans from Northern Israel — agri-food market-access file | `agriculture_and_agri_food` | `identified` | ML1 note indicates a live effort to broker pecan sales from Northern Israel | Confirm target buyer, countries in scope, live contact status, and the actual legal / market-access issue before qualification |
| `MA-002` | Flavored butter from Manitoba — agri-food market-access file | `agriculture_and_agri_food` | `identified` | ML1 note indicates a live effort to broker flavored butter from Manitoba | Confirm target market, counterparties, and whether this is a concrete trade / customs / regulatory file before qualification |

## Operating Notes

- Use [`../26-1639-00001/MATTER_BRIEF.md`](../26-1639-00001/MATTER_BRIEF.md) for Andersen relationship-level management.
- Use [`../26-1639-00001/BUSINESS_DEVELOPMENT_OVERVIEW.md`](../26-1639-00001/BUSINESS_DEVELOPMENT_OVERVIEW.md) for cross-lane Andersen business-development visibility.
- Use this matter for the market-access lane within that Andersen relationship.
- Use [`../26-1639-00002/SALES_PIPELINE.md`](../26-1639-00002/SALES_PIPELINE.md) as the parallel Andersen lane using the same stage model.
