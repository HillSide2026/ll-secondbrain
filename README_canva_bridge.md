# Canva MCP Server + Bulk Autofill

`canva_bridge.py` runs as a persistent stdio MCP server registered in `.mcp.json`.

## Tools (11)

### Auth
| Tool | Description |
|---|---|
| `auth_status` | Inspect OAuth readiness, token presence, expiry |
| `start_oauth` | Start one-time OAuth bootstrap; returns authorization URL |

### Designs
| Tool | Description |
|---|---|
| `list_designs` | List all designs in the account |
| `get_design` | Fetch one design by ID — returns edit/view URLs |
| `create_design` | Create a blank design from a preset type (e.g. "presentation") |

### Brand Templates + Autofill
| Tool | Description |
|---|---|
| `list_brand_templates` | List brand templates available to the account |
| `get_brand_template_dataset` | Get field names and types for a template (call before autofill) |
| `create_autofill` | Submit a fill job — maps field names to text/image values |
| `get_autofill_job` | Poll job status; on success contains design ID + edit URL |

### Export
| Tool | Description |
|---|---|
| `export_design` | Start an async export (pdf, png, jpg, gif, pptx, mp4) |
| `get_export_job` | Poll export status; on success contains download URL(s) |

## Repeatable slide workflow

```
1. Build the template once in Canva UI
   - Add text/image placeholders, name each field clearly
   - Publish as a brand template

2. Discover field names
   list_brand_templates → get brand_template_id
   get_brand_template_dataset → see exact field names

3. Generate a design
   create_autofill(brand_template_id, {field_name: value, ...})
   → job_id
   get_autofill_job(job_id) → design_id + edit_url

4. Export (optional)
   export_design(design_id, format="pdf")
   → export_id
   get_export_job(export_id) → download URL
```

## Bulk generation from data

`scripts/canva_bulk_autofill.py` handles step 3 and 4 at scale.

### Data file format

```json
[
  {
    "title": "Slide title (used as design name)",
    "fields": {
      "slide_title": "Real-Time Payments Are Not Faster Batch Systems",
      "left_column_header": "Batch",
      "right_column_header": "Real-Time",
      "left_body": "Files Sent → Queued → ACH → Released → Settlement",
      "right_body": "Initiated → Authorized → Screened → Credited",
      "left_footer": "Hours to Days",
      "right_footer": "Seconds"
    }
  }
]
```

String values are auto-wrapped as `{"type": "text", "text": "..."}`.
For image fields pass `{"type": "image", "asset_id": "..."}` directly.

### Run

```bash
python3 scripts/canva_bulk_autofill.py \
  --template-id <brand_template_id> \
  --data-file path/to/slides.json \
  --export-format pdf \
  --output-log 06_RUNS/ops/canva_bulk_output.ndjson
```

Output log (ndjson): one entry per slide with `design_id`, `edit_url`, `export_urls`, `status`.

## OAuth setup

Scopes required: `design:content:read design:content:write design:meta:read brandtemplate:meta:read brandtemplate:content:read`

If you previously authorized without the `brandtemplate:*` scopes, re-authorize:

```
call start_oauth(force_reauth=true)
open the returned authorization_url in browser
call auth_status until authenticated == true
```

## Environment

```env
CANVA_CLIENT_ID=
CANVA_CLIENT_SECRET=
CANVA_REDIRECT_URI=http://127.0.0.1:3000/oauth/callback
CANVA_SCOPES=design:content:read design:content:write design:meta:read brandtemplate:meta:read brandtemplate:content:read
CANVA_TOKEN_FILE=./tokens.json
```
