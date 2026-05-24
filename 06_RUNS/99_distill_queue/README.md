---
id: 06_runs_99_distill_queue_readme_md
title: Distill Queue
owner: ML2
status: draft
created_date: 2026-05-24
last_updated: 2026-05-24
tags: []
---

# Distill Queue

Rule: Every run ends in exactly one outcome.

Outcomes:
1. Promote
2. Park
3. Archive

When outcome is PARK, create a stub in this folder named:
- `YYYY-MM-DD__<run_id>__<short_slug>.md`

Stub contents (minimum):
- What to distill
- Candidate target (template/playbook/doctrine)
- Blocking questions (if any)
- Canon refs (exact paths)
