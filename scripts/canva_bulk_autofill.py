#!/usr/bin/env python3
"""
Canva Bulk Autofill — LL Second Brain
======================================
Generate multiple Canva designs from one brand template by filling named fields
from a JSON data file. Polls each autofill job to completion, then optionally
exports each design to a requested format.

Usage:
    python3 scripts/canva_bulk_autofill.py \\
        --template-id <brand_template_id> \\
        --data-file <path/to/slides.json> \\
        [--export-format pdf|png|pptx] \\
        [--output-log <path/to/output.ndjson>] \\
        [--poll-interval 3] \\
        [--max-wait 120]

Data file format (JSON array):
    [
      {
        "title": "Slide title for naming the design",
        "fields": {
          "field_name_1": "text value",
          "field_name_2": "another value"
        }
      },
      ...
    ]

Field values that are strings are automatically wrapped as text fields.
Pass a dict directly for image or other field types:
    "logo": {"type": "image", "asset_id": "abc123"}

Output log (ndjson): one entry per design with job_id, design_id, edit_url,
export_url (if requested), and status.

Requires CANVA_CLIENT_ID, CANVA_CLIENT_SECRET, and a valid tokens.json.
Reads .env from the repo root if present.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
import base64

_REPO_ROOT = Path(__file__).resolve().parents[1]
_ENV_FILE = _REPO_ROOT / ".env"


# ---------------------------------------------------------------------------
# Minimal env loader (mirrors canva_bridge.py)
# ---------------------------------------------------------------------------

def _load_env(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        if key and key not in os.environ:
            os.environ[key] = value


_load_env(_ENV_FILE)

CANVA_CLIENT_ID = os.getenv("CANVA_CLIENT_ID", "").strip()
CANVA_CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET", "").strip()
TOKEN_FILE = Path(os.getenv("CANVA_TOKEN_FILE", str(_REPO_ROOT / "tokens.json")))

TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"
AUTOFILLS_URL = "https://api.canva.com/rest/v1/autofills"
EXPORTS_URL = "https://api.canva.com/rest/v1/exports"
TOKEN_SKEW = 60


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _http(method: str, url: str, headers: Dict[str, str],
          body: Optional[bytes] = None, timeout: int = 30) -> tuple[int, Any]:
    req = Request(url, data=body, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return resp.status, json.loads(raw) if raw else {}
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"error": raw}
        return exc.code, parsed
    except URLError as exc:
        return 0, {"error": str(exc)}


def _post_json(url: str, token: str, body: Dict[str, Any]) -> tuple[int, Any]:
    payload = json.dumps(body).encode("utf-8")
    return _http("POST", url, {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }, body=payload)


def _get(url: str, token: str) -> tuple[int, Any]:
    return _http("GET", url, {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    })


# ---------------------------------------------------------------------------
# Token management
# ---------------------------------------------------------------------------

def _load_token() -> Dict[str, Any]:
    if not TOKEN_FILE.exists():
        sys.exit(f"ERROR: token file not found at {TOKEN_FILE}. Run start_oauth via the Canva MCP first.")
    return json.loads(TOKEN_FILE.read_text(encoding="utf-8"))


def _refresh(refresh_token: str, previous: Dict[str, Any]) -> Dict[str, Any]:
    creds = base64.b64encode(f"{CANVA_CLIENT_ID}:{CANVA_CLIENT_SECRET}".encode()).decode()
    body = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CANVA_CLIENT_ID,
    }).encode("utf-8")
    status, payload = _http("POST", TOKEN_URL, {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }, body=body)
    if status != 200 or not payload.get("access_token"):
        sys.exit(f"ERROR: token refresh failed ({status}): {payload}")
    expires_in = int(payload.get("expires_in", 0) or 0)
    record = {
        "access_token": payload["access_token"],
        "refresh_token": payload.get("refresh_token") or previous.get("refresh_token"),
        "expires_in": expires_in,
        "expires_at": int(time.time()) + expires_in if expires_in else None,
        "scope": payload.get("scope") or previous.get("scope"),
        "saved_at": int(time.time()),
        "token_type": payload.get("token_type"),
    }
    TOKEN_FILE.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def get_access_token() -> str:
    record = _load_token()
    access_token = record.get("access_token")
    refresh_token = record.get("refresh_token")
    expires_at = record.get("expires_at")
    now = int(time.time())

    if not access_token or (isinstance(expires_at, int) and now >= expires_at - TOKEN_SKEW):
        if not refresh_token:
            sys.exit("ERROR: token is expired and no refresh_token available. Re-run OAuth.")
        record = _refresh(refresh_token, record)
        access_token = record["access_token"]

    return access_token


# ---------------------------------------------------------------------------
# Autofill helpers
# ---------------------------------------------------------------------------

def _wrap_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap bare string values as Canva text field objects."""
    result = {}
    for k, v in fields.items():
        if isinstance(v, str):
            result[k] = {"type": "text", "text": v}
        else:
            result[k] = v
    return result


def create_autofill(token: str, template_id: str, title: str, data: Dict[str, Any]) -> str:
    body = {"brand_template_id": template_id, "data": data}
    if title:
        body["title"] = title
    status, payload = _post_json(AUTOFILLS_URL, token, body)
    if status not in (200, 201):
        raise RuntimeError(f"create_autofill failed ({status}): {payload}")
    job_id = (payload.get("job") or {}).get("id") or payload.get("id")
    if not job_id:
        raise RuntimeError(f"create_autofill: no job id in response: {payload}")
    return job_id


def poll_autofill(token: str, job_id: str, max_wait: int, interval: int) -> Dict[str, Any]:
    deadline = time.time() + max_wait
    while time.time() < deadline:
        status, payload = _get(f"{AUTOFILLS_URL}/{quote(job_id, safe='')}", token)
        if status not in (200, 201):
            raise RuntimeError(f"get_autofill_job failed ({status}): {payload}")
        job = payload.get("job") or payload
        job_status = job.get("status", "")
        if job_status == "success":
            return job
        if job_status == "failed":
            raise RuntimeError(f"autofill job {job_id} failed: {job}")
        time.sleep(interval)
    raise TimeoutError(f"autofill job {job_id} did not complete within {max_wait}s")


def create_export(token: str, design_id: str, fmt: str) -> str:
    status, payload = _post_json(EXPORTS_URL, token, {
        "design_id": design_id,
        "format": {"type": fmt},
    })
    if status not in (200, 201):
        raise RuntimeError(f"export_design failed ({status}): {payload}")
    export_id = (payload.get("job") or {}).get("id") or payload.get("id")
    if not export_id:
        raise RuntimeError(f"export_design: no job id in response: {payload}")
    return export_id


def poll_export(token: str, export_id: str, max_wait: int, interval: int) -> Dict[str, Any]:
    deadline = time.time() + max_wait
    while time.time() < deadline:
        status, payload = _get(f"{EXPORTS_URL}/{quote(export_id, safe='')}", token)
        if status not in (200, 201):
            raise RuntimeError(f"get_export_job failed ({status}): {payload}")
        job = payload.get("job") or payload
        job_status = job.get("status", "")
        if job_status == "success":
            return job
        if job_status == "failed":
            raise RuntimeError(f"export job {export_id} failed: {job}")
        time.sleep(interval)
    raise TimeoutError(f"export job {export_id} did not complete within {max_wait}s")


def _extract_design(job: Dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
    result = job.get("result") or {}
    design = result.get("design") or {}
    design_id = design.get("id")
    urls = design.get("urls") or {}
    edit_url = urls.get("edit_url") or urls.get("edit") or design.get("edit_url")
    return design_id, edit_url


def _extract_export_urls(job: Dict[str, Any]) -> List[str]:
    result = job.get("result") or {}
    urls = result.get("urls") or []
    if isinstance(urls, list):
        return [u.get("url") or u if isinstance(u, dict) else u for u in urls]
    if isinstance(urls, str):
        return [urls]
    return []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk-generate Canva designs from a brand template.")
    parser.add_argument("--template-id", required=True, help="Canva brand template ID")
    parser.add_argument("--data-file", required=True, help="JSON file with array of {title, fields} objects")
    parser.add_argument("--export-format", choices=["pdf", "png", "jpg", "gif", "pptx", "mp4"],
                        help="If set, export each design to this format after generation")
    parser.add_argument("--output-log", default=str(_REPO_ROOT / "06_RUNS" / "ops" / "canva_bulk_output.ndjson"),
                        help="Output ndjson log path")
    parser.add_argument("--poll-interval", type=int, default=3, help="Poll interval in seconds (default: 3)")
    parser.add_argument("--max-wait", type=int, default=120, help="Max seconds to wait per job (default: 120)")
    args = parser.parse_args()

    data_path = Path(args.data_file)
    if not data_path.exists():
        sys.exit(f"ERROR: data file not found: {data_path}")

    slides: List[Dict[str, Any]] = json.loads(data_path.read_text(encoding="utf-8"))
    if not isinstance(slides, list) or not slides:
        sys.exit("ERROR: data file must be a non-empty JSON array")

    output_path = Path(args.output_log)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    token = get_access_token()
    total = len(slides)
    print(f"Processing {total} slides from template {args.template_id}", flush=True)

    with output_path.open("a", encoding="utf-8") as log_fh:
        for i, slide in enumerate(slides, 1):
            title = str(slide.get("title", f"Slide {i}"))
            raw_fields = slide.get("fields", {})
            if not isinstance(raw_fields, dict) or not raw_fields:
                print(f"  [{i}/{total}] SKIP '{title}': no fields", flush=True)
                continue

            data = _wrap_fields(raw_fields)
            entry: Dict[str, Any] = {
                "index": i,
                "title": title,
                "template_id": args.template_id,
                "status": "pending",
            }

            try:
                print(f"  [{i}/{total}] Submitting '{title}' ...", end=" ", flush=True)
                job_id = create_autofill(token, args.template_id, title, data)
                entry["autofill_job_id"] = job_id

                job = poll_autofill(token, job_id, args.max_wait, args.poll_interval)
                design_id, edit_url = _extract_design(job)
                entry["design_id"] = design_id
                entry["edit_url"] = edit_url
                entry["status"] = "created"
                print(f"created ({design_id})", end="", flush=True)

                if args.export_format and design_id:
                    export_id = create_export(token, design_id, args.export_format)
                    entry["export_job_id"] = export_id
                    export_job = poll_export(token, export_id, args.max_wait, args.poll_interval)
                    export_urls = _extract_export_urls(export_job)
                    entry["export_urls"] = export_urls
                    entry["status"] = "exported"
                    print(f" → exported", end="", flush=True)

                print(flush=True)

            except Exception as exc:
                entry["status"] = "error"
                entry["error"] = str(exc)
                print(f"ERROR: {exc}", flush=True)

            log_fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
            log_fh.flush()

    print(f"\nDone. Output written to {output_path}", flush=True)


if __name__ == "__main__":
    main()
