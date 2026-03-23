---
id: 02_playbooks__financial_services__solutions__carf_aml_integration__solution_scope_md
title: Solution Scope: CARF AML/KYC Integration
owner: ML1
status: draft
created_date: 2026-03-23
last_updated: 2026-03-23
tags: [financial-services, payments, carf, aml, integration]
---

# Solution Scope: CARF AML/KYC Integration

Component 8 of CARF_PROGRAM.

## Purpose

Defines the relationship between existing AML/KYC infrastructure and CARF
requirements. Partial reuse of AML infrastructure is possible but not complete.

## Reusable from AML

- Identity verification
- Core client data

## Not Directly Reusable

- Tax residency data (CARF-specific)
- CARF-specific trigger logic
- Data validation standards

## Included

- Separate CARF data fields defined
- Mapping between AML profiles and CARF profiles
- Integration gap analysis

## Excluded

- AML program build or redesign (separate engagement)
- CARF client onboarding controls (CARF_CLIENT_ONBOARDING)
