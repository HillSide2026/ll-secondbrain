# Dependencies

Project ID: LLP-004
Project Path: 03_FIRM_OPERATIONS/LLP-004_ONBOARDING
Stage: Planning

## Lifecycle Dependencies
- Gate model definition (Qualified Lead -> Engagement).
- Handoff contract to LLP-005 opening.

## Operational Dependencies
- Intake evidence stream (consult status + proceed intent).
- Engagement agreement templates/signature workflow.
- Clio pending matter creation and field consistency.
- Exception and run logging path under `06_RUNS/`.

## Governance Dependencies
- ML1 gate and threshold approvals.
- Boundary controls to prevent pre-authorization delivery.

## Dependency Risks
- Missing Gate 1 evidence blocks valid onboarding start.
- Template/signature delays reduce Gate 2 throughput.
- Pending-matter setup defects cause downstream opening mismatch.
