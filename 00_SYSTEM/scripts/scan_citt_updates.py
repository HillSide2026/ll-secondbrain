#!/usr/bin/env python3
"""
scan_citt_updates.py

Monitor official CITT pages for matter-specific trade-remedies signals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import warnings
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

warnings.filterwarnings(
    "ignore",
    message=r"urllib3 v2 only supports OpenSSL 1\.1\.1\+, currently the 'ssl' module is compiled with 'LibreSSL.*",
)

import requests
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WATCHLIST = REPO_ROOT / "05_MATTERS/ESSENTIAL/26-1639-00002/CITT_WATCHLIST.yaml"
DEFAULT_REPORT = REPO_ROOT / "05_MATTERS/ESSENTIAL/26-1639-00002/CITT_SIGNAL_REPORT.md"
DEFAULT_STATE = REPO_ROOT / "06_RUNS/state/citt_scan_26-1639-00002.json"
CASE_LINE_RE = re.compile(r"^[A-Z]{1,3}-\d{4}-\d{3}\b")
LAST_UPDATED_RE = re.compile(r"This page was last updated on ([A-Za-z]+ \d{1,2}, \d{4})\.")
DATE_RE = re.compile(r"[A-Za-z]+ \d{1,2}, \d{4}")
DATE_ONLY_RE = re.compile(r"^[A-Za-z]+ \d{1,2}, \d{4}$")
MEASURE_CASE_RE = re.compile(r"^(?P<measure>.+?)\((?P<case>[A-Z]{1,3}-\d{4}-\d{3})\)(?P<underway>\*)?(?P<tail>.*)$")
USER_AGENT = "ll-secondbrain-citt-scanner/1.0"
TRADE_REMEDY_DECISION_PREFIXES = {"GC", "NQ", "PI", "RD", "RR"}
DOCUMENT_DATE_LABEL = "Document Date issued or updated"
PAGE_END_MARKERS = ("Mandates", "Accountability", "Resources", "Contact us")
TORONTO_TZ = ZoneInfo("America/Toronto")
TRACKED_STAGE_HEADINGS = (
    "Preliminary injury inquiries",
    "Final injury inquiries",
    "Expiry reviews",
    "Interim reviews",
    "Public interest inquiries",
    "Requests for ruling",
    "Anti-dumping injury inquiries",
)
NON_SUBJECT_MARKERS = (
    "case number",
    "document type and language",
    "date issued or updated",
    "this page was last updated on",
    "notice of",
    "questionnaires",
    "public hearing",
    "finding",
    "reasons for",
    "order and reasons",
    "decision and reasons",
    "determination and reasons",
    "revised notice",
    "there are no active",
    "table of contents",
    "below is a list of tribunal decisions",
    "requests for a copy",
    "to comply with the official languages act",
)


@dataclass
class SourceResult:
    source_id: str
    label: str
    url: str
    fetched_at: str
    title: str
    last_updated: Optional[str]
    fingerprint: Optional[str]
    changed: bool
    case_lines: List[str]
    news_items: List[Dict[str, str]]
    expiry_review_items: List[Dict[str, object]]
    track_matches: Dict[str, List[str]]
    generic_matches: List[str]
    error: Optional[str] = None


class LinkTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self._skip_depth = 0
        self._current_href: Optional[str] = None
        self._current_link_chunks: List[str] = []
        self._text_chunks: List[str] = []
        self.links: List[Dict[str, str]] = []
        self.title = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"noscript", "script", "style", "svg"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in {"p", "div", "section", "article", "header", "footer", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "br"}:
            self._text_chunks.append("\n")
        if tag == "title":
            self._in_title = True
        if tag == "a":
            attr_map = dict(attrs)
            self._current_href = attr_map.get("href")
            self._current_link_chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"noscript", "script", "style", "svg"}:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag == "title":
            self._in_title = False
        if tag == "a":
            text = normalize_space(" ".join(self._current_link_chunks))
            if self._current_href and text:
                self.links.append({"href": self._current_href, "text": text})
            self._current_href = None
            self._current_link_chunks = []
        if tag in {"p", "div", "section", "article", "header", "footer", "li", "ul", "ol", "table", "tr", "td", "th"}:
            self._text_chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = unescape(data)
        if self._in_title:
            self.title += text
        self._text_chunks.append(text)
        if self._current_href is not None:
            self._current_link_chunks.append(text)

    @property
    def text(self) -> str:
        return "".join(self._text_chunks)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_line(value: str) -> str:
    line = normalize_space(value)
    line = line.replace("Read more", "").strip()
    return line


def split_lines(text: str) -> List[str]:
    lines: List[str] = []
    for raw_line in text.splitlines():
        line = normalize_line(raw_line)
        if line:
            lines.append(line)
    return lines


def unique_preserve_order(values: List[str]) -> List[str]:
    seen = set()
    ordered: List[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            ordered.append(value)
    return ordered


def slice_from_marker(lines: List[str], marker: str) -> List[str]:
    marker_lower = marker.lower()
    for idx, line in enumerate(lines):
        if marker_lower in line.lower():
            return lines[idx:]
    return lines


def slice_until_marker(lines: List[str], markers: tuple[str, ...]) -> List[str]:
    lowered_markers = [marker.lower() for marker in markers]
    for idx, line in enumerate(lines):
        lowered_line = line.lower()
        if any(lowered_line == marker or marker in lowered_line for marker in lowered_markers):
            return lines[:idx]
    return lines


def strip_document_suffix(line: str) -> str:
    return normalize_space(line.replace(DOCUMENT_DATE_LABEL, " "))


def is_follow_on_subject_line(line: str) -> bool:
    lowered = line.lower()
    if CASE_LINE_RE.match(line):
        return False
    if line in TRACKED_STAGE_HEADINGS:
        return False
    return not any(marker in lowered for marker in NON_SUBJECT_MARKERS)


def toronto_today() -> date:
    return datetime.now(TORONTO_TZ).date()


def parse_human_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.strptime(normalize_space(value), "%B %d, %Y").date()
    except ValueError:
        return None


def format_relative_days(days: Optional[int]) -> str:
    if days is None:
        return "date unavailable"
    if days == 0:
        return "today"
    if days == 1:
        return "in 1 day"
    if days > 1:
        return f"in {days} days"
    if days == -1:
        return "1 day ago"
    return f"{abs(days)} days ago"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def fetch_source(url: str) -> str:
    response = requests.get(url, timeout=30, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    return response.text


def parse_page(url: str, html: str) -> dict:
    parser = LinkTextParser()
    parser.feed(html)
    lines = split_lines(parser.text)
    links = []
    for link in parser.links:
        href = urljoin(url, link["href"])
        text = normalize_line(link["text"])
        if href and text:
            links.append({"href": href, "text": text})
    title = normalize_space(parser.title) or (lines[0] if lines else url)
    last_updated = None
    text_blob = "\n".join(lines)
    match = LAST_UPDATED_RE.search(text_blob)
    if match:
        last_updated = match.group(1)
    return {
        "title": title,
        "lines": lines,
        "links": links,
        "fingerprint": hashlib.sha256(text_blob.encode("utf-8")).hexdigest(),
        "last_updated": last_updated,
    }


def focus_lines(source_id: str, parsed: dict) -> List[str]:
    lines = parsed["lines"]
    if source_id == "citt_home":
        return [item["title"] for item in extract_news_items(parsed["links"])]
    if source_id == "measures_in_force_and_expiry_timelines":
        focused = slice_from_marker(lines, "Measure Expiry date Tentative date of Notice of Expiry Review")
        return slice_until_marker(focused, PAGE_END_MARKERS)

    focused = slice_from_marker(lines, "This page was last updated on")
    focused = slice_until_marker(focused, PAGE_END_MARKERS)

    if source_id == "decisions_not_yet_published":
        focused = slice_from_marker(focused, "Anti-dumping injury inquiries")
        focused = slice_until_marker(focused, ("Customs and excise appeals",))

    return focused


def extract_case_lines(lines: List[str], allowed_prefixes: Optional[set[str]] = None) -> List[str]:
    case_lines: List[str] = []
    for idx, line in enumerate(lines):
        if not CASE_LINE_RE.match(line):
            continue
        case_line = strip_document_suffix(line)
        prefix = case_line.split("-", 1)[0]
        if allowed_prefixes and prefix not in allowed_prefixes:
            continue
        if "—" not in case_line and idx + 1 < len(lines):
            subject_line = strip_document_suffix(lines[idx + 1])
            if is_follow_on_subject_line(subject_line):
                case_line = f"{case_line}—{subject_line}"
        case_lines.append(case_line)
    return unique_preserve_order(case_lines)


def extract_news_items(links: List[Dict[str, str]]) -> List[Dict[str, str]]:
    items = []
    for link in links:
        href = link["href"]
        if "/en/news/" not in href:
            continue
        text = link["text"]
        if len(text) < 12:
            continue
        items.append({"title": text, "url": href})
    deduped = []
    seen = set()
    for item in items:
        signature = (item["title"], item["url"])
        if signature not in seen:
            seen.add(signature)
            deduped.append(item)
    return deduped


def build_snippets(lines: List[str], keywords: List[str], max_matches: int = 5) -> List[str]:
    lowered_keywords = [keyword.lower() for keyword in keywords]
    snippets: List[str] = []
    seen = set()
    for line in lines:
        lowered_line = line.lower()
        if not any(keyword in lowered_line for keyword in lowered_keywords):
            continue
        snippet = line
        if snippet not in seen:
            seen.add(snippet)
            snippets.append(snippet)
        if len(snippets) >= max_matches:
            break
    return snippets


def compare_items(current: List[str], previous: List[str]) -> List[str]:
    previous_set = set(previous)
    return [item for item in current if item not in previous_set]


def extract_expiry_review_items(
    lines: List[str],
    window_days: int,
    recent_notice_lookback_days: int,
) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    today = toronto_today()
    window_end = today + timedelta(days=window_days)
    lookback_floor = today - timedelta(days=recent_notice_lookback_days)

    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if line.startswith("Measure Expiry date Tentative date of Notice of Expiry Review"):
            idx += 1
            continue

        match = MEASURE_CASE_RE.match(line)
        if not match:
            idx += 1
            continue

        measure = normalize_space(match.group("measure"))
        case_ref = match.group("case")
        underway = bool(match.group("underway"))
        tail = normalize_space(match.group("tail"))
        dates = DATE_RE.findall(tail)
        expiry_date_text = dates[0] if dates else None
        notice_date_text = dates[1] if len(dates) > 1 else None

        cursor = idx + 1
        while cursor < len(lines) and DATE_ONLY_RE.match(lines[cursor]):
            next_date = normalize_space(lines[cursor])
            if not expiry_date_text:
                expiry_date_text = next_date
            elif not notice_date_text:
                notice_date_text = next_date
            else:
                break
            cursor += 1

        idx = cursor
        expiry_date = parse_human_date(expiry_date_text)
        notice_date = parse_human_date(notice_date_text)
        days_to_expiry = (expiry_date - today).days if expiry_date else None
        days_to_notice = (notice_date - today).days if notice_date else None

        if notice_date and lookback_floor <= notice_date <= window_end:
            signal_kind = "underway_expiry_review" if underway else "upcoming_notice"
            signal_date = notice_date
        elif expiry_date and today <= expiry_date <= window_end:
            signal_kind = "approaching_expiry"
            signal_date = expiry_date
        else:
            continue

        items.append(
            {
                "id": f"{case_ref}|{expiry_date_text or ''}|{notice_date_text or ''}",
                "measure": measure,
                "case_ref": case_ref,
                "underway": underway,
                "expiry_date": expiry_date_text,
                "notice_date": notice_date_text,
                "days_to_expiry": days_to_expiry,
                "days_to_notice": days_to_notice,
                "signal_kind": signal_kind,
                "signal_date": signal_date.isoformat() if signal_date else "",
            }
        )

    return sorted(items, key=lambda item: (str(item.get("signal_date") or ""), str(item.get("measure") or "")))


def render_report(
    watchlist: dict,
    results: List[SourceResult],
    prior_state: dict,
    state_path: Path,
) -> str:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    baseline = not bool(prior_state.get("sources"))
    lines: List[str] = []
    lines.append(f"# CITT Signal Report — {watchlist.get('matter_name', 'Unknown Matter')}")
    lines.append("")
    lines.append(f"- Generated at: `{generated_at}`")
    lines.append(f"- Matter ID: `{watchlist.get('matter_id', 'unknown')}`")
    lines.append(f"- Client of record: `{watchlist.get('client_of_record', 'unknown')}`")
    lines.append(f"- Scanner: `{watchlist.get('scanner_name', 'unknown')}`")
    lines.append(f"- State file: `{state_path}`")
    lines.append("")
    if baseline:
        lines.append("## Run Mode")
        lines.append("")
        lines.append("Baseline run. Current official observations are recorded below; they are not being compared against a prior saved scan.")
        lines.append("")

    lines.append("## Source Status")
    lines.append("")
    lines.append("| Source | Last updated | Changed vs prior | Notes |")
    lines.append("|--------|--------------|------------------|-------|")
    for result in results:
        notes = result.error or "ok"
        last_updated = result.last_updated or "not stated"
        changed = "n/a" if baseline else ("yes" if result.changed else "no")
        lines.append(f"| {result.label} | {last_updated} | {changed} | {notes} |")
    lines.append("")

    lines.append("## Proceeding Signals")
    lines.append("")
    for result in results:
        prior_source = prior_state.get("sources", {}).get(result.source_id, {})
        previous_case_lines = prior_source.get("case_lines", [])
        new_case_lines = result.case_lines if baseline else compare_items(result.case_lines, previous_case_lines)
        if not new_case_lines:
            continue
        lines.append(f"### {result.label}")
        lines.append("")
        for case_line in new_case_lines:
            label = "Observed" if baseline else "New"
            lines.append(f"- `{label}`: {case_line}")
        lines.append(f"- Source: {result.url}")
        lines.append("")

    lines.append("## Upcoming Expiry Review Signals")
    lines.append("")
    wrote_expiry_section = False
    for result in results:
        if not result.expiry_review_items:
            continue
        wrote_expiry_section = True
        prior_source = prior_state.get("sources", {}).get(result.source_id, {})
        prior_ids = set(prior_source.get("expiry_review_ids", []))
        lines.append(f"### {result.label}")
        lines.append("")
        for item in result.expiry_review_items:
            if baseline:
                label = "Observed"
            else:
                label = "New" if item["id"] not in prior_ids else "Current"
            if item["signal_kind"] == "underway_expiry_review":
                summary = "Expiry review underway"
            elif item["signal_kind"] == "upcoming_notice":
                summary = "Upcoming notice of expiry review"
            else:
                summary = "Approaching measure expiry"

            details = [f"{item['measure']} ({item['case_ref']})"]
            if item.get("notice_date"):
                details.append(
                    f"tentative notice {item['notice_date']} ({format_relative_days(item.get('days_to_notice'))})"
                )
            if item.get("expiry_date"):
                details.append(
                    f"measure expiry {item['expiry_date']} ({format_relative_days(item.get('days_to_expiry'))})"
                )
            if item.get("underway"):
                details.append("review marked underway on the CITT page")
            lines.append(f"- `{label}`: {summary} — {'; '.join(details)}")
        lines.append(f"- Source: {result.url}")
        lines.append("")
    if not wrote_expiry_section:
        lines.append("- No approaching expiry-review or sunset-review signal was detected within the configured window.")
        lines.append("")

    lines.append("## Matter-Specific Track Matches")
    lines.append("")
    for track in watchlist.get("tracks", []):
        track_id = track["track_id"]
        track_stage = track.get("stage", "unknown")
        matches: List[str] = []
        for result in results:
            for snippet in result.track_matches.get(track_id, []):
                matches.append(f"{snippet} [{result.label}]")
        lines.append(f"### {track_id} — {track.get('label', '')}")
        lines.append("")
        lines.append(f"- Stage: `{track_stage}`")
        if matches:
            for match in unique_preserve_order(matches):
                lines.append(f"- Observed signal: {match}")
        else:
            lines.append("- No direct keyword hit in the scanned official sources for this run.")
        lines.append("")

    lines.append("## Official News Signals")
    lines.append("")
    news_items = []
    for result in results:
        prior_source = prior_state.get("sources", {}).get(result.source_id, {})
        previous_urls = prior_source.get("news_urls", [])
        current_titles = result.news_items if baseline else [
            item for item in result.news_items if item["url"] not in set(previous_urls)
        ]
        news_items.extend(current_titles)
    if news_items:
        for item in news_items:
            label = "Observed" if baseline else "New"
            lines.append(f"- `{label}`: {item['title']} — {item['url']}")
    else:
        lines.append("- No new official news items were detected in this run.")
    lines.append("")

    lines.append("## Manual Review Queue")
    lines.append("")
    for result in results:
        if result.error:
            lines.append(f"- Review fetch failure for `{result.label}`: {result.error}")
            continue
        if result.generic_matches:
            lines.append(f"- Review generic proceeding signals from `{result.label}` for possible business-development relevance.")
        if result.changed and not result.case_lines and not result.news_items and not result.expiry_review_items:
            lines.append(f"- `{result.label}` changed but no structured proceeding/news item was extracted; manual page review recommended.")
    if lines[-1] == "":
        lines.append("- No manual review item generated.")
    return "\n".join(lines).strip() + "\n"


def build_source_result(source: dict, watchlist: dict, prior_state: dict) -> SourceResult:
    source_id = source["source_id"]
    label = source["label"]
    url = source["url"]
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    prior_source = prior_state.get("sources", {}).get(source_id, {})

    try:
        html = fetch_source(url)
        parsed = parse_page(url, html)
    except Exception as exc:  # pragma: no cover - best effort runtime reporting
        return SourceResult(
            source_id=source_id,
            label=label,
            url=url,
            fetched_at=fetched_at,
            title=label,
            last_updated=None,
            fingerprint=None,
            changed=False,
            case_lines=[],
            news_items=[],
            expiry_review_items=[],
            track_matches={},
            generic_matches=[],
            error=str(exc),
        )

    focused_lines = focus_lines(source_id, parsed)
    allowed_prefixes = TRADE_REMEDY_DECISION_PREFIXES if source_id == "decisions_not_yet_published" else None
    case_lines = extract_case_lines(focused_lines, allowed_prefixes=allowed_prefixes)
    news_items = extract_news_items(parsed["links"])
    expiry_review_items: List[Dict[str, object]] = []
    if source_id == "measures_in_force_and_expiry_timelines":
        expiry_review_window_days = int(watchlist.get("expiry_review_window_days") or 120)
        recent_notice_lookback_days = int(watchlist.get("recent_notice_lookback_days") or 21)
        expiry_review_items = extract_expiry_review_items(
            focused_lines,
            window_days=expiry_review_window_days,
            recent_notice_lookback_days=recent_notice_lookback_days,
        )
    track_matches = {}
    for track in watchlist.get("tracks", []):
        track_matches[track["track_id"]] = build_snippets(focused_lines, track.get("keywords", []))
    generic_matches = build_snippets(focused_lines, watchlist.get("generic_keywords", []))
    changed = parsed["fingerprint"] != prior_source.get("fingerprint")
    return SourceResult(
        source_id=source_id,
        label=label,
        url=url,
        fetched_at=fetched_at,
        title=parsed["title"],
        last_updated=parsed["last_updated"],
        fingerprint=parsed["fingerprint"],
        changed=changed,
        case_lines=case_lines,
        news_items=news_items,
        expiry_review_items=expiry_review_items,
        track_matches=track_matches,
        generic_matches=generic_matches,
    )


def build_state(watchlist: dict, results: List[SourceResult]) -> dict:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    state = {
        "generated_at": generated_at,
        "matter_id": watchlist.get("matter_id"),
        "sources": {},
    }
    for result in results:
        if result.error:
            continue
        state["sources"][result.source_id] = {
            "label": result.label,
            "url": result.url,
            "last_updated": result.last_updated,
            "case_lines": result.case_lines,
            "news_urls": [item["url"] for item in result.news_items],
            "expiry_review_ids": [str(item["id"]) for item in result.expiry_review_items],
            "fingerprint": result.fingerprint,
        }
    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan official CITT pages for matter-specific trade-remedies signals.")
    parser.add_argument("--watchlist", type=Path, default=DEFAULT_WATCHLIST, help="Path to the matter-local CITT watchlist YAML.")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT, help="Path to the markdown report output.")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE, help="Path to the JSON state snapshot.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    watchlist = load_yaml(args.watchlist)
    prior_state = load_state(args.state)

    results = [build_source_result(source, watchlist, prior_state) for source in watchlist.get("sources", [])]
    report = render_report(watchlist, results, prior_state, args.state)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    save_state(args.state, build_state(watchlist, results))

    errors = [result for result in results if result.error]
    return 1 if errors and len(errors) == len(results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
