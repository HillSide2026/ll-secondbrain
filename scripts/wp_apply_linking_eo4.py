#!/usr/bin/env python3
"""
wp_apply_linking_eo4.py

Sets slugs and applies the internal linking architecture across all EO4 Crypto AML posts.

Architecture (ML1 spec 2026-03-30):
  pillar  → links down to each supporting post (one per section)
  every post → 1 link up (pillar) + 1 link forward (next in journey)

Flow:
  stablecoins → on-chain/off-chain → wallet attribution → STR for crypto → (exits to EO2 + EO3)
  MSB classification bridge → EO1 MSB pillar

Cross-pillar exits:
  STR for crypto (1944) → EO2 STR pillar (1934) + EO3 monitoring failures (1912)
  MSB classification (1955) → EO1 MSB pillar (1867)
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

# ── EO4 Post registry ────────────────────────────────────────────────────────

POSTS = {
    1951: {
        "slug": "crypto-payments-aml-risk-canada",
        "title": "Crypto Payments and AML Risk in Canada: What Changes and What Doesn't",
        "anchor": "crypto payments and AML risk in Canada",
        "role": "pillar",
    },
    1952: {
        "slug": "stablecoins-payment-flows-aml-assumptions-canada",
        "title": "Stablecoins and Payment Flows: Do AML Assumptions Still Hold?",
        "anchor": "stablecoins and AML assumptions",
        "role": "post",
        "forward": 1953,
        "forward_anchor": "where AML visibility breaks",
    },
    1953: {
        "slug": "on-chain-off-chain-aml-visibility-canada",
        "title": "On-Chain vs Off-Chain Activity: Where AML Visibility Breaks",
        "anchor": "where AML visibility breaks",
        "role": "post",
        "forward": 1954,
        "forward_anchor": "who the counterparty is in wallet-based payments",
    },
    1954: {
        "slug": "wallet-based-payments-counterparty-canada",
        "title": "Wallet-Based Payments: Who Is the Counterparty?",
        "anchor": "who the counterparty is in wallet-based payments",
        "role": "post",
        "forward": 1944,
        "forward_anchor": "STR reporting for crypto-enabled MSBs",
    },
    1944: {
        "slug": "str-reporting-crypto-enabled-msbs-canada",
        "title": "STR Reporting for Crypto-Enabled MSBs",
        "anchor": "STR reporting for crypto-enabled MSBs",
        "role": "post",
        # Two forward links for this exit post
        "forward": 1934,
        "forward_anchor": "the STR framework in Canada",
        "forward2": 1912,
        "forward2_anchor": "transaction monitoring failures in fintech",
    },
    1955: {
        "slug": "crypto-payment-flows-msb-classification-canada",
        "title": "Crypto Payment Flows and MSB Classification in Canada",
        "anchor": "crypto payment flows and MSB classification",
        "role": "post",
        "forward": 1867,
        "forward_anchor": "whether you need to register as an MSB in Canada",
    },
}

EO4_PILLAR_ID = 1951

# Pillar section → post it links to
PILLAR_SECTION_LINKS = [
    (1952, "stablecoins and AML assumptions"),
    (1953, "where AML visibility breaks"),
    (1954, "who the counterparty is in wallet-based payments"),
    (1944, "STR reporting for crypto-enabled MSBs"),
    (1955, "crypto payment flows and MSB classification"),
]

# Cross-pillar URLs (not in POSTS registry, so we hardcode)
CROSS_PILLAR_URLS = {
    1867: f"{BASE_URL}/do-you-need-to-register-as-an-msb-in-canada/",
    1934: f"{BASE_URL}/str-framework-canada-how-decisions-get-made/",
    1912: f"{BASE_URL}/transaction-monitoring-failures-fintech-canada/",
}


def url_for(post_id):
    if post_id in CROSS_PILLAR_URLS:
        return CROSS_PILLAR_URLS[post_id]
    slug = POSTS[post_id]["slug"]
    return f"{BASE_URL}/{slug}/"


def link(post_id, override_anchor=None):
    if post_id in POSTS:
        anchor = override_anchor or POSTS[post_id]["anchor"]
    else:
        anchor = override_anchor or str(post_id)
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

    # Regular post: 1 up + 1 (or 2) forward
    forward_id = p.get("forward")
    forward_anchor = p.get("forward_anchor")
    forward2_id = p.get("forward2")
    forward2_anchor = p.get("forward2_anchor")

    html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
    html += f'  <li>{link(EO4_PILLAR_ID)}</li>\n'
    if forward_id:
        html += f'  <li>{link(forward_id, forward_anchor)}</li>\n'
    if forward2_id:
        html += f'  <li>{link(forward2_id, forward2_anchor)}</li>\n'
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
