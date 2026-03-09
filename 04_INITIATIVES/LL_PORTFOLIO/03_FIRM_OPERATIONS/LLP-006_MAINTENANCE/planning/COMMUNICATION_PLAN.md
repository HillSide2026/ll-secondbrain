# Communication Plan

Project ID: LLP-26-07
Project Path: 03_FIRM_OPERATIONS/LLP-006_MAINTENANCE
Stage: Planning

## Audiences
- ML1 (approval authority)
- Matter maintenance operator/orchestrator
- System maintainers for Clio/SharePoint/Asana connectors
- LLP-005 Matter Command consumers of reconciliation outputs

## Cadence

| Audience | Frequency | Artifact | Owner |
| --- | --- | --- | --- |
| ML1 | Weekly (Sunday/Monday) | Reconciliation summary + exception queue + prior-cycle diff | Matter Maintenance Orchestrator |
| Maintenance operator | Weekly | Run completion report and failure notes | Matter Maintenance Orchestrator |
| Connector maintainers | Event-driven + weekly | Integration fault and retry report | Matter Maintenance Orchestrator |
| LLP-005 stakeholders | Weekly | Reconciliation health status note | Matter Maintenance Orchestrator |

## Required Implementation Communications
- Run completion status (full, partial, failed)
- Exception counts by severity and by system
- Net movement since prior cycle (new/resolved/persisting exceptions)
- Items requiring ML1 judgment or authorization

## Escalation Triggers
- Any critical mismatch affecting Essential or Strategic matters
- Two consecutive missed Sunday runs
- Any unresolved critical exception older than 7 days
- Any connector failure preventing full-system reconciliation
