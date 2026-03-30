#!/usr/bin/env python3
"""
wp_apply_linking_eo3.py

Sets slugs and applies the internal linking architecture across all EO3 AML blog posts.

Architecture rules (simple, per ML1 spec 2026-03-30):
  pillar  → links down to one post per section (monitoring, suspicion, reporting,
             documentation, banks, fintrac)
  every post → 1 link up to pillar (early in post) + 1 link sideways (most natural next)

Sideways map:
  fintrac_exam       → monitoring_failures
  monitoring_failures → suspicious_transaction
  aml_documentation  → fintrac_exam
  common_failures    → monitoring_failures
  bank_rejection     → monitoring_failures
  what_banks_ask     → bank_rejection
  how_banks_assess   → what_banks_ask
  suspicious_tx      → str_timing
  str_timing         → after_str
  unusual_tx         → suspicious_tx
  after_str          → aml_documentation
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

# ── Post registry ────────────────────────────────────────────────────────────

POSTS = {
    1910: {
        "slug": "aml-compliance-msbs-canada",
        "title": "AML Compliance for MSBs in Canada: How Risk Actually Shows Up",
        "anchor": "how AML risk actually shows up",
        "role": "pillar",
    },
    1911: {
        "slug": "how-to-prepare-fintrac-examination-msb-canada",
        "title": "How to Prepare for a FINTRAC Examination (MSBs in Canada)",
        "anchor": "how to prepare for a FINTRAC examination",
        "role": "post",
        "sideways": 1912,
        "sideways_anchor": "transaction monitoring failures",
    },
    1912: {
        "slug": "transaction-monitoring-failures-fintech-canada",
        "title": "Transaction Monitoring Failures in Fintech (Canada)",
        "anchor": "transaction monitoring failures in fintech",
        "role": "post",
        "sideways": 1918,
        "sideways_anchor": "what counts as a suspicious transaction",
    },
    1913: {
        "slug": "aml-documentation-requirements-msb-canada",
        "title": "AML Documentation Requirements for MSBs in Canada",
        "anchor": "AML documentation requirements",
        "role": "post",
        "sideways": 1911,
        "sideways_anchor": "how to prepare for a FINTRAC examination",
    },
    1914: {
        "slug": "common-aml-program-failures-canadian-msbs",
        "title": "Common AML Program Failures in Canadian MSBs",
        "anchor": "common AML program failures",
        "role": "post",
        "sideways": 1912,
        "sideways_anchor": "transaction monitoring failures",
    },
    1915: {
        "slug": "why-banks-reject-fintechs-aml-grounds-canada",
        "title": "Why Banks Reject Fintechs on AML Grounds (Canada)",
        "anchor": "why banks reject fintechs on AML grounds",
        "role": "post",
        "sideways": 1912,
        "sideways_anchor": "transaction monitoring failures",
    },
    1916: {
        "slug": "what-banks-ask-fintech-onboarding-aml",
        "title": "What Banks Ask During Fintech Onboarding (AML Focus)",
        "anchor": "what banks ask during fintech onboarding",
        "role": "post",
        "sideways": 1915,
        "sideways_anchor": "why banks reject fintechs on AML grounds",
    },
    1917: {
        "slug": "how-banks-assess-aml-msb-risk-canada",
        "title": "How Banks Assess AML and MSB Risk in Canada",
        "anchor": "how banks assess AML and MSB risk",
        "role": "post",
        "sideways": 1916,
        "sideways_anchor": "what banks ask during fintech onboarding",
    },
    1918: {
        "slug": "what-counts-as-suspicious-transaction-canada",
        "title": "What Counts as a Suspicious Transaction in Canada (Fintech Context)",
        "anchor": "what counts as a suspicious transaction in Canada",
        "role": "post",
        "sideways": 1919,
        "sideways_anchor": "when you have to file an STR",
    },
    1919: {
        "slug": "when-do-you-have-to-file-str-canada-fintrac",
        "title": "When Do You Have to File an STR in Canada (FINTRAC Timing Explained)",
        "anchor": "when you have to file an STR",
        "role": "post",
        "sideways": 1921,
        "sideways_anchor": "what happens after you file an STR",
    },
    1920: {
        "slug": "do-all-unusual-transactions-require-str-canada",
        "title": "Do All Unusual Transactions Require an STR?",
        "anchor": "whether all unusual transactions require an STR",
        "role": "post",
        "sideways": 1918,
        "sideways_anchor": "what counts as a suspicious transaction in Canada",
    },
    1921: {
        "slug": "what-happens-after-you-file-str-canada",
        "title": "What Happens After You File an STR in Canada",
        "anchor": "what happens after you file an STR",
        "role": "post",
        "sideways": 1913,
        "sideways_anchor": "AML documentation requirements",
    },
}

PILLAR_ID = 1910

# Pillar section → post ID it links to
PILLAR_SECTION_LINKS = [
    ("Monitoring", 1912),
    ("Suspicion", 1918),
    ("Reporting", 1919),
    ("Documentation", 1913),
    ("Banks", 1915),
    ("FINTRAC", 1911),
]


def url_for(post_id):
    slug = POSTS[post_id]["slug"]
    return f"{BASE_URL}/{slug}/"


def link(post_id, override_anchor=None):
    p = POSTS[post_id]
    anchor = override_anchor or p["anchor"]
    return f'<a href="{url_for(post_id)}">{anchor}</a>'


# ── Build related-links HTML block ───────────────────────────────────────────

def build_related_block(post_id):
    p = POSTS[post_id]

    if p["role"] == "pillar":
        html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
        for section_label, target_id in PILLAR_SECTION_LINKS:
            html += f'  <li>{link(target_id)}</li>\n'
        html += '</ul>\n'
        return html

    # Regular post: 1 up + 1 sideways
    sideways_id = p.get("sideways")
    sideways_anchor = p.get("sideways_anchor")

    html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
    html += f'  <li>{link(PILLAR_ID)}</li>\n'
    if sideways_id:
        html += f'  <li>{link(sideways_id, sideways_anchor)}</li>\n'
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

        # Strip any previously appended related block
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
