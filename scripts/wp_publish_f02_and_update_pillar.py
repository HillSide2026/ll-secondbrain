#!/usr/bin/env python3
"""
wp_publish_f02_and_update_pillar.py

Three-phase script:
  Phase 1 — Publish 36 existing F02 draft posts (IDs 1980–2015), set featured_media=1240
  Phase 2 — Upload and publish 8 P6 markdown files from the repo
  Phase 3 — Update Corporate Pillar page (ID=2144) to replace old placeholder post URLs
             with new F02 post URLs (4 slots per sub-pillar, pillar post first)
"""

import base64
import html
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


# ── Credentials ──────────────────────────────────────────────────────────────

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

FEATURED_MEDIA_ID = 1240  # shared image used by all existing published posts
CATEGORY_ID = 105          # Ontario Corporate


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


def api_patch(path, payload):
    return api_post(path, payload, method="POST")  # WP REST uses POST for updates too


# ── Phase 1: Publish existing drafts ─────────────────────────────────────────

def phase1_publish_drafts():
    print("\n=== PHASE 1: Publishing 36 F02 draft posts ===")
    ids = list(range(1980, 2016))
    id_str = ",".join(map(str, ids))
    posts = api_get("posts", f"include={id_str}&per_page=100&status=any")

    results = []
    for p in sorted(posts, key=lambda x: x["id"]):
        pid = p["id"]
        payload = {
            "status": "publish",
            "featured_media": FEATURED_MEDIA_ID,
        }
        result, err = api_post(f"posts/{pid}", payload)
        if err:
            print(f"  FAIL  ID={pid} — {err}")
            results.append((pid, p["slug"], "FAIL", err))
        else:
            print(f"  OK    ID={pid} slug={result['slug']}")
            results.append((pid, result["slug"], "published", ""))
    return results


# ── Phase 2: Upload & publish P6 posts ───────────────────────────────────────

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


def md_to_html(text):
    if HAS_MARKDOWN:
        return md_lib.markdown(text, extensions=["extra", "nl2br"])
    return "<pre>" + text + "</pre>"


def get_or_create_tag(name):
    slug = name.lower().replace(" ", "-")
    existing = api_get("tags", f"slug={slug}")
    if existing:
        return existing[0]["id"]
    result, err = api_post("tags", {"name": name, "slug": slug})
    if result:
        return result["id"]
    return None


SKIP_TAGS = {"funnel-02", "blog", "p6", "pillar", "supporting"}

P6_SLUG_MAP = {
    "p6_commercial_loan_agreement_ontario_v1.md":    "commercial-loan-agreement-ontario",
    "p6_commercial_loan_default_ontario_v1.md":       "commercial-loan-default-ontario",
    "p6_crypto_backed_lending_ontario_v1.md":         "crypto-backed-lending-ontario",
    "p6_personal_guarantee_commercial_loan_ontario_v1.md": "personal-guarantee-commercial-loan-ontario",
    "p6_ppsa_security_registration_ontario_v1.md":    "ppsa-security-registration-ontario",
    "p6_private_lender_ontario_business_v1.md":       "private-lender-ontario-business",
    "p6_private_mortgage_lender_ontario_v1.md":       "private-mortgage-lender-ontario",
    "p6_set_up_private_lending_company_ontario_v1.md": "set-up-private-lending-company-ontario",
}


def phase2_upload_p6():
    print("\n=== PHASE 2: Uploading 8 P6 posts ===")
    blog_dir = Path("04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/04_FUNNELS/funnel-02/content/blog")
    p6_files = sorted(blog_dir.glob("p6_*.md"))

    published = {}
    for f in p6_files:
        content = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        title = fm.get("title", f.stem)
        slug = P6_SLUG_MAP.get(f.name, f.stem.replace("_", "-").replace("-v1", ""))

        # Build tag IDs
        raw_tags = fm.get("tags", "").strip("[]").split(",")
        tag_ids = []
        for t in raw_tags:
            t = t.strip()
            if t and t not in SKIP_TAGS:
                tid = get_or_create_tag(t)
                if tid:
                    tag_ids.append(tid)

        payload = {
            "title": title,
            "slug": slug,
            "content": md_to_html(body),
            "status": "publish",
            "categories": [CATEGORY_ID],
            "tags": tag_ids,
            "featured_media": FEATURED_MEDIA_ID,
        }
        result, err = api_post("posts", payload)
        if err:
            print(f"  FAIL  {f.name} — {err}")
        else:
            wp_id = result["id"]
            wp_slug = result["slug"]
            wp_link = result["link"]
            print(f"  OK    ID={wp_id} slug={wp_slug}")
            published[f.name] = {"id": wp_id, "slug": wp_slug, "link": wp_link, "title": title}

    return published


# ── Phase 3: Update Corporate Pillar page ─────────────────────────────────────

# Sub-pillar slot assignments:
#   [0] = pillar post (always first)
#   [1–3] = top supporting posts
#
# Format: (new_url, new_title)
# URLs are constructed from slug after publishing.

SUBPILLAR_NEW_POSTS = {
    "Shareholder Agreements Ontario": [
        ("https://levinelegal.ca/shareholder-agreements-ontario-what-they-actually-control/",
         "Shareholder Agreements in Ontario: What They Actually Control \u2014 and Where They Break"),
        ("https://levinelegal.ca/shotgun-clause-ontario/",
         "The Shotgun Clause in Ontario: When It Stops Being Fair"),
        ("https://levinelegal.ca/death-disability-insolvency-shareholder-shares-ontario/",
         "Death, Disability, and Insolvency: When Shares Pass to the Wrong Hands"),
        ("https://levinelegal.ca/minority-shareholder-rights-ontario/",
         "Minority Shareholder Rights in Ontario: How Veto Power Emerges"),
    ],
    "Contractor vs. Employee Ontario": [
        ("https://levinelegal.ca/contractor-employee-misclassification-ontario/",
         "Contractor vs Employee in Ontario: Where Misclassification Actually Creates Liability"),
        ("https://levinelegal.ca/cra-test-contractors-ontario/",
         "The CRA Test for Contractors in Ontario: How Risk Actually Shows Up"),
        ("https://levinelegal.ca/non-compete-agreements-ontario-employer/",
         "Non-Compete Agreements in Ontario: What Still Works After the Ban"),
        ("https://levinelegal.ca/termination-clauses-ontario-unenforceable/",
         "Termination Clauses in Ontario: Why Many Don\u2019t Work"),
    ],
    "Canadian Subsidiary Setup": [
        ("https://levinelegal.ca/setting-up-subsidiary-canada/",
         "Setting Up a Subsidiary in Canada: What Foreign Businesses Need to Know"),
        ("https://levinelegal.ca/branch-vs-subsidiary-canada/",
         "Branch vs Subsidiary in Canada: Which Structure Actually Fits"),
        ("https://levinelegal.ca/director-residency-requirements-canada/",
         "Director Residency Requirements in Canada: What Has Changed"),
        ("https://levinelegal.ca/canadian-subsidiary-compliance-obligations/",
         "Ongoing Compliance for a Canadian Subsidiary: What Gets Missed"),
    ],
    "Commercial Contracts Ontario": [
        ("https://levinelegal.ca/commercial-contracts-ontario-businesses/",
         "Commercial Contracts for Ontario Businesses: What to Review Before You Sign"),
        ("https://levinelegal.ca/personal-guarantees-ontario-business/",
         "Personal Guarantees in Ontario: What Business Owners Are Actually Agreeing To"),
        ("https://levinelegal.ca/limitation-of-liability-clauses-ontario/",
         "Limitation of Liability Clauses in Ontario: What They Actually Protect"),
        ("https://levinelegal.ca/auto-renewal-clauses-ontario-contracts/",
         "Auto-Renewal Clauses in Ontario Contracts: When the Agreement Doesn\u2019t End"),
    ],
    "Corporate &amp; Commercial Transactions": [
        ("https://levinelegal.ca/buying-selling-business-ontario/",
         "Buying or Selling a Business in Ontario: How Deals Actually Come Together \u2014 and Fall Apart"),
        ("https://levinelegal.ca/share-purchase-vs-asset-purchase-ontario/",
         "Share Purchase vs Asset Purchase in Ontario: What Actually Changes"),
        ("https://levinelegal.ca/due-diligence-ontario-business-purchases/",
         "Due Diligence in Ontario Business Purchases: What Gets Reviewed"),
        ("https://levinelegal.ca/selling-business-ontario-what-needs-to-be-ready/",
         "Selling Your Business in Ontario: What Needs to Be Ready"),
    ],
    "Commercial &amp; Private Lending Ontario": [
        ("https://levinelegal.ca/commercial-loan-agreement-ontario/",
         "Commercial Lending in Ontario: What the Legal Documents Actually Say"),
        ("https://levinelegal.ca/ppsa-security-registration-ontario/",
         "PPSA Security in Ontario: What It Means When a Lender Registers Against a Business"),
        ("https://levinelegal.ca/personal-guarantee-commercial-loan-ontario/",
         "Personal Guarantees in Commercial Lending: What Ontario Business Owners Are Actually Signing"),
        ("https://levinelegal.ca/private-lender-ontario-business/",
         "Private Lenders in Ontario: What Borrowers Need to Know Before They Sign"),
    ],
}

# Old placeholder URLs in each section (in order of appearance)
SUBPILLAR_OLD_POSTS = {
    "Shareholder Agreements Ontario": [
        ("https://levinelegal.ca/directors-residency-requirements-in-ontario/",
         "Directors\u2019 Residency Requirements in Ontario"),
        ("https://levinelegal.ca/six-practical-features-of-a-canadian-corporation/",
         "Six Practical Features of a Canadian Corporation"),
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
    ],
    "Contractor vs. Employee Ontario": [
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
        ("https://levinelegal.ca/five-tips-for-naming-a-new-corporation/",
         "Five Tips For Naming a New Corporation"),
        ("https://levinelegal.ca/discover-what-is-a-certificate-of-incorporation/",
         "Discover What is a Certificate of Incorporation"),
    ],
    "Canadian Subsidiary Setup": [
        ("https://levinelegal.ca/directors-residency-requirements-in-ontario/",
         "Directors\u2019 Residency Requirements in Ontario"),
        ("https://levinelegal.ca/six-practical-features-of-a-canadian-corporation/",
         "Six Practical Features of a Canadian Corporation"),
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
    ],
    "Commercial Contracts Ontario": [
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
        ("https://levinelegal.ca/five-tips-for-naming-a-new-corporation/",
         "Five Tips For Naming a New Corporation"),
        ("https://levinelegal.ca/discover-what-is-a-certificate-of-incorporation/",
         "Discover What is a Certificate of Incorporation"),
    ],
    "Corporate &amp; Commercial Transactions": [
        ("https://levinelegal.ca/directors-residency-requirements-in-ontario/",
         "Directors\u2019 Residency Requirements in Ontario"),
        ("https://levinelegal.ca/six-practical-features-of-a-canadian-corporation/",
         "Six Practical Features of a Canadian Corporation"),
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
    ],
    "Commercial &amp; Private Lending Ontario": [
        ("https://levinelegal.ca/discover-why-every-corporation-has-at-least-one-director/",
         "Discover Why Every Corporation Has at Least One Director"),
        ("https://levinelegal.ca/ontario-corporation-vs-federal-corporation/",
         "Ontario Corporation vs Federal Corporation"),
        ("https://levinelegal.ca/five-tips-for-naming-a-new-corporation/",
         "Five Tips For Naming a New Corporation"),
        ("https://levinelegal.ca/discover-what-is-a-certificate-of-incorporation/",
         "Discover What is a Certificate of Incorporation"),
    ],
}


def replace_post_entry(content, old_url, old_title, new_url, new_title):
    """
    Replace all occurrences of old_url / old_title with new equivalents.
    Handles: href=, data-attr-static-link JSON, title=, and link text.
    """
    # Escape for use in JSON within HTML attributes
    def js(s):
        return s.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&#039;")

    old_url_stripped = old_url.rstrip("/")
    new_url_stripped = new_url.rstrip("/")

    # 1. Replace bare href values
    content = content.replace(f'href="{old_url}"', f'href="{new_url}"')
    content = content.replace(f'href="{old_url_stripped}"', f'href="{new_url_stripped}"')

    # 2. Replace href= within data-attr-static-link JSON (escaped)
    old_href_escaped = old_url.replace("/", "\\/")
    new_href_escaped = new_url.replace("/", "\\/")
    content = content.replace(old_href_escaped, new_href_escaped)

    # 3. Replace title= attributes
    content = content.replace(f'title="{old_title}"', f'title="{new_title}"')
    # Also handle HTML-encoded title variants
    old_title_html = html.escape(old_title)
    new_title_html = html.escape(new_title)
    content = content.replace(f'title="{old_title_html}"', f'title="{new_title_html}"')

    # 4. Replace link text content (between tags — targeted)
    content = content.replace(f'>{old_title}<', f'>{new_title}<')
    content = content.replace(f'>{old_title_html}<', f'>{new_title_html}<')

    # 5. Replace in data-attr-static-link JSON values
    # Format: "href":"URL","title":"TITLE" (JSON-encoded inside HTML attribute)
    old_json_href = js(old_url)
    new_json_href = js(new_url)
    content = content.replace(f'&quot;href&quot;:&quot;{old_json_href}&quot;',
                               f'&quot;href&quot;:&quot;{new_json_href}&quot;')
    old_json_title = js(old_title)
    new_json_title = js(new_title)
    content = content.replace(f'&quot;title&quot;:&quot;{old_json_title}&quot;',
                               f'&quot;title&quot;:&quot;{new_json_title}&quot;')

    return content


def split_by_h3(content):
    """Split content into [(full_h3_tag, heading_text, section_body), ...] plus leading header."""
    parts = []
    pattern = re.compile(r'(<h3[^>]*>)(.*?)(</h3>)', re.DOTALL)
    last_end = 0
    header_text = ""

    for m in pattern.finditer(content):
        if last_end == 0:
            header_text = content[:m.start()]
        else:
            # assign body to the previous section
            parts[-1] = (parts[-1][0], parts[-1][1], content[last_end:m.start()])
        parts.append((m.group(0), m.group(2), ""))  # body filled in next iteration or below
        last_end = m.end()

    # Assign body of the LAST section (everything after its closing </h3>)
    if parts:
        parts[-1] = (parts[-1][0], parts[-1][1], content[last_end:])

    return header_text, parts, ""  # tail is always empty now


def phase3_update_pillar_page():
    print("\n=== PHASE 3: Updating Corporate Pillar page ===")
    page = api_get("pages/2144", "context=edit")
    content = page["content"]["raw"]

    header_text, sections, tail = split_by_h3(content)

    new_sections = []
    for (h3_tag, heading_text, body) in sections:
        # Match heading to our sub-pillar map (strip HTML entities for matching)
        heading_clean = heading_text.strip()

        if heading_clean in SUBPILLAR_OLD_POSTS:
            old_posts = SUBPILLAR_OLD_POSTS[heading_clean]
            new_posts = SUBPILLAR_NEW_POSTS[heading_clean]
            print(f"  Updating section: {heading_clean}")
            for i, ((old_url, old_title), (new_url, new_title)) in enumerate(zip(old_posts, new_posts)):
                body = replace_post_entry(body, old_url, old_title, new_url, new_title)
                print(f"    slot {i+1}: {new_url.split('/')[-2]}")
        else:
            print(f"  Skipping section (no mapping): {heading_clean}")

        new_sections.append((h3_tag, heading_text, body))

    # Reassemble (tail is empty — last section body is included in its tuple)
    new_content = header_text
    for (h3_tag, heading_text, body) in new_sections:
        new_content += h3_tag + body

    if new_content == content:
        print("  WARNING: Content unchanged — check old URL/title mappings")
        return False

    result, err = api_post("pages/2144", {"content": new_content})
    if err:
        print(f"  FAIL updating page: {err}")
        return False
    print(f"  Page updated successfully. Link: {result.get('link', '')}")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("F02 Publish + Corporate Pillar Update")
    print("=" * 60)

    # Phase 1
    p1_results = phase1_publish_drafts()
    p1_ok = sum(1 for r in p1_results if r[2] == "published")
    p1_fail = sum(1 for r in p1_results if r[2] == "FAIL")
    print(f"\nPhase 1 complete: {p1_ok} published, {p1_fail} failed")

    # Phase 2
    p2_results = phase2_upload_p6()
    print(f"\nPhase 2 complete: {len(p2_results)}/8 P6 posts uploaded and published")
    for fname, info in p2_results.items():
        print(f"  ID={info['id']} {info['link']}")

    # Phase 3
    page_ok = phase3_update_pillar_page()

    # Summary report
    print("\n" + "=" * 60)
    print("COMPLETION REPORT")
    print("=" * 60)

    PILLAR_MAP = {
        1980: ("P2", "Contractor vs. Employee Ontario"),
        1981: ("P2", "Contractor vs. Employee Ontario"),
        1982: ("P2", "Contractor vs. Employee Ontario"),
        1983: ("P2", "Contractor vs. Employee Ontario"),
        1984: ("P2", "Contractor vs. Employee Ontario"),
        1985: ("P2", "Contractor vs. Employee Ontario"),
        1986: ("P3", "Canadian Subsidiary Setup"),
        1987: ("P3", "Canadian Subsidiary Setup"),
        1988: ("P3", "Canadian Subsidiary Setup"),
        1989: ("P3", "Canadian Subsidiary Setup"),
        1990: ("P3", "Canadian Subsidiary Setup"),
        1991: ("P3", "Canadian Subsidiary Setup"),
        1992: ("P3", "Canadian Subsidiary Setup"),
        1993: ("P4", "Commercial Contracts Ontario"),
        1994: ("P4", "Commercial Contracts Ontario"),
        1995: ("P4", "Commercial Contracts Ontario"),
        1996: ("P4", "Commercial Contracts Ontario"),
        1997: ("P4", "Commercial Contracts Ontario"),
        1998: ("P4", "Commercial Contracts Ontario"),
        1999: ("P5", "Corporate & Commercial Transactions"),
        2000: ("P5", "Corporate & Commercial Transactions"),
        2001: ("P5", "Corporate & Commercial Transactions"),
        2002: ("P5", "Corporate & Commercial Transactions"),
        2003: ("P5", "Corporate & Commercial Transactions"),
        2004: ("P5", "Corporate & Commercial Transactions"),
        2005: ("P5", "Corporate & Commercial Transactions"),
        2006: ("P5", "Corporate & Commercial Transactions"),
        2007: ("P5", "Corporate & Commercial Transactions"),
        2008: ("P1", "Shareholder Agreements Ontario"),
        2009: ("P1", "Shareholder Agreements Ontario"),
        2010: ("P1", "Shareholder Agreements Ontario"),
        2011: ("P1", "Shareholder Agreements Ontario"),
        2012: ("P1", "Shareholder Agreements Ontario"),
        2013: ("P1", "Shareholder Agreements Ontario"),
        2014: ("P1", "Shareholder Agreements Ontario"),
        2015: ("P1", "Shareholder Agreements Ontario"),
    }

    print(f"\n{'ID':<6} {'Status':<12} {'Sub-Pillar':<35} {'Slug'}")
    print("-" * 90)
    for pid, slug, status, err in sorted(p1_results, key=lambda x: x[0]):
        pillar_info = PILLAR_MAP.get(pid, ("??", "Unknown"))
        note = f" !! {err}" if err else ""
        print(f"{pid:<6} {status:<12} {pillar_info[1]:<35} {slug}{note}")

    if p2_results:
        print("\nP6 — Commercial & Private Lending Ontario")
        for fname, info in p2_results.items():
            print(f"{'':6} {'published':<12} {'Commercial & Private Lending Ontario':<35} {info['slug']}")

    print(f"\nCorporate Pillar page update: {'SUCCESS' if page_ok else 'FAILED'}")
    print("URL: https://levinelegal.ca/homepage/corporate-pillar/")

    print("\nPosts on pillar page per sub-pillar (4 slots each):")
    for section, posts in SUBPILLAR_NEW_POSTS.items():
        clean = html.unescape(section)
        print(f"  {clean}:")
        for i, (url, title) in enumerate(posts):
            marker = " [PILLAR]" if i == 0 else ""
            print(f"    {url}{marker}")


if __name__ == "__main__":
    main()
