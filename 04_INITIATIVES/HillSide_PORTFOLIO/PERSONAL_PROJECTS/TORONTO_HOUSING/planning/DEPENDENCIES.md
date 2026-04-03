---
id: 04_initiatives__hillside_portfolio__personal_projects__toronto_housing__planning__dependencies_md
title: Toronto Housing - Dependencies
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [hillside, personal-projects, housing, toronto, planning, dependencies]
---

# Dependencies

Project ID: `TORONTO_HOUSING`
Stage: `Planning`

| Dependency | Type | Why It Matters | Current Status |
| --- | --- | --- | --- |
| ML1 decision authority | Internal | Controls option selection, guardrails, and planning exit | available |
| `HBP-001_WEALTH_MANAGEMENT` capital-governance model | Internal | Needed to anchor the housing budget and liquidity rules | open dependency |
| Toronto ownership market reality | External | Needed to determine whether a credible owned-Toronto path exists inside guardrails | open |
| Leave-Toronto destination logic | Strategic | Needed to test whether leaving Toronto is a real alternative rather than an abstraction | open |
| Optional legal / financing / transaction support | External | May be needed if the preferred path requires execution detail beyond current internal clarity | not yet engaged |

## Dependency Rule

No execution recommendation should treat the housing budget as valid until it
is anchored in `HBP-001_WEALTH_MANAGEMENT`, and no Toronto-ownership path
should be treated as credible while market reality remains hypothetical.
