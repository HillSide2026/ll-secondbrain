---
id: 02_playbooks__corporate__solutions__business_acquisition__solution_assembly_md
title: Solution Assembly: Business Acquisition
owner: ML1
status: draft
created_date: 2026-02-25
last_updated: 2026-03-12
tags: [business-acquisition, solution-assembly]
---

# Solution Assembly: Business Acquisition

---

## Required Inputs

| Input | Notes |
|-------|-------|
| Deal size (total purchase price) | Determines Level 1 / 2 / 3 pathway |
| Transaction structure | Asset purchase or share purchase |
| Identity of buyer and seller | Individuals or corporations |
| Description of the business | Type, sector, Ontario location |
| Proposed closing date or timeline | If known |
| Whether APA has already been prepared | Determines entry point |
| Financing structure | Cash, VTB, bank financing, earnout — flag each |
| Whether employees are being assumed | Triggers employment succession assessment |
| Whether a lease assignment is required | Triggers landlord consent track |
| Sector-specific licences or permits | Flag for escalation assessment |

---

## Assembly Sequence

### Level 1 — < $250,000 (Agent-Prepared APA)

1. **Confirm eligibility** against Solution Scope; classify as Level 1
2. **Obtain agent-prepared APA** from client
3. **Review APA** — assess completeness, identify deficiencies, flag missing standard protections
4. **Advise client** on APA terms, risk flags, and negotiation points
5. **Assist with negotiation** (limited scope — lawyer does not redraft; identifies issues for client to raise with agent)
6. **Pre-closing checklist** — confirm conditions, consents, and regulatory items
7. **Closing**
8. **Post-closing checklist** — business licence, lease, regulatory registrations, PPSA discharges

---

### Level 2 — $250,000–$1,000,000 (Lawyer-Prepared APA, No LOI)

1. **Confirm eligibility** against Solution Scope; classify as Level 2
2. **Intake** — complete Required Inputs; flag escalation conditions
3. **Diligence** — proportionate scope; review corporate records, material contracts, licences, PPSA, tax status
4. **Draft APA** — lawyer-prepared; asset purchase or share purchase as instructed
5. **Negotiate APA** with counterparty / counterparty counsel
6. **Conditions satisfaction** — track and confirm each closing condition
7. **Closing**
8. **Post-closing checklist** — business licence, lease, regulatory registrations, PPSA discharges

---

### > $1,000,000 — See BUSINESS_ACQUISITION Strategy

Transactions exceeding $1,000,000 where an LOI is required are governed by the **BUSINESS_ACQUISITION Strategy**, not this Solution.

See: `../../STRATEGIES/BUSINESS_ACQUISITION/`

The Strategy defines four S-Levels ($1M–$10M) with proportionate LOI, diligence, and APA requirements.

---

## Conditional Branches

| Condition | Action |
|-----------|--------|
| Share purchase selected | Escalation flag; assess non-assignable assets driving the choice |
| VTB financing present | Escalation flag; VTB terms require separate instrument |
| Earnout present | Escalation flag; earnout mechanics drafted as schedule or separate agreement |
| Employees being assumed | Employment succession assessment; ESA obligations |
| Lease assignment required | Landlord consent track; confirm consent condition in APA |
| Regulatory licence is primary asset | Escalation flag; confirm assignability before proceeding |
| CRA clearance certificate required | Add as closing condition; monitor timeline |
| Agent-prepared APA received for Level 2+ | Escalation flag; reassess level classification |

---

## Issue Maps

| ID | Name | Relevance |
|----|------|-----------|
| IM-ACQ-01 | Deal Classification | Level determination at intake |
| IM-ACQ-02 | Transaction Structure | Asset vs. share purchase decision |
| IM-ACQ-03 | Diligence Scope | What to search and review by deal level |
| IM-ACQ-04 | Closing Conditions | Standard and deal-specific conditions |
| IM-ACQ-05 | Post-Closing Obligations | Regulatory registrations and transition items |

---

## Decision Lenses

| ID | Name | Application |
|----|------|-------------|
| DL-ACQ-01 | Deal Size Classification | Level 1 / 2 / 3 determination; handle threshold cases |
| DL-ACQ-02 | Asset vs. Share Purchase | Drivers and implications of each structure |
| DL-ACQ-03 | LOI vs. Straight-to-APA | When an LOI is warranted below Level 3 |
| DL-ACQ-04 | Diligence Proportionality | Calibrating diligence scope to deal size and risk |
| DL-ACQ-05 | Earnout and VTB Complexity | When payment structure triggers escalation |

---

## Regulatory Surfaces

| ID | Name | Jurisdiction |
|----|------|--------------|
| RS-ACQ-ON-01 | PPSA — Personal Property Security Act | Ontario |
| RS-ACQ-ON-02 | Employment Standards Act (employee succession) | Ontario |
| RS-ACQ-ON-03 | Municipal business licensing | Ontario (municipal) |
| RS-ACQ-FED-01 | HST — Going concern exemption (s. 167 election) | Federal (CRA) |
| RS-ACQ-FED-02 | CRA tax clearance certificate | Federal (CRA) |
| RS-ACQ-SEC-01 | Sector-specific licensing (AGCO, CPHO, etc.) | Ontario (sector-dependent) |

---

## Question Banks

| ID | Name | Use Case |
|----|------|----------|
| QB-ACQ-INTAKE | Acquisition Intake Questions | Initial scoping and level classification |
| QB-ACQ-DILIGENCE | Diligence Request List | Scaled by deal level |
| QB-ACQ-CLOSING | Closing Conditions Checklist | Pre-closing confirmation |
| QB-ACQ-POSTCLOSING | Post-Closing Checklist | Regulatory and administrative items |

---

## Required Gates

| Gate | Purpose |
|------|---------|
| Level classification confirmed (Level 1 or 2, or redirect to Strategy) | Before proceeding to pathway |
| Escalation conditions cleared or escalated | Before drafting |
| Diligence complete and reviewed | Before APA finalized (Level 2) |
| All closing conditions confirmed satisfied | Before closing |
| Post-closing checklist reviewed | Within 30 days of closing |

---

## Assembly Notes

- Level classification is based on total purchase price including all deferred and contingent consideration; do not classify on headline cash consideration alone
- Agent-prepared APAs at Level 1 vary significantly in quality; treat as a review mandate, not a negotiation mandate, unless specifically instructed otherwise
- At Level 3, the LOI sets the commercial framework; the APA should not re-open settled LOI points without a documented reason
- Component selection remains judgment-based; artifact presence does not imply necessity in every matter
