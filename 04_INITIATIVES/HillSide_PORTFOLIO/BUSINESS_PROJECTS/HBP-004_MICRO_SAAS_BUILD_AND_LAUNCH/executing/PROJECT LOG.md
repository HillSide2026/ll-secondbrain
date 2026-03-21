---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_004_micro_saas_build_and_launch__executing__project_log_md
title: Develop and Launch Micro SaaS (TariffLookup.ca) - Project Log
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-03-20
tags: [micro-saas, executing, log]
---

# Project Log

Project ID: `HBP-004`
Stage: `Executing`

## Timeline

| Date | Entry Type | Entry | Status | Evidence |
| --- | --- | --- | --- | --- |
| 2026-03-20 | milestone | Planning -> Executing authorization recorded for TariffLookup.ca | completed | `../APPROVAL_RECORD.md` |
| 2026-03-20 | deliverable | Static landing site bundle confirmed in `executing/tarifflookup_site/` | completed | site bundle files present |
| 2026-03-20 | blocker | Production website deployment remains blocked pending HostGator-side resolution | open | hosting verification still pending |
| 2026-03-20 | controls | Canonical executing-stage control packet created in `executing/` | completed | executing artifact set present |

## Decisions

| Decision ID | Date | Decision | Owner | Reason |
| --- | --- | --- | --- | --- |
| EX-D-001 | 2026-03-20 | Treat TariffLookup.ca as the explicit product name for `HBP-004` across current project artifacts. | ML1 | Remove ambiguity about which micro SaaS is actually being executed. |
| EX-D-002 | 2026-03-20 | Use the static site bundle as the current public launch surface while the lookup MVP remains under execution. | ML1 | A controlled launch surface is already available and supports early market presence. |
| EX-D-003 | 2026-03-20 | Keep MVP scope locked to one HS code plus one destination across the approved six-jurisdiction set. | ML1 | Preserve the frozen planning scope and avoid premature feature expansion. |

## Changes

| Date | Change | Type | Impact |
| --- | --- | --- | --- |
| 2026-03-20 | Project naming normalized to `Develop and Launch Micro SaaS (TariffLookup.ca)` in current project artifacts. | governance | Aligns project identity with the actual product under execution. |
| 2026-03-20 | Executing workplan rewritten from a generic application build sequence to a TariffLookup.ca execution sequence. | scope / controls | Removes internal inconsistency from the executing packet. |
| 2026-03-20 | Canonical executing-stage control artifacts created in `executing/`. | controls | Brings the stage packet closer to repo policy compliance. |

## Open Issues

| Issue ID | Date Opened | Issue | Severity | Status | Owner | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| EX-I-001 | 2026-03-20 | TariffLookup.ca landing site deployment is pending HostGator-side resolution for upload / document-root confirmation. | high | open | Project Owner | Resolve hosting-side blocker and verify live deployment. |
| EX-I-002 | 2026-03-20 | Target launch date for the lookup MVP is not yet posted in the executing packet, making launch-timing KPI variance not yet measurable. | medium | open | Project Owner | Record target launch date once execution sequence is fixed beyond the hosting blocker. |

## Status Snapshot

Report Date: `2026-03-20`
Overall Status: `amber`

- Executing is authorized.
- TariffLookup.ca is the explicit named product in the current artifact set.
- The static site bundle exists, but production deployment is still blocked by HostGator-side resolution.
- The lookup MVP itself is not yet live.

Current blockers:

- HostGator-side deployment / document-root resolution remains open.
- No formal MVP target launch date is yet posted in the executing packet.

Next actions:

- resolve the HostGator deployment blocker
- verify live landing page deployment
- assemble MVP data and rule inputs for the six approved jurisdictions
- begin the frozen one-workflow tariff lookup build

## Risk Notes

| Risk | Current Status | Trend | Owner | Update |
| --- | --- | --- | --- | --- |
| Host/deployment resolution delays public launch surface | open | worsening | Project Owner | Live landing page deployment is blocked pending HostGator-side resolution. |
| Tariff / agreement data availability delays MVP build | open | steady | Project Owner | Six-jurisdiction data and rule inputs still need to be assembled in execution. |
| Eligibility logic may be too weak for reliable notes | open | steady | Project Owner | Risk remains until QA sampling begins on real outputs. |
| Budget envelope may be exceeded once build work starts | open | steady | Project Owner | No booked spend is recorded yet; control remains active but untested in execution. |
| Weak pilot-user access may slow validation | open | steady | Project Owner | Pilot activation work has not started yet. |

## Stakeholder Notes

| Date | Audience | Update | Status |
| --- | --- | --- | --- |
| 2026-03-20 | ML1 | Executing is authorized; TariffLookup.ca remains the in-scope product; the static site bundle exists; production deployment is still blocked by HostGator-side resolution. | issued |
| 2026-03-20 | Matthew Holdings | Executing-stage control packet has been normalized and the project is now being tracked with canonical execution artifacts. | issued |
| 2026-03-20 | Project Owner / Delivery Team | Immediate priorities are to resolve deployment, verify the live landing surface, and begin the frozen MVP build sequence. | issued |
