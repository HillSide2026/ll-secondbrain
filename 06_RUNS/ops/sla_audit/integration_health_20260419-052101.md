---
run_id: 20260419-052101
timestamp: 2026-04-19T05:21:01.716531Z
type: integration_health_check
sla: SLA-SYS-001
classification: internal_working_material
---

# Integration Health Check
**Run:** 20260419-052101  
**Overall:** FAIL

## Results

| Integration | Status | Issue |
|---|---|---|
| .mcp.json → gmail | FAIL | Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/gmail_mcp_server.py |
| .mcp.json → sharepoint | FAIL | Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/sharepoint_mcp_server.py |
| .claude/settings.json → PreToolUse hook | FAIL | Path exists but is not executable: /Users/matthewlevine/Repos/ll-secondbrain_fresh/scripts/validate_canonical_write.py |
| .claude/settings.json → mcpServer:sharepoint | FAIL | Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/sharepoint_mcp_server.py |
| .claude/settings.json → mcpServer:gmail | FAIL | Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/gmail_mcp_server.py |

## Failures

- **.mcp.json → gmail**: Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/gmail_mcp_server.py
- **.mcp.json → sharepoint**: Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/sharepoint_mcp_server.py
- **.claude/settings.json → PreToolUse hook**: Path exists but is not executable: /Users/matthewlevine/Repos/ll-secondbrain_fresh/scripts/validate_canonical_write.py
- **.claude/settings.json → mcpServer:sharepoint**: Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/sharepoint_mcp_server.py
- **.claude/settings.json → mcpServer:gmail**: Path does not exist: /Users/matthewajlevinelaw/Repos/ll-secondbrain/scripts/gmail_mcp_server.py