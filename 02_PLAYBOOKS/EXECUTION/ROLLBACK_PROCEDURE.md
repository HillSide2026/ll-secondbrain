# Rollback Procedure — Stage 2.5

## Purpose

Provide a deterministic method to reverse a single supervised action.

---

## Rollback Triggers

- Execution error
- ML1 reversal request
- Governance failure identified post-execution

---

## Rollback Steps

1. Identify executed action via execution log
2. Determine rollback method:
   - Move reversal
   - Label removal
   - Placeholder artifact deletion
3. Execute rollback
4. Verify system state matches pre-execution condition
5. Record rollback event in execution log

---

## Constraints

- Rollback must be possible for every permitted action
- If rollback is not possible, the action must not be executed

---

## Notes

- Rollback does not erase history
- Original execution and rollback are both preserved
