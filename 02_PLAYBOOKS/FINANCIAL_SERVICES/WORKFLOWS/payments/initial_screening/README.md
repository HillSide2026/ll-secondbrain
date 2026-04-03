---
id: 02_playbooks__financial_services__payments__initial_screening__readme_md
title: Initial Screening — Payments
owner: ML1
status: draft
version: 1.0
supersedes:
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [financial-services, payments, screening, token, stablecoin, securities]
---

## Playbook Header
Playbook ID: 02_playbooks__financial_services__payments__initial_screening__readme_md
Version: 1.0
Status: draft

Principles Referenced: PRN-001, PRN-002, PRN-003, PRN-004, PRN-006, PRN-009
Policies Applied: POL-004, POL-006, POL-009, POL-011
Protocols Enforced: PRO-004, PRO-006, PRO-009, PRO-011
Doctrine Invoked: 00_SYSTEM/constitution.md, 01_DOCTRINE/index.yaml

Inputs: intake facts, product description, marketing copy, routing question
Outputs: initial screening note, regime-routing recommendation, touchability assessment
Acceptance Criteria: mandatory trigger fact patterns are screened; routing and escalation outputs are explicit


# Initial Screening — Payments

Internal front-door screening workflow for token, stablecoin, crypto-enabled
payments, custody, marketplace, and hybrid regulatory matters.

This workflow is designed to prevent premature routing, premature comfort, or
premature outward claims where securities, money-services, and payment-services
issues may overlap.

---

## When To Use

Use this workflow before consult booking, scope proposal, or outward positioning
when the intake involves any of the following:

- token issuance, distribution, or presale
- stablecoin or value-referenced crypto asset features
- custody, control, safeguarding, or contractual claims to crypto assets
- platform matching, secondary trading, or exchange functionality
- staking, yield, fee-sharing, rebate, or reward features
- hybrid payment / MSB / securities fact patterns

---

## Contents

| File | Purpose |
|------|---------|
| [ARE_THERE_SECURITIES_ISSUES.md](ARE_THERE_SECURITIES_ISSUES.md) | First-pass securities screening note covering issuer and dealer questions in the Muggah Securities posture |
| [ARE_THEY_AN_MSB.md](ARE_THEY_AN_MSB.md) | First-pass MSB / FINTRAC screening note prepared in the Muggah Money Services posture |
| [ARE_THEY_A_PSP.md](ARE_THEY_A_PSP.md) | First-pass PSP / RPAA screening note prepared in the Muggah Payment Services posture |
| [acceptance.md](acceptance.md) | Acceptance criteria for this workflow |
| [steps.yaml](steps.yaml) | Workflow step map |
