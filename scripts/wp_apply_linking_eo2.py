#!/usr/bin/env python3
"""
wp_apply_linking_eo2.py

Sets slugs and applies the internal linking architecture across all EO2 STR posts.

Architecture (ML1 spec 2026-03-30):
  pillar  → links down to each supporting post
  every post → 1 link up (pillar, with post-specific anchor) + 1 link forward (next in journey)

Linear flow:
  suspicion_vs_reportability (1935)
  → when_unusual_becomes_reportable (1936)
  → over_under_reporting (1937)
  → why_documentation (1938)
  → defensible_narrative (1939)
  → what_fintrac_reviews (1940)
  → internal_escalation (1941)
  → when_to_seek_triage (1942)
  → controlled_vs_reactive (1943)
  → crypto_str (1944)
  → cross_border (1945)
  → loops back to suspicion_vs_reportability (1935)
"""

import base64
import json
import os
import urllib.request
import urllib.error


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
    "User-Agent": "Mozilla/5.0 (compatible; SB_Bot/1.0)",
    "Accept": "application/json",
}

# ── EO2 Post registry ────────────────────────────────────────────────────────

POSTS = {
    1934: {
        "slug": "str-framework-canada-how-decisions-get-made",
        "title": "STR Framework in Canada: How Decisions Get Made",
        "anchor": "the STR framework in Canada",
        "role": "pillar",
    },
    1935: {
        "slug": "suspicion-vs-reportability-reasonable-grounds-str-canada",
        "title": "Suspicion vs. Reportability: What Reasonable Grounds Actually Means",
        "anchor": "suspicion vs reportability",
        "role": "post",
        "up_anchor": "how STR decisions are structured",
        "forward": 1936,
        "forward_anchor": "when unusual activity crosses into suspicion",
    },
    1936: {
        "slug": "when-does-unusual-transaction-become-reportable-canada",
        "title": "When Does an Unusual Transaction Become Reportable?",
        "anchor": "when unusual activity crosses into suspicion",
        "role": "post",
        "up_anchor": "reasonable grounds to suspect",
        "forward": 1937,
        "forward_anchor": "how thresholds are applied in practice",
    },
    1937: {
        "slug": "over-reporting-vs-under-reporting-str-canada",
        "title": "Over-Reporting vs Under-Reporting: The Real STR Risk",
        "anchor": "how thresholds are applied in practice",
        "role": "post",
        "up_anchor": "STR decision framework",
        "forward": 1938,
        "forward_anchor": "why decisions need to be supported clearly",
    },
    1938: {
        "slug": "why-documentation-matters-more-than-filing-str-canada",
        "title": "Why Documentation Matters More Than Filing",
        "anchor": "why decisions need to be supported clearly",
        "role": "post",
        "up_anchor": "STR system as a whole",
        "forward": 1939,
        "forward_anchor": "how reasoning is actually expressed",
    },
    1939: {
        "slug": "building-defensible-str-narrative-canada",
        "title": "Building a Defensible STR Narrative",
        "anchor": "how reasoning is actually expressed",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1940,
        "forward_anchor": "how this gets tested under scrutiny",
    },
    1940: {
        "slug": "what-fintrac-reviews-str-reporting-msbs",
        "title": "What FINTRAC Reviews When It Looks at STR Reporting",
        "anchor": "how this gets tested under scrutiny",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1941,
        "forward_anchor": "where decisions break internally",
    },
    1941: {
        "slug": "internal-escalation-str-review-process-canada",
        "title": "The Internal Escalation and STR Review Process",
        "anchor": "where decisions break internally",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1942,
        "forward_anchor": "when internal processes stop working",
    },
    1942: {
        "slug": "when-to-seek-str-triage-support-canada",
        "title": "When to Seek STR Triage Support",
        "anchor": "when internal processes stop working",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1943,
        "forward_anchor": "difference between structured and reactive decisions",
    },
    1943: {
        "slug": "controlled-regulatory-response-vs-reactive-str-filing",
        "title": "Controlled Regulatory Response vs. Reactive Filing",
        "anchor": "difference between structured and reactive decisions",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1944,
        "forward_anchor": "how this plays out in complex environments",
    },
    1944: {
        "slug": "str-reporting-crypto-enabled-msbs-canada",
        "title": "STR Reporting for Crypto-Enabled MSBs",
        "anchor": "how this plays out in complex environments",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1945,
        "forward_anchor": "how cross-border complexity affects suspicion",
    },
    1945: {
        "slug": "cross-border-payments-str-complexity-canada",
        "title": "Cross-Border Payments and STR Complexity",
        "anchor": "how cross-border complexity affects suspicion",
        "role": "post",
        "up_anchor": "the STR framework in Canada",
        "forward": 1935,
        "forward_anchor": "suspicion vs reportability",
    },
}

EO2_PILLAR_ID = 1934

# Pillar section → post it links to
PILLAR_SECTION_LINKS = [
    (1935, "suspicion vs reportability"),
    (1936, "when unusual activity crosses into suspicion"),
    (1937, "how thresholds are applied in practice"),
    (1938, "why decisions need to be supported clearly"),
    (1939, "how reasoning is actually expressed"),
    (1940, "how this gets tested under scrutiny"),
    (1941, "where decisions break internally"),
    (1942, "when internal processes stop working"),
    (1943, "difference between structured and reactive decisions"),
    (1944, "how this plays out in complex environments"),
    (1945, "how cross-border complexity affects suspicion"),
]


def url_for(post_id):
    slug = POSTS[post_id]["slug"]
    return f"{BASE_URL}/{slug}/"


def link(post_id, anchor):
    return f'<a href="{url_for(post_id)}">{anchor}</a>'


# ── Build related-links HTML block ───────────────────────────────────────────

def build_related_block(post_id):
    p = POSTS[post_id]

    if p["role"] == "pillar":
        html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
        for target_id, anchor in PILLAR_SECTION_LINKS:
            html += f'  <li>{link(target_id, anchor)}</li>\n'
        html += '</ul>\n'
        return html

    # Regular post: 1 up + 1 forward
    up_anchor = p.get("up_anchor", POSTS[EO2_PILLAR_ID]["anchor"])
    forward_id = p["forward"]
    forward_anchor = p["forward_anchor"]

    html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
    html += f'  <li>{link(EO2_PILLAR_ID, up_anchor)}</li>\n'
    html += f'  <li>{link(forward_id, forward_anchor)}</li>\n'
    html += '</ul>\n'
    return html


# ── WordPress API helpers ────────────────────────────────────────────────────

def wp_get(post_id):
    url = f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?status=draft"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def wp_patch(post_id, payload):
    url = f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    req.add_header("X-HTTP-Method-Override", "PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code}: {e.read().decode()[:200]}")
        return None


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    for post_id, meta in POSTS.items():
        print(f"Updating post {post_id}: {meta['title'][:60]}...")

        post = wp_get(post_id)
        current_content = post.get("content", {}).get("rendered", "")

        if "<hr>" in current_content:
            current_content = current_content[:current_content.rfind("<hr>")]

        related_block = build_related_block(post_id)
        new_content = current_content.strip() + related_block

        result = wp_patch(post_id, {
            "slug": meta["slug"],
            "content": new_content,
        })

        if result:
            print(f"  ✓ slug={result.get('slug')}  link={result.get('link')}")
        else:
            print(f"  ✗ failed")


if __name__ == "__main__":
    main()
