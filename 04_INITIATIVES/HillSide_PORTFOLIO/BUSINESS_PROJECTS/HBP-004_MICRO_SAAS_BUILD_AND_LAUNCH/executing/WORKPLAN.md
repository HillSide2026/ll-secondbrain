---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_004_micro_saas_build_and_launch__executing__workplan_md
title: Develop and Launch Micro SaaS (TariffLookup.ca) - Executing Workplan
owner: ML1
status: active
created_date: 2026-03-12
last_updated: 2026-03-20
tags: [micro-saas, executing, workplan]
---

# Executing Workplan

Project ID: HBP-004
Project Path: 04_INITIATIVES/HillSide_PORTFOLIO/BUSINESS_PROJECTS/HBP-004_MICRO_SAAS_BUILD_AND_LAUNCH
Stage: Executing

## Objective
Deliver TariffLookup.ca through deployment, MVP build, launch, and
stabilization under the approved scope and budget controls.

## Decision Use
Use this file as the canonical executing plan, including scope control, sequence, and evidence requirements.

## Stage Entry Rule
Executing starts once ML1 records Planning -> Executing approval in `../APPROVAL_RECORD.md`.
Concept, ICP, and workflow scope must already be frozen in planning artifacts.
This requirement was satisfied on 2026-03-20.

## Current Execution Posture

- TariffLookup.ca remains the only in-scope product.
- A deployable static landing site bundle exists in `tarifflookup_site/`.
- Production deployment is not yet confirmed because HostGator-side resolution is still pending.
- The tariff-lookup MVP itself is not yet live.

## Executing Sequence

| Step | Executing Action | Status | Owner | Completion Evidence |
| --- | --- | --- | --- | --- |
| EX-01 Executing Control Packet | Normalize the executing-stage artifact set and make control files live. | complete | Project Owner | Executing folder contains canonical control artifacts |
| EX-02 Landing Site Deployment | Upload and verify the TariffLookup.ca landing bundle in production. | in progress | Project Owner | Live site verification and deployment notes |
| EX-03 Data and Rule Source Assembly | Assemble the six-jurisdiction tariff schedules, preferential schedules, and agreement-note logic inputs. | pending | Project Owner | Source register and data-readiness notes |
| EX-04 MVP Lookup Build | Build the one HS-code + one destination lookup workflow for the frozen MVP scope. | pending | Project Owner | Working lookup flow and sample output evidence |
| EX-05 QA and Reliability Pass | Run sampled accuracy, completeness, and performance checks against approved thresholds. | pending | Project Owner | QA evidence and KPI updates |
| EX-06 Pilot Activation | Onboard pilot users and capture activation evidence from real lookup usage. | pending | Project Owner | Pilot activation records and issue trends |
| EX-07 Launch and Stabilization | Move from initial launch into controlled stabilization and issue burn-down. | pending | Project Owner | Execution log updates, issue closure, and KPI dashboard |

## Workstreams

| Workstream | Scope | Owner | Evidence |
| --- | --- | --- | --- |
| EW-01 Launch Surface | Landing page deployment, domain verification, and public launch surface readiness | Project Owner | Site deployment notes and QA checklist |
| EW-02 MVP Data and Logic | Tariff, agreement, and eligibility-note data/model readiness for the six-jurisdiction MVP | Project Owner | Data-readiness notes and lookup samples |
| EW-03 Product Reliability | QA, issue triage, and threshold tracking for accuracy, completeness, and response time | Project Owner | QA checklist and KPI dashboard |
| EW-04 Adoption and Stabilization | Pilot onboarding, launch support, and first-30-day control loop | Project Owner | Execution log, KPI dashboard, and deliverables tracker |

## Milestones

Milestones are tracked in `DELIVERABLES_TRACKER.md`.

## Controls

- Scope control: no feature expansion outside the approved one-product, one-workflow MVP without ML1 approval.
- Budget control: maintain variance within the approved threshold from `planning/ML1_METRIC_APPROVAL.md`.
- Schedule control: escalate any blocked milestone or unresolved deployment dependency in `PROJECT LOG.md`.
- Quality control: tariff, preferential, and eligibility outputs must be validated against approved QA checks before launch.
- Governance control: all execution reporting must be reflected in the canonical executing-stage artifacts in this folder.

## Exit Rule
Executing is complete when the TariffLookup.ca MVP is live, stabilization
thresholds are met, and evidence is recorded across the canonical executing
artifact set.
