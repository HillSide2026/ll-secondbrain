---
id: DOCTRINE-RISK-0005
title: Risk Classification Invariants
owner: ML1
status: draft
version: 1.0
created_date: 2026-03-13
last_updated: 2026-03-13
tags: [doctrine, invariant, risk]
---

# DOCTRINE-RISK-0005 - RISK CLASSIFICATION INVARIANTS

## 1. Purpose

Define non-negotiable invariants for how risks are classified, labeled, and decomposed across initiative artifacts.

## 2. Invariants

1. Every canonical risk statement must be assignable to exactly one canonical category.
2. Canonical categories are limited to `Scope`, `Schedule`, `Budget`, `Financial`, and `Strategic`, subject to portfolio and work-type applicability rules.
3. A risk statement must describe the exposure itself, not the mitigation, owner, or control response.
4. If one sentence contains more than one category, it must be split into separate risk statements.
5. `RISK_SCAN.md` may be narrative, but each listed risk must still classify cleanly.
6. `RISK_REGISTER.md` must assign one explicit category to each risk row.
7. Legacy labels such as `Primary`, `Control`, `Execution`, `Governance`, and `Residual` are not canonical categories.
8. Category names must use canonical capitalization and wording exactly as defined by doctrine.
9. A `Budget` risk exists only where there is an explicit or implied spend ceiling, approved budget, or tracked spending baseline.
10. `Financial` risk is distinct from `Budget` risk: it covers broader capital or transaction exposure and is not limited to budget overrun.

## 3. Traceability Rule

Every canonical risk artifact must make it possible to answer:
- what the risk is
- which category it belongs to
- why that category applies
- which initiative, project, or matter the risk belongs to

## 4. Portfolio Applicability

- Levine Law initiatives follow `DOCTRINE-RISK-0003`.
- Matthew Holdings initiatives follow `DOCTRINE-RISK-0004`.
- Generic lifecycle artifact requirements remain governed by `DOCTRINE-RISK-0002`.

## 5. Related Doctrine

- `01_DOCTRINE/01_INVARIANTS/DOCTRINE-RISK-0001-risk-model.md`
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0002-project-risk-artifact-lifecycle-policy.md`
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0003-ll-initiative-risk-policy.md`
- `01_DOCTRINE/03_POLICIES/DOCTRINE-RISK-0004-matthew-holdings-initiative-risk-policy.md`
