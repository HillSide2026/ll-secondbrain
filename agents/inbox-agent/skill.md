# Inbox Triage Agent — Skill

## Core Operating Rule

If a thread belongs to a matter, tag the matter.
If not, assign exactly one state label.

---

## Decision Order

1. Work at thread level only.
2. Attempt matter detection first.
3. If matter found → apply matter label and stop.
4. If no matter found → assign exactly one state label.
5. Never apply multiple state labels.

---

## Matter Authority Rule

Existing matter labels are authoritative.
Do not override unless there is strong contradictory evidence.

---

## Anti-Churn Rule

Do not change labels without new information — a new message or a material context change.

---

## Priority Interpretation Rule

Priority is not determined in Gmail.
Priority is inherited from the linked matter's delivery status.

---

## Failure Bias

When uncertain, assign `00_Triage`.
Do not guess a matter.

---

## Prohibited Actions

Do not:
- create synthetic priority labels
- split a thread across multiple state labels
- archive threads that may still require action
- downgrade a matter thread into a state label
