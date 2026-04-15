#!/usr/bin/env python3
"""Classify 2026 Stream Money Gmail threads into existing Gmail matter labels.

This runner is intentionally narrow: it uses the repo's Gmail MCP helpers for
auth, thread retrieval, label discovery, backoff, and Gmail thread mutation.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import gmail_mcp_server as gmail


CANDIDATE_QUERY = (
    'in:anywhere after:2026/01/01 -in:spam -in:trash '
    '{Stream "Stream Money" stream.money get-stream.com snowcap '
    '"Equals Money" Equals EMI RPAA wallet '
    '"25-927-00003" "25-927-00004" "26-927-00004"}'
)

COMPLIANCE_LABEL = "LL/1./1.1/25-927-00003 -- Stream Ventures Limited"
COUNSEL_LABEL = "LL/1./1.1/26-927-00004 -- Stream Ventures Limited"
PARKED_STREAM_LABEL = "LL/1./1.4/24-682-00002 -- Stream Ventures Limited"

TARGET_LABELS = {
    "25-927-00003": COMPLIANCE_LABEL,
    "26-927-00004": COUNSEL_LABEL,
}

STREAM_LABEL_NAMES = {COMPLIANCE_LABEL, COUNSEL_LABEL, PARKED_STREAM_LABEL}

STRONG_STREAM_PATTERNS = [
    r"\bstream money\b",
    r"\bstream ventures\b",
    r"\bget stream\b",
    r"\bget-stream\.com\b",
    r"\bstream\.money\b",
    r"\b@s?stream\.money\b",
    r"\bsnowcap\b",
    r"\bmaple wave\b",
    r"\bstream\s+x\b",
    r"\bstream\s*<>\b",
    r"\bverto\s*(<>|and)\s*stream\b",
    r"\bequals money and stream\b",
]

STREAM_CONTEXT_TERMS = {
    "aml",
    "atf",
    "banking",
    "camlo",
    "elliptic",
    "emi",
    "equals",
    "fccq",
    "fintrac",
    "fireblocks",
    "fraud",
    "innowise",
    "kyb",
    "kyc",
    "marble",
    "msb",
    "onboarding",
    "payments",
    "program",
    "rpaa",
    "transaction monitoring",
    "verto",
    "wallet",
    "wolfsberg",
}

COUNSEL_PATTERNS = [
    r"\bagreement\b",
    r"\bcontract\b",
    r"\bcontract review\b",
    r"\bdms\.s\d+\b",
    r"\benterprise platform\b",
    r"\bhamlins\b",
    r"\bnegotiat",
    r"\bpricing\b",
    r"\bredline\b",
    r"\bterms\b",
    r"\bwhite label\b",
]

COMPLIANCE_PATTERNS = [
    r"\baml\b",
    r"\batf\b",
    r"\bcamlo\b",
    r"\bfccq\b",
    r"\bfintrac\b",
    r"\bfraud\b",
    r"\bindustry risk\b",
    r"\bkyb\b",
    r"\bkyc\b",
    r"\bmsb\b",
    r"\bonboarding guidance\b",
    r"\bops risk\b",
    r"\bpolicy\b",
    r"\bprocedure\b",
    r"\brisk assessment\b",
    r"\brpaa\b",
    r"\bsop\b",
    r"\btransaction monitoring\b",
    r"\bwolfsberg\b",
]

GENERIC_EXCLUDE_PATTERNS = [
    r"\basana overdue tasks\b",
    r"\basana weekly tasks\b",
    r"\bsecurity alert\b",
    r"\byour google account\b",
]


def now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")


def header_value(headers: Iterable[Dict[str, str]], name: str) -> str:
    name_low = name.lower()
    for header in headers:
        if str(header.get("name", "")).lower() == name_low:
            return str(header.get("value", ""))
    return ""


def message_headers(message: Dict[str, Any]) -> Dict[str, str]:
    headers = message.get("payload", {}).get("headers", []) or []
    return {
        "from": header_value(headers, "From"),
        "to": header_value(headers, "To"),
        "cc": header_value(headers, "Cc"),
        "bcc": header_value(headers, "Bcc"),
        "subject": header_value(headers, "Subject"),
        "date": header_value(headers, "Date"),
    }


def decode_body_data(data: str) -> str:
    if not data:
        return ""
    try:
        padded = data + "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8", errors="replace")
    except Exception:
        return ""


def payload_text(payload: Dict[str, Any], limit: int = 12000) -> str:
    chunks: List[str] = []

    def walk(part: Dict[str, Any]) -> None:
        if sum(len(chunk) for chunk in chunks) > limit:
            return
        mime_type = str(part.get("mimeType", ""))
        body = part.get("body", {}) or {}
        if mime_type in {"text/plain", "text/html"} and body.get("data"):
            chunks.append(decode_body_data(str(body.get("data", ""))))
        for child in part.get("parts", []) or []:
            walk(child)

    walk(payload)
    text = "\n".join(chunks)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text[:limit]


def thread_text(thread: Dict[str, Any]) -> Tuple[str, str, str, str]:
    messages = thread.get("messages", []) or []
    subjects: List[str] = []
    snippets: List[str] = []
    participants: List[str] = []
    bodies: List[str] = []
    dates: List[int] = []

    for message in messages:
        headers = message_headers(message)
        subject = headers["subject"]
        if subject:
            subjects.append(subject)
        for field in ("from", "to", "cc", "bcc"):
            if headers[field]:
                participants.append(headers[field])
        snippet = str(message.get("snippet", ""))
        if snippet:
            snippets.append(snippet)
        bodies.append(payload_text(message.get("payload", {}) or {}, limit=6000))
        try:
            dates.append(int(message.get("internalDate", "0")))
        except ValueError:
            pass

    latest_subject = subjects[-1] if subjects else "(no subject)"
    date_range = ""
    if dates:
        start = datetime.fromtimestamp(min(dates) / 1000, timezone.utc).date().isoformat()
        end = datetime.fromtimestamp(max(dates) / 1000, timezone.utc).date().isoformat()
        date_range = start if start == end else f"{start} to {end}"

    summary_text = "\n".join(subjects + snippets + participants)
    full_text = "\n".join([summary_text] + bodies)
    return latest_subject, date_range, summary_text, full_text


def label_names_for_thread(thread: Dict[str, Any], label_id_to_name: Dict[str, str]) -> List[str]:
    return [
        label_id_to_name.get(label_id, label_id)
        for label_id in gmail._collect_thread_label_ids(thread)
    ]


def regex_hits(patterns: Iterable[str], text: str) -> List[str]:
    hits = []
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def is_stream_thread(label_names: List[str], summary_text: str, full_text: str) -> Tuple[bool, str]:
    label_signal = sorted(set(label_names).intersection(STREAM_LABEL_NAMES))
    if label_signal:
        return True, f"existing Stream Gmail label: {', '.join(label_signal)}"

    text_low = full_text.lower()
    summary_low = summary_text.lower()

    if regex_hits(STRONG_STREAM_PATTERNS, text_low):
        return True, "strong Stream/SnowCap/domain signal"

    if "stream" in summary_low or "stream" in text_low:
        context_hits = sorted(term for term in STREAM_CONTEXT_TERMS if term in text_low)
        if context_hits:
            shown = ", ".join(context_hits[:5])
            return True, f"Stream plus related context: {shown}"

    return False, "no Stream Money matter signal strong enough for tagging"


def classify_thread(label_names: List[str], summary_text: str) -> Tuple[str, str]:
    if COMPLIANCE_LABEL in label_names and COUNSEL_LABEL not in label_names:
        return "25-927-00003", "already has compliance label"
    if COUNSEL_LABEL in label_names and COMPLIANCE_LABEL not in label_names:
        return "26-927-00004", "already has counsel label"

    text_low = summary_text.lower()
    if "26-927-00004" in text_low or "25-927-00004" in text_low:
        return "26-927-00004", "explicit counsel matter code signal"
    if "25-927-00003" in text_low:
        return "25-927-00003", "explicit compliance matter code signal"

    counsel_hits = regex_hits(COUNSEL_PATTERNS, text_low)
    compliance_hits = regex_hits(COMPLIANCE_PATTERNS, text_low)

    if counsel_hits:
        return "26-927-00004", "counsel/commercial signal; mixed threads default to counsel"
    if compliance_hits:
        return "25-927-00003", "regulatory/compliance signal dominates"
    return "26-927-00004", "default counsel classification"


def target_state(
    label_names: List[str],
    assigned_code: str,
    name_to_id: Dict[str, str],
) -> Tuple[str, List[str], List[str], bool]:
    target_label = TARGET_LABELS[assigned_code]
    target_id = name_to_id[target_label]
    current_ids = [
        name_to_id[name]
        for name in label_names
        if name in name_to_id
    ]
    current_matter_ids = [
        name_to_id[name]
        for name in label_names
        if name in name_to_id and any(name.startswith(prefix) for prefix in gmail.MATTER_TIER_PREFIXES)
    ]
    remove_ids = sorted({label_id for label_id in current_matter_ids if label_id != target_id})
    no_change = target_id in current_ids and not remove_ids
    return target_label, [target_id], remove_ids, no_change


def audit_entry_to_md(entry: Dict[str, Any]) -> str:
    return (
        f"| `{entry['thread_id']}` | {entry['date_range']} | "
        f"{entry['subject'].replace('|', '/')} | {entry['assigned_code']} | "
        f"{entry['action']} | {entry['justification'].replace('|', '/')} |"
    )


def write_outputs(run_id: str, summary: Dict[str, Any], entries: List[Dict[str, Any]]) -> Tuple[Path, Path]:
    md_path = REPO_ROOT / "06_RUNS" / f"{run_id}_stream_money_classification.md"
    json_path = REPO_ROOT / "06_RUNS" / f"{run_id}_stream_money_thread_mapping.json"

    review_entries = [entry for entry in entries if entry["action"] == "review_required"]
    conflict_entries = [entry for entry in entries if entry.get("had_conflict")]

    lines = [
        f"# Stream Money Gmail Classification — {run_id}",
        "",
        "## Scope",
        "",
        f"- Gmail query: `{CANDIDATE_QUERY}`",
        "- Scope: Gmail threads after 2026/01/01, including inbox and archived, excluding spam and trash.",
        "- Mutation: Gmail thread labels only. No subjects, bodies, or deletion actions.",
        "- Target labels: existing Gmail labels `LL/1./1.1/25-927-00003 -- Stream Ventures Limited` and `LL/1./1.1/26-927-00004 -- Stream Ventures Limited`.",
        "",
        "## Summary",
        "",
        f"- Candidate threads retrieved: {summary['candidate_threads']}",
        f"- Stream-qualified threads processed: {summary['stream_threads']}",
        f"- Gmail threads changed: {summary['changed']}",
        f"- Already consistent / skipped: {summary['skipped_consistent']}",
        f"- Flagged for review: {summary['review_required']}",
        f"- Excluded as not matter-specific: {summary['excluded']}",
        f"- Errors: {summary['errors']}",
        "",
        "## Counts By Matter Code",
        "",
        "| Matter code | Threads |",
        "|---|---:|",
    ]
    for code, count in sorted(summary["assigned_counts"].items()):
        lines.append(f"| {code} | {count} |")

    lines.extend([
        "",
        "## Exception Report",
        "",
        "### Review Required",
        "",
    ])
    if review_entries:
        lines.extend(f"- `{entry['thread_id']}` — {entry['subject']}: {entry['justification']}" for entry in review_entries)
    else:
        lines.append("- None.")

    lines.extend(["", "### Conflicts Resolved", ""])
    if conflict_entries:
        lines.extend(
            f"- `{entry['thread_id']}` — {entry['subject']}: {', '.join(entry.get('prior_matter_labels', []))} -> {entry['target_label']}"
            for entry in conflict_entries
        )
    else:
        lines.append("- None.")

    lines.extend([
        "",
        "## Audit Log",
        "",
        "| Thread ID | Date range | Subject | Assigned matter | Action | Justification |",
        "|---|---|---|---|---|---|",
    ])
    lines.extend(audit_entry_to_md(entry) for entry in entries)

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path.write_text(json.dumps({"summary": summary, "threads": entries}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return md_path, json_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify Stream Money 2026 Gmail threads")
    parser.add_argument("--execute", action="store_true", help="Apply Gmail label changes")
    parser.add_argument("--run-id", default=now_slug())
    args = parser.parse_args()

    service = gmail._get_gmail_service()
    labels = gmail._list_all_labels(service)
    name_to_id = gmail._label_name_to_id(labels)
    label_id_to_name = gmail._label_id_to_name(labels)

    missing = [label for label in TARGET_LABELS.values() if label not in name_to_id]
    if missing:
        raise SystemExit(f"Required Gmail label(s) missing: {missing}")

    thread_ids = gmail._collect_thread_ids_by_query(service, CANDIDATE_QUERY)
    entries: List[Dict[str, Any]] = []
    counters = Counter()
    assigned_counts = Counter()

    for index, thread_id in enumerate(thread_ids, 1):
        thread = gmail._with_backoff(lambda tid=thread_id: gmail._get_thread(service, tid), f"stream_money:get_thread:{thread_id}")
        subject, date_range, summary_text, full_text = thread_text(thread)
        labels_present = label_names_for_thread(thread, label_id_to_name)
        matter_labels_present = [
            name
            for name in labels_present
            if any(name.startswith(prefix) for prefix in gmail.MATTER_TIER_PREFIXES)
        ]

        excluded = False
        generic_hits = regex_hits(GENERIC_EXCLUDE_PATTERNS, (summary_text + "\n" + full_text).lower())
        if generic_hits and not set(labels_present).intersection(STREAM_LABEL_NAMES):
            excluded = True

        qualifies, qualify_reason = is_stream_thread(labels_present, summary_text, full_text)
        if excluded:
            counters["excluded"] += 1
            entries.append({
                "thread_id": thread_id,
                "date_range": date_range,
                "subject": subject,
                "assigned_code": "",
                "target_label": "",
                "action": "excluded",
                "justification": "generic account/task notification; not matter-specific",
                "prior_matter_labels": matter_labels_present,
                "had_conflict": False,
            })
            continue

        if not qualifies:
            counters["review_required"] += 1
            entries.append({
                "thread_id": thread_id,
                "date_range": date_range,
                "subject": subject,
                "assigned_code": "",
                "target_label": "",
                "action": "review_required",
                "justification": qualify_reason,
                "prior_matter_labels": matter_labels_present,
                "had_conflict": False,
            })
            continue

        counters["stream_threads"] += 1
        assigned_code, classification_reason = classify_thread(labels_present, summary_text)
        assigned_counts[assigned_code] += 1
        target_label, add_ids, remove_ids, no_change = target_state(labels_present, assigned_code, name_to_id)
        had_conflict = bool(remove_ids)

        if no_change:
            action = "skipped_consistent"
            counters["skipped_consistent"] += 1
        else:
            action = "would_label"
            if args.execute:
                gmail._with_backoff(
                    lambda tid=thread_id, adds=add_ids, removes=remove_ids: gmail._apply_thread_modify(service, tid, adds, removes),
                    f"stream_money:modify:{thread_id}",
                )
                action = "labeled"
            counters["changed"] += 1

        entry = {
            "thread_id": thread_id,
            "date_range": date_range,
            "subject": subject,
            "assigned_code": assigned_code,
            "target_label": target_label,
            "action": action,
            "justification": f"{qualify_reason}; {classification_reason}",
            "prior_matter_labels": matter_labels_present,
            "had_conflict": had_conflict,
        }
        entries.append(entry)

        if args.execute and action == "labeled":
            gmail._append_audit({
                "timestamp": gmail._now_iso(),
                "tool": "stream_money_gmail_classify",
                "thread_id": thread_id,
                "new_matter_label": target_label,
                "removed_label_count": len(remove_ids),
                "reason": entry["justification"],
            })

        if index % 50 == 0:
            print(f"processed {index}/{len(thread_ids)} threads")

    summary = {
        "run_id": args.run_id,
        "executed": args.execute,
        "candidate_threads": len(thread_ids),
        "stream_threads": counters["stream_threads"],
        "changed": counters["changed"],
        "skipped_consistent": counters["skipped_consistent"],
        "review_required": counters["review_required"],
        "excluded": counters["excluded"],
        "errors": counters["errors"],
        "assigned_counts": dict(assigned_counts),
        "query": CANDIDATE_QUERY,
    }
    md_path, json_path = write_outputs(args.run_id, summary, entries)
    print(json.dumps({
        "summary": summary,
        "markdown": str(md_path.relative_to(REPO_ROOT)),
        "json": str(json_path.relative_to(REPO_ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
