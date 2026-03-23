---
layer: 08_RESEARCH
domain: financial-services-law
status: draft
owner: ML2
authority: not-approved
confidence: exploratory
created: 2026-03-23
updated: 2026-03-23
scope: "CA - federal; international"
matter_id: null
sources: []
open_questions:
  - McCarthy Tétrault — all three articles (final regs, draft regs, supervisory guidance) returned HTTP 429 rate-limit errors on multiple retry attempts; content not retrieved
  - Fasken final regulations article returned HTTP 403 Forbidden on all attempts
  - Dentons RPAA article returned HTTP 403 Forbidden on all attempts
  - Department of Finance RPAA page (canada.ca) returned HTTP 404 on all attempts; URL may have changed
  - RPAA statute (laws-lois.justice.gc.ca) returned HTTP 404; legislation database URL structure may have changed
  - KPMG Canada — no RPAA article URL confirmed; several candidate URLs returned 404
  - FSB PSP Recommendations report — page loaded but substantive PDF content not accessible via HTML scrape
  - BIS CPMI d193 — page loaded but content is a 2020 cross-border payments roadmap (G20 Building Blocks), not a direct RPAA analogue; limited relevance captured
  - Blakes, Norton Rose Fulbright, Bennett Jones, Torys portal searches — no RPAA articles surfaced initially; Blakes article subsequently found and retrieved (see #23 below)
  - Deloitte Canada RPAA PDF retrieved as binary; text extraction failed — content partially known from search result metadata
  - MNP RPAA article (https://www.mnp.ca/en/insights/directory/retail-payment-activities-act-what-you-need-to-know) returned 403
  - Payments Canada RPAA article (https://www.payments.ca/retail-payment-activities-act-and-what-it-means-retail-payments) returned 403
  - KPMG Canada — no specific RPAA article found; portal search returned only regulatory primary sources
  - PwC Canada — no specific RPAA article found
next_actions:
  - Retry McCarthy Tétrault articles outside business hours to avoid rate limiting
  - Retry Fasken and Dentons articles via alternate access routes
  - Confirm current Department of Finance RPAA URL (may have moved)
  - Download FSB December 2024 PDF directly for substantive recommendations
  - Retry MNP and Payments Canada RPAA articles
  - Search KPMG and PwC Canada websites directly for RPAA publications
---

# RPAA Source Index

Sources assembled for RPAA research. 9 of 20+ attempted sources successfully retrieved.

---

## Canadian Law Firms

| # | Source | URL | Retrieval | Notes |
|---|--------|-----|-----------|-------|
| 1 | Osler — RPAA Hub | https://www.osler.com/en/expertise/services/financial-services/financial-services-regulatory/retail-payment-activities-act/ | Retrieved | Full hub page; registration timeline, supervisory framework overview, AMP regime, Payments Canada integration |
| 2 | Osler — Draft Regulations | https://www.osler.com/en/resources/regulations/2023/retail-payment-activities-act-draft-regulations-published-for-comment | Retrieved | National security review process, acquisition of control thresholds, risk management framework, safeguarding models, third-party requirements, incident reporting |
| 3 | Osler — Final Regulations | https://www.osler.com/en/resources/regulations/2023/the-future-of-payments-regulation-has-arrived-final-regulations-to-the-retail-payment-activities-ac | Retrieved | Key changes from draft, eased requirements, new obligations, board approval, fee structure methodology, expected ~2,500 PSPs |
| 4 | McCarthy Tétrault — Final Regs | https://www.mccarthy.ca/en/insights/blogs/techlex/final-retail-payment-activities-regulations-issued | Failed (429) | Rate-limited on all attempts; retry |
| 5 | McCarthy Tétrault — Draft | https://www.mccarthy.ca/en/insights/blogs/techlex/federal-government-releases-draft-retail-payment-activities-act | Failed (429) | Rate-limited on all attempts; retry |
| 6 | McCarthy Tétrault — Supervisory Guidance | https://www.mccarthy.ca/en/insights/blogs/techlex/bank-canada-releases-new-retail-payment-activities-act-supervisory-guidance | Failed (429) | Rate-limited on all attempts; retry |
| 7 | Dentons — RPAA: The Wheels Are In Motion | https://www.dentons.com/en/insights/articles/2023/december/7/retail-payment-activities-act-the-wheels-are-in-motion | Failed (403) | Access blocked |
| 8 | Fasken — Final Regulations Released | https://www.fasken.com/en/knowledge/2023/11/final-retail-payment-activities-regulations-released | Failed (403) | Access blocked |
| 9 | Miller Thomson — Call to Action for PSPs | https://www.millerthomson.com/en/insights/structured-finance-and-securitization/payment-service-providers-canadas-retail-payment-activities-act-regulations/ | Retrieved | Four registration criteria, five payment functions, timelines, safeguarding framework, AMP severity levels |
| 10 | Blakes — Insights portal search | https://www.blakes.com/insights | Not found | No RPAA articles surfaced via portal search query |
| 11 | Norton Rose Fulbright — Knowledge portal search | https://www.nortonrosefulbright.com/en/knowledge | Not found | No RPAA articles surfaced via portal search query |
| 12 | Bennett Jones — Blog search | https://www.bennettjones.com/Blogs-Section | Not found | No RPAA articles surfaced via portal search query |
| 13 | Torys — Insights search | https://www.torys.com/insights | Not found | No RPAA articles surfaced via portal search query |
| 14 | KPMG Canada — Retail Payments | https://kpmg.com/ca/en/home/insights.html (portal) | Not found | No specific RPAA article identified; portal is dynamically rendered — requires direct site search |
| 23 | Blakes — Final Regulations Released | https://www.blakes.com/insights/the-wait-is-over-final-regulations-to-the-retail-payment-activities-act/ | Retrieved | Risk management framework (operational objectives, measurable targets, monitoring, incident response), safeguarding models (trust vs insurance/guarantee), compliance oversight (senior officer + board annual approval, triennial independent review), AMP regime ($1M serious / $10M very serious), annual reporting requirements, disproportionate compliance burden for smaller PSPs |
| 24 | Deloitte Canada — What RPAA Means for PSPs | https://www2.deloitte.com/content/dam/Deloitte/ca/Documents/ca-fsi-banking-rpaa-pov-en-v2-aoda.pdf | Partial (binary) | PDF retrieved but text extraction failed; presence confirmed; retry via readable HTML version |
| 25 | MNP — RPAA: What You Need to Know | https://www.mnp.ca/en/insights/directory/retail-payment-activities-act-what-you-need-to-know | Failed (403) | Accounting firm mid-market lens; retry |
| 26 | DLA Piper — Scope and Requirements of the RPAA | https://www.dlapiper.com/en/insights/publications/2024/02/scope-and-requirements-of-the-retail-payment-activities-act-in-canada | Not yet fetched | Found via search (Feb 2024); covers scope analysis and PSP requirements; fetch pending |
| 27 | PwC — Global Payments Regulation | https://www.pwc.com/gx/en/industries/financial-services/payments.html | Failed (404) | URL returned 404; PwC payments page may have moved |

## Primary / Regulatory

| # | Source | URL | Retrieval | Notes |
|---|--------|-----|-----------|-------|
| 15 | Bank of Canada — Supervisory Framework: Supervision | https://www.bankofcanada.ca/core-functions/retail-payments-supervision/supervisory-framework-supervision/ | Retrieved | Supervision methodology, enforcement tools (warning letters, compliance agreements, AMPs, compliance orders, court enforcement), review/appeal rights |
| 16 | Bank of Canada — Supervisory Framework: Registration | https://www.bankofcanada.ca/core-functions/retail-payments-supervision/supervisory-framework-registration/ | Retrieved | Registration criteria, PSP Connect portal, required information, grounds for refusal/revocation, review/appeal process |
| 17 | Bank of Canada — Information for PSPs | https://www.bankofcanada.ca/core-functions/retail-payments-supervision/information-for-payment-service-providers/ | Retrieved | Overview only; points to self-assessment tool, case scenarios, PSP Connect, registry |
| 18 | Bank of Canada — Retail Payments Supervision landing | https://www.bankofcanada.ca/core-functions/retail-payments-supervision/ | Retrieved | Programme overview; confirms Sept 8, 2025 operational requirements effective date |
| 19 | Department of Finance — RPAA Overview | https://www.canada.ca/en/department-finance/programs/financial-sector-policy/retail-payments-oversight-framework.html | Failed (404) | URL appears to have changed; retry with updated URL |

## International / Comparative

| # | Source | URL | Retrieval | Notes |
|---|--------|-----|-----------|-------|
| 20 | FSB — PSP Recommendations Final Report (Dec 2024) | https://www.fsb.org/2024/12/recommendations-for-regulating-and-supervising-bank-and-non-bank-payment-service-providers-offering-cross-border-payment-services-final-report/ | Partial | Page loaded but substantive content in PDF only; title and scope confirmed |
| 21 | BIS CPMI — d193 (Cross-Border Payments Building Blocks) | https://www.bis.org/cpmi/publ/d193.htm | Partial | Confirmed as July 2020 G20 Stage 2 roadmap; 19 building blocks for faster, cheaper, more transparent cross-border payments; foundational framework only |
| 22 | UK FCA — Payment Services Regulations | https://www.fca.org.uk/firms/payment-services-regulations-e-money-regulations | Retrieved | PSRs 2017 authorization/registration tiers, scope, major incident reporting (EBA criteria), safeguarding obligations, FCA enforcement approach |
