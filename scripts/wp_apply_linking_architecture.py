#!/usr/bin/env python3
"""
wp_apply_linking_architecture.py

Sets slugs and applies the internal linking architecture across all F03 MSB blog posts.

Architecture rules:
  pillar       → links to all classification + process + consequence
  classification → up (pillar) + sideways (2-3 peers) + down (process) + forward (consequence)
  process      → up (pillar) + back (2-3 classification) + forward (AML/FINTRAC/consequence)
  consequence  → back (pillar + 2-3 classification) + down (registration) + forward (AML/FINTRAC)
  compliance   → back (registration + consequence) + sideways (each other) + up (pillar, light)
  operator     → links everywhere (pillar + classification peers + process)
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
    1867: {
        "slug": "do-you-need-to-register-as-an-msb-in-canada",
        "title": "Do You Need to Register as an MSB in Canada?",
        "anchor": "money services business in Canada",
        "role": "pillar",
    },
    1876: {
        "slug": "payment-facilitator-vs-msb-canada",
        "title": "Payment Facilitator vs MSB in Canada",
        "anchor": "payment facilitator vs MSB",
        "role": "classification",
        "sideways": [1877, 1883, 1881],
    },
    1877: {
        "slug": "crypto-stablecoin-business-msb-canada",
        "title": "Does a Crypto or Stablecoin Business Count as an MSB in Canada?",
        "anchor": "crypto and stablecoin MSB classification",
        "role": "classification",
        "sideways": [1876, 1883, 1880],
    },
    1879: {
        "slug": "remittance-license-canada-msb-rules",
        "title": "Do You Need a Remittance License in Canada?",
        "anchor": "remittance and MSB registration",
        "role": "classification",
        "sideways": [1876, 1880, 1881],
    },
    1880: {
        "slug": "cross-border-payments-canada-regulatory-requirements-fintechs",
        "title": "Cross-Border Payments Canada: Regulatory Requirements for Fintechs",
        "anchor": "cross-border payments regulatory requirements",
        "role": "classification",
        "sideways": [1879, 1877, 1883],
    },
    1881: {
        "slug": "do-payment-processors-need-register-msb-canada",
        "title": "Do Payment Processors Need to Register as MSBs in Canada?",
        "anchor": "payment processors and MSB registration",
        "role": "classification",
        "sideways": [1876, 1882, 1883],
    },
    1882: {
        "slug": "are-marketplaces-msbs-canada",
        "title": "Are Marketplaces Considered MSBs in Canada?",
        "anchor": "marketplace MSB classification",
        "role": "classification",
        "sideways": [1876, 1881, 1883],
    },
    1883: {
        "slug": "banking-partner-sponsor-msb-obligations-canada",
        "title": "Does Using a Banking Partner or Sponsor Remove MSB Obligations in Canada?",
        "anchor": "banking partner and MSB obligations",
        "role": "classification",
        "sideways": [1876, 1881, 1880],
    },
    1870: {
        "slug": "cross-border-payroll-contractor-payments-msb-canada",
        "title": "Cross-Border Payroll and Contractor Payments: Do MSB Rules Apply?",
        "anchor": "payroll and contractor payment MSB rules",
        "role": "classification",
        "sideways": [1879, 1880, 1883],
    },
    1878: {
        "slug": "msb-registration-canada-timeline-process-delays",
        "title": "MSB Registration in Canada: Timeline, Process, and Common Delays",
        "anchor": "MSB registration process",
        "role": "process",
        "back": [1882, 1881, 1879],
    },
    1873: {
        "slug": "how-long-does-msb-registration-take-canada",
        "title": "How Long Does MSB Registration Take in Canada?",
        "anchor": "MSB registration timeline",
        "role": "process",
        "back": [1876, 1880, 1877],
    },
    1871: {
        "slug": "msb-registration-canada-requirements-checklist",
        "title": "MSB Registration Canada Requirements Checklist",
        "anchor": "MSB registration requirements checklist",
        "role": "process",
        "back": [1882, 1881, 1883],
    },
    1874: {
        "slug": "fintrac-msb-registration-form-information-required",
        "title": "FINTRAC MSB Registration Form: What Information Is Required",
        "anchor": "FINTRAC MSB registration form",
        "role": "process",
        "back": [1876, 1877, 1879],
    },
    1872: {
        "slug": "do-you-need-canadian-entity-register-msb",
        "title": "Do You Need a Canadian Entity to Register as an MSB?",
        "anchor": "Canadian entity and MSB registration",
        "role": "process",
        "back": [1880, 1877, 1870],
    },
    1875: {
        "slug": "how-to-map-payment-flow-msb-analysis-canada",
        "title": "How to Map a Payment Flow for MSB Analysis (Canada)",
        "anchor": "mapping a payment flow for MSB analysis",
        "role": "operator",
    },
    1884: {
        "slug": "operating-without-msb-registration-canada",
        "title": "What Happens If You Operate Without MSB Registration in Canada?",
        "anchor": "operating without MSB registration",
        "role": "consequence",
        "back_classification": [1882, 1881, 1876],
    },
    1868: {
        "slug": "ongoing-aml-obligations-msbs-canada",
        "title": "What Are Ongoing AML Obligations for MSBs in Canada?",
        "anchor": "ongoing AML obligations for MSBs",
        "role": "compliance",
    },
    1869: {
        "slug": "what-fintrac-looks-for-msb-compliance-review",
        "title": "What Does FINTRAC Look for in an MSB Compliance Review?",
        "anchor": "what FINTRAC looks for in a compliance review",
        "role": "compliance",
    },
    1903: {
        "slug": "saas-embedded-payments-msb-canada",
        "title": "Do SaaS Platforms with Embedded Payments Need to Register as MSBs in Canada?",
        "anchor": "SaaS platforms with embedded payments and MSB registration",
        "role": "classification",
        "sideways": [1876, 1882, 1881],
    },
    1904: {
        "slug": "how-banks-assess-msb-risk-canada",
        "title": "How Banks Assess MSB Risk in Canada (From a Fintech Perspective)",
        "anchor": "how banks assess MSB risk in Canada",
        "role": "consequence",
        "back_classification": [1876, 1883, 1903],
    },
    1905: {
        "slug": "designing-payment-flows-msb-risk-canada",
        "title": "Designing Payment Flows to Reduce MSB Risk in Canada",
        "anchor": "designing payment flows to reduce MSB risk",
        "role": "operator",
    },
}


def url_for(post_id):
    slug = POSTS[post_id]["slug"]
    return f"{BASE_URL}/{slug}/"


def link(post_id, override_anchor=None):
    p = POSTS[post_id]
    anchor = override_anchor or p["anchor"]
    return f'<a href="{url_for(post_id)}">{anchor}</a>'


# ── Build related-links HTML block per role ──────────────────────────────────

def build_related_block(post_id):
    p = POSTS[post_id]
    role = p["role"]
    items = []

    if role == "pillar":
        items.append(("<strong>Classification: Is Your Business an MSB?</strong>", [
            (1876, None), (1877, None), (1879, None),
            (1880, None), (1881, None), (1882, None),
            (1883, None), (1870, None), (1903, None),
        ]))
        items.append(("<strong>Registration</strong>", [
            (1878, None), (1873, None), (1871, None),
        ]))
        items.append(("<strong>Consequences</strong>", [
            (1884, None),
        ]))

    elif role == "classification":
        items.append(("<strong>MSB Definition</strong>", [
            (1867, "money services business in Canada"),
        ]))
        sideways = p.get("sideways", [])
        if sideways:
            items.append(("<strong>Related Classification Issues</strong>",
                          [(s, None) for s in sideways]))
        items.append(("<strong>Registration</strong>", [
            (1878, "MSB registration process"),
            (1871, "MSB registration requirements checklist"),
        ]))
        items.append(("<strong>Consequences</strong>", [
            (1884, "operating without MSB registration"),
        ]))

    elif role == "process":
        items.append(("<strong>MSB Definition</strong>", [
            (1867, "money services business in Canada"),
        ]))
        back = p.get("back", [])
        if back:
            items.append(("<strong>Classification Issues This Applies To</strong>",
                          [(b, None) for b in back]))
        items.append(("<strong>After Registration: Ongoing Obligations</strong>", [
            (1868, None),
            (1869, None),
        ]))
        items.append(("<strong>Consequences of Non-Registration</strong>", [
            (1884, "operating without MSB registration"),
        ]))

    elif role == "consequence":
        items.append(("<strong>MSB Definition</strong>", [
            (1867, "money services business in Canada"),
        ]))
        back_cls = p.get("back_classification", [])
        if back_cls:
            items.append(("<strong>Classification Issues That Lead Here</strong>",
                          [(b, None) for b in back_cls]))
        items.append(("<strong>How to Resolve It</strong>", [
            (1878, "MSB registration process"),
            (1871, "MSB registration requirements checklist"),
        ]))
        items.append(("<strong>Ongoing Obligations After Registration</strong>", [
            (1868, None),
            (1869, None),
        ]))

    elif role == "compliance":
        sibling = 1868 if post_id == 1869 else 1869
        items.append(("<strong>Related</strong>", [
            (sibling, None),
        ]))
        items.append(("<strong>Registration</strong>", [
            (1878, "MSB registration process"),
        ]))
        items.append(("<strong>Consequences of Non-Registration</strong>", [
            (1884, "operating without MSB registration"),
        ]))
        items.append(("<strong>MSB Definition</strong>", [
            (1867, "money services business in Canada"),
        ]))

    elif role == "operator":
        items.append(("<strong>MSB Definition</strong>", [
            (1867, "money services business in Canada"),
        ]))
        items.append(("<strong>Classification Issues</strong>", [
            (1876, None), (1882, None), (1881, None), (1883, None),
        ]))
        items.append(("<strong>Registration</strong>", [
            (1878, "MSB registration process"),
        ]))
        items.append(("<strong>Consequences</strong>", [
            (1884, "operating without MSB registration"),
        ]))

    if not items:
        return ""

    html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
    for section_label, links in items:
        html += f"  <li>{section_label}\n    <ul>\n"
        for pid, anchor in links:
            html += f"      <li>{link(pid, anchor)}</li>\n"
        html += "    </ul>\n  </li>\n"
    html += "</ul>\n"
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
