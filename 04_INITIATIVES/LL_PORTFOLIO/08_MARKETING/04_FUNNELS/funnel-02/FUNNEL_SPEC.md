---
id: 04_initiatives__ll_portfolio__08_marketing__funnels__funnel_02__funnel_spec_md
title: Funnel Spec — Funnel 02
owner: ML1
status: planned
created_date: 2026-02-25
last_updated: 2026-03-15
tags: []
---

# Funnel Spec — Funnel 02

## Funnel ID + Status

- funnel_id: funnel-02
- status: planned

## Purpose / Role

Corporate-law acquisition path for growing businesses with more than `$1M`
annual cash flow, using a preventative paid diagnostic as the entry point.

## Funnel Distinction

Funnel 02 is the primary awareness-and-interest building path for growth-stage
corporate-law demand. It carries prospects from discovery through
consideration and inquiry before conversion handoff.

## Positioning Reference

- 00_POSITIONING/MARKET_POSITIONING.md
- ICP-01: Ontario Operating Company
- Category: Fractional Counsel / Legal Function as a Service (preventative entry)
- Competitive framing: `COMPETITIVE_DIFFERENTIATION_MATRIX.md`
- Proof architecture: `PROOF_ARCHITECTURE.md`

## Target ICP (Must Match Positioning)

- Ontario-based operating businesses
- more than `$1M` annual cash flow
- 5-30 employees
- 2+ years in operation
- Accountant involved
- Document-ready
- Not in active crisis

Secondary planning hypothesis (research only):
- operators acquiring an existing operating business (independent or backed), pending cohort-comparison findings and ML1 approval.

## Entry Channel(s)

- Content
- Google Ads
- `levine-law.ca`
- overlapping NDA Esq landing-page acquisition surface on `levine-law.ca`

## Traffic / Acquisition

- Lead magnet: Growth Without Structural Drift (TM)
- higher-quality, higher-cost Google Ads traffic is allowed where it improves fit and downstream economics
- authority content / SEO is a core acquisition lane
- NDA Esq may act as a supplementary traffic and lead source for Funnel 02 where the acquisition surface overlaps, without changing project boundaries

## Intake Mechanism

- Go High Level (GHL) form
- Voice AI
- SMS follow-up
- SDR qualification call (mandatory for `intake_completed`)
- setter-supported qualification and scheduling

## Qualification Gates

- annual_cash_flow_min: $1M
- employee_min: 5
- years_in_operation_min: 2
- ontario_incorporation_required: true
- active_operating_business_required: true
- accountant_involved_required: true
- pre_conversion_minimum_readiness_required: true
- post_purchase_document_package_required: true
- qualification_call_evidence_required: true

Required documents:
- articles and bylaws
- shareholder agreement
- director and officer registers
- key commercial contracts
- employment and contractor agreements
- option or equity documents
- minute book (if maintained)
- recent financing documents

## Core Narrative / Promise

Structured corporate-law and governance assessment for operating companies that
have outgrown their original setup.

## Conversion Event Definition

- health_check_purchased

## Pipeline Stages

- awareness_discovery
- awareness_interest
- lead_magnet_downloaded
- inquiry_submitted
- intake_completed
- health_check_purchased
- review_in_progress
- delivery_meeting
- remediation_project
- fractional_counsel_retainer
- closed_lost

Stage ownership is governed in `pipeline.yaml` under `stage_ownership` and `lifecycle_boundary`.
Canonical lifecycle mapping is governed in `pipeline.yaml` under `lifecycle_mapping`.

Lifecycle interpretation:
- `awareness_discovery` maps to `discovery`.
- `awareness_interest` maps to `interest`.
- `lead_magnet_downloaded` maps to `consideration`.
- `inquiry_submitted` maps to `inquiry` (alias: `intake`).
- `intake_completed` is an intake-readiness checkpoint within `inquiry`.
- `health_check_purchased` maps to `conversion` and is the fulfillment handoff state.

## Primary Metrics

- paid_health_check_conversion_rate
- remediation_project_conversion_rate
- retainer_conversion_rate
- lead_response_time
- scheduled_consult_rate
- intake_reporting_completeness

## KPI Targets (Must Map to Goals)

- Goals reference: 02_GOALS/KPI_DEVELOPMENT_PROJECT/GOALS_2026.md
- KPI targets: TBD

## Objective Mapping (Reference OBJECTIVES.md Items)

- OBJ-01
- OBJ-02

## Offer Mapping (Strategy/Solution Supported)

- Strategy: Corporate Health Check -> Remediation -> Fractional Counsel
- Strategy folder: 02_PLAYBOOKS/CORPORATE/STRATEGIES/CORPORATE_HEALTH_CHECK_REMEDIATION/
- Entry offer: Corporate Health Check (paid diagnostic)
- Core offer: Remediation + Fractional Counsel
- Solutions: Corporate solution frames as indicated by remediation scope (TBD)

## Compliance Constraints / Disclaimers

- Do not launch until Positioning, Objectives, and Goals are formalized
- Marketing only; no legal advice or acceptance decisions
- ML1 approval required for acceptance

## Owner + Review Cadence

- Owner: ML1
- Review cadence: TBD
