#!/usr/bin/env python3
"""
wp_publish_f01_content.py

Publishes Funnel 1 content to levinelegal.ca as WordPress posts.

Phase 1 — Publish 6 posts for the Shareholder Disputes cluster.
Phase 2 — Publish 6 posts for the Business Structure cluster.
Phase 3 — Create F1 hub page (second Corporate Pillar) as a sibling of the
           existing Corporate Pillar page (ID 2144), with live links to all
           published posts.

Posts use flat slugs, category 105 (Ontario Corporate), featured image 1240.
"""

import base64
import html
import json
import os
import re
import urllib.request
import urllib.error
from pathlib import Path

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


# ── Credentials ───────────────────────────────────────────────────────────────

def load_env(path=".env"):
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

load_env()

BASE_URL = os.environ["WORDPRESS_BASE_URL"].rstrip("/")
CREDS = base64.b64encode(
    f"{os.environ['WORDPRESS_USERNAME']}:{os.environ['WORDPRESS_APP_PASSWORD']}".encode()
).decode()
HEADERS = {
    "Authorization": f"Basic {CREDS}",
    "Content-Type": "application/json",
    "User-Agent": "SB_Bot/1.0",
    "Accept": "application/json",
}

FEATURED_MEDIA_ID = 1240
CATEGORY_ID = 105  # Ontario Corporate

F1_CONTENT_DIR = Path(
    "04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/04_FUNNELS"
    "/funnel-01/funnel_01_toronto_corporate_lawyer/content"
)

# Hub page placement: sibling of Corporate Pillar (ID 2144)
CORPORATE_PILLAR_PAGE_ID = 2144
F1_HUB_SLUG = "f1-topic-hub"
F1_HUB_TITLE = "F1 Corporate Pillar \u2014 Shareholder Disputes & Business Structure"


# ── Cluster definitions: (filename, slug, title) ─────────────────────────────

SHAREHOLDER_DISPUTES_CLUSTER = [
    (
        "shareholder-disputes-pillar-page-DRAFT.md",
        "shareholder-disputes-ontario",
        "Shareholder Disputes in Ontario",
    ),
    (
        "pillar-post-1-partnership-legally-meaningful-phase.md",
        "partnership-legally-meaningful-phase",
        "A Business Partnership Is Rarely \u201cTense.\u201d It Is Usually Entering a Legally Meaningful Phase.",
    ),
    (
        "supporting-post-1-early-signs-breakdown.md",
        "early-signs-business-partner-breakdown",
        "Early Signs a Business Partner Relationship Is Breaking Down",
    ),
    (
        "supporting-post-2-what-to-document.md",
        "what-to-document-shareholder-dispute",
        "What to Document When a Shareholder Dispute Is Emerging",
    ),
    (
        "supporting-post-3-can-partner-be-removed.md",
        "removing-business-partner-ontario",
        "Can a Business Partner Be Removed From a Company in Ontario?",
    ),
    (
        "supporting-post-4-sha-no-longer-reflects-reality.md",
        "shareholder-agreement-no-longer-reflects-reality",
        "When a Shareholder Agreement No Longer Reflects Reality",
    ),
]

BUSINESS_STRUCTURE_CLUSTER = [
    (
        "business-structure-pillar-page.md",
        "business-structure-ontario",
        "Business Structure Ontario",
    ),
    (
        "business-structure-pillar-post-drift.md",
        "business-structure-drift-ontario",
        "Most Business Structures Drift. The Problem Is That the Drift Remains Invisible Until It Matters.",
    ),
    (
        "business-structure-supporting-post-structure-outdated.md",
        "business-structure-stops-reflecting-operations",
        "When a Business Structure Stops Reflecting How a Company Operates",
    ),
    (
        "business-structure-supporting-post-adding-shareholder.md",
        "adding-shareholder-informally-ontario",
        "Adding a Shareholder Informally: What Actually Changes",
    ),
    (
        "business-structure-supporting-post-investor-diligence.md",
        "investor-diligence-corporate-structure",
        "What Investors Flag First in a Company\u2019s Structure",
    ),
    (
        "business-structure-supporting-post-documents-vs-reality.md",
        "corporate-documents-vs-business-reality",
        "When Corporate Documents No Longer Match Business Reality",
    ),
]


# ── HTTP helpers ──────────────────────────────────────────────────────────────

def api_get(path, params=""):
    url = f"{BASE_URL}/wp-json/wp/v2/{path}"
    if params:
        url += f"?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def api_post(path, payload, method="POST"):
    url = f"{BASE_URL}/wp-json/wp/v2/{path}"
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read()), None
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        return None, f"HTTP {e.code}: {err[:300]}"


# ── Content processing ────────────────────────────────────────────────────────

def parse_frontmatter(content):
    fm = {}
    body = content
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            for line in content[3:end].strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    fm[k.strip()] = v.strip().strip('"')
            body = content[end + 4:].strip()
    return fm, body


def clean_pillar_page_body(body):
    """Strip layout/builder annotations from pillar page markdown."""
    body = re.sub(r'^\[LAYOUT:[^\]]*\]\s*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\[ANCHOR:[^\]]*\]\s*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'\[LAYOUT:[^\]]*\]', '', body)
    body = re.sub(r'\[ANCHOR:[^\]]*\]', '', body)
    body = re.sub(r'\*\*\[([^\]]+)\]\*\*', r'**\1**', body)
    body = re.sub(r'^\[Card [^\]]+\]\s*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\[Left Column[^\]]*\]\s*\n', '', body, flags=re.MULTILINE)
    body = re.sub(r'^\[Right Column[^\]]*\]\s*\n', '', body, flags=re.MULTILINE)
    impl_idx = body.find('## IMPLEMENTATION NOTES')
    if impl_idx != -1:
        body = body[:impl_idx]
    return body.strip()


def md_to_html(text):
    if HAS_MARKDOWN:
        return md_lib.markdown(text, extensions=["extra", "nl2br"])
    paragraphs = re.split(r'\n{2,}', text.strip())
    return "\n".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())


def load_content(filename, is_pillar_page=False):
    path = F1_CONTENT_DIR / filename
    raw = path.read_text(encoding="utf-8")
    _, body = parse_frontmatter(raw)
    if is_pillar_page:
        body = clean_pillar_page_body(body)
    return md_to_html(body)


# ── Phase 1 & 2: Publish posts ────────────────────────────────────────────────

def publish_cluster(cluster, phase_label):
    print(f"\n=== {phase_label} ===")
    results = {}

    # First item in each cluster is the pillar/overview page
    for i, (filename, slug, title) in enumerate(cluster):
        is_pillar = (i == 0)
        html_content = load_content(filename, is_pillar_page=is_pillar)

        payload = {
            "title": title,
            "slug": slug,
            "content": html_content,
            "status": "publish",
            "categories": [CATEGORY_ID],
            "featured_media": FEATURED_MEDIA_ID,
        }

        result, err = api_post("posts", payload)
        if err:
            print(f"  FAIL  {slug} — {err}")
            results[slug] = {"id": None, "link": None, "title": title, "error": err}
        else:
            print(f"  OK    ID={result['id']} slug={result['slug']}  {result['link']}")
            results[slug] = {"id": result["id"], "link": result["link"], "title": title}

    return results


def phase1_publish_shareholder_disputes():
    return publish_cluster(SHAREHOLDER_DISPUTES_CLUSTER, "PHASE 1: Shareholder Disputes cluster")


def phase2_publish_business_structure():
    return publish_cluster(BUSINESS_STRUCTURE_CLUSTER, "PHASE 2: Business Structure cluster")


# ── Phase 3: Create F1 hub page ───────────────────────────────────────────────

def build_hub_html(sd_results, bs_results):
    def link_item(slug, results, is_pillar=False):
        info = results.get(slug, {})
        url = info.get("link", "#")
        title = html.escape(info.get("title", slug))
        label = " <em>[pillar post]</em>" if is_pillar else ""
        return f'<li><a href="{url}">{title}</a>{label}</li>'

    sd_overview = sd_results.get("shareholder-disputes-ontario", {})
    bs_overview = bs_results.get("business-structure-ontario", {})

    intro = (
        "<p>F1 content cluster — Funnel 1 (reactive acquisition, Ontario SMB). Two topic areas:</p>\n"
        "<ul>\n"
        f"<li><a href=\"{sd_overview.get('link', '#')}\">Shareholder Disputes</a></li>\n"
        f"<li><a href=\"{bs_overview.get('link', '#')}\">Business Structure</a></li>\n"
        "</ul>\n"
    )

    sd_links = "\n".join([
        link_item("shareholder-disputes-ontario", sd_results, is_pillar=True),
        link_item("partnership-legally-meaningful-phase", sd_results),
        link_item("early-signs-business-partner-breakdown", sd_results),
        link_item("what-to-document-shareholder-dispute", sd_results),
        link_item("removing-business-partner-ontario", sd_results),
        link_item("shareholder-agreement-no-longer-reflects-reality", sd_results),
    ])

    bs_links = "\n".join([
        link_item("business-structure-ontario", bs_results, is_pillar=True),
        link_item("business-structure-drift-ontario", bs_results),
        link_item("business-structure-stops-reflecting-operations", bs_results),
        link_item("adding-shareholder-informally-ontario", bs_results),
        link_item("investor-diligence-corporate-structure", bs_results),
        link_item("corporate-documents-vs-business-reality", bs_results),
    ])

    sd_section = f"<h3>Shareholder Disputes</h3>\n<ul>\n{sd_links}\n</ul>\n"
    bs_section = f"<h3>Business Structure</h3>\n<ul>\n{bs_links}\n</ul>\n"

    return intro + sd_section + bs_section


def get_corporate_pillar_parent_id():
    try:
        page = api_get(f"pages/{CORPORATE_PILLAR_PAGE_ID}")
        return page.get("parent", 0)
    except Exception as e:
        print(f"  WARNING: Could not fetch Corporate Pillar parent: {e}. Using top-level.")
        return 0


def phase3_create_hub(sd_results, bs_results):
    print("\n=== PHASE 3: Creating F1 hub page ===")
    parent_id = get_corporate_pillar_parent_id()
    print(f"  Corporate Pillar parent ID: {parent_id}")

    hub_html = build_hub_html(sd_results, bs_results)
    payload = {
        "title": F1_HUB_TITLE,
        "slug": F1_HUB_SLUG,
        "content": hub_html,
        "status": "publish",
        "featured_media": FEATURED_MEDIA_ID,
        "parent": parent_id,
    }

    result, err = api_post("pages", payload)
    if err:
        print(f"  FAIL creating hub page: {err}")
        return None
    print(f"  OK    ID={result['id']} link={result['link']}")
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("F01 Content Publish — Shareholder Disputes & Business Structure")
    print("=" * 60)

    sd_results = phase1_publish_shareholder_disputes()
    sd_ok = sum(1 for v in sd_results.values() if v.get("id"))
    print(f"\nPhase 1 complete: {sd_ok}/{len(sd_results)} posts published")

    bs_results = phase2_publish_business_structure()
    bs_ok = sum(1 for v in bs_results.values() if v.get("id"))
    print(f"\nPhase 2 complete: {bs_ok}/{len(bs_results)} posts published")

    hub = phase3_create_hub(sd_results, bs_results)

    print("\n" + "=" * 60)
    print("COMPLETION REPORT")
    print("=" * 60)

    print("\nShareholder Disputes posts:")
    for slug, info in sd_results.items():
        status = "published" if info.get("id") else "FAILED"
        print(f"  {status:<10} {info.get('link', info.get('error', ''))}")

    print("\nBusiness Structure posts:")
    for slug, info in bs_results.items():
        status = "published" if info.get("id") else "FAILED"
        print(f"  {status:<10} {info.get('link', info.get('error', ''))}")

    if hub:
        print(f"\nF1 hub page: {hub['link']}")
    else:
        print("\nF1 hub page: FAILED")


if __name__ == "__main__":
    main()
