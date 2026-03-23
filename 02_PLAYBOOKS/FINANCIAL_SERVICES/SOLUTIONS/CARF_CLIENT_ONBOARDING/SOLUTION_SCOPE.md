---
id: 02_playbooks__financial_services__solutions__carf_client_onboarding__solution_scope_md
title: Solution Scope: CARF Client Onboarding
owner: ML1
status: draft
created_date: 2026-03-23
last_updated: 2026-03-23
tags: [financial-services, payments, carf, onboarding]
---

# Solution Scope: CARF Client Onboarding

Component 3 of CARF_PROGRAM. Depends on CARF_SCOPING_AND_CLASSIFICATION.

## Purpose

Operationalizes CARF obligations at client onboarding. Ensures tax residency and
required identifying information is captured at the point of onboarding.

## Included

- Data collection requirements:
  - Tax residency (self-certification)
  - Jurisdiction(s)
  - Identifying information: name, address, date of birth
- CARF-specific self-certification added to onboarding flow
- Control: absence of valid certification results in restricted functionality
  or flagged account status

## Excluded

- Reliance on AML/KYC data alone — CARF requires separate self-certification
- Due diligence re-verification triggers (CARF_DUE_DILIGENCE)
