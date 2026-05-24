---
id: 06_runs_inbox_governance_pro_018_soft_junk_approvals_approval_2026_03_14_pro018_soft_junk_selected_archive_md
title: Approval Record - PRO-018 Selected Soft-Junk Archive
owner: ML2
status: draft
created_date: 2026-05-24
last_updated: 2026-05-24
tags: []
---

# Approval Record - PRO-018 Selected Soft-Junk Archive

- Date: 2026-03-14
- Approved by: ML1 (Matthew Levine)
- Protocol lane: `PRO-018`
- Source review: `06_RUNS/INBOX_GOVERNANCE/PRO-018_SOFT_JUNK/reviews/soft_junk_review_20260314_181534Z.json`
- Action: archive approved soft-junk cleanup candidates by removing `INBOX` only

Approved selection basis:

- approved sender strings explicitly listed by ML1
- approved thread ids explicitly listed by ML1
- only where `soft_junk_cleanup_candidate = true` in the source review

Execution constraints:

- do not trash
- do not delete
- do not create labels
- do not remove labels other than `INBOX`
- do not include matter-matched or review-required exclusions unless explicitly approved by thread id
