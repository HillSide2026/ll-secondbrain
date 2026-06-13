---
id: funnel-02-tactical-funnel-map
title: Tactical Funnel Map — Funnel 02 (Corporate)
owner: ML1
status: draft
created_date: 2026-06-11
last_updated: 2026-06-11
tags: [funnel-02, tactical-funnels, ghl, corporate]
---

# Tactical Funnel Map — Funnel 02 (Corporate)

## Purpose

Document the tactical funnels that operate within Funnel 02 (the corporate
macro funnel). Each tactical funnel is a distinct offer path inside the single
GHL corporate pipeline.

This map does not replace the macro funnel definition in `FUNNEL_SPEC.md`. It
adds the tactical layer beneath it.

## Context: Two Levels of "Funnel"

| Level | Scope | GHL Mapping |
|---|---|---|
| **Macro funnel** | Strategic acquisition path (F02 = corporate) | One GHL pipeline per macro funnel |
| **Tactical funnel** | Specific offer path within the macro funnel | Stages or sub-paths within the macro GHL pipeline |

This document governs the tactical level for F02.

---

## Tactical Funnel Register

| ID | Name | Entry Offer | GHL Availability | Traffic Source | Status | Role |
|---|---|---|---|---|---|---|
| F02-T01 | Corporate Health Check | Paid diagnostic (CAD 2,000 / 3,500 / 6,000 tiers) | TBC | TBC | Draft | **Dominant** |
| F02-T02 | Founders Pack (Pure) | Founders Pack | Welcoming stage | TBC | Draft | Supporting |
| F02-T03 | Founders Agreement | Founders Agreement with upsell to Founders Pack | Welcoming stage | TBC | Draft | Supporting |
| F02-T04 | Corporate Law Firm Landing Page | TBC | TBC | Organic / direct | Draft | Supporting |
| F02-T05 | Inquiries Page | TBC | TBC | TBC | Draft | Supporting |

---

## Tactical Funnel Descriptions

### F02-T01 — Corporate Health Check (Dominant)

**Entry offer:** Paid diagnostic — three tiers (CAD 2,000 / 3,500 / 6,000)  
**Role:** Proposed dominant tactical funnel within F02  
**GHL availability:** TBC  
**Traffic source:** TBC  
**Description:** The Corporate Health Check is a preventative paid diagnostic
for Ontario operating businesses meeting the F02 ICP (5M+ cash flow). ML1
reviews the client's legal structure and identifies gaps. Findings create a
natural conversion path into remediation work and downstream fractional
counsel retainer (governed by the pricing model in LLP-012).

**Status in LLP-012:** LLP-012 (Funnel 2 Management) is the governing project
for this tactical funnel. The Information Product 3 execution bundle (landing
page, GHL intake path, qualification-call spec, Stripe product) is in
progress.

**Three distinct offers (ML1-confirmed 2026-06-11):** These are not tier
variants of the same product — they are structurally distinct offers:

| Offer | Price | Nature |
|---|---|---|
| Diagnostic | ~CAD 600 | Diagnostic product — default entry offer; ML1-confirmed 2026-06-11 |
| Consultation | TBC | Consultation offer — price to be confirmed |
| Implementation | TBC | Implementation offer — price to be confirmed |

Default Stripe product to be created at ~CAD 600 (Diagnostic).

**Open items:**
- GHL stage mapping for this tactical funnel
- Deliverable definition (what the client receives, ML1 time required)
- Traffic source and acquisition channel

---

### F02-T02 — Founders Pack (Pure)

**Entry offer:** Founders Pack  
**GHL availability:** Made available at the Welcoming stage  
**Traffic source:** To be confirmed  
**Description:** A direct Founders Pack offer with no preceding Founders
Agreement step. Target profile to be defined.

**Open items:**
- Traffic source and acquisition channel
- ICP sub-type this path targets within the F02 taxonomy
- Pricing (governed by SHA service line architecture)

---

### F02-T03 — Founders Agreement

**Entry offer:** Founders Agreement, with upsell to Founders Pack  
**GHL availability:** Made available at the Welcoming stage  
**Traffic source:** To be confirmed  
**Description:** Entry via a Founders Agreement engagement. After delivery,
a Founders Pack upsell is offered. The Founders Agreement is the lower-friction
entry; the Founders Pack is the fuller relationship offer.

**Open items:**
- Traffic source and acquisition channel
- ICP sub-type this path targets within the F02 taxonomy
- Relationship between Founders Agreement pricing and Founders Pack pricing
- Whether the upsell is offered at close of Founders Agreement or earlier

---

### F02-T04 — Corporate Law Firm Landing Page

**Entry offer:** TBC  
**GHL availability:** TBC  
**Traffic source:** Organic / direct  
**Description:** The corporate law firm landing page as a tactical funnel
entry point. Role within the GHL pipeline and offer architecture to be
defined.

**Open items:**
- What offer or CTA this page routes to
- How it maps to GHL stages
- Which tactical funnel(s) it feeds into

---

### F02-T05 — Inquiries Page

**Entry offer:** TBC  
**GHL availability:** TBC  
**Traffic source:** TBC  
**Description:** The inquiries page as a tactical funnel entry point.
Role within the GHL pipeline and offer architecture to be defined.

**Open items:**
- What offer or CTA this page routes to
- How it maps to GHL stages
- Whether inquiries route into a specific tactical funnel or are triaged
  manually before assignment

---

## Open Questions for ML1

| # | Question |
|---|---|
| OQ-1 | Are there additional tactical funnels within F02 beyond the four listed above? |
| OQ-2 | What are the traffic sources for F02-T01 and F02-T02? |
| OQ-3 | What offer or CTA does the corporate law firm landing page (F02-T03) route to? |
| OQ-4 | What offer or CTA does the inquiries page (F02-T04) route to? Is it triaged manually or routed to a specific tactical funnel? |
| ~~OQ-5~~ | ~~Does the Corporate Health Check remain as a tactical funnel within F02?~~ **Resolved 2026-06-11:** Corporate Health Check is confirmed as the dominant tactical funnel within F02. |

---

## Relationship to GHL Pipeline Governance

The GHL Pipeline Governance project (backlog) must account for this tactical
funnel map when standardizing GHL stages. Each tactical funnel should have
explicit GHL stage coverage in the pipeline.

The macro F02 GHL pipeline is: `LL - Corporate (New)`.

Stage standardization work cannot be finalized until the tactical funnel map
is approved by ML1.

---

## Governing Artifacts

- Macro funnel definition: `FUNNEL_SPEC.md`
- GHL pipeline spec: `pipeline.yaml`
- SHA service line architecture: `02_PLAYBOOKS/CORPORATE/SOLUTIONS/SHAREHOLDER_AGREEMENT/SHA_SERVICE_LINE_ARCHITECTURE/`
- LLP-012 (Funnel 2 Management project): `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/LLP-012/`
