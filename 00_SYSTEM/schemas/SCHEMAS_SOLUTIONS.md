---
id: 00_system__schemas_solutions_md
title: Solutions — Schema
owner: ML1
status: draft
created_date: 2026-02-24
last_updated: 2026-02-24
tags: [schema, solutions]
---

# Solutions — Schema

**Status:** Draft

---

## Data Model — Solution Object

```json
{
  "solution_id": "string",
  "matter_id": "string",
  "solution_name": "string",
  "solution_type": "enum",
  "fee_model": "enum",
  "est_value": "number",
  "probability_of_close": "number",
  "solution_stage": "enum",
  "production_owner": "string",
  "estimated_effort_hours": "number",
  "hours_logged": "number",
  "invoice_id": "string | null",
  "amount_billed": "number",
  "amount_collected": "number",
  "created_at": "timestamp",
  "last_updated": "timestamp"
}
```

## solution_type Enum Values
- business_acquisition
- corporate_advisory
- incorporation
- shareholder_agreement
- shareholder_change
- shareholder_conflict
- customer_agreement
- intercompany
- licensing
- nda_confidentiality
- service_agreement
- vendor_agreement
- fintrac_response
- msb_intake_and_registration
- msb_review
- rpaa_registration
- rpaa_three_year_review
- solution_packet_template (template-only; not valid for live matters)

## fee_model Enum Values
- flat_fee
- hourly_paid_on_invoice
- hourly_with_retainer
- subscription

## solution_stage Enum Values
- identified
- scoped
- approved
- in_production
- client_review
- awaiting_external
- delivered
- billed
- collected
