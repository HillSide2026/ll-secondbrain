---
id: ws-a-company-universe-v0.2
title: WS-A Company Universe v0.2
workstream: WS-A
artifact_type: WS-A/0
status: approved
approved_by: ML1
approved_date: 2026-04-25
version: 0.2
output_label: Derived from disclosed agreement (SEC)
---

# WS-A/0 — Company Universe v0.2

**Workstream:** WS-A (SEC Disclosure Mining)
**Artifact Type:** WS-A/0 — Company Universe
**Status:** Approved (ML1, 2026-04-25)
**Output Label:** Derived from disclosed agreement (SEC)

---

## Purpose

This document is the canonical target list for Workstream A research. It defines
which companies are in scope for SEC EDGAR disclosure mining, their filing status,
expected agreement archetypes, and research priority.

The universe is organized into six categories. Sponsor Banks are an elevated
category: they are not payment fintechs, but they are load-bearing counterparties
in issuer processor, program manager, and sponsor bank agreements. Their SEC
filings disclose these relationships from the bank's perspective, which is often
different from the fintech counterparty's disclosure.

---

## Category 1 — Issuer Processing / Program Management / BaaS

| Company | SEC Status | CIK | Priority | Target Archetypes | Notes |
|---|---|---|---|---|---|
| Marqeta, Inc. | SEC-registered (NASDAQ: MQ) | 1522540 | HIGH | Issuer Processor, Program Manager, Platform/Customer MSA | Initial harvest done (draft, 2026-04-25). EX-10.21 (Sutton Bank PM Agreement) and EX-10.14 (Block MSA) extracted. Limitation of liability redacted. |
| Galileo Financial Technologies | Not SEC-registered; appears via SoFi Technologies (NASDAQ: SOFI) | 1818874 (SoFi) | MEDIUM | Issuer Processor, Program Manager, BaaS | Galileo acquired by SoFi 2020. Commercial agreements may appear as EX-10 in SoFi SEC filings post-acquisition. SoFi Bank N.A. is an OCC-chartered bank (as of 2022), altering the sponsor bank dependency. |
| Green Dot Corporation | SEC-registered (NYSE: GDOT) | 1309108 | HIGH | Sponsor Bank, Program Manager, Prepaid Card Program | Green Dot Bank is Green Dot's wholly-owned subsidiary. Dual role: sponsor bank for third-party programs AND issuer of own prepaid products. 10-K disclosures include bank partnership agreements. |
| i2c Inc. | Not SEC-registered (private) | — | LOW | Issuer Processor, Program Manager | Private company. No SEC filing. May appear as counterparty in clients' filings. Use client filings as indirect source. |

---

## Category 2 — Merchant Acquiring / Payment Processing

| Company | SEC Status | CIK | Priority | Target Archetypes | Notes |
|---|---|---|---|---|---|
| Adyen NV | Not SEC-registered (Euronext Amsterdam: ADYEN) | 1788707 (ADR admin only) | LOW (SEC) / MEDIUM (Dutch) | FI Partnership, Issuer Processor, Enterprise Payment Services | No Form 20-F. No EX-10 exhibits. Holds own Dutch banking licence (2017) and UK banking licence (2023). Research requires Dutch annual reports from investors.adyen.com — separate workstream. |
| Block, Inc. | SEC-registered (NYSE: SQ) | 1512673 | HIGH | Sponsor Bank, Platform/Customer MSA, Embedded Finance | Initial harvest done (draft, 2026-04-25). Sutton Bank and Celtic Bank disclosed in 10-K body text only — no standalone EX-10 filed. Marqeta EX-10.14 (filed by Marqeta) is the primary clause-level source for Block's card programs. |
| PayPal Holdings, Inc. | SEC-registered (NASDAQ: PYPL) | 1633917 | HIGH | Enterprise Payment Services, FI Partnership, Program Manager | Initial harvest partial (draft, 2026-04-25). eBay Operating Agreement (EX-10.1, 2015) extracted but indemnification and liability provisions not retrieved (HTTP 403). Bank partnership agreements (Synchrony, Bancorp) not filed as PayPal EX-10 exhibits. |
| Stripe, Inc. | Not SEC-registered (private) | — | MEDIUM (via counterparties) | Embedded Finance, Platform/Customer MSA, Sponsor Bank | Private. No SEC filings. Search counterparty filings for disclosed Stripe agreements. Stripe's bank partners (notably Evolve and Cross River) may disclose Stripe-related structures in their own filings. |
| Global Payments Inc. | SEC-registered (NYSE: GPN) | 1123360 | MEDIUM | Issuer Processor, Enterprise Payment Services, FI Partnership | Large acquirer. Likely has disclosed bank-fintech partnership and enterprise processing agreements as EX-10 material contracts. |
| Fiserv, Inc. | SEC-registered (NASDAQ: FISV) | 798354 | MEDIUM | Issuer Processor, Enterprise Payment Services, Bank-Fintech Partnership | Large processor and bank services provider. Acquired First Data (2019) and Clover network. Material agreement EX-10 filings likely to include bank processing agreements. |
| FIS (Fidelity National Information Services) | SEC-registered (NYSE: FIS) | 798354 | MEDIUM | Issuer Processor, Enterprise Payment Services, Bank-Fintech Partnership | Spun off Worldpay (2023). Material agreement filings may include bank card processing and enterprise payment agreements. |
| Shift4 Payments, Inc. | SEC-registered (NYSE: FOUR) | 1794669 | MEDIUM | Payment Facilitator, Enterprise MSA, Platform/Customer MSA | Integrated payments for hospitality/restaurant. S-1 (2020) and 10-K filings. |
| Toast, Inc. | SEC-registered (NYSE: TOST) | 1793463 | MEDIUM | Payment Facilitator, Platform/Customer MSA, Merchant Acquiring | Restaurant-focused payment platform. S-1 (2021) and 10-K filings. |

---

## Category 3 — Cross-Border / Remittance / FX

| Company | SEC Status | CIK | Priority | Target Archetypes | Notes |
|---|---|---|---|---|---|
| Wise plc | Not SEC-registered (LSE: WISE) | — | LOW (SEC) / MEDIUM (UK) | FI Partnership, Cross-Border MSB, Correspondent Banking | UK-listed. No SEC filing. Holds FCA EMI licence and US state MTL licences. Annual reports and FCA disclosures are the primary source. Outside SEC workstream scope. |
| Remitly Global, Inc. | SEC-registered (NASDAQ: RELY) | 1782372 | MEDIUM | FI Partnership, Cross-Border MSB, Enterprise Disbursement | Filed S-1 2021. Sends remittances via bank partnerships. EX-10 material agreements may include bank partnership and disbursement agreements. |
| Western Union Company | SEC-registered (NYSE: WU) | 1348925 | MEDIUM | FI Partnership, Enterprise Payment Services, Agent Network | Major MSB. Long SEC filing history. Material agreements may include agent appointment, bank partnership, and settlement agreements. |
| MoneyGram International | Went private 2023 (acquired by Madison Dearborn Partners) | 1273931 | MEDIUM | FI Partnership, Agent Network, Cross-Border MSB | SEC filing history available through 2023. Historical 10-K EX-10 exhibits may be extractable for archival doctrine purposes. |
| Flywire Corporation | SEC-registered (NASDAQ: FLYW) | 1816806 | MEDIUM | Enterprise Payment Services, FI Partnership, International MSA | Institutional/enterprise international payments. S-1 (2021) and 10-K filings. |
| OFX Group Limited | Not SEC-registered (ASX: OFX) | — | LOW | FI Partnership, Cross-Border MSB | ASX-listed Australian company. No SEC filing. Outside SEC workstream scope. |

---

## Category 4 — Embedded Finance / Platform Payments

| Company | SEC Status | CIK | Priority | Target Archetypes | Notes |
|---|---|---|---|---|---|
| Shopify Inc. | SEC-registered (NYSE/TSX: SHOP) | 1594805 | MEDIUM | Embedded Finance, Platform/Customer MSA, Sponsor Bank | Shopify Balance and Shopify Capital involve banking partnerships. EX-10 filings may disclose bank and payment processor arrangements. |
| Uber Technologies, Inc. | SEC-registered (NYSE: UBER) | 1543151 | MEDIUM | Embedded Finance, Enterprise Payment Services, FI Partnership | Uber Money / Uber Pro Card involve banking and prepaid card structures. S-1 (2019) and 10-K filings. |
| Lyft, Inc. | SEC-registered (NASDAQ: LYFT) | 1759509 | LOW | Embedded Finance, FI Partnership | Smaller payment footprint than Uber. S-1 (2019) and 10-K filings. |
| DoorDash, Inc. | SEC-registered (NYSE: DASH) | 1792789 | LOW | Embedded Finance, Enterprise Payment Services | DoorDash Pay and driver banking relationships. S-1 (2020) and 10-K filings. |
| Airbnb, Inc. | SEC-registered (NASDAQ: ABNB) | 1559720 | LOW | Enterprise Payment Services, FI Partnership | Cross-border payment and disbursement structures. S-1 (2020) and 10-K filings. |

---

## Category 5 — Crypto / Hybrid MSB Models

| Company | SEC Status | CIK | Priority | Target Archetypes | Notes |
|---|---|---|---|---|---|
| Coinbase Global, Inc. | SEC-registered (NASDAQ: COIN) | 1679788 | MEDIUM | FI Partnership, Cross-Border MSB, Enterprise Payment Services | Registered MSB. Bank partnerships for fiat on/off ramps. S-1 (2021 direct listing) and 10-K filings. Material agreements may include bank partnership and custodian agreements. |
| Robinhood Markets, Inc. | SEC-registered (NASDAQ: HOOD) | 1783879 | LOW | FI Partnership, Embedded Finance, Sponsor Bank | Robinhood Money (spending account) and Robinhood Gold Card involve banking partnerships. S-1 (2021) and 10-K filings. |

---

## Category 6 — Sponsor Banks / Issuing Banks (Elevated)

Sponsor banks are a distinct research target. Unlike fintech filers who disclose
their bank relationships from the program manager's perspective, sponsor banks
that are SEC-registered disclose these relationships from the bank's perspective.
This provides a different documentary angle on the same commercial structures.

Private sponsor banks (not SEC-registered) may still be relevant as counterparties
disclosed in fintech filers' agreements. They are tracked here for completeness.

### 6.1 Core U.S. Fintech Sponsor Banks

| Bank | SEC Status | CIK | Priority | Notes |
|---|---|---|---|---|
| Cross River Bank | Not SEC-registered (private NJ-chartered bank) | — | MEDIUM (via counterparties) | Major fintech sponsor bank (Affirm, Upgrade, Coinbase, others). Consent order with FDIC (2023) for fair lending — enforcement record is relevant to WS-B. Search counterparty SEC filings for Cross River relationship disclosures. |
| Sutton Bank | Not SEC-registered (private Ohio-chartered bank) | — | HIGH (via counterparties) | Primary issuing bank for Marqeta programs (Block Cash App Card, Square Debit Card) and others. Disclosed in Marqeta and Block 10-K filings (initial harvest done). |
| Evolve Bank & Trust | Not SEC-registered (private Arkansas state bank; OCC enforcement action 2024) | — | HIGH (via counterparties) | Major fintech BaaS bank. Consent order with Federal Reserve (June 2024) for AML/BSA failures — critical WS-B source. Search Stripe, Mercury, Synapse-adjacent counterparty filings. |
| The Bancorp Bank | SEC-registered via The Bancorp, Inc. (NASDAQ: TBBK) | 1359190 | HIGH | Major fintech prepaid and debit card sponsor bank (Chime, etc.). 10-K filings disclose program manager relationships from the bank's perspective. Primary sponsor bank with SEC disclosure. |
| Pathward Financial (formerly MetaBank / Meta Financial Group) | SEC-registered (NASDAQ: CASH) | 798354 | HIGH | Prepaid card sponsor bank and BaaS provider. Long SEC filing history as Meta Financial Group (prior to 2022 rebrand). EX-10 filings may disclose program manager agreements from bank's perspective. |

### 6.2 Secondary / Emerging Sponsor Banks

| Bank | SEC Status | CIK | Priority | Notes |
|---|---|---|---|---|
| Lincoln Savings Bank | Not SEC-registered (private Iowa state bank) | — | LOW (via counterparties) | Appears as sponsor bank in some fintech structures. No SEC filings. Track via counterparty disclosures. |
| Blue Ridge Bank | Was SEC-registered (NASDAQ: BRBS) through 2024; acquired by National Bankshares October 2024 | 835324 | MEDIUM (historical) | Filed 10-K through 2023. Had significant fintech BaaS partnerships (including Unit, Synctera). Fed consent order re: BSA/AML. Historical SEC filings are accessible for doctrine purposes. |
| First Electronic Bank | Not SEC-registered (Utah ILC; subsidiary of CardWorks) | — | LOW (via counterparties) | Utah ILC. Issues prepaid and credit cards. No SEC filings. Track via counterparty disclosures. |

### 6.3 Canadian / Cross-Border Adjacent

| Institution | SEC Status | CIK | Priority | Notes |
|---|---|---|---|---|
| Peoples Bank of Canada | Not SEC-registered (Schedule I Canadian bank) | — | LOW | Canadian sponsor bank context. No SEC filings. OSFI reporting. |
| Equitable Bank (EQB Inc.) | Not SEC-registered in US (TSX: EQB) | — | LOW | Canadian digital bank. TSX-listed. No US SEC filing. SEDAR+ filings are the source. |

---

## Research Status Summary

| Company | Status | Source | Output Location |
|---|---|---|---|
| Marqeta | Initial harvest complete (draft) | EX-10.21, EX-10.14 | WS_A/RESEARCH_2026-04-25_INITIAL_HARVEST.md |
| Adyen | No SEC filing confirmed | — | WS_A/RESEARCH_2026-04-25_INITIAL_HARVEST.md (noted) |
| Block | Partial (body text only) | 10-K FY2023 body | WS_A/RESEARCH_2026-04-25_INITIAL_HARVEST.md |
| PayPal | Partial (eBay OpAg; bank partnerships pending) | 8-K EX-10.1 (2015) | WS_A/RESEARCH_2026-04-25_INITIAL_HARVEST.md |
| All others | Not yet initiated | — | — |

---

## Priority Queue for Next Research Engagements

Recommended sequencing based on disclosure quality and archetype coverage gaps:

1. **The Bancorp, Inc. (TBBK)** — sponsor bank SEC filer; bank-side perspective on program manager agreements; fills sponsor bank archetype from the bank's disclosure angle
2. **Pathward Financial (CASH)** — sponsor bank SEC filer; same rationale; long prepaid card program history
3. **PayPal / eBay Operating Agreement** — complete the indemnification and liability extraction (403 error in initial session; retry)
4. **Synchrony Financial (CIK 1601712)** — PayPal credit program partner; may disclose PayPal bank partnership from Synchrony's perspective
5. **Green Dot Corporation (GDOT)** — dual sponsor bank and program manager; covers both sides of the relationship in a single filer
6. **Affirm Holdings (AFRM)** — BNPL; Cross River Bank relationship likely disclosed from Affirm's SEC filings

---

## Version History

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-04-25 | Initial universe defined in agent spec §4.1 and §4.2 (Marqeta primary; 11-company secondary list; no sponsor bank category) |
| 0.2 | 2026-04-25 | Expanded to 6 categories; sponsor banks elevated to standalone category; 40+ targets; research status and priority queue added |
