---
id: PRO-016
title: Fulfillment Stage Classification and Handoff
owner: ML1
status: draft
version: 0.2
created_date: 2026-03-09
last_updated: 2026-03-09
tags: [protocol, fulfillment, lifecycle, handoff, gates]
---

# PRO-016 — Fulfillment Stage Classification and Handoff

Enforces Policies: POL-034, POL-032, POL-033

Trigger condition:
- A fulfillment run, workflow, checklist, or artifact is created, updated, or promoted.
- A fulfillment stage transition is requested.
- A marketing conversion handoff is requested into fulfillment.

Required stage taxonomy:
- `onboarding` (`LLP-004`)
- `opening` (`LLP-005`)
- `maintenance` (`LLP-006`)
- `closing` (`LLP-008`)

Normalization rules:
- Canonical fulfillment stages must use the taxonomy above.
- `conversion` is a marketing-stage label; it may be accepted only as an inbound handoff alias and must be normalized to `onboarding` in canonical structured fields.
- `intake` and `inquiry` are marketing terms and are not valid fulfillment stages.
- `accounts` and `admin` are cross-cutting functions and must not be used as fulfillment stage values.

Protocol steps:
1. Classify each governed fulfillment artifact/run with exactly one fulfillment stage from the required taxonomy.
2. Validate stage sequence and prohibit skipping: `onboarding -> opening -> maintenance -> closing`.
3. For entry to `onboarding`, verify Gate 1 evidence exists (qualified lead criteria and client intent to proceed).
4. During `onboarding`, enforce matter status `pending` until engagement agreement is signed.
5. For transition to `opening`, verify Gate 2 evidence exists (engagement agreement signed) and confirm matter status transition to `open`.
6. For transition to `maintenance`, verify Gate 3 evidence exists (opening controls complete and internally approved).
7. For transition to `closing`, verify fulfillment closure preconditions and explicit ML1 approval artifact.
8. Execute handoff controls:
   - Marketing `conversion` handoff enters fulfillment as `onboarding`.
   - Post-`closing` records are routed to non-fulfillment closed/archive handling under governing doctrine.

Block condition:
- Stage value not in required fulfillment taxonomy.
- More than one fulfillment stage assigned to the same governed artifact/run.
- Stage skip or out-of-order transition.
- `onboarding` asserted without Gate 1 evidence.
- Matter status is `open` before engagement agreement signature.
- `opening` asserted without Gate 2 evidence and status transition proof.
- `maintenance` asserted without Gate 3 completion evidence.
- `closing` asserted without closure preconditions and ML1 approval artifact.
- `accounts` or `admin` used as stage values rather than cross-cutting functions.

Escalation path:
- Escalate ambiguous stage assignment, missing gate evidence, status-transition conflict, or handoff conflict to ML1.

Logging requirement:
- Record stage classification, normalization behavior, gate evidence references, `pending/open` status checks, transition decision, handoff target, and any block/escalation event in run artifacts.

Version: 0.2
Status: Draft
