# Stage 2 Cross-Integration Comparison Matrix

## Systems Compared
- Gmail
- SharePoint
- Microsoft Word

## Approaches Evaluated
- API
- Connector
- Export

## Comparison Dimensions
- Read-only scope fidelity
- Audit/logging support
- Permission complexity
- Rate limits / throttling
- Administrative overhead
- Policy/compliance risk

## Summary Table
| System | Read-only scope fidelity | Audit/logging support | Permission complexity | Rate limits / throttling | Administrative overhead | Policy/compliance risk |
| --- | --- | --- | --- | --- | --- | --- |
| Gmail | High for message metadata and bodies within mailbox scope. | API access logs supported; scope usage must be documented. | Medium (mailbox scope approvals, delegated access decisions). | API quotas and per-user limits apply. | Medium (scope governance and mailbox selection). | Medium (email sensitivity and retention constraints). |
| SharePoint | High for site/library metadata and document access within approved sites. | Site/library access logs where enabled; tenant-level audit varies. | High (site/library permissions and tenant policies). | API throttling and paging limits likely. | High (site selection, permissions coordination). | Medium-High (content sensitivity and tenant policy constraints). |
| Microsoft Word | Medium-High for document content and basic structure within approved repositories. | Audit support depends on repository provider; document-level access logs may vary. | Medium (repository-level permissions). | Repository or API limits vary by storage system. | Medium (repository identification and access mapping). | Medium (document sensitivity and format exclusions). |

## Constraints and Assumptions
- No live credential testing performed.
- Documentation and admin confirmation only.

## Observations
- Gmail offers consistent read-only access patterns but is sensitive to mailbox scope and retention rules.
- SharePoint presents the highest permissions complexity due to tenant-level policy and site variability.
- Word document access fidelity depends on repository controls and may vary across storage systems.

## Open Questions
- Which approach minimizes compliance risk?
- Which approach best supports future Stage 3 sequencing?
