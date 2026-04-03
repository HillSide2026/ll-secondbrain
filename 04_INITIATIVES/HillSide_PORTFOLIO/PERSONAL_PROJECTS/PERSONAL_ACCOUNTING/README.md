---
id: 04_initiatives__hillside_portfolio__personal_projects__personal_accounting__readme_md
title: Personal Accounting
owner: ML1
status: draft
created_date: 2026-04-03
last_updated: 2026-04-03
tags: [hillside, personal-projects, accounting, personal-accounting]
---

# Personal Accounting

This folder is the placeholder container for ML1 personal accounting.

## Current State

- placeholder only
- repo-side governance pointer, not the storage location for raw statements
- intended to support `HBP-001_WEALTH_MANAGEMENT` and `HBP-002_CASH_FLOW`
  with cleaner personal source records over time
- ML1 personally owns `17513721 Canada Inc` and `Levine Professional Corporation`,
  but those entities still require distinct accounting boundaries

## Purpose

Create a governed place for the personal accounting fact layer so statements,
supporting schedules, reconciliation readiness, and close discipline have a
clear home on the personal side of the HillSide repo.

## In Scope

- personal accounting fact-layer definition
- monthly and periodic source-record intake discipline
- bank, brokerage, credit-card, and tax-source record expectations
- boundary rules between personal records and records of personally owned
  corporations
- reconciliation readiness and handoff to downstream wealth and cash-flow work
- definition of the secure external evidence-vault relationship

## Out Of Scope

- storing raw bank or brokerage statements in git
- wealth modeling, budgeting, or strategic recommendations
- replacing a bookkeeping system, accountant, or CPA workflow
- treating accounting facts as decision authority without ML1 review

## Placeholder Rule

The actual master accounting evidence vault should live outside this repo in a
secure document system. This folder exists so the governance, scope, and
downstream dependencies have an explicit placeholder now rather than remaining
implicit.

## Likely Next Artifacts

- `SOURCE_RECORD_MAP.md`
- `MONTHLY_CLOSE_CHECKLIST.md`
- `ACCOUNT_LIST.md`
- `EVIDENCE_VAULT_SPEC.md`
