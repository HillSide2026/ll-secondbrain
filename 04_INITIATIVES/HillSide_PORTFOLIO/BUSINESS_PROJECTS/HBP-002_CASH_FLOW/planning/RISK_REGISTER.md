---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_002_cash_flow__planning__risk_register_md
title: Cash Flow - Risk Register
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-03-22
tags: [cash-flow, planning, risk-register]
---

# Risk Register

Project ID: `HBP-002`
Stage: `Planning`

| Risk | Category | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- | --- |
| Source data is incomplete or inconsistent across Matthew and the in-scope entities | Data | M | H | Freeze the source-record map early and escalate any missing records immediately |
| Matthew-level inflows and outflows are mixed inconsistently or omitted | Definition / control | M | H | Lock formula and treatment rules before pack design proceeds |
| Intercompany flows that do not touch Matthew distort the management view | Financial / reconciliation | M | M | Define elimination and disclosure rules explicitly |
| Direct Levine Law economics may be insufficient to support the `CAD 80,000` owner-compensation target without crediting Andersen Service Line economics | Financial / governance | M | H | Keep Andersen receipts as a cross-entity reconciliation item by default and require an explicit ML1 crediting rule before using Andersen economics to support Levine Law compensation planning |
| The close process cannot be completed within 10 business days | Schedule / operations | M | H | Keep the pack minimum viable and assign a clear review owner |
| Planning expands into a broad systems project | Scope | M | M | Reject automation or accounting-replacement work during planning |
| New businesses or residual cash events are added informally without classification rules | Governance | M | M | Require explicit admission to the reporting boundary before inclusion |
