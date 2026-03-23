---
id: 02_playbooks__financial_services__payments__strategies__carf_program__strategy_architecture_md
title: Strategy Architecture: CARF Program (Minimum Viable but Defensible)
owner: ML1
status: draft
created_date: 2026-03-23
last_updated: 2026-03-23
tags: [financial-services, payments, carf, crypto, strategy]
---

# Strategy Architecture: CARF Program (Minimum Viable but Defensible)

## Architecture Summary

10 components delivered in dependency order. Components 1 and 2 are foundational
and must be completed before downstream components can be validly executed.
Components 3–8 are operational and may be parallelized. Components 9 and 10
are control and documentation layers that run across the full program.

## Component Sequence

```
[1] CARF_GOVERNANCE              ← must complete first
[2] CARF_SCOPING_AND_CLASSIFICATION  ← must complete before 3–8
        ↓
[3] CARF_CLIENT_ONBOARDING
[4] CARF_DUE_DILIGENCE
[5] CARF_TRANSACTION_CLASSIFICATION
[6] CARF_REPORTING_OUTPUT
[7] CARF_RECORDKEEPING
[8] CARF_AML_INTEGRATION
        ↓
[9] CARF_CONTROLS_AND_TESTING
[10] CARF_DOCUMENTATION          ← consolidates full program
```

## Dependency Rules

- Component 2 (Scoping and Classification) is the primary control point.
  Errors here invalidate downstream processes.
- Components 3–8 are operationally parallel but logically downstream of Component 2.
- Component 10 (Documentation) is the primary defensibility layer —
  it must reflect the outputs of all prior components.

## Orchestration Logic

- TBD
