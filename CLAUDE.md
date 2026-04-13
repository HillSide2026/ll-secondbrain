# CLAUDE.md — Agent Instructions for ll-secondbrain_fresh

## Integration and Tool Access Rules

### MCP Servers

Two MCP servers are registered for this repo. Both appear in `.mcp.json` (project-level) and in `.claude/settings.json` (local settings with hooks):

| Server | Script | Purpose |
|--------|--------|---------|
| `gmail` | `scripts/gmail_mcp_server.py` | Read Gmail inbox; controlled label writes |
| `sharepoint` | `scripts/sharepoint_mcp_server.py` | Read SharePoint folder/item metadata |

`.claude/settings.json` additionally defines the `PreToolUse` hook that validates all Write/Edit operations via `scripts/validate_canonical_write.py`. This is the only intentional split between the two config files.

**Before claiming a tool is unavailable**, use ToolSearch to check whether it loaded. If a tool is missing, check `.mcp.json` — do not assume it does not exist.

Full tool surface documented in:
- `00_SYSTEM/integrations/gmail/README.md`
- `00_SYSTEM/integrations/sharepoint/README.md`

### Gmail / Inbox

- **Gmail inbox** = `Matthew@levinelegalservices.com`, accessed via the `gmail` MCP server (`list_messages`, `get_message`, `list_threads`, `get_thread`)
- **09_INBOX** = ML2's in-tray pipeline for processed data (SharePoint metadata, drive sync, etc.) — this is NOT the Gmail inbox
- Never conflate these two. When asked to check the inbox, use the Gmail MCP.

### SharePoint

- The SharePoint MCP provides **folder and item metadata only** — it cannot read file content
- Locally synced raw files exist only for the Stream matter (`09_INBOX/_sources/sharepoint/raw/legalmatters_library/LL Matters (Essential)/24-682-00003 -- Stream`)
- The authoritative map of what is in SharePoint is: `09_INBOX/_sources/sharepoint/raw/legalmatters/phase2_enumeration.json`
- For all other matters, use `list_folder` via SharePoint MCP to enumerate live — do not assume files are missing because they are not locally synced

---

## Matter Index Governance

`05_MATTERS/INDEX.md` is updated on explicit ML1 instruction only. Do not modify it as part of any automated pipeline or housekeeping task.

## Lawyer Task Tracker Governance

`05_MATTERS/LAWYER_TASK_TRACKER.md` is maintained by the system subject to ML1 override.

- When ML1 marks a task as Done, move it to the Completed section. Do not delete it.
- Before adding any new task, check the Completed section. If the same task has already been completed on this matter, do not recreate it. A follow-up task is a new task with a distinct description — it is not the same task.
- Tasks are added by the system when ML1 directs it. Do not infer or auto-generate tasks from emails or other sources without ML1 instruction.
