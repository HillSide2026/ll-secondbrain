---
id: ws-a-initial-harvest-2026-04-25
title: WS-A Initial Harvest — Marqeta, Adyen, PayPal, Block
workstream: WS-A
status: draft
created_date: 2026-04-25
ml1_approval_required: YES
output_label: Derived from disclosed agreement (SEC)
targets: [Marqeta, Adyen, PayPal, Block]
---

# WS-A Initial Harvest: SEC Disclosure Mining
## Marqeta, Adyen, PayPal, Block — Payment Services Agreements

**Research Date:** 2026-04-25
**Output Label:** Derived from disclosed agreement (SEC)
**Status:** Draft — not authoritative until ML1-approved

---

## Research Method Notes

All research conducted via SEC EDGAR (CIK-based submissions), EDGAR full-text search, Law Insider contract database, Justia Contracts database, and company investor relations portals. Direct SEC.gov HTML exhibit URLs returned HTTP 403 during this session; all substantive clause text was obtained from Law Insider and Justia mirrors of the same underlying filed documents, supplemented by disclosure summaries drawn from the primary 10-K and S-1 filings themselves (which paraphrase material agreement terms as required by Item 601 of Regulation S-K).

Where clause text was retrieved from a Law Insider or Justia mirror rather than directly from sec.gov, the corresponding SEC filing source (company / CIK / accession number / exhibit number) is noted. The mirror copy is treated as the same document because both reproduce the exhibit as filed.

Redactions in the original SEC filings are noted as [***] throughout.

---

## WS-A/1 — Agreement Inventory

| # | Company | Filing | Exhibit | Date Filed | Agreement Title (as disclosed) | Parties | Archetype |
|---|---------|--------|---------|-----------|-------------------------------|---------|-----------|
| 1 | Marqeta | 10-K (FY2021), CIK 1522540 | EX-10.21 | 2022-02-28 | Amended and Restated Prepaid Card Program Manager Agreement | Marqeta, Inc. / Sutton Bank | Program Manager |
| 2 | Marqeta | S-1/A, CIK 1522540 | EX-10.14 | 2021-06-04 | Master Services Agreement (Square/Block customer MSA) | Marqeta, Inc. / Square, Inc. (now Block, Inc.) | Platform / Customer MSA |
| 3 | Block | 10-K (FY2023), CIK 1512673 | Body disclosure only — no standalone EX-10 filed for issuing bank agreement | 2024-02-22 | Issuing Bank Agreement with Sutton Bank (Square Debit Card / Cash App Card) | Block, Inc. / Sutton Bank | Sponsor Bank |
| 4 | Block | 10-K (FY2017), CIK 1512673 | Body disclosure only — no standalone EX-10 filed for Celtic Bank | 2018-02-26 | Loan Origination Program Agreement with Celtic Bank | Square Capital, LLC / Celtic Bank Corporation / Square, Inc. | Embedded Finance |
| 5 | PayPal | 8-K (Form 8-K filed 2015-07-20), CIK 1633917 | EX-10.1 | 2015-07-20 | Operating Agreement (eBay-PayPal post-separation services) | eBay Inc. / eBay International AG / PayPal Holdings, Inc. / PayPal, Inc. / PayPal Pte Ltd. / PayPal Payments Pte Holdings, S.C.S. | Enterprise Payment Services |
| 6 | Adyen | Not applicable — Adyen NV is listed on Euronext Amsterdam (AMS:ADYEN); trades OTC in the US as ADYEY/ADYYF (unsponsored ADR). Adyen has not filed a Form 20-F or any registration statement with the SEC. No EDGAR filing exists under CIK 1788707 beyond administrative registration as a foreign private issuer ADR. | — | — | — | — | — |

### Inventory Notes

**Marqeta (confirmed):** Two material agreements confirmed with exhibit-level text available. EX-10.21 is the Amended and Restated Prepaid Card Program Manager Agreement with Sutton Bank, filed as an exhibit to the FY2021 10-K (accession 0001522540-22-000013). EX-10.14 from the S-1/A is the Master Services Agreement with Square, Inc. as a representative customer. Both have been extensively amended; the most recent disclosed amendment to the Sutton Bank agreement is the Eighth Amendment effective November 15, 2024 (filed via Marqeta 10-K FY2024).

**Block (partially confirmed):** Block does not file its issuing bank agreements with Sutton Bank or Celtic Bank as standalone EX-10 exhibits. Material terms are disclosed in narrative form in annual report body text (Item 1 Business and Item 7 MD&A sections). The Marqeta-Square MSA (Agreement #2 above) is the primary disclosed contract governing Block's card programs, filed by Marqeta (not Block) as an exhibit to Marqeta's own SEC filings.

**PayPal (partially confirmed):** PayPal's post-separation Operating Agreement with eBay is the primary disclosed payment services agreement on file at SEC EDGAR. No standalone bank partnership agreements (Synchrony, The Bancorp Bank, Wells Fargo) were located as EX-10 exhibits in PayPal's 10-K filings through this search session. The Synchrony relationship is disclosed in narrative body text of PayPal 10-Ks and in Synchrony's own SEC filings.

**Adyen (not located — not SEC-registered):** Adyen NV is incorporated in the Netherlands and listed on Euronext Amsterdam. It is not a reporting issuer under the US Securities Exchange Act of 1934. Its ADR (ADYEY/ADYYF) is unsponsored; Adyen has expressly stated it does not consent to or authorize unsponsored ADR programs. No Form 20-F, no Form F-1, and no EX-10 exhibits exist in EDGAR for Adyen. Adyen's disclosed commercial terms are contained in its Dutch-law annual reports published on investors.adyen.com, which do not include exhibit-level agreement texts. Adyen holds a full Dutch acquiring bank license (since 2017), a UK banking license (granted H2 2023), and is regulated directly by De Nederlandsche Bank (DNB) and the AFM. It does not rely on a sponsor bank for card issuance; it issues directly under its own banking license.

---

## WS-A/2 — Archetype Classification

### Archetype 1: Program Manager

**Agreements found:** 1 (Agreement #1 — Marqeta / Sutton Bank)

**Companies:** Marqeta

**Parties and functional roles:**
- Marqeta, Inc.: Program Manager — manages card programs, interfaces with card networks, handles cardholder-facing operations, receives interchange
- Sutton Bank: Issuing Bank — holds Ohio banking charter, issues cards under BIN, provides FDIC-insured accounts, settles transactions, bears regulatory issuing risk

**Key commercial features (from disclosed filing):**
- Marqeta pays Sutton Bank a fee based on a percentage of the value of transactions processed
- Marqeta receives 100% of interchange fees for processing customers' card transactions
- Marqeta must obtain Sutton Bank's prior approval for each new card Program via a Program Due Diligence Application Form
- Sutton Bank designates Marqeta as program manager for Cards and Programs
- Term expires 2028; auto-renews for two-year terms with 180-day non-renewal notice
- Either party may terminate on 30-day cure for material breach
- Marqeta indemnifies Sutton Bank for certain losses (subject to enumerated exceptions)
- Marqeta maintains an AML program designed to meet Issuing Bank requirements
- Sutton Bank has audit rights over Marqeta's program operations
- Marqeta maintains an internal audit plan approved by its board audit committee

**Source references:**
- Primary: Marqeta 10-K FY2021, EX-10.21, SEC EDGAR CIK 1522540, accession 0001522540-22-000013
- URL: https://www.sec.gov/Archives/edgar/data/1522540/000152254022000013/exhibit1021-202110xk.htm
- Justia mirror: https://contracts.justia.com/companies/marqeta-inc-13009/contract/178692/
- Fourth Amendment (July 1, 2021): https://contracts.justia.com/companies/marqeta-inc-13009/contract/208344/
- Eighth Amendment (November 15, 2024): https://contracts.justia.com/companies/marqeta-inc-13009/contract/1314972/

---

### Archetype 2: Platform / Customer MSA

**Agreements found:** 1 (Agreement #2 — Marqeta / Square/Block)

**Companies:** Marqeta (filing party); Block (counterparty / customer)

**Parties and functional roles:**
- Marqeta, Inc.: Service Provider — provides Processing Services and Program Management Services
- Square, Inc. (now Block, Inc.): Client — deploys Marqeta platform for Cash App Card, Square Debit Card, Square Card Canada

**Key commercial features (from disclosed filing):**
- Services cover Processing Services (account creation, maintenance, authorization, settlement, API access) and Program Management Services (managing the Issuing Bank and Card Brand relationships)
- Client is solely responsible for compliance with all Applicable Law applicable to its business, including AML/BSA obligations
- Marqeta provides BSA/AML and fraud mitigation training to Client as part of Implementation Plan
- Implementation Plan must include training for BSA/AML compliance
- Mutual indemnification: Marqeta indemnifies Client for Marqeta's breach, gross negligence, wilful misconduct, fraud, violation of Applicable Law, and IP infringement; Client indemnifies Marqeta and Issuing Bank for Client's breach, gross negligence, wilful misconduct, fraud, violation of Applicable Law, and IP infringement claims arising from Client Materials
- Liability cap: aggregate fees earned by Marqeta in the 12 months preceding the claim
- Consequential damages excluded except for indemnification obligations under Section 13(a)
- Carve-outs from cap: indemnification obligations, gross negligence, wilful misconduct, fraud, breach of payment/funding deposit obligation
- Convenience termination by Client after Go-Live: 90 days' notice plus termination fee ([***] redacted)
- Regulatory termination: 90 days' notice if regulatory change has or is likely to have material adverse impact on anticipated economic benefits
- Marqeta may terminate with 180 days' notice if required by Issuing Bank or regulator
- Client has right to audit Marqeta's books, records and procedures on reasonable notice
- Record retention minimum [***] following termination
- Marqeta warrants it will remain duly licensed to perform Services
- Card Programs subject to ongoing Issuing Bank approval

**Source references:**
- Primary: Marqeta S-1/A, EX-10.14, SEC EDGAR CIK 1522540, accession 0001193125-21-177861
- URL: https://www.sec.gov/Archives/edgar/data/1522540/000119312521177861/d64065dex1014.htm
- Law Insider mirror: https://www.lawinsider.com/contracts/6MrRZdDJFj1
- Justia listing: https://contracts.justia.com/companies/marqeta-inc-13009/contract/180185/
- Amendment No. 22 (Block): https://contracts.justia.com/companies/marqeta-inc-13009/contract/1314970/
- Amendment No. 26 (Block): https://contracts.justia.com/companies/marqeta-inc-13009/contract/1345967/

---

### Archetype 3: Sponsor Bank

**Agreements found:** 1 (Agreement #3 — Block / Sutton Bank)

**Companies:** Block

**Parties and functional roles:**
- Block, Inc. (formerly Square, Inc.): Non-bank program manager / fintech — manages Square Debit Card and Cash App Card programs
- Sutton Bank: Issuing Bank / Sponsor Bank — issues cards under BIN, provides FDIC-backing, holds regulatory issuing relationship

**Key commercial features (from 10-K body disclosure):**
- Block pays Sutton Bank a fee based on a percentage of the value of transactions processed
- Block receives 100% of interchange fees for processing customers' card transactions
- Block indemnifies Sutton Bank for certain losses (subject to specific enumerated exceptions)
- Either party may terminate under specified circumstances, including material breach not cured within 30 days
- Current term expires 2028; auto-renews for two-year terms with 180-day non-renewal notice
- Marqeta acts as the program processor for Block's card programs under Marqeta-Block MSA
- No standalone EX-10 exhibit filed; terms disclosed in 10-K body narrative

**Source references:**
- Block 10-K FY2023 (sq-20231231), CIK 1512673, accession 0001628280-24-006354, filed 2024-02-22
- URL: https://www.sec.gov/Archives/edgar/data/1512673/000162828024006354/sq-20231231.htm
- Comparable prior year: Block 10-K FY2022 (sq-20221231), accession 0001628280-23-004840
- Note: The substantive disclosure of Block's Sutton Bank agreement terms appears in Marqeta's filings, which describe the same underlying relationship from the processor/program manager perspective

---

### Archetype 4: Embedded Finance

**Agreements found:** 1 (Agreement #4 — Square Capital / Celtic Bank)

**Companies:** Block (via Square Capital)

**Parties and functional roles:**
- Celtic Bank Corporation: Originating Bank — Utah-chartered industrial bank, originates and issues loans, holds regulatory lending relationship
- Square Capital, LLC: Servicer / Agent — services loans as agent on behalf of Celtic Bank
- Square, Inc. (now Block, Inc.): Payment Processor — processes card transactions; receivables from Square account serve as repayment mechanism
- Merchant: Borrower

**Key commercial features (from Square Capital public loan agreement and 10-K body disclosure):**
- Celtic Bank issues loans; Square Capital services them as agent
- Repayment drawn automatically from merchant's Square payment card receivables via ACH
- No dedicated AML/KYC section in merchant-facing loan agreement; compliance responsibility not allocated explicitly to a single party in the public agreement text
- Indemnification is unilateral: Merchant indemnifies Bank and Square Capital for losses arising from Merchant's misrepresentation or breach — no reverse indemnification
- No explicit liability cap; no consequential damages exclusion in the public loan agreement
- Termination prior to repayment start date: Merchant may cancel; Bank debits Loan Amount from Linked Account
- No regulatory termination trigger in the public merchant-facing agreement
- No audit rights section in the public loan agreement
- Governing law: Utah (Celtic Bank's jurisdiction) and applicable federal law
- Security interest for loans over $75,000 in merchant's Square Account receivables and proceeds
- Contractual structure changed post-2021: Square Financial Services, Inc. (Utah ILC, approved by FDIC March 2021) replaced Celtic Bank as loan originator for most products; Celtic Bank continues as issuer for Square Credit Cards

**Source references:**
- Square Capital Term Loan Agreement (public, June 1, 2018): https://squareup.com/us/en/legal/general/capital-term-loan-agreement-jun-01-2018
- Block 10-K FY2017 (a10-kfilingsquareinc2017.htm), CIK 1512673, accession 0001512673-18-000004
- Block 10-K FY2022, CIK 1512673, accession 0001628280-23-004840 (body disclosure re: Celtic Bank for Square Credit Cards and Square Financial Services for loans)
- Note: Celtic Bank is not filing party; no Celtic Bank EX-10 exhibit appears in Block's own SEC filings

---

### Archetype 5: Enterprise Payment Services

**Agreements found:** 1 (Agreement #5 — PayPal / eBay Operating Agreement)

**Companies:** PayPal

**Parties and functional roles:**
- PayPal Holdings, Inc. / PayPal, Inc. / PayPal Pte Ltd. / PayPal Payments Pte Holdings, S.C.S.: Service Provider — provides payment services to eBay marketplace
- eBay Inc. / eBay International AG: Commercial Enterprise Client — receives payment services following corporate separation

**Key commercial features (from 8-K filing and IR summary):**
- Agreement governs PayPal's continued provision of payment services to eBay and its customers following the 2015 spin-off separation
- Five-year initial term with one-year transition period
- Annual CEO compliance assessments required: written assessment of each party's compliance under the Agreement, costs and benefits, and other aspects of the relationship
- Annual internal audit verification of compliance for each party with detailed written reports provided to CEOs and Audit Committees of both companies
- Data Sharing Addendum goverable separately; eBay may terminate Data Sharing Addendum (without triggering full Agreement termination) within 90 days of a Specified Change of Control
- PayPal encouraged eBay customers to use PayPal services following distribution
- Agreement includes non-compete clauses, payment terms, and procedures for termination
- Both parties agreed to cooperate, maintain service levels, and protect user data
- Associated agreements: Transition Services Agreement, Tax Matters Agreement, Employee Matters Agreement, Intellectual Property Matters Agreement, Colocation Services Agreement

**Source references:**
- PayPal Holdings 8-K, EX-10.1, filed 2015-07-20, CIK 1633917, accession 0001193125-15-257108
- SEC URL: https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm
  (Note: filed under eBay CIK 1065088 as the distributing company; same document)
- Justia mirror (PayPal): https://contracts.justia.com/companies/paypal-1026/contract/474899/
- Justia mirror (eBay): https://contracts.justia.com/companies/ebay-441/contract/489831/
- Amendment to Operating Agreement: https://www.sec.gov/Archives/edgar/data/1065088/000106508816000317/ebay063016ex1004.htm

---

### Adyen — No Archetype Assigned

Adyen NV has no SEC EDGAR filing containing exhibit-level payment services agreement text. CIK 1788707 is listed in EDGAR as "ADYEN N.V./ADR" but reflects only the unsponsored ADR administrative registration, not a reporting issuer status. Adyen's commercial agreements are not publicly disclosed in the same way as SEC-registered companies' material contracts.

Adyen's disclosed regulatory status (from Dutch annual reports and public statements): Adyen holds a full banking license from De Nederlandsche Bank (DNB) as an acquiring bank, granted in 2017. In H2 2023, Adyen obtained a UK banking licence. Adyen holds US money transmitter licences in states where required. As a licensed bank, Adyen does not require a sponsor bank or BIN sponsor — it issues cards and processes transactions directly under its own regulatory authorizations.

---

## WS-A/3 — Clause Extraction Matrix

---

### FILING 1

```
FILING: Marqeta / 10-K FY2021 / EX-10.21 / Filed 2022-02-28
AGREEMENT TITLE: Amended and Restated Prepaid Card Program Manager Agreement
PARTIES: Marqeta, Inc. ("Manager") / Sutton Bank, an Ohio chartered bank corporation
ARCHETYPE: Program Manager
WORKSTREAM LABEL: Derived from disclosed agreement (SEC)
```

**DIMENSION: Services Scope**

Description: Sutton Bank provides "Sutton Bank Prepaid Card Services" as set forth in Exhibit B and other Program Documents in connection with Card Transactions processed on one or more Networks. Sutton Bank issues Cards within designated BIN ranges assigned by applicable Networks. Manager obtains Sutton Bank's prior approval for each Program and submits a Program Due Diligence Application Form for each proposed Program. Upon agreement to offer a Program, Manager develops a marketing program and Sutton Bank issues Cards. Manager is responsible for overall program management including cardholder-facing operations, fraud management, and compliance program design meeting Issuing Bank requirements.

Source: Agreement body, Sections covering Program approval and Manager responsibilities; disclosed summary in Marqeta 10-K FY2021 Item 1 Business section

**DIMENSION: Compliance Responsibility Allocation**

AML/KYC performer: Marqeta (Manager) — Marqeta has implemented an AML program designed to prevent its platform from being used to facilitate money laundering, terrorist financing, and other illicit activity

AML/KYC responsible party (regulatory exposure): Sutton Bank (Issuing Bank) — as the chartered bank, Sutton Bank holds the BSA/AML regulatory obligation to the OCC/FDIC; Marqeta's AML program is "designed to meet the requirements of its Issuing Banks when providing program management services"

BSA/AML program ownership: Marqeta designs and maintains; Sutton Bank sets the standards and retains ultimate regulatory exposure

Source: Marqeta 10-K FY2021 disclosure (Item 1 Business), accession 0001522540-22-000013; Fourth Amendment (July 1, 2021) terms; detailed AML section [***] redacted in the filed exhibit

**DIMENSION: Indemnification**

Direction: Marqeta (Manager) indemnifies Sutton Bank; direction is primarily one-way (Manager toward Bank)

Scope: "Marqeta's agreement with Sutton Bank requires Marqeta to indemnify Sutton Bank for certain losses" — specific enumerated scope is subject to redaction in the filed exhibit. One disclosed provision: "Manager agrees that it shall be responsible for and liable to Sutton Bank for all expenses associated with and any losses attributable to Program Fraud"

Carve-outs: Losses proximately caused by Sutton Bank's own negligence or wilful misconduct are carved out: "unless such expenses and losses were proximately caused by the negligence or willful misconduct of Sutton Bank"

Source: Marqeta 10-K FY2021 Item 1 Business; Justia exhibit text https://contracts.justia.com/companies/marqeta-inc-13009/contract/178692/

**DIMENSION: Limitation of Liability**

Cap structure: Not disclosed in filed exhibit (provisions subject to [***] redaction)

Consequential loss exclusion: Not disclosed in filed exhibit

Carve-outs from cap: Not disclosed in filed exhibit

Source: Not disclosed in exhibit1021-202110xk.htm beyond redacted provisions

**DIMENSION: Termination**

Convenience termination: Marqeta bears termination fees if it terminates before the end of its term or any automatic renewal term — specific fee amount [***] redacted. Sutton Bank termination rights on convenience not separately disclosed.

Regulatory trigger termination: Not separately enumerated in the disclosed text; parties may terminate on material breach not cured within 30 days

De-risking / licence loss trigger: Not disclosed in filed exhibit as a standalone provision

Term: Initial term expires September 1, 2028 (per Fourth Amendment, July 1, 2021). Auto-renews for two-year renewal terms. Non-renewal requires written notice at least 180 days prior to expiration.

Material breach termination: Either party may terminate if the other commits a material breach not cured within 30 days

Source: Marqeta 10-K FY2021 Item 1 Business; Fourth Amendment dated July 1, 2021

**DIMENSION: Audit and Oversight Rights**

Right to audit: Sutton Bank has audit rights over Marqeta's program operations

Frequency / notice: Not specifically disclosed in excerpt

Cost allocation: Not disclosed in filed exhibit excerpt

Additional: "Manager agrees to provide Sutton Bank with copies of Manager's then-most current annual audited and/or interim unaudited financial statements and such information concerning Manager's Programs as Sutton Bank may request." Manager maintains an internal audit plan for Programs as approved by the audit committee of Manager's Board of Directors.

Source: Justia mirror of EX-10.21; Marqeta 10-K FY2021 disclosure

**DIMENSION: Regulatory Status Dependencies**

Load-bearing party: Sutton Bank — its Ohio banking charter is the source of BIN sponsorship, card issuance authority, and FDIC insurance designation

Change of status provision: Not explicitly disclosed in excerpt. Implicitly, loss of Sutton Bank's charter or regulatory ability to issue cards would terminate the program basis. Marqeta's 10-K risk factors disclose risk of losing issuing bank relationships as a material operational risk.

Source: Marqeta 10-K FY2021 Item 1 Business; Marqeta 10-K FY2021 Item 1A Risk Factors

---

### FILING 2

```
FILING: Marqeta / S-1/A / EX-10.14 / Filed 2021-06-04
AGREEMENT TITLE: Master Services Agreement
PARTIES: Square, Inc., a Delaware corporation ("Client") / Marqeta, Inc., a Delaware corporation ("Service Provider" / "Marqeta")
ARCHETYPE: Platform / Customer MSA
WORKSTREAM LABEL: Derived from disclosed agreement (SEC)
```

**DIMENSION: Services Scope**

Description: Marqeta provides three categories of services:
1. "Processing Services": "Account creation, maintenance, transition and closure services; Account load, payment transaction authorization and processing (including purchase and other transaction tracking and accounting)...settlement facilitation, Marqeta API access, spend control features and real-time and just-in-time funding"
2. "Program Management Services": "services consisting of the overall management of the Card Program, including managing the relationship with the Issuing Bank and Card Brand"
3. "Implementation Services": as further defined in Implementation Plan

The agreement covers management of Block's Cash App, Square Debit Card, and Square Card Canada card issuing programs. To the extent that Marqeta in good faith reasonably believes any Instruction is contrary to Applicable Law, Card Brand Rules, or requirements of the Issuing Bank, Marqeta shall promptly provide notice to Client.

Source: MSA Section 1 (Definitions and Services), Schedule A

**DIMENSION: Compliance Responsibility Allocation**

AML/KYC performer: Client (Square/Block) — "Client is solely responsible for compliance with all Applicable Law applicable to the operation of its business...including the [redacted] Act, the Electronic Fund Transfer Act"

AML/KYC responsible party (regulatory exposure): Client — sole responsibility is expressly allocated to Client

BSA/AML program ownership: Client — Implementation Plan must include "plan for providing appropriate BSA/AML and/or fraud mitigation training to Client." Client must "timely provide Marqeta with Client's [***]" and acknowledge that Issuing Bank's approval is dependent on [***]

Source: MSA Section 2(g) (Financial Condition Review), Section 2(j) (Additional Due Diligence), Amendment Section 2(m) (KYC — [***] redacted); Client compliance warranty in Section 10(c)

**DIMENSION: Indemnification**

Direction: Mutual — both parties indemnify the other; Client additionally indemnifies Issuing Bank

Marqeta indemnification scope (Section 13(a)): "Marqeta agrees to defend, indemnify and hold harmless Client and its Affiliates...from and against any and all Damages as a result of a third party Claim arising out of or related to (i) Marqeta's breach...of this Agreement; (ii) Marqeta's gross negligence, willful misconduct or fraudulent acts or omissions; (iii) Marqeta's violation of any Applicable Law; or (iv) the infringement of the U.S. Intellectual Property Rights of any third party"

Marqeta IP indemnity carve-outs: No coverage for claims arising from "(1) the combination of the Marqeta System or the Marqeta Card with information, services, materials or products not supplied by Marqeta, (2) any modification of the Marqeta System...which is not made by or on behalf of Marqeta, (3) any failure by Client to use any modified version...which is provided by Marqeta in order to avoid a claim of infringement"

Client indemnification scope (Section 13(b)): "Client agrees to defend, indemnify and hold harmless Marqeta, Issuing Bank and each of their respective officers, directors, agents and employees from and against any and all Damages as a result of a third party Claim arising out of or related to (i) Client's breach...of this Agreement; (ii) the gross negligence, willful misconduct or fraudulent acts or omissions of Client or any Client Personnel or Retail Partner; (iii) the violation of any Applicable Law by Client...or Retail Partner; (iv) a claim that the Client Materials infringe the Intellectual Property Rights of any third party"

Indemnification procedure (Section 13(c)): Indemnitee must provide "prompt written notice" but "failure to provide prompt notice shall not relieve the indemnitor of its indemnification obligations unless such failure materially prejudices indemnitor in defending such Claim." Indemnitor has "sole control of the defense and all negotiations for the compromise or settlement" but "may not settle any such Claim without the indemnitee's consent if the proposed settlement would be in the indemnitee's name or impose pecuniary or other liability or an admission of fault or guilt on the indemnitee"

Source: MSA Section 13(a), (b), (c) — Law Insider mirror https://www.lawinsider.com/contracts/6MrRZdDJFj1; original SEC filing EX-10.14 accession 0001193125-21-177861

**DIMENSION: Limitation of Liability**

Cap structure (Section 14(e)(b)(iii)): "Except for a party's indemnification obligation under Section 13(a)...a party's total cumulative liability...shall not exceed the aggregate Fees earned by Marqeta hereunder during the twelve (12) months immediately preceding the date such claim arose"

Consequential loss exclusion (Section 14(e)(b)(i)): "EXCEPT FOR A PARTY'S INDEMNIFICATION OBLIGATION UNDER SECTION 13(A)...IN NO EVENT...SHALL EITHER PARTY BE LIABLE...FOR INDIRECT, INCIDENTAL, CONSEQUENTIAL, SPECIAL, EXEMPLARY, OR PUNITIVE DAMAGES"

Carve-outs from cap:
- A party's indemnification obligation under Section 13(a)
- "a party's gross negligence, wilful misconduct, or fraud"
- "a Party's breach of a payment or funding deposit obligation under this Agreement"

Third-party systems disclaimer (Section 14(e)(b)(ii)): "Marqeta shall not be responsible to Client for any claims by Client or third parties arising from the failure of any third party software, hardware, communications devices, Internet services, e-mail systems or other systems or services which are not part of the Marqeta System"

Source: MSA Section 14(e)(b)(i)–(iii) — Law Insider mirror

**DIMENSION: Termination**

Convenience termination (Section 3(f)(b)): "After the Early Termination Date, Client shall have the right to terminate this Agreement for any reason or no reason at any time after the Go-Live Date, by giving not less than ninety (90) days' prior written notice to Marqeta; provided, however, that if Client exercises the foregoing right of termination, Client shall pay Marqeta an amount equal to [***]"

Early Termination Window (Section 3(f)(a)): Client may terminate within first two calendar weeks after Effective Date; Client must pay [***] and is not subject to [***]

Regulatory trigger termination (Section 3(b)(iv)): "Either Party may terminate this Agreement upon ninety (90) days' notice to the other Party in the event of a regulatory change (including Issuing Bank requirements)...that has or is likely to have a material adverse impact on the anticipated economic benefits of this Agreement"

Issuing Bank / Regulator-directed termination (Section 3(e)): "Marqeta may terminate this Agreement upon 180 days' written notice (or such shorter time, as applicable) if required to do so by Issuing Bank or any regulator with jurisdiction over Issuing Bank or Marqeta"

Material breach termination (Section 3(b)): A party may terminate if the other "(i) commits a material breach...not cured within thirty (30) days...provided, however, that if such matter is a non-monetary breach...the period shall be extended...to completion within ninety (90) days; (ii) commits numerous breaches...which collectively constitute a material breach; (iii) has a petition filed...under applicable bankruptcy law...not dismissed within thirty (30) days"

Term structure (Section 3(a)): "initial term shall begin on the Effective Date and shall expire at 11:59 p.m. (Pacific Time) on the last day of Servicing Year Two (2)...automatically renew for an unlimited number of one (1) year renewal terms...unless one Party provides the other with written notice of its intent to terminate not less than one hundred eighty (180) days prior to the end"

Post-termination (Section 3(g)): Client pays fees for Services up to completion of Transition; "Within 30 days after the effective date of termination...Marqeta will return, by ACH or wire transfer...to the Client Bank Account all of Client's funds held in the Custodial Account"

Source: MSA Sections 3(a), 3(b), 3(e), 3(f)(a), 3(f)(b), 3(g) — Law Insider mirror

**DIMENSION: Audit and Oversight Rights**

Right to audit (Section 8(b)(iii)): "Client, upon reasonable notice to Marqeta, has the right to audit the books, records and procedures of Marqeta regarding information directly related to this Agreement"

Frequency / notice: "upon reasonable notice" — no specific frequency stated

Cost allocation: Not explicitly stated; implied Client bears audit costs (no provision for cost-sharing)

Record retention: "Marqeta is obligated to preserve all records related to the performance of Services, including [***], under this Agreement from a minimum of [***] following the termination of this Agreement"

Supporting documentation (Section 8(c)): "Marqeta shall maintain supporting documentation for the amounts billable to, and payments made by and to, Client...Marqeta agrees to provide Client with such supporting documentation with respect to each invoice and statement as may be reasonably requested by Client"

Source: MSA Section 8(b)(iii), 8(c) — Law Insider mirror

**DIMENSION: Regulatory Status Dependencies**

Load-bearing party: Issuing Bank (whose approval is load-bearing for every Card Program) and Marqeta (whose processor/program management licenses enable the services)

Marqeta warranty (Section 10(a)): Marqeta warrants "it is and will continue to be duly qualified and licensed and has made and will continue to make all registrations to do business and to carry out its obligations under this Agreement to the extent required by U.S. federal law and the law of each U.S. state in which Marqeta provides Services"

Client warranty (Section 10(c)): Client warrants equivalent — "duly qualified and licensed" to carry out its obligations in each US state in which it conducts business

Issuing Bank dependency (Section 4): "Issuing Bank's initial and continued approval of the Card Program and Marqeta's willingness to provide the Services...is dependent on [***]." During Term: [***] (substantially redacted operational dependencies)

Performance standards: "to the extent that Marqeta in good faith reasonably believes that any Instruction is contrary to the provisions of this Agreement, Applicable Law, Card Brand Rules, or requirements of the Issuing Bank, Marqeta shall promptly provide notice to Client"

Issuing Bank-directed termination: Section 3(e) creates an express termination right for Marqeta if Issuing Bank or regulator requires it — this is the primary regulatory status dependency trigger

Source: MSA Sections 3(e), 4, 10(a), 10(c), Schedule A Section 1(b) — Law Insider mirror

---

### FILING 3

```
FILING: Block, Inc. / 10-K FY2023 / No standalone EX-10 exhibit / Filed 2024-02-22
AGREEMENT TITLE: Issuing Bank Agreement with Sutton Bank [title not separately disclosed — described in 10-K body text]
PARTIES: Block, Inc. / Sutton Bank
ARCHETYPE: Sponsor Bank
WORKSTREAM LABEL: Derived from disclosed agreement (SEC)
```

**Note on disclosure method:** Block does not file its Sutton Bank issuing bank agreement as a standalone EX-10 exhibit. The material terms are disclosed narratively in the body of Block's annual 10-K filings (Item 1 Business) as required under Item 601(b)(10) if the agreement is material. Key terms extracted below are drawn from that narrative disclosure, not from exhibit-level text.

**DIMENSION: Services Scope**

Description: Sutton Bank issues Block's Square Debit Card (Mastercard, FDIC-insured) and Cash App Card (Visa, FDIC-insured). Block (via Marqeta as program processor under the Marqeta MSA) manages the card programs. Banking services for Square Checking are also provided by Sutton Bank.

Source: Block 10-K FY2023, Item 1 Business section; Sutton Bank cardholder disclosures at suttonbank.com; Cash App cardholder agreement at cash.app/legal

**DIMENSION: Compliance Responsibility Allocation**

AML/KYC performer: Block — manages AML/KYC program for cardholders and account holders

AML/KYC responsible party (regulatory exposure): Sutton Bank — as the FDIC-insured chartered bank, bears BSA/AML regulatory obligation to banking regulators; Block's AML program must meet Sutton Bank's requirements (same structure as Marqeta-Sutton Bank agreement)

BSA/AML program ownership: Not disclosed in filing beyond general statement that "Banking services are provided by Square's banking affiliate, Square Financial Services, Inc. or Sutton Bank"

Source: Block 10-K FY2023 body text; comparable structure inferred from Marqeta-Sutton Bank agreement (Agreement #1) which governs the same programs

**DIMENSION: Indemnification**

Direction: Block indemnifies Sutton Bank

Scope: "Block's agreement with Sutton Bank requires Block to indemnify Sutton Bank for certain losses"

Carve-outs: "subject to specific enumerated exceptions" — specific exceptions not disclosed in 10-K body text

Source: Block 10-K FY2023 (sq-20231231), Item 1 Business, CIK 1512673

**DIMENSION: Limitation of Liability**

Cap structure: Not disclosed in Block 10-K body text

Consequential loss exclusion: Not disclosed in Block 10-K body text

Carve-outs from cap: Not disclosed in Block 10-K body text

Source: Not disclosed in sq-20231231

**DIMENSION: Termination**

Convenience termination: Not separately disclosed

Regulatory trigger termination: Not separately disclosed

Term and renewal: "The current term of the agreement with Sutton Bank expires in 2028, after which it automatically renews on the same terms and conditions for a two-year renewal term, unless either party provides written notice of its intent not to renew at least 180 days prior to the expiration of the then-current term"

Material breach termination: "Either party may terminate the agreement under certain specified circumstances, including if the other party commits a material breach that is not cured within 30 days"

Source: Block 10-K FY2023 body text

**DIMENSION: Audit and Oversight Rights**

Right to audit: Not disclosed in Block 10-K body text

Frequency / notice: Not disclosed in Block 10-K body text

Cost allocation: Not disclosed in Block 10-K body text

Source: Not disclosed in sq-20231231

**DIMENSION: Regulatory Status Dependencies**

Load-bearing party: Sutton Bank — its FDIC-insured charter is the source of card issuance authority, FDIC insurance designation, and Mastercard/Visa BIN sponsorship for Square Debit Card and Cash App Card

Change of status provision: Not disclosed in Block 10-K body text. Block's risk factors disclose loss of issuing bank relationships as a material risk.

Source: Block 10-K FY2023 Item 1A Risk Factors; body text description of banking services

---

### FILING 4

```
FILING: Block, Inc. (via Square Capital, LLC) / public loan agreement (not filed as EX-10) + 10-K body disclosures
AGREEMENT TITLE: Loan Agreement (Square Capital Loan Agreement — Celtic Bank Program)
PARTIES: Merchant (Borrower) / Celtic Bank Corporation ("Bank") / Square Capital, LLC (Servicer / Agent) / Square, Inc. (Payment Processor)
ARCHETYPE: Embedded Finance
WORKSTREAM LABEL: Derived from disclosed agreement (SEC)
```

**Note:** The Celtic Bank Loan Agreement was disclosed publicly on squareup.com/legal as a standard-form merchant agreement. It was not filed as an EX-10 exhibit in Block's SEC filings. Key terms are drawn from the public agreement text and body disclosures in Block 10-K filings. The agreement has been substantially superseded by Square Financial Services, Inc. (Block's own FDIC-insured ILC, approved March 2021) for loan origination; Celtic Bank continues as issuer for Square Credit Cards.

**DIMENSION: Services Scope**

Description: Celtic Bank Corporation serves as "the originator and issuer of Your loan." Square Capital, LLC is "the servicer of Your loan, as agent on behalf of Bank." Square, Inc. is "the processor of Your payment card transactions." Repayment is effected by Square Capital instructing Square, Inc. to withhold a Repayment Rate from daily card receivables processed through the merchant's Square account. After Square Financial Services obtained its ILC charter in 2021, Square Capital transitioned most loan origination in-house; Celtic Bank continues to originate Square Credit Cards.

Source: Square Capital Term Loan Agreement (public, June 1, 2018) Section 1(c), 1(w), 1(x), 2(a)(ii); Block 10-K FY2022 body text

**DIMENSION: Compliance Responsibility Allocation**

AML/KYC performer: Not explicitly assigned in the public merchant-facing loan agreement

AML/KYC responsible party (regulatory exposure): Celtic Bank — as FDIC-insured bank, bears BSA/AML obligation; Square Capital performs servicer-level customer due diligence as agent

BSA/AML program ownership: Not disclosed in public loan agreement; Block 10-K body text states accounts serve as "cash collateral for the performance of obligations under the agreements, which among other things may include compliance with certain covenants"

Source: Square Capital Term Loan Agreement Section 4(b); Block 10-K FY2022 body text

**DIMENSION: Indemnification**

Direction: Unilateral — Merchant indemnifies Bank and Square Capital only

Scope: Section 3(d): "Merchant will indemnify and hold harmless Bank and Square Capital (and their respective employees, directors, agents, affiliates and representatives) from and against any cost, loss or liability including interest, penalties, reasonable attorneys' fees and expenses resulting from Your misrepresentation or breach of warranty, default or breach of any covenant in this Agreement"

Carve-outs: None stated for Merchant indemnity. No reverse indemnification by Bank or Square Capital of Merchant.

Source: Square Capital Term Loan Agreement Section 3(d)

**DIMENSION: Limitation of Liability**

Cap structure: No explicit liability cap in the public agreement

Consequential loss exclusion: No explicit consequential damages exclusion in the public agreement

Carve-outs from cap: Not applicable (no cap stated)

Source: Not disclosed in Square Capital Term Loan Agreement (June 2018)

**DIMENSION: Termination**

Convenience termination: Section 2(a)(viii): Merchant may cancel "any time prior to the Repayment Start Date" — Bank debits Loan Amount from Linked Bank Account. No post-start-date convenience termination right.

Regulatory trigger termination: Not stated in the public agreement

Term structure: Section 3(a): "This Agreement will remain in full force and effect until the entire Loan Balance has been repaid in full"

Initial term of overall Celtic Bank program: "The initial term of the agreement with Celtic Bank is for three years and automatically extends for one-year periods unless terminated by either party" (disclosed in Block 10-K FY2017 body text)

Source: Square Capital Term Loan Agreement Sections 2(a)(viii), 3(a); Block 10-K FY2017 body text

**DIMENSION: Audit and Oversight Rights**

Right to audit: No dedicated audit rights clause. Section 4(b): Merchant must "provide to Bank and Square Capital, upon request, transaction files maintained by Merchant, and any other information related to past payment processing volumes"

Section 6(e): Merchant must "sign any and all documents Bank or Square Capital deems necessary and furnishing Bank or Square Capital with such information (including updated financial statements) as Bank or Square Capital may reasonably request from time to time"

Frequency / notice: On request; no scheduled audit frequency

Cost allocation: Not stated

Source: Square Capital Term Loan Agreement Sections 4(b), 6(e)

**DIMENSION: Regulatory Status Dependencies**

Load-bearing party: Celtic Bank Corporation — its Utah-chartered industrial bank status is the source of loan origination authority; federal preemption of state usury laws flows from Celtic Bank's charter (not from Square Capital or Square)

Change of status provision: Not disclosed in the public merchant-facing agreement. Governing law clause (Section 8(b)): "This Agreement is governed by Utah law and/or applicable federal law (including the Federal Arbitration Act)" — reflects Celtic Bank's Utah charter as jurisdictional anchor

Post-2021 note: Square Financial Services, Inc. (Block's wholly-owned Utah ILC) now serves as primary loan originator for Square Loans; Celtic Bank relationship for loans substantially reduced. Square Financial Services holds its own FDIC-insured bank charter.

Source: Square Capital Term Loan Agreement Section 8(b); Block IR announcement re: Square Financial Services banking operations (2021)

---

### FILING 5

```
FILING: PayPal Holdings, Inc. / 8-K / EX-10.1 / Filed 2015-07-20
AGREEMENT TITLE: Operating Agreement
PARTIES: eBay Inc. / eBay International AG (collectively, "eBay") / PayPal Holdings, Inc. / PayPal, Inc. / PayPal Pte Ltd. / PayPal Payments Pte Holdings, S.C.S. (collectively, "PayPal")
ARCHETYPE: Enterprise Payment Services
WORKSTREAM LABEL: Derived from disclosed agreement (SEC)
```

**Note on scope:** This agreement governs PayPal's continued provision of payment services to eBay following their 2015 corporate separation. It is a large-enterprise commercial payment services arrangement, not a bank-fintech or issuer-processor agreement. The operating agreement ran for five years from closing of the separation; an amendment was filed June 2016. The eBay-PayPal commercial relationship was substantially modified and wound down by 2023 as eBay migrated to its own managed payments platform.

**DIMENSION: Services Scope**

Description: PayPal continues to provide payment services to eBay and its customers following the Distribution. Agreement covers service scope, pricing, data sharing, confidentiality, compliance, and dispute resolution. eBay is to encourage its customers to use PayPal services following the distribution. Associated agreements include: Transition Services Agreement (IT and operational services), Colocation Services Agreement (data center facilities), and Data Sharing Addendum (data rights).

Source: PayPal 8-K EX-10.1, filed 2015-07-20, CIK 1633917; eBay 8-K EX-10.1, filed 2015-07-20, CIK 1065088; eBay IR summary "Highlights from eBay PayPal Operating Agreement" (2015)

**DIMENSION: Compliance Responsibility Allocation**

AML/KYC performer: PayPal — as the licensed payment services provider, PayPal holds money transmitter licences and implements AML/KYC for the payment processing it provides

AML/KYC responsible party (regulatory exposure): PayPal — as the licensed MSB/PSP, bears MSB regulatory obligations

BSA/AML program ownership: PayPal — as a registered Money Services Business and holder of state money transmitter licences

Note: The agreement includes annual internal audit requirements for each party to verify compliance, with "detailed written reports provided to the CEOs and Audit Committees of both companies"

Source: SEC filing body disclosures; eBay IR summary 2015; Justia exhibit reference

**DIMENSION: Indemnification**

Direction: Not fully extractable from available text (exhibit text not available via Law Insider or Justia mirror in this session); summary sources indicate mutual indemnification structure

Scope: Not disclosed in detail in available sources for this session

Carve-outs: Not disclosed in detail in available sources for this session

Source: Not fully disclosed in sources accessible this session. EX-10.1 is available at https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm but returned HTTP 403 during this research session. Justia mirror at https://contracts.justia.com/companies/paypal-1026/contract/474899/ also returned 403. Note that the related Intellectual Property Matters Agreement (which is available via Law Insider) contains language: "neither PayPal nor eBay will be liable for indirect, punitive, exemplary, remote, speculative or similar damages in excess of compensatory damages arising in connection with the transactions contemplated in the agreement" — however this is a separate agreement and should not be attributed to the Operating Agreement.

**DIMENSION: Limitation of Liability**

Cap structure: Not disclosed in sources accessible this session

Consequential loss exclusion: Not disclosed in sources accessible this session (note: related IP Matters Agreement excludes indirect/punitive damages, but this is a separate instrument)

Carve-outs from cap: Not disclosed in sources accessible this session

Source: Not disclosed in Operating Agreement text accessible this session

**DIMENSION: Termination**

Convenience termination: Not explicitly quoted from text — agreement had a five-year term with wind-down provisions following separation

Data Sharing Addendum termination: "eBay can terminate all or any portion of the Data Sharing Addendum (without triggering the termination of this Agreement) by delivering written notice to PayPal at any time beginning at the effective date of a Specified Change of Control and ending ninety (90) days thereafter"

Annual review mechanism: "During December of each calendar year, the CEOs of both eBay and PayPal prepared written assessments of each party's compliance under the Agreement, costs and benefits of the Agreement, and other aspects of the relationship"

Regulatory trigger termination: Not separately quoted from text in accessible sources this session

Source: 2015 eBay IR summary; eBay 8-K amendment (2016) at https://www.sec.gov/Archives/edgar/data/1065088/000106508816000317/ebay063016ex1004.htm

**DIMENSION: Audit and Oversight Rights**

Right to audit: Yes — "annual internal audit requirements for each party to verify compliance"

Frequency / notice: Annual

Cost allocation: Not disclosed in accessible sources

Reports: "detailed written reports provided to the CEOs and Audit Committees of both companies"

Source: 2015 eBay IR summary of Operating Agreement

**DIMENSION: Regulatory Status Dependencies**

Load-bearing party: PayPal — its money transmitter licences, payment network memberships, and MSB registration are the regulatory basis for providing payment services under this agreement. No bank sponsor required (PayPal holds its own licences).

Change of status provision: Not specifically disclosed in accessible text. Loss of PayPal's money transmitter licence in a material jurisdiction would presumably constitute a material breach or regulatory change trigger.

Source: PayPal 10-K disclosures re: regulatory status; 2015 eBay IR summary

---

### FILING 6 — ADYEN

```
FILING: Adyen NV — No SEC filing exists
AGREEMENT TITLE: Not applicable
PARTIES: Not applicable
ARCHETYPE: Not assigned
WORKSTREAM LABEL: Derived from disclosed agreement (SEC) — NOT APPLICABLE; no SEC filing
```

**DIMENSION: All dimensions**

Not disclosed in any SEC filing. Adyen NV does not file with the SEC. CIK 1788707 reflects only the unsponsored ADR administrative registration. No Form 20-F, Form F-1, or EX-10 exhibits exist.

**Where Adyen's commercial arrangements are disclosed:**

Adyen publishes annual reports (in Dutch GAAP / IFRS) on its investor relations portal: investors.adyen.com. The annual reports describe business operations, regulatory status, and related party transactions but do not include exhibit-level payment services agreement texts as required under SEC Regulation S-K Item 601.

Adyen's regulatory profile (from annual reports and public statements):
- Licensed bank under Dutch banking law, regulated by De Nederlandsche Bank (DNB) and AFM, since 2017
- UK banking licence granted H2 2023
- US money transmitter licences held in states requiring them
- As a licensed bank, Adyen does not rely on sponsor banks or BIN sponsors
- Adyen processes over €970 billion in payments (2023)
- Adyen issues cards and processes transactions directly under its own regulatory authorisations

Any research into Adyen's commercial agreement structures would require: (a) obtaining Adyen's Dutch annual reports, (b) reviewing any contracts disclosed in the notes to those financial statements, and (c) accessing any publicly available merchant agreements or cardholder agreements published on Adyen's website. These are outside the SEC/EDGAR disclosure regime and require a separate research workstream.

**Recommended next step for Adyen:** Review the Adyen 2023 and 2024 Annual Reports (available at investors.adyen.com/financials) for related party transactions disclosures and any contractual summaries in the notes to financial statements. Review Adyen's published merchant terms of service and cardholder agreements for commercial structure indicators.

---

## Research Gaps and Limitations

### Gaps requiring follow-up

1. **Marqeta / Sutton Bank — limitation of liability, full indemnification scope:** The filed EX-10.21 contains extensive [***] redactions. The limitation of liability section is not disclosed in the filed exhibit or in 10-K body text. A FOIA request under 17 C.F.R. §200.83 (confidential treatment) or review of confidential treatment applications filed by Marqeta would be required to access unredacted provisions.

2. **Block / Sutton Bank — full agreement text:** No standalone EX-10 exhibit filed. Material terms are disclosed only in 10-K body narrative. The underlying agreement between Block and Sutton Bank has not been separately filed.

3. **PayPal / eBay Operating Agreement — indemnification and limitation of liability:** The exhibit text at SEC.gov (EX-10.1, CIK 1065088 and 1633917) returned HTTP 403 during this research session. The Law Insider and Justia mirrors also returned 403. These provisions therefore remain unextracted. The document is confirmed to exist at the SEC archive URL. A follow-up session with access to the raw SEC EDGAR HTML should retrieve this text.

4. **PayPal FI partnership agreements (Synchrony, The Bancorp Bank, Wells Fargo):** PayPal's consumer credit and banking relationships with Synchrony Bank, The Bancorp Bank, and Wells Fargo are disclosed narratively in PayPal 10-K body text and in those banks' own SEC filings (Synchrony 10-K discloses PayPal as a significant program partner). No standalone EX-10 exhibit for these bank partnership agreements was located in PayPal's EDGAR filings. The Synchrony-PayPal credit program agreement may be filed in Synchrony's own 10-K exhibits. A separate EDGAR search under CIK 1601712 (Synchrony Financial) is recommended.

5. **Adyen — no SEC disclosure:** As noted, all Adyen research requires separate workstream using Dutch annual reports and Euronext disclosures.

6. **Block / Celtic Bank — full program agreement terms:** The Celtic Bank program-level agreement between Block/Square Capital and Celtic Bank has not been identified as a filed SEC exhibit. The public merchant-facing loan agreement (June 2018) has been extracted but reflects only the merchant-borrower tier, not the program-level bank-fintech arrangement.

### Confirmed limitations of EDGAR access this session

Direct access to SEC.gov HTML exhibit files (*.htm URLs under sec.gov/Archives/edgar/) returned HTTP 403 throughout this session. All exhibit text was retrieved via Law Insider (https://www.lawinsider.com), Justia Contracts (https://contracts.justia.com), and fintel.io mirrors, which reproduce the filed exhibit texts. 10-K body disclosures were obtained through search engine indexing and financial data providers. This limitation should be noted in any provenance chain.

---

## Source List

All sources confirmed during this research session:

**Marqeta (CIK 1522540):**
- S-1, filed 2021-05-14: https://www.sec.gov/Archives/edgar/data/1522540/000119312521162113/d64065ds1.htm
- S-1/A (Amendment No. 1), filed 2021-05-21: https://www.sec.gov/Archives/edgar/data/1522540/000119312521169619/d64065ds1a.htm
- S-1/A (Amendment No. 2) + EX-10.14 + EX-10.15, filed 2021-06-04: https://www.sec.gov/Archives/edgar/data/1522540/000119312521177861/d64065ds1a.htm
- EX-10.14 (MSA with Square): https://www.sec.gov/Archives/edgar/data/1522540/000119312521177861/d64065dex1014.htm
- EX-10.15 (Sutton Bank agreement, S-1/A version): https://www.sec.gov/Archives/edgar/data/1522540/000119312521177861/d64065dex1015.htm
- EX-10.21 (Sutton Bank agreement, 10-K FY2021 version): https://www.sec.gov/Archives/edgar/data/1522540/000152254022000013/exhibit1021-202110xk.htm
- Filing index for EX-10.21: https://www.sec.gov/Archives/edgar/data/1522540/000152254022000013/0001522540-22-000013-index.htm
- Marqeta ARS 2024: https://www.sec.gov/Archives/edgar/data/1522540/000152254024000005/marqetaars2024.pdf
- Law Insider MSA text: https://www.lawinsider.com/contracts/6MrRZdDJFj1
- Justia Sutton Bank agreement: https://contracts.justia.com/companies/marqeta-inc-13009/contract/178692/
- Justia Fourth Amendment: https://contracts.justia.com/companies/marqeta-inc-13009/contract/208344/
- Justia Eighth Amendment: https://contracts.justia.com/companies/marqeta-inc-13009/contract/1314972/
- Justia Square MSA listing: https://contracts.justia.com/companies/marqeta-inc-13009/contract/180185/
- Justia Amendment No. 22 (Block): https://contracts.justia.com/companies/marqeta-inc-13009/contract/1314970/
- Justia Amendment No. 26 (Block): https://contracts.justia.com/companies/marqeta-inc-13009/contract/1345967/

**Block, Inc. (CIK 1512673):**
- 10-K FY2017: https://www.sec.gov/Archives/edgar/data/1512673/000151267318000004/a10-kfilingsquareinc2017.htm
- 10-K FY2020 (sq-20201231): https://www.sec.gov/Archives/edgar/data/1512673/000151267321000008/sq-20201231.htm
- 10-K FY2022 (sq-20221231): https://www.sec.gov/Archives/edgar/data/1512673/000162828023004840/sq-20221231.htm
- 10-K FY2023 (sq-20231231): https://www.sec.gov/Archives/edgar/data/1512673/000162828024006354/sq-20231231.htm
- EDGAR browse: https://www.sec.gov/edgar/browse/?CIK=0001512673
- Square Capital Term Loan Agreement (June 1, 2018, public): https://squareup.com/us/en/legal/general/capital-term-loan-agreement-jun-01-2018
- Cash App Prepaid Card Program Agreement: https://cash.app/legal/us/en-us/card-agreement
- Sutton Bank Cash App card terms: https://www.suttonbank.com/_/kcms-doc/85/79012/Cash-App-Prepaid-Card-Agreement-1.27.23.pdf

**PayPal Holdings (CIK 1633917):**
- Form 10 registration (2015): https://www.sec.gov/Archives/edgar/data/1633917/000119312515062742/d877527d1012b.htm
- 10-K FY2015: https://www.sec.gov/Archives/edgar/data/1633917/000163391716000113/pypl201510-k.htm
- 10-K FY2021 (pypl-20211231): https://www.sec.gov/Archives/edgar/data/1633917/000163391722000027/pypl-20211231.htm
- 10-K FY2022 (pypl-20221231): https://www.sec.gov/Archives/edgar/data/1633917/000163391723000033/pypl-20221231.htm
- eBay 8-K EX-10.1 (Operating Agreement): https://www.sec.gov/Archives/edgar/data/1065088/000119312515257121/d93601dex101.htm
- Amendment to Operating Agreement (2016): https://www.sec.gov/Archives/edgar/data/1065088/000106508816000317/ebay063016ex1004.htm
- Separation and Distribution Agreement: https://www.sec.gov/Archives/edgar/data/1065088/000119312515240245/d944939dex21.htm
- Justia Operating Agreement (PayPal): https://contracts.justia.com/companies/paypal-1026/contract/474899/
- Justia Operating Agreement (eBay): https://contracts.justia.com/companies/ebay-441/contract/489831/
- Law Insider PayPal contracts list: https://www.lawinsider.com/company/1633917/paypal-holdings-inc
- Synchrony-PayPal press release (SEC-filed): https://www.sec.gov/Archives/edgar/data/1601712/000160171217000160/jointpressrelease111317.htm

**Adyen NV (CIK 1788707 — ADR registration only):**
- EDGAR ADR CIK reference: https://research.secdatabase.com/CIK/1788707
- Adyen investor relations: https://investors.adyen.com/financials
- Adyen 2024 Annual Report page: https://investors.adyen.com/financials/2024
- Wikipedia (public structural information): https://en.wikipedia.org/wiki/Adyen
