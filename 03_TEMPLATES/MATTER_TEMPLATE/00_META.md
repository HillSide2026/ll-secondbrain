---
id: 03_templates__matter_template__00_meta_md
title: Matter Metadata
owner: ML1
status: draft
created_date: 2026-02-08
last_updated: 2026-02-08
tags: []
---

# Matter Metadata

## Three-Field Status Model

```yaml
status: unknown
delivery_status: unknown
fulfillment_status: unknown
```

## Field Definitions

### status (Clio Matter Status) — METADATA
- Source: Clio
- Values: Open | Pending | Closed
- Stored as metadata field

### delivery_status (Lawyer Attention Priority) — DIRECTORY
- Source: ML1 / lawyer
- Values: Essential | Strategic | Standard | Parked
- Determines directory location in 05_MATTERS/

### fulfillment_status (Admin Workload State) — METADATA
- Source: Admin team / ops
- Values: urgent | active | keep in view | dormant
- Stored as metadata field

---

## Matter Information

```yaml
matter_id:
matter_name:
client:
practice_area:
opened_date:
```

---

## Notes

- Each field is independently set
- Do not infer one field from another
- If unknown, request explicit input from ML1 or admin
