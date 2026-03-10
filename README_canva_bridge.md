# Canva Bridge (Python, OAuth + PKCE)

This bridge proves local Canva connectivity by:
1. Completing OAuth 2.0 Authorization Code flow with PKCE
2. Calling `GET https://api.canva.com/rest/v1/designs`
3. Calling `POST https://api.canva.com/rest/v1/designs` to create a test design titled **SB Connection Test**

The server exposes exactly two routes:
- `GET /oauth/start`
- `GET /oauth/callback`

## Files
- `canva_bridge.py`
- `.env` (local, not committed)
- `tokens.json` (generated after successful callback)
- `oauth_state.json` (temporary state/verifier file)

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

## Run Instructions

1. Ensure `.env` contains valid Canva client credentials.
2. Start the bridge:

```bash
python3 canva_bridge.py
```

3. In browser, open:

```text
http://127.0.0.1:3000/oauth/start
```

4. Complete Canva consent in the browser.
5. Canva redirects to `/oauth/callback`, which automatically:
   - exchanges code for tokens
   - stores tokens in `tokens.json`
   - calls `GET /rest/v1/designs`
   - calls `POST /rest/v1/designs`
   - prints API responses, design ID, and edit URL (if returned)

## Terminal Output

On success, terminal output includes:
- token exchange success
- full JSON result for `GET /rest/v1/designs`
- full JSON result for `POST /rest/v1/designs`
- created design ID and edit URL (if available)

On failure, terminal output includes clear errors for:
- state mismatch
- failed token exchange
- expired/unauthorized token responses
- non-200 API responses
