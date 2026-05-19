---
id: hbp-013-dependencies
title: Dependencies — HBP-013 — Sale of Granville
owner: ML1
status: draft
created_date: 2026-05-19
last_updated: 2026-05-19
tags: [hillside, hbp-013, granville, planning, dependencies]
---

# Dependencies

**Project:** Sale of Granville
**Project ID:** HBP-013
**Stage:** Planning

| ID | Dependency | Type | Owner | Impact if Not Met |
| --- | --- | --- | --- | --- |
| D-01 | FINTRAC registration progress and status clarity for `17409052 Canada Inc` | Regulatory | ML1 / regulator | The licensed-entity thesis remains weak or deferred |
| D-02 | RPAA status, blockers, and filing implications | Regulatory | ML1 / Bank of Canada process | Market-ready posture stays incomplete and credibility is reduced |
| D-03 | EMI written indication or equally clear infrastructure support evidence | Counterparty | ML1 / EMI counterparties | Supporting-stack narrative remains too abstract |
| D-04 | AML program and buyer-review materials | Internal compliance | ML1 | Diligence packet is too thin to support later sale launch |
| D-05 | Minimum supporting software posture decision | Internal / vendor | ML1 | Vendor work drifts, costs rise, and scope loses discipline |
| D-06 | Vendor clarity from FinLego, Crassula, Rhizome, and others | External vendor | ML1 / vendors | Market-ready package cannot distinguish useful support from overbuild |
| D-07 | Q4 restructuring context under `17513721 Canada Inc` | Adjacent strategic context | ML1 | Eventual sale timing and use-of-proceeds logic stay under-anchored |

## Internal Dependencies

| ID | Dependency | Notes |
| --- | --- | --- |
| D-08 | `SCOPE_AND_POSITIONING_NOTE.md` | Must remain aligned with all vendor and planning documents |
| D-09 | `VENDOR_POSITIONING_NOTE.md` | Must remain aligned with the entity-branch source notes |
| D-10 | `PROJECT_PLAN.md` and `METRICS.md` | Must use the same readiness definitions and gate language |

## Dependency Risk Summary

The highest-risk dependency is `D-01` plus `D-03` together: without licensing
clarity and visible infrastructure support, the project cannot produce a
credible licensed-entity story.

The second priority is `D-05`: if the support-stack decision remains loose, the
project can easily drift into paying for software breadth that does not improve
eventual entity-sale value.
