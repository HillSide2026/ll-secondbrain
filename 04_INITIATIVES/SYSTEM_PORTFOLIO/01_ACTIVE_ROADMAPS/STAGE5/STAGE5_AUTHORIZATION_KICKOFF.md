# Stage 5 — Authorization & Kickoff

## Status
- Status: DRAFT (pending ML1 sign-off)
- Owner: ML1
- Date: 2026-01-26

## Purpose
Authorize implementation of system-level agents and read-only integrations.
This is the first stage that builds actual running infrastructure.

## Preconditions
- Stage 3 (Agent Orchestration) complete with agent roster and runbooks
- Stage 4 (Operating Rhythm) complete with cadence and governance rules
- Roadmap promoted to ACTIVE status

## Authorized Scope (Stage 5)

### Agent Implementation
Stage 5 is authorized to:
- Select agent runtime (Claude Code agents, MCP servers, or custom SDK)
- Create agent configurations and deployment artifacts
- Deploy all 5 system-level agents to operational state
- Test agent execution against runbooks

### Integration Activation
Stage 5 is authorized to:
- Create OAuth applications for Gmail API access (read-only scopes only)
- Configure Microsoft Graph API access for SharePoint (read-only)
- Configure OneDrive/Word document access (read-only)
- Implement audit logging per Stage 2 specifications
- Test integrations to verify no write paths exist

### Credential Handling
Stage 5 is authorized to:
- Create service accounts or OAuth apps as needed
- Store credentials in secure location (not in repo)
- Document credential inventory (names/locations, not secrets)
- Implement credential rotation reminders

## Not Authorized (Stage 5)
Explicitly prohibited:
- **Write operations** — No creating, updating, or deleting data in external systems
- **Matter data access** — No accessing client/matter-specific content
- **Automated scheduling** — No cron jobs, polling, or background automation
- **Doctrine changes** — No modifications to system doctrine
- **Production client use** — Testing only, no live client workflows

## Binding Inputs (Stage 5 must use these)

### From Stage 2 (Integration Specs)
Located at `10_ARCHIVE/INITIATIVES/SYSTEM_PORTFOLIO/STAGE2/`:
- STAGE2_GMAIL_READ_ONLY_SPEC.md — Gmail scopes and boundaries
- STAGE2_SHAREPOINT_READ_ONLY_SPEC.md — SharePoint access requirements
- STAGE2_WORD_READ_ONLY_SPEC.md — Document access patterns
- STAGE2_AUDIT_LOGGING_EXPECTATIONS.md — Logging requirements
- STAGE2_NO_WRITE_PATH_REVIEW.md — Write-path prohibition verification

### From Stage 3 (Agent Definitions)
Located at `01_ACTIVE_ROADMAPS/STAGE3/`:
- STAGE3_AGENT_ROSTER.md — 5 agent definitions
- STAGE3_HANDOFF_MAP.md — Agent interactions
- STAGE3_RUNBOOK_*.md — 5 agent runbooks
- STAGE3_METRICS_AND_CADENCE.md — Success metrics

### From Stage 4 (Operating Rules)
Located at `01_ACTIVE_ROADMAPS/STAGE4/`:
- STAGE4_OPERATING_CADENCE.md — Review rhythm
- STAGE4_AUDIT_CHECKLIST.md — Compliance checks

## Stage 5 Definition of Done (DoD)

### Agent Deployment
- [ ] Agent runtime selected and documented (SYS-001)
- [ ] System Governance Agent deployed and tested (SYS-005)
- [ ] Portfolio Planning Agent deployed and tested (SYS-006)
- [ ] Integration Steward Agent deployed and tested (SYS-007)
- [ ] Knowledge Curation Agent deployed and tested (SYS-008)
- [ ] Runbook & QA Agent deployed and tested (SYS-009)

### Integration Activation
- [ ] Gmail read-only integration active with audit logging (SYS-002)
- [ ] SharePoint read-only integration active with audit logging (SYS-003)
- [ ] Word/OneDrive read-only integration active with audit logging (SYS-004)
- [ ] No-write-path verification completed for all integrations

### Documentation
- [ ] Agent deployment guide created
- [ ] Integration configuration documented (no secrets in repo)
- [ ] Credential inventory documented
- [ ] Stage 5 closure recommendation prepared

## Stage 5 Workstreams

### Workstream A: Agent Runtime (SYS-001)
**Owner:** ML1
**Deliverables:**
- Runtime selection document (Claude Code vs MCP vs custom)
- Configuration approach
- Deployment strategy

### Workstream B: Agent Deployment (SYS-005 to SYS-009)
**Owner:** Runbook & QA Agent
**Deliverables:**
- Agent configuration files
- Deployment verification tests
- Agent operational status report

### Workstream C: Integration Activation (SYS-002 to SYS-004)
**Owner:** Integration Steward Agent
**Deliverables:**
- OAuth/API configuration
- Audit logging implementation
- No-write-path test results
- Integration operational status report

## ML1 Decisions Required

1. **Agent Runtime Choice:**
   - Option A: Claude Code agents (subprocess model)
   - Option B: MCP servers (tool-based model)
   - Option C: Custom SDK agents
   - **Recommendation:** [TBD by ML1]

2. **Credential Storage:**
   - Option A: Environment variables
   - Option B: Secrets manager (1Password, etc.)
   - Option C: Encrypted config file
   - **Recommendation:** [TBD by ML1]

3. **Integration Priority:**
   - Option A: All three in parallel
   - Option B: Gmail first, then SharePoint, then Word
   - Option C: SharePoint first (most documents)
   - **Recommendation:** [TBD by ML1]

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Wrong runtime choice | Medium | High | Prototype before full deployment |
| API rate limits | Medium | Medium | Implement backoff, document limits |
| OAuth scope creep | Low | High | Strict scope review, no write permissions |
| Credential exposure | Low | Critical | No secrets in repo, use secrets manager |
| Agent role confusion | Medium | Medium | Test against runbooks before deployment |

## Sign-Off
- ML1: ____________________  Date: __________

---

## Appendix: Agent Runtime Options

### Option A: Claude Code Agents
**Pros:**
- Native integration with current tooling
- Subprocess model familiar from this session
- Task tool provides orchestration

**Cons:**
- Limited persistence between sessions
- Manual invocation required

### Option B: MCP Servers
**Pros:**
- Tool-based model with clear boundaries
- Can expose integrations as tools
- Better for automation

**Cons:**
- Requires MCP server setup
- Different programming model

### Option C: Custom SDK Agents
**Pros:**
- Full control over agent behavior
- Can implement exact runbook logic

**Cons:**
- Most development effort
- Maintenance burden
