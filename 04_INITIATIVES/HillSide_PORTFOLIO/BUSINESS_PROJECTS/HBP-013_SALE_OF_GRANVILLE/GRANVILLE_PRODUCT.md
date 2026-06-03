---
id: hbp-013-granville-product
title: Granville Finance — Product Description
owner: ML1
status: draft
created_date: 2026-05-31
last_updated: 2026-05-31
tags: [granville, product, payments, orchestration, hbp-013]
---

# Granville Finance — Product Description

## What Granville Is

Granville Finance is a payment orchestration platform for businesses that need to move money across borders. It sits between a business's product and its payment providers — EMI accounts, bank rails, FX — and handles the infrastructure layer that makes payments reliable, auditable, and operable at scale.

The core offer is a provider-portable orchestration layer: connect multiple payment rails, route each payment to the best available provider based on rules (currency, country, amount, provider health), and fail over automatically if a provider goes down. Switching providers or adding new ones does not require rebuilding the integration.

---

## Core Capabilities

**Provider-portable orchestration**
Connect multiple payment rails and route each payment to the best available provider based on configurable rules: currency, country, amount, provider health. Automatic failover if a provider goes down. Switching or adding providers does not require rebuilding the integration.

**Ledger integrity**
Every payment, settlement, and reconciliation event is recorded as an immutable double-entry posting via Formance Ledger. The audit trail is always complete and replayable.

**Continuous reconciliation**
Transaction-level reconciliation runs automatically. Mismatches, missing provider transactions, amount discrepancies, and stale pending payments surface as typed exceptions with evidence attached.

**Operational tooling**
An operator console for approving payments, retrying failed webhooks, replaying dead-lettered ledger postings, and managing provider health. Designed for ops and compliance teams, not just engineers.

**Durable event processing**
Webhooks, provider commands, and ledger postings all go through queue-backed workers with idempotency and dead-letter handling. Nothing is silently lost.

---

## Purpose

The problem Granville solves: the infrastructure layer under a payments product — provider integration, reconciliation, audit trails, failover — is expensive to build and fragile to maintain. Every new provider requires a new integration. Reconciliation is typically an afterthought.

Granville packages this infrastructure so businesses do not have to build it themselves.

The design philosophy is institutional-grade from the start: deterministic, replay-safe, audit-ready, and multi-provider by design rather than retrofit.

---

## Target Customer

**Who Granville is for:**

Founders with less than $1M in revenue and small businesses up to $10M in revenue, across e-commerce, SaaS, marketplaces, agencies, and professional services. The defining characteristic is international exposure — these businesses are moving money across borders and need more than a single provider can reliably deliver.

The founder makes the buying decision. This is not a technical purchase driven by a CTO or engineer — it is a founder who has hit a wall with their current payments setup and needs a more reliable, auditable infrastructure layer.

**Who Granville is not for:**

- Freelancers
- Pure crypto businesses
- Regulated financial institutions, including MSBs

**Open items — to be confirmed:**

- Direction of cross-border flow: receiving foreign revenue, sending internationally, or multi-currency treasury management — primary pain not yet confirmed
- Triggering event: what specifically breaks first for the target customer — single provider failure, reconciliation breakdown, new market entry, or hitting provider limits
- Industry narrowing: all five sectors (e-commerce, SaaS, marketplaces, agencies, professional services) are in scope for now; to be narrowed as distribution channels become clearer

---

## Relationship to 174

Granville Finance is the market-facing brand and product layer. `17409052 Canada Inc` (174) is the regulated corporate entity that holds the FINTRAC and RPAA credentials underpinning the platform.

The Granville brand and domain (`granvillefinance.ca`) travel with the entity on sale unless ML1 directs otherwise.

---

## Open Items

- EMI: Airwallex is primary candidate (pending). Modulr is secondary.
- Formance Ledger: procurement and integration status TBC
- Rhizome vs Sumsub: Rhizome is default unless EMI requires Sumsub
- Product software candidates: see `VALUE_STACK.md`
