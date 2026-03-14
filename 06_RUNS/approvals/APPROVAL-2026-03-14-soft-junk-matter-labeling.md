# Approval Record - Soft Junk Matter Labeling

- Date: 2026-03-14
- Approved by: ML1 (Matthew Levine)
- Scope: Add-only matter/state labeling for high-confidence matter-associated inbox threads found during Promotions/Social/Forums soft-junk review
- Query: `in:inbox (category:promotions OR category:social OR category:forums)`
- Review report: `06_RUNS/ops/soft_junk_review_20260314_174858Z.json`

Approved actions:

- Apply canonical matter labels only where the matter signal is determinative or high-confidence.
- Apply canonical state labels only where no state label already exists.
- Do not create labels.
- Do not remove labels.
- Do not archive or delete any threads under this approval.

Excluded from execution:

- Medium-confidence identity-name-key matches
- Ambiguous matter matches
- Soft-junk archive candidates
