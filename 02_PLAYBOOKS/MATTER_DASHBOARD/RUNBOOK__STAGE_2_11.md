# Runbook — Matter Dashboard (Stage 2.11)

## When to Run
- Business days (Mon–Fri)
- During business hours (09:00–17:00)
- Typically hourly, by manual invocation

---

## Preconditions
- OAuth authenticated
- Boundary guard passes
- Ledger accessible and writable

---

## Execution Steps
1. Load environment + auth
2. Verify Drive boundary
3. Snapshot inputs (matter registry, mappings)
4. Run dashboard reconciliation
5. Apply permitted ledger writes
6. Generate run log
7. Exit cleanly

---

## Failure Handling
- Boundary failure → immediate refusal
- Input ambiguity → NO-OP + needs_review
- Write conflict → preserve human data + log

---

## Outputs
- Updated ledger (if applicable)
- Run log under `06_RUNS/`
