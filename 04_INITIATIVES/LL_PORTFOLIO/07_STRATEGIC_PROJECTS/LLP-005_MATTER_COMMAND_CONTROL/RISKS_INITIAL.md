# Initial Risks

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| Label drift in Gmail hierarchy reduces routing accuracy | High | Medium | Enforce regex + unmapped exception stream + ML1 review queue |
| SharePoint folder naming inconsistency breaks folder mapping | High | Medium | Deterministic naming rule + explicit `matter_sharepoint_map.yml` overrides |
| Source assertion without citation pointer | High | Low | Hard requirement in output contract; omit assertion if citation missing |
| Scope creep into shadow database behavior | High | Medium | Restrict persisted state to caches + derived artifacts only |
| False confidence from fallback heuristics | Medium | Medium | Mark fallback routes as ML1 review-required |
