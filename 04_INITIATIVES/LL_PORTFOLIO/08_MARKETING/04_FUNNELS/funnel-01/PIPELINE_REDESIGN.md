---
id: funnel-01-pipeline-redesign
title: Funnel 01 — GHL Pipeline Redesign Analysis
owner: ML1
status: draft
created_date: 2026-04-26
last_updated: 2026-04-26
tags: [funnel-01, ghl, pipeline, redesign]
---

# Funnel 01 — GHL Pipeline Redesign Analysis

## Core Diagnosis

The current pipeline is doing too much stage-based babysitting and not enough intake control.

The current stages mix four different things with no separation:

| Category | Current Stages |
|----------|---------------|
| Lead status | New Inquiry / Lead, Outbound - No Answer, Unresponsive |
| Qualification status | Pending Qualification, Disqualified |
| Appointment status | Consultation Booked, Rescheduled / No-Show, Consultation Completed |
| Sales status | Engagement Sent, Retained (Closed - Won), Closed - Not Proceeding |

This makes reporting muddy and lets a weak setter hide behind stage movement instead of measurable actions.

---

## Proposed Changes

### 1. Reduce Stages to Actual Revenue Milestones

Recommended core pipeline (9 stages):

1. New Lead
2. Contact Attempted
3. Qualified / Needs Booking
4. Consult Booked
5. Consult Completed
6. Engagement Sent
7. Retained / Won
8. Closed Lost
9. Disqualified

Move "No Answer," "Unresponsive," "No-Show," and "Rescheduled" out of pipeline stages entirely. These belong in tags, tasks, appointment status, or custom fields — not as stage parking lots.

### 2. Use Tasks to Supervise the Setter

The setter should not "manage the pipeline" manually. GHL should assign required tasks triggered by stage entry:

- Call within 5 hours of lead capture
- Send SMS immediately
- Second call same day
- Follow-up next day
- Mark lead outcome (qualify or disqualify — no parking)
- Book consult or disqualify

The PPC intake SLA (call within 5 hours) should become an enforced workflow task, not a vague expectation. Stage movement is not a substitute for completing required actions.

### 3. Build Reporting Around the Real Bottlenecks

The business target is not "move cards around." The three ratios that matter:

| Conversion | Target |
|-----------|--------|
| Lead → Consult Scheduled | 25–30% |
| Consult → Paid Project | 40–50% |
| Lead → Paid Project | 8–10% |

The pipeline structure should make those three ratios directly readable without manual calculation.

### 4. Separate Disqualification Reasons

"Disqualified" alone is not actionable. Add a required custom field: **Disqualification Reason**

- Wrong legal area
- Too small / low budget
- Geography issue
- Needs litigation
- Wants free advice
- Not ready
- Duplicate / spam
- Bad contact info

This exposes whether the problem is PPC quality, intake quality, or offer fit — three different diagnoses with three different fixes.

### 5. Add Offer and Source Tracking

Each opportunity should carry:

**Lead Source** (custom field or GHL source field):
- Google Ads
- Referral
- Organic
- Manual

**Offer Interest** (custom field):
- Incorporation
- Shareholder Agreement
- Shareholder Conflict
- Corporate Advisory
- Shareholder Changes
- Small Business Acquisition

These offers are distinct enough that they should not be treated as one generic "corporate law" bucket.

### 6. Replace Stage-Parking with Automation

"No answer," "unresponsive," and "pending qualification" should trigger automation, not become holding areas.

Use instead:
- **Tags:** `status_no_answer`, `status_unresponsive`
- **Tasks:** "Call attempt 2 due" (auto-assigned with deadline)
- **Custom fields:** `last_contact_attempt`, `call_attempt_count`
- **Workflow branches:** auto-trigger on no reply within defined window

---

## Summary

The current pipeline is designed as a visual holding area. It needs to become a conversion control system. The redesign reduces stages to revenue milestones, enforces setter accountability through tasks and automation, and makes the three core conversion ratios directly measurable.

---

## Status

- [ ] ML1 approval of redesign direction
- [ ] GHL workflow design (tasks + automation triggers)
- [ ] Custom fields spec (disqualification reason, offer interest, lead source)
- [ ] Stage migration plan (existing opportunities)
- [ ] Implementation

## Change Log

- 2026-04-26 — Initial analysis drafted. Diagnosis: pipeline mixing four category types. Proposed: 9-stage revenue-milestone structure + task enforcement + custom fields.
