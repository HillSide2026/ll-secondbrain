---
id: POL-022
title: Worker Scope Limitation
owner: ML1
status: active
version: 1.0
created_date: 2026-03-08
last_updated: 2026-03-08
tags: [policy, workers, scope]
---

# POL-022 — Worker Scope Limitation

Policy Statement: Each worker invocation must have an explicit bounded task definition, including purpose, allowed inputs, and expected outputs.
Authority (Principles referenced): PRN-023, PRN-028
Enforcement expectation: Worker invocations lacking explicit task bounds are non-compliant and must not execute.
Supersedes: None
Version: 1.0
Status: Active
