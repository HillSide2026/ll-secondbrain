# Canva MCP Server (Python, OAuth + PKCE)

`canva_bridge.py` now runs as a persistent stdio MCP server.

It supports:
1. One-time OAuth bootstrap with PKCE
2. Token reuse and automatic refresh for normal tool calls
3. Tool-callable Canva operations for design listing, lookup, and draft creation

Primary MCP tools:
- `auth_status`
- `start_oauth`
- `list_designs`
- `get_design`
- `create_design`

## Files
- `canva_bridge.py`
- `.env` (local, not committed)
- `tokens.json` (generated after successful callback)
- `oauth_state.json` (temporary state/verifier file)
- `.claude/settings.json` (project-level MCP registration)

## Environment
Use these variables in `.env`:

```env
CANVA_CLIENT_ID=
CANVA_CLIENT_SECRET=
CANVA_REDIRECT_URI=http://127.0.0.1:3000/oauth/callback
CANVA_SCOPES=design:meta:read design:content:write
SESSION_SECRET=
PORT=3000
CANVA_TOKEN_FILE=./tokens.json
CANVA_STATE_FILE=./oauth_state.json
```

Important:
- In Canva developer settings, the redirect URI must exactly match:
  - `http://127.0.0.1:3000/oauth/callback`

## Runtime Model

The server is registered in `.claude/settings.json` as the `canva` MCP server.
Claude starts it as a persistent background process and calls tools over stdio.

## OAuth Bootstrap

Initial auth still requires one browser consent step.

1. Ensure `.env` contains valid Canva client credentials.
2. Start Claude in this repo so the `canva` MCP server is available.
3. Call the `start_oauth` tool.
4. Open the returned `authorization_url` in a browser.
5. Complete Canva consent.
6. Canva redirects to `CANVA_REDIRECT_URI`, and the running MCP server exchanges the code and stores tokens in `tokens.json`.
7. Call `auth_status` until `authenticated` is `true`.

After that, normal Canva tool calls should work without repeating manual consent unless the refresh token becomes invalid.

## Notes

- `start_oauth` starts a local callback listener at `CANVA_REDIRECT_URI`.
- `create_design` defaults to creating a draft preset design using `presentation` unless a raw payload is supplied.
- All tool calls append lightweight audit entries to `06_RUNS/ops/canva_mcp_audit.ndjson`.
