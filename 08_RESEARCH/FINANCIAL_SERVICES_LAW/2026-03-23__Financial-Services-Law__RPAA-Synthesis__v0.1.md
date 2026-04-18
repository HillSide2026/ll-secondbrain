---
layer: 08_RESEARCH
domain: financial-services-law
status: draft
owner: ML2
authority: not-approved
confidence: exploratory
created: 2026-03-23
updated: 2026-03-23
scope: "CA - federal"
matter_id: null
sources:
  - type: url
    citation: "Osler, Hoskin & Harcourt LLP — Retail Payment Activities Act Hub"
  - type: url
    citation: "Osler, Hoskin & Harcourt LLP — RPAA Draft Regulations Published for Comment (2023)"
  - type: url
    citation: "Osler, Hoskin & Harcourt LLP — Final Regulations to the RPAA (2023)"
  - type: url
    citation: "Miller Thomson LLP — Payment Service Providers: Canada's RPAA Regulations"
  - type: url
    citation: "Bank of Canada — Supervisory Framework: Supervision"
  - type: url
    citation: "Bank of Canada — Supervisory Framework: Registration"
  - type: url
    citation: "Bank of Canada — Information for Payment Service Providers"
  - type: url
    citation: "UK FCA — Payment Services Regulations and E-Money Regulations"
  - type: url
    citation: "BIS CPMI — d193: Enhancing Cross-Border Payments (Stage 2 Report, 2020)"
  - type: url
    citation: "FSB — Recommendations for Regulating and Supervising PSPs Offering Cross-Border Payment Services (Final Report, December 2024)"
open_questions:
  - AMP penalty dollar amounts not confirmed in sources retrieved — Bank of Canada policy document (June 2024) cited but not fetched
  - Exact annual assessment fee formula not confirmed — final regs deleted draft formula; methodology to be set post-registration based on actual PSP enrolment data
  - Whether Bank of Canada has commenced any enforcement actions under RPAA as of early 2026 — not confirmed in sources
  - Treatment of stablecoin and crypto-backed payment services under RPAA (Bank of Canada case scenarios reference crypto services; detail not fully retrieved)
  - Whether provincially regulated credit unions and caisses populaires are entirely exempt or only exempt for certain functions
  - PCMLTFA/FINTRAC interaction — whether RPAA registration triggers automatic FINTRAC notification or whether dual registration obligations arise
  - McCarthy Tétrault, Fasken, and Dentons articles not retrieved (rate limits/access blocks) — may contain additional detail on specific provisions
next_actions:
  - Retrieve McCarthy Tétrault articles (3) on final regs, draft regs, and supervisory guidance
  - Retrieve Fasken and Dentons RPAA articles
  - Download Bank of Canada June 2024 AMP policy document directly from bankofcanada.ca
  - Confirm annual assessment fee methodology once Bank of Canada publishes post-registration framework
  - Review Bank of Canada case scenarios on crypto/stablecoin services
  - Consider promotion to 07_REFERENCE once ML1 reviews and content stabilizes
---

# RPAA Research Synthesis — v0.1

> **Research grade — not approved. Not to be treated as authoritative.**
> Sources: 9 of 22 attempted sources retrieved or partially retrieved. See RPAA-Source-Index for full source list and retrieval status.

---

## 1. What is the RPAA

The **Retail Payment Activities Act** (RPAA) is Canadian federal legislation that establishes a regulatory oversight framework for payment service providers (PSPs) operating in Canada. It was enacted as part of the **Budget Implementation Act, 2021, No. 1** (S.C. 2021, c. 23), which received Royal Assent on **June 29, 2021**. The RPAA provisions were brought into force in stages, with the regulatory framework completing its publication cycle in November 2023 and the full operational requirements taking effect on **September 8, 2025**.

**Regulator:** The **Bank of Canada** is the designated supervisor. The Bank administers registration, conducts ongoing supervision, and exercises enforcement powers. The **Minister of Finance** retains a parallel national security review authority (see Section 9 below).

**Purpose:** The RPAA aims to:
- Build confidence in the safety and reliability of retail payment services
- Protect end-users from specific risks, including loss of funds held by PSPs and operational failures
- Professionalize the industry and establish a level playing field between traditional financial institutions and fintech PSPs
- Provide the Bank of Canada with visibility into a sector that had previously operated outside prudential oversight

**What the RPAA is not:** The RPAA is not a prudential regime (PSPs are not subject to capital adequacy requirements). It does not replace AML/PCMLTFA obligations or displace FINTRAC oversight. It is a conduct and operational risk framework focused on safeguarding, system integrity, and supervisory transparency.

---

## 2. Entity Scope — Who Must Register

### The Four Registration Criteria

A person or entity must register with the Bank of Canada if it meets **all four** of the following criteria:

1. **Is a PSP**: Performs one or more payment functions as part of its business (not merely incidental to another activity)
2. **Performs retail payment activities**: Handles electronic funds transfers in Canadian or foreign currency (the Act explicitly excludes digital currencies — i.e., cryptocurrencies are subject to separate Bank of Canada case scenario analysis)
3. **Meets geographic nexus**: Either has a **place of business in Canada**, or operates outside Canada but **serves Canadian end-users**
4. **Is not excluded**: Not a bank, authorized foreign bank, provincially-regulated credit union or caisse populaire, insurance company, SWIFT member, or other specifically enumpted entity

### In Scope (examples)

- Payment processors (acquirers, issuers, card managers)
- Money service businesses performing payment functions
- Fintech companies offering e-wallets, disbursement services, or payment initiation
- Cryptocurrency-related services that involve holding fiat funds or processing fiat transfers (subject to case scenario guidance)
- Marketplace platforms that hold and transmit funds on behalf of buyers/sellers
- Lending platforms where payment activity is not merely incidental

### Out of Scope / Excluded

- **Deposit-taking institutions** regulated under the Bank Act (Schedule I/II banks, authorized foreign banks)
- **Provincially regulated deposit-taking institutions** (credit unions, caisses populaires, trust companies under provincial law)
- **Insurance companies** regulated under the Insurance Companies Act
- **SWIFT members** (as defined in the RPAA)
- **Securities intermediaries** performing securities-related payment functions within a regulated securities transaction
- **Automatic banking machine operators** (for ABM-specific transactions only)
- **Internal group transactions** (payments between affiliates within a corporate group, subject to conditions)

### Nexus Rule — Offshore Entities Serving Canadian End-Users

A PSP incorporated or headquartered outside Canada must register if it **provides retail payment services to Canadian end-users**. Offshore incorporation does not provide shelter. The extraterritorial application is a significant feature distinguishing the RPAA from some provincial MSB regimes, and it mirrors the approach taken in the UK PSRs for non-EEA firms serving UK customers.

### Scale of the Regime

The Bank of Canada anticipated approximately **2,500 PSPs** would seek registration when the regime launched.

---

## 3. Payment Functions

The RPAA defines five **payment functions** in s. 2 that trigger registration obligations when performed as part of a business. Exact statutory language:

| # | Payment Function | Statutory Text |
|---|-----------------|----------------|
| (a) | **Account provision/maintenance** | The provision or maintenance of an account that, in relation to an electronic funds transfer, is held on behalf of one or more end users |
| (b) | **Holding funds** | The holding of funds on behalf of an end user until they are withdrawn or transferred |
| (c) | **Initiating EFTs** | The initiation of an electronic funds transfer at the request of an end user |
| (d) | **Authorizing / transmitting EFTs** | The authorization of an electronic funds transfer or the transmission, reception or facilitation of an instruction in relation to an electronic funds transfer |
| (e) | **Clearing or settlement** | The provision of clearing or settlement services |

**Note — prior synthesis error:** An earlier draft of this synthesis incorrectly listed function 5 as "safeguarding/custodying payment instruments." That is wrong. Safeguarding is an *obligation* that attaches to PSPs performing function (b); it is not itself a payment function.

### The (a)/(b) Structural Distinction

Functions (a) and (b) are legally separate and architecturally significant.

Function (a) — *provision or maintenance of an account* — is an infrastructure role. The PSP maintains the account as a record or ledger. The account can be provided without the PSP controlling or holding the funds in it. A PSP performing only (a) may have a bank sponsor or other institution holding the underlying funds while the PSP operates the account layer.

Function (b) — *holding funds* — is where the PSP takes actual custody of end-user money until withdrawn or transferred.

A PSP can perform (a) without (b). This is the structural design of most pass-through and bank-sponsored fintech models. The safeguarding obligation under the RPAA attaches only to PSPs performing function (b).

**Practical note:** A single entity may perform multiple functions. The Bank of Canada has published **case scenarios** clarifying how these functions apply to specific business models, including acquirers, card managers, cryptocurrency services (fiat-touching aspects), marketplace lending, and cloud computing arrangements. Registration is triggered by the performance of any one of the five functions.

---

## 4. Registration Requirements

### Application Window and Timeline

| Event | Date |
|-------|------|
| Registration opens (PSP Connect portal live) | November 1, 2024 |
| Initial 15-day application window closes | November 15, 2024 |
| Transition period begins | November 16, 2024 |
| Transition period ends / operational requirements effective | September 8, 2025 |
| PSPs applying after transition: delay before commencing operations | 60 days from application submission |

**Critical point:** PSPs that submitted applications during the November 1–15, 2024 window were permitted to continue operating through the transition period while their applications were processed. PSPs that missed this window face a mandatory **60-day cessation period** — they may not conduct payment activities until the Bank has processed their application. This creates a material business risk for late applicants.

PSPs that commence operations after September 8, 2025 without submitting an application are in **violation of section 104 of the RPAA** and risk substantial administrative penalties.

### PSP Connect Portal

Applications are submitted via the Bank of Canada's **PSP Connect** portal (https://rps.bankofcanada.ca). The portal is also used for:
- Ongoing compliance management
- Submission of annual reports
- Notification of significant changes
- Communication with the Bank

### Application Fee

- **One-time, non-refundable registration fee: $2,500 CAD** (payable by credit card or electronic transfer at time of application)
- Annual assessment fees apply post-registration; the methodology was deleted from the final regulations and is to be set by the Bank based on actual PSP enrolment data

### Required Application Information

Applicants must disclose:
- Contact details for third parties and affiliates
- Business structure and beneficial ownership
- Retail payment functions performed and business description
- Projected end-user fund values and transaction volumes
- Fund safeguarding methods and arrangements
- Risk management frameworks and control documentation
- Other regulatory registrations (FINTRAC MSB, provincial licences, etc.)

Additionally, applications include **17 elements specific to the National Security Review** (NSR) process (see Section 9).

### Grounds for Refusal or Revocation

Registration may be refused or revoked if a PSP:
- Does not meet the registration criteria
- Omits requested information or fails to respond to Bank requests
- Provides false or misleading statements
- Ceases retail payment activities
- Violates the RPAA or its regulations
- Fails to pay annual assessment fees
- Is the subject of an adverse national security determination by the Minister of Finance

### Review and Appeal

- **Internal review**: PSP may request review of a refusal or revocation decision within **30 days**
- **Review officer**: The Bank's Executive Director of Payments, Supervision and Oversight must complete the review within **90 days**
- **Appeal**: Subsequent appeal rights to the **Federal Court**
- Separately, PSPs may seek review of a **ministerial national security decision** within **30 days** of the Minister's determination

---

## 5. Operational Risk Management

### Framework Requirement

PSPs must **establish and maintain a written operational risk management and incident response framework**. The framework must address:

- **System availability**: Ensuring payment systems remain operational within acceptable parameters
- **Data integrity**: Ensuring accuracy and completeness of payment data
- **Confidentiality**: Protecting sensitive end-user and transaction data from unauthorized access
- **Third-party oversight**: Managing risks posed by service providers and technology vendors
- **Incident detection, response, and recovery**: Identifying operational failures and restoring service

Operational requirements became effective **September 8, 2025**.

### Governance

- The governing **board** must approve the operational risk management framework **annually**
- A **designated senior officer** must approve "in-year" material changes to the framework
- A **senior compliance officer** must be designated as accountable for framework oversight

### Testing Requirements

- PSPs must establish a **testing methodology** customized to their risk profile
- Testing must be sufficient to identify gaps in framework effectiveness
- The draft regulations' mandatory **three-year comprehensive testing** requirement was removed from the final regulations; PSPs must instead establish their own testing procedures
- **Independent audits** are required **every three years** (extended from the draft's biennial cycle)
- The Bank may require special audits at its discretion during supervision

### Third-Party Risk

PSPs must conduct **annual operational assessments** of all service providers. These assessments must evaluate:
- Data protection capabilities
- System security and connection management
- Third-party risk management practices

**No materiality threshold** was specified for third-party assessments — all service providers are in scope regardless of size or criticality level.

### Incident Reporting

PSPs must notify both **affected end-users** and the **Bank of Canada** of any operational incident with "material impact." Notifications must include:
- Description of the incident
- Timing and duration
- Impacts on end-users and payment systems
- Corrective measures taken or planned

The regulations do not define "material" for this purpose, nor do they expressly address interaction with existing **privacy legislation** obligations (e.g., PIPEDA breach notification requirements). This creates a practical compliance gap requiring legal judgment until further guidance is published.

The Bank requires notification within **specified timeframes** (not quantified in sources retrieved; Bank of Canada supervisory guidance materials reference these thresholds). For significant changes (not incidents), PSPs must provide **five business days' advance notice** before implementation.

---

## 6. Safeguarding of End-User Funds

### Scope of Obligation

PSPs that **hold end-user funds** must establish and maintain a written safeguarding framework. Not all PSPs hold funds — PSPs that only initiate, authorize, or clear/settle payments without holding customer funds are not subject to the safeguarding requirements (though they must still comply with operational risk management obligations).

### Three Permitted Safeguarding Models

The RPAA and its regulations prescribe three permissible approaches:

| Model | Description |
|-------|-------------|
| **Trust account** | Maintain client funds in a trust account used **exclusively** for end-user funds; account must be segregated and ring-fenced from the PSP's own assets |
| **Insurance/guarantee account** | Maintain funds in a dedicated account backed by insurance or a guarantee that equals or exceeds the account balance; protects end-users in a PSP insolvency |
| **Prescribed method** | Any method prescribed by regulation — **none currently prescribed** as of regulations published |

Both the trust and insurance/guarantee models require strict **segregation** from the PSP's operating funds. The framework documentation must specify how end-users can access funds in **normal operations** and in **PSP insolvency** scenarios.

### Governance of the Safeguarding Framework

- The **board** must **annually approve** the safeguarding framework
- A **senior officer** must approve safeguarding review results
- The framework must be reviewed:
  - **Annually** (mandatory)
  - After any **material change** (account openings/closures, administrator changes, insurance or guarantee provider changes)
  - At a minimum **triennial independent evaluation** (extended from the draft's biennial cycle)
- Annual reports must disclose **prior-year insolvency risks** related to safeguarding arrangements
- **Change notices** must include **safeguarding impact assessments**

### AMP Severity

Non-compliance with safeguarding obligations is classified as a **"very serious"** administrative monetary penalty — the highest severity tier available under the AMP regime.

---

## 7. Annual Reporting

PSPs must file **annual reports** with the Bank of Canada by **March 31 each year**. Annual reports must cover:

- Confirmation of registration status and current registration information
- Quantitative metrics on retail payment activities (volumes, values, end-user fund levels)
- Compliance practices and framework status
- Disclosure of prior-year insolvency risks related to safeguarding arrangements
- Disclosure of any changes to payment activities, business structure, or service provider arrangements

Additionally, PSPs must submit **quantitative metrics** at the time of initial registration, and subsequently as part of the annual reporting cycle. The reporting period for historical metrics was shortened from 24 months (draft regulations) to **12 months** in the final regulations.

**Significant changes** must be reported at least **five business days** before implementation — not only in the annual report. The Bank also requires notification of changes to registration information on an ongoing basis via PSP Connect.

---

## 8. Supervisory Framework

### Risk-Based, Proportional Approach

The Bank of Canada employs a **risk-based and proportional** supervisory model. The intensity of supervision is calibrated to each PSP's:
- Business structure and complexity
- Volume and value of payment activities
- End-user fund exposure
- Operational risk profile

The Bank published detailed **supervisory policies and guidelines** throughout 2024–2025, including:
- Registration criteria guidance (distinguishing PSPs from entities performing incidental payment activities)
- Case scenarios for specific business models
- Acquisitions of control and prescribed change procedures (published alongside the registration framework)
- Annual reporting metrics standards
- Fund safeguarding supervisory expectations (final guidelines published **December 12, 2024**)
- **Reviews and appeals policy** (published **January 31, 2025**)
- **AMP regime policy** (published **June 2024**)

### Ongoing Monitoring

The Bank monitors PSP compliance through:
- **Annual reports** submitted via PSP Connect by March 31 each year
- **Incident notifications** for material-impact operational events
- **Significant change notices** (five business days advance notice required)
- **Information requests**: PSPs must respond within **15 days** in normal circumstances; within **24 hours** in urgent or significant adverse impact situations
- **Desk reviews** of submitted documentation
- **On-site visits** (at Bank discretion)
- **Special audits** (at Bank discretion, in addition to the mandatory triennial independent audit)

### Enforcement Toolkit

The Bank has a graduated enforcement toolkit:

| Tool | Description |
|------|-------------|
| **Warning letter** | Identifies non-compliance and specifies expected corrective actions; earliest-stage tool |
| **Compliance agreement** | Formalizes remediation terms between the Bank and the PSP; non-adherence triggers a Notice of Violation with AMPs |
| **Administrative Monetary Penalty (AMP)** | Monetary penalty; amount considers actual/potential harm, violation history, and intent/negligence level; AMP is reduced by **50%** if PSP accepts an accompanying compliance agreement |
| **Compliance order** | Directs PSP to stop or remedy actions creating "significant adverse impact" on end-users, other PSPs, or settlement systems; may be issued at any stage of supervision |
| **Court enforcement** | Bank may seek superior court order compelling compliance with RPAA provisions or existing compliance orders |
| **Registration refusal or revocation** | Removes PSP from the registry; triggers cessation of activities |
| **Public notice** | Bank publishes enforcement decisions; reputational consequence |

### AMP Factors

AMPs are calibrated to:
- Actual or potential **harm** caused by the violation
- PSP's **history** of violations
- PSP's **intent or degree of negligence**

Safeguarding violations are the "very serious" tier. Other violation severity tiers are defined in the June 2024 AMP policy (document not retrieved in full; specific dollar amounts not confirmed in sources retrieved).

### PSP Reviews and Appeals

- PSPs may request review of enforcement decisions within **30 days**
- Review is conducted by the Bank's Executive Director of Payments, Supervision and Oversight within **90 days**
- Further appeals proceed to **Federal Court**

---

## 9. National Security Review

### Minister of Finance Authority

The RPAA includes a parallel **national security review (NSR)** mechanism separate from the Bank of Canada's supervisory role. NSR is triggered by:
- Initial registration applications
- **Acquisitions of control** of a registered PSP
- Certain prescribed changes to a PSP's registration (e.g., new state-owned enterprise involvement)

### Process and Timelines

| Stage | Timeline |
|-------|----------|
| Department of Finance review window | **60 days** post-application to determine whether formal NSR is required |
| Formal NSR by Minister of Finance | **180 days** (extendable at ministerial discretion) |
| PSP request for review of Minister's decision | Within **30 days** of Minister's determination |

### Acquisition of Control Thresholds

- General threshold: acquisition of **one-third or more** of voting shares or equivalent ownership interests
- **State-owned enterprises (SOEs)**: stricter scrutiny — any voting rights in director elections or any ownership interests trigger new registration/NSR requirements

### Data Jurisdiction Change

PSPs must obtain **pre-approval** before transferring data storage or processing to countries not previously disclosed in their application. This is a separate obligation distinct from the NSR process but similarly implicates national security and data sovereignty considerations.

### Consequences of Adverse NSR Determination

- Registration may be **refused** (initial applicants) or **revoked** (registered PSPs)
- PSPs that missed the initial November 1–15, 2024 application window face mandatory **cessation of activities** during a pending NSR, unlike early-window applicants who are permitted to continue operating during the review period

---

## 10. Key Dates and Timeline

| Date | Event |
|------|-------|
| **June 29, 2021** | Budget Implementation Act, 2021, No. 1 receives Royal Assent; RPAA enacted |
| **2022–2023** | Department of Finance consultations; draft regulations developed |
| **2023 (early)** | Draft RPAA regulations published for public comment |
| **November 2023** | Final RPAA regulations published in Canada Gazette, Part II |
| **June 2024** | Bank of Canada publishes AMP regime policy |
| **November 1, 2024** | PSP Connect portal opens; registration applications accepted |
| **November 1–15, 2024** | Critical 15-day window for existing PSPs to file applications and preserve right to continue operating |
| **November 16, 2024** | Transition period begins; late applicants face 60-day operational delay |
| **December 12, 2024** | Bank of Canada publishes final safeguarding supervisory guidelines |
| **January 31, 2025** | Bank of Canada publishes reviews and appeals policy |
| **February 2025** | Public consultation launched on expanding Payments Canada membership to registered PSPs |
| **September 8, 2025** | Operational requirements (risk management and safeguarding frameworks) become effective |
| **March 31, 2026** | First annual reports due from registered PSPs covering 2025 operational period |

---

## 11. Relationship to Other Frameworks

| Framework | Relationship to RPAA |
|-----------|---------------------|
| **PCMLTFA / AML (FINTRAC)** | Separate, overlapping regime. PSPs that are money services businesses (MSBs) remain subject to PCMLTFA registration with FINTRAC and full AML/ATF program obligations regardless of RPAA registration. RPAA does not displace or reduce PCMLTFA obligations. Dual registration (Bank of Canada + FINTRAC) is the expected posture for many PSPs. |
| **CARF** | Separate regime. CARF is a tax transparency framework for crypto-asset reporting to CRA. A PSP handling crypto-fiat payment flows may face both RPAA registration (for the fiat payment functions) and CARF obligations (for the crypto-asset transaction reporting). No direct overlap but potential dual-compliance populations. |
| **Payments Canada / Large Value Transfer System (LVTS) / Retail Payment Rail Access** | Related. Payments Canada governs access to clearing and settlement systems. A registered RPAA PSP is not automatically a Payments Canada member. A February 2025 public consultation proposed expanding Payments Canada membership eligibility to registered PSPs — this would allow non-bank PSPs to access payment rails directly rather than through a bank sponsor, significantly altering the competitive landscape. |
| **Bank Act / OSFI** | RPAA explicitly excludes Schedule I/II banks and authorized foreign banks from registration; these entities remain subject to OSFI prudential supervision. There is no RPAA overlap for regulated deposit-taking institutions. |
| **Provincial MSB / Trust Company legislation** | Provincially regulated trust companies and credit unions are excluded from RPAA. Some provincial MSB licences (e.g., Quebec Autorité des marchés financiers money service business registration) may overlap with RPAA in practical terms but are legally separate regimes. |
| **FINTRAC / Proceeds of Crime** | RPAA registration with the Bank of Canada does not constitute FINTRAC registration. PSPs that are MSBs must maintain both registrations independently. |

---

## 12. UK FCA Analogue

### UK Payment Services Regulations 2017 (PSRs)

The UK's **Payment Services Regulations 2017** (PSRs), implementing the EU's revised Payment Services Directive (PSD2), provide the closest international analogue to the RPAA. Key structural parallels:

| Dimension | UK PSRs | Canadian RPAA |
|-----------|---------|---------------|
| **Authorization tiers** | Three tiers: Authorised Payment Institution (API), Small Payment Institution, Registered AISP | Single registration tier (no tiering by size in RPAA) |
| **Regulator** | Financial Conduct Authority (FCA) | Bank of Canada |
| **Scope** | Banks, building societies, e-money issuers, remittance firms, acquirers, card issuers, PISPs, AISPs | PSPs performing defined payment functions not incidental to other business |
| **Safeguarding** | Segregation + insurance/guarantee model; detailed FCA rules | Trust account or insurance/guarantee; similar structural models |
| **Incident reporting** | Major incident notification using EBA criteria/thresholds | Material impact incident notification to Bank of Canada |
| **Enforcement** | FCA powers including fines, prohibition, public censure | AMPs, compliance orders, court enforcement, revocation |
| **Open banking** | PISPs and AISPs explicitly regulated under PSRs | No open banking/PISP/AISP category in RPAA (separate Canadian open banking initiative underway) |

### What Canadian Enforcement May Look Like

The FCA's enforcement track record under the PSRs provides a practical reference point for what Bank of Canada enforcement may look like over time:

- **Early-stage focus on registration compliance**: FCA initially focused enforcement on unauthorised payment service providers; the Bank of Canada's first enforcement actions are likely to focus on registration non-compliance (PSPs operating without registration)
- **Graduated approach**: FCA historically used supervisory tools (requirement notices, voluntary requirements) before formal enforcement; the Bank's toolkit mirrors this structure
- **Safeguarding as a priority area**: FCA enforcement has prominently targeted safeguarding failures; the RPAA's classification of safeguarding violations as "very serious" AMPs signals similar prioritization
- **Public enforcement register**: Both FCA and the Bank maintain public registers of enforcement decisions; reputational consequences are a material enforcement tool

---

## 13. Relevance to LL Practice

The RPAA directly supports the following LL solutions:

| RPAA Requirement | Relevant LL Solution |
|-----------------|---------------------|
| Determining whether a client must register; analyzing payment functions and geographic nexus | **RPAA_REGISTRATION** |
| Preparing registration application (PSP Connect, documentation, quantitative metrics) | **RPAA_REGISTRATION** |
| Drafting operational risk management and incident response framework | **RPAA_REGISTRATION** (initial) |
| Drafting safeguarding framework (trust/insurance/guarantee model selection, board approval, testing regime) | **RPAA_REGISTRATION** (initial) |
| NSR information elements and national security risk assessment | **RPAA_REGISTRATION** |
| Triennial independent framework review and compliance assessment | **RPAA_THREE_YEAR_REVIEW** |
| In-depth testing methodology update and gap analysis | **RPAA_THREE_YEAR_REVIEW** |
| Annual report preparation and submission (March 31 deadline, quantitative metrics, insolvency risk disclosure) | **RPAA_REPORT** |
| Annual board approval of safeguarding and risk management frameworks | **RPAA_REPORT** |
| Significant change notices and acquisition of control notifications | **ONGOING_PAYMENTS_COUNSEL** |
| Third-party risk assessments (annual, all service providers) | **ONGOING_PAYMENTS_COUNSEL** |
| Incident response (material impact notification to Bank of Canada and end-users) | **ONGOING_PAYMENTS_COUNSEL** |
| Acquisition structuring for PSP targets (NSR thresholds, SOE rules, data jurisdiction pre-approvals) | **ONGOING_PAYMENTS_COUNSEL** |
| Enforcement defence (warning letters, compliance agreements, AMP proceedings, Bank review and Federal Court appeals) | **ONGOING_PAYMENTS_COUNSEL** |
| RPAA + PCMLTFA dual compliance (mapping overlapping obligations for MSB-PSPs) | **ONGOING_PAYMENTS_COUNSEL** |
| Payments Canada membership strategy (accessing clearing/settlement rails post-RPAA registration) | **ONGOING_PAYMENTS_COUNSEL** |

**Key practitioner point:** The RPAA creates a **triennial compliance cycle** (independent framework review, in-depth testing) that is distinct from the annual cycle (annual reports, board approvals, annual third-party assessments). This makes RPAA_THREE_YEAR_REVIEW a standalone recurring engagement — not just a one-time registration deliverable — and positions LL for durable client relationships with registered PSPs across both the annual and triennial cycles.

A further practitioner point: the **Payments Canada membership consultation** (February 2025) represents a potential structural shift in Canadian payments access. If non-bank PSPs gain direct rail access, the demand for payments legal counsel will increase significantly, particularly around system access agreements, operational rules compliance, and dispute resolution. This warrants monitoring as an emerging ONGOING_PAYMENTS_COUNSEL opportunity.
