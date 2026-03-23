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
sources:
  - type: url
    citation: "Osler, Hoskin & Harcourt LLP — Canada's Crypto Realignment (2025)"
  - type: url
    citation: "Rotfleisch & Samulovitch via Global Law Experts"
  - type: url
    citation: "Carey Olsen — Introducing CARF"
  - type: url
    citation: "VG Law Firm — CARF for Founders, Investors and GC"
  - type: url
    citation: "Aurum Law — How OECD CARF Affects Your Project"
  - type: url
    citation: "PwC Ireland — Understanding CARF"
  - type: url
    citation: "International Tax Review — CARF Could Be Pivotal"
  - type: url
    citation: "TaxDo — CARF Canada Crypto-Asset Reporting 2026"
open_questions:
  - Exact penalty amounts under Canadian CARF legislation not yet finalized
  - Treatment of DeFi protocols under Canadian implementation — unclear
  - Whether Canadian CARF legislation will mirror OECD model rules exactly or diverge
  - TaxPage and CryptoTaxLawyer content not yet retrieved
next_actions:
  - Retry failed sources (TaxPage, CryptoTaxLawyer, OECD, Wikipedia)
  - Review draft Canadian CARF legislation (August 2025 release) directly
  - Validate penalty figures once legislation finalized
  - Consider promotion to 07_REFERENCE once ML1 reviews and content stabilizes
---

# CARF Research Synthesis — v0.1

> **Research grade — not approved. Not to be treated as authoritative.**
> Sources: 8 of 12 retrieved. See CARF-Source-Index for full source list and retrieval status.

---

## 1. What is CARF

The Crypto-Asset Reporting Framework (CARF) is an OECD standard for automatic
exchange of tax information on crypto-asset transactions. It is the crypto
equivalent of the Common Reporting Standard (CRS).

**CARF is not a licensing regime.** It is tax transparency infrastructure —
separate from AML/KYC, securities regulation, and money services business
requirements. Compliance with AML/PCMLTFA does not satisfy CARF obligations.

---

## 2. Entity Scope — Who Must Report

Obligated entities are **Reporting Crypto-Asset Service Providers (RCASPs)**:
entities that facilitate exchange transactions involving crypto-assets for customers.

**In scope:**
- Centralized exchanges
- Decentralized protocols / platforms with execution capability
- Brokers and dealers
- Custodial wallet providers
- Payment processors
- Crypto ATM operators

**Out of scope:**
- Price information platforms (CoinMarketCap, CoinGecko)
- Software developers
- Token issuers (unless reselling)
- Self-custody wallet providers
- Central bank digital currencies (CBDCs)
- Closed-loop crypto-assets
- Certain e-money products

**Nexus rule:** CARF applies to RCASPs that are tax-resident, incorporated,
managed from, or have a business presence in a CARF-adopting jurisdiction.
**Offshore incorporation does not provide shelter** — development teams, offices,
or tax registration in a signatory country is sufficient to trigger obligations.

**CARF is broader than FATF's VASP definition** — captures a wider range of
digital service operators (Carey Olsen).

---

## 3. Reportable Assets

**In scope:**
- Cryptocurrencies (Bitcoin, Ether, XRP, etc.)
- Stablecoins on distributed ledger technology
- Tradeable NFTs functioning as payment or investment assets
- Tokenized securities
- DeFi positions

**Out of scope:**
- CBDCs
- Closed-loop crypto-assets
- Purely collectible NFTs

---

## 4. Reportable Transactions

| Transaction Type | Threshold |
|-----------------|-----------|
| Crypto-to-fiat exchanges | All |
| Crypto-to-crypto exchanges | All |
| Transfers (internal vs external) | All |
| Transfers to unhosted/external wallets | All |
| Retail payment transactions (goods/services) | USD 50,000 per customer annually |
| Staking rewards and airdrops | All (per TaxDo) |

---

## 5. Due Diligence and Data Collection

RCASPs must identify whether users are **Reportable Persons** (tax-resident in
CARF-adopting jurisdictions) and collect:

- Full legal name
- Residential address
- Date of birth
- Jurisdiction(s) of tax residence
- Tax Identification Number(s) (TINs)
  - Where TINs unavailable: placeholder codes (e.g., "NOTIN") with documented reason
- For entities: controlling person details / beneficial ownership

**Self-certification requirement:**
- CARF requires **separate** tax residency self-certification
- Cannot rely exclusively on AML/KYC data — CARF has distinct data requirements
- For pre-existing users: 12 months from effective date to obtain certifications
- Updated certifications required within 90 days of circumstance changes
- **Absence of valid certification → restricted functionality or halted transactions**

---

## 6. Reporting Format and Technical Requirements

- Annual XML submissions using OECD prescribed XML schema
- Data aggregated per reportable user
- Report structure: message headers + organization/person party sections + transaction bodies
- Transaction bodies include: timestamps, wallet addresses, asset quantities, fiat equivalents
- Record retention: minimum **6 years** (Canadian standard per TaxDo)

---

## 7. Canadian Timeline

| Date | Event |
|------|-------|
| November 10, 2023 | Canada endorses CARF alongside 67 jurisdictions |
| August 2025 | Draft CARF legislation published by Canadian government |
| January 1, 2026 | Due diligence and data collection obligations commence |
| 2027 | First annual XML submissions to CRA covering 2026 transaction data |
| 2027–2028 | Cross-border automatic exchange via OECD network |

**Receiving authority in Canada:** CRA

---

## 8. Relationship to Other Regulatory Frameworks

| Framework | Relationship to CARF |
|-----------|---------------------|
| PCMLTFA / AML | Separate regime; partial data reuse possible but CARF requires distinct tax residency data and trigger logic |
| CRS (Common Reporting Standard) | CARF is the crypto extension of CRS; entities may be subject to both — dual reporting obligations possible (PwC) |
| RPAA | Separate regime; no direct overlap |
| FATF / VASP rules | CARF entity scope is broader than FATF VASP definition |
| US Section 6045 / Form 1099-DA | US parallel — US is NOT a CARF signatory but implementing equivalent domestically |

---

## 9. Global Adoption

- ~70 jurisdictions committed to CARF adoption
- First international data exchange: 2027 (based on 2026 data)
- EU implementation via DAC8
- US implementing parallel requirements under Section 6045 (not CARF signatory)
- UK, France, Canada, Singapore, Japan among signatories

---

## 10. Enforcement (Canada — Preliminary)

- Specific Canadian penalty amounts not yet finalized (draft legislation stage as of 2026-03)
- CRS analogue suggests penalties of up to $2,500 per offence for failure to verify account holders
- CRA enforcement tools include compound interest (5% daily) and criminal penalties up to 200% of unpaid taxes plus potential imprisonment for underlying tax evasion (Rotfleisch)

---

## 11. Relevance to LL Practice

CARF directly supports the **CARF_PROGRAM strategy** and the following solutions:

| CARF Component | Relevant LL Solution |
|---------------|---------------------|
| Governance | CARF_GOVERNANCE |
| Scoping and classification (entity and transaction scope) | CARF_SCOPING_AND_CLASSIFICATION |
| Self-certification at onboarding | CARF_CLIENT_ONBOARDING |
| Re-verification triggers | CARF_DUE_DILIGENCE |
| Transaction classification logic | CARF_TRANSACTION_CLASSIFICATION |
| XML reporting output | CARF_REPORTING_OUTPUT |
| 6-year record retention | CARF_RECORDKEEPING |
| AML/KYC data separation requirement | CARF_AML_INTEGRATION |
| Annual testing | CARF_CONTROLS_AND_TESTING |
| Documentation set | CARF_DOCUMENTATION |

Key practitioner point: CARF's requirement for **separate** tax residency data
distinct from AML/KYC data validates the CARF_AML_INTEGRATION component as a
non-trivial standalone engagement.
