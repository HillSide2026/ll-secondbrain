#!/usr/bin/env python3
"""
Build Ontario Corporate Health Check landing page.
Copies page 1741 (corporate-law-firm) and applies copy replacements.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import base64
import os

# ---------------------------------------------------------------------------
# Load credentials from .env
# ---------------------------------------------------------------------------

ENV_PATH = "/Users/matthewlevine/Repos/ll-secondbrain_fresh/.env"

def load_env(path):
    env = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                env[key.strip()] = val.strip()
    return env

env = load_env(ENV_PATH)

BASE_URL = env["WORDPRESS_BASE_URL"].rstrip("/")
USERNAME = env["WORDPRESS_USERNAME"]
APP_PASSWORD = env["WORDPRESS_APP_PASSWORD"]

# Build basic auth header
credentials = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()
AUTH_HEADER = f"Basic {credentials}"

DEFAULT_HEADERS = {
    "Authorization": AUTH_HEADER,
    "Accept": "application/json",
    "User-Agent": "Python/3.9",
}

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def wp_get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def wp_post(path, data):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    headers = dict(DEFAULT_HEADERS)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def wp_put(path, data):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    headers = dict(DEFAULT_HEADERS)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ---------------------------------------------------------------------------
# Step 1 — Fetch source page 1741
# ---------------------------------------------------------------------------

print("Step 1: Fetching source page 1741...")
source = wp_get("/wp-json/wp/v2/pages/1741?context=edit")
raw_content = source["content"]["raw"]
print(f"  Fetched. Content length: {len(raw_content)} chars")

# ---------------------------------------------------------------------------
# Step 2 — Create new draft page with original content
# ---------------------------------------------------------------------------

print("Step 2: Creating new draft page...")
new_page = wp_post("/wp-json/wp/v2/pages", {
    "title": "Ontario Corporate Health Check",
    "slug": "ontario-corporate-health-check",
    "status": "draft",
    "content": raw_content,
})
new_page_id = new_page["id"]
new_page_slug = new_page["slug"]
new_page_link = new_page.get("link", "")
print(f"  Created page ID: {new_page_id}, slug: {new_page_slug}")

# ---------------------------------------------------------------------------
# Steps 3 & 4 — Apply all copy replacements
# ---------------------------------------------------------------------------

print("Steps 3+4: Applying copy replacements...")

replacements = [
    # --- Step 3: Main copy ---
    (
        "Toronto Corporate Law Firm",
        "The Ontario Corporate Health Check",
    ),
    (
        "Levine Law provides business owners and executives with strategic, results-driven legal solutions. Let us help you grow and protect your business.",
        "A structured legal review for growing Ontario businesses that have outgrown their original legal setup.",
    ),
    (
        "Solutions That Drive Business Growth",
        "Five Areas. One Structured Review.",
    ),
    (
        "Legal clarity creates business momentum. Whether you're raising capital, restructuring, or expanding through franchising, Levine Law helps turn complex challenges into practical, results-driven strategies. Our approach protects ownership, accelerates transactions, and positions your business for sustainable growth.",
        "Most growing Ontario businesses are operating on legal documents that were written for an earlier version of the company. The Health Check identifies where that structure has drifted \u2014 and what needs to be addressed.",
    ),
    # "Why Serious Operators Work with Levine Law" is unchanged per spec — no-op, skip
    (
        "Corporate Law Services",
        "What the Health Check Covers",
    ),
    # Service card 1 — Shareholder Agreements body (H3 heading stays the same per spec)
    (
        "Prevent disputes before they start. We draft clear, enforceable agreements that define control, protect your investment, and support long-term business stability.",
        "Are exit mechanisms, valuation provisions, governance thresholds, and transfer restrictions still aligned with how the business actually operates?",
    ),
    # Service card 2 — Reorganization -> Corporate Records
    (
        "Reorganization",
        "Corporate Records",
    ),
    (
        "Navigate transitions with confidence. We design restructuring strategies that strengthen governance, manage liability, and align ownership with future growth.",
        "Are the minute book, resolutions, director appointments, and annual filings current and complete? Gaps here create friction in financing and transactions.",
    ),
    # Service card 3 — Financing -> Employment Structure
    (
        "Financing",
        "Employment Structure",
    ),
    (
        "Secure capital on the right terms. Our counsel ensures funding structures, guarantees, and investor agreements protect your interests and reduce risk.",
        "Are contractor relationships properly classified? Are termination clauses enforceable? Are equity promises documented?",
    ),
    # Service card 4 — Franchising -> Commercial Contracts
    (
        "Franchising",
        "Commercial Contracts",
    ),
    (
        "Expand with structure. We help business owners franchise their operations, maintain compliance, and protect the integrity of their brand.",
        "Are your key contracts consistent? Do limitation of liability, indemnity, and assignment provisions reflect your current risk tolerance?",
    ),
    # Service card 5 — Share Transactions -> Transaction Readiness
    (
        "Share Transactions",
        "Transaction Readiness",
    ),
    (
        "Execute equity transfers with precision. We guide buyers and sellers through due diligence, documentation, and closing\u2014ensuring each deal is compliant, efficient, and CRA ready.",
        "If a buyer, investor, or lender reviewed your structure today, what would they find? Are the documents organized to support a transaction?",
    ),
    # Service card 6 — Asset Transactions -> The Findings Report
    (
        "Asset Transactions",
        "The Findings Report",
    ),
    (
        "Buy or sell business assets with clarity and confidence. Our team structures transactions to protect value, allocate risk appropriately, and ensure seamless legal transfer.",
        "You receive a written report documenting alignment, gaps, and exposures across all five areas \u2014 plus a prioritized action plan organized by risk level and business impact.",
    ),
    # CTA section
    (
        "Ready to Move Your Business Forward? Contact Levine Law",
        "Understand Where Your Business Stands.",
    ),
    (
        "Levine Law&#8217;s mission is to provide clear, commercially grounded legal counsel that helps businesses grow with structure, integrity, and confidence. Contact Levine Law",
        "The Corporate Health Check gives Ontario business owners a clear picture of structural alignment and a prioritized path forward. Book your review today.",
    ),
    # --- Step 4: FAQ section ---
    (
        "What types of businesses does Levine Law work with?",
        "What is the Ontario Corporate Health Check?",
    ),
    (
        "Levine Law primarily serves small to medium-sized businesses in the Greater Toronto Area, including franchises or prospective franchise owners, family-owned companies, and growing companies needing corporate legal support.",
        "A structured legal review of your company&#8217;s governance and commercial structure. We examine five areas \u2014 shareholder agreements, corporate records, employment, commercial contracts, and transaction readiness \u2014 and deliver a written findings report with a prioritized action plan.",
    ),
    (
        "What legal services do you specialize in?",
        "Who is it for?",
    ),
    (
        "We focus on shareholder agreements, franchising, mergers &amp; acquisitions, asset/share transactions and business contracts to help businesses structure, protect, and grow efficiently.",
        "Ontario businesses with $1M&#8211;$8M in revenue that have been operating for several years and want to understand whether their legal structure still reflects how the business actually works.",
    ),
    (
        "How quickly can I get legal assistance?",
        "What do I receive at the end?",
    ),
    (
        "We prioritize fast turnaround times and responsive communication, ensuring businesses receive timely legal support when they need it most.",
        "A written findings report documenting alignment, gaps, and exposures across the five pillars &#8212; plus a prioritized action plan organized by risk level and business impact.",
    ),
    (
        "Do you only work with businesses in Toronto?",
        "How is this different from a free consultation?",
    ),
    (
        "We work with businesses across the Greater Toronto Area and surrounding regions, providing high-quality legal support to companies in smaller markets.",
        "A free consultation is a conversation. The Health Check is a structured engagement that produces written deliverables. It is designed for business owners who want a documented baseline, not a general discussion.",
    ),
]

updated_content = raw_content
replacement_log = []

for find, replace in replacements:
    count = updated_content.count(find)
    if count > 0:
        updated_content = updated_content.replace(find, replace)
        short_find = (find[:70] + "...") if len(find) > 70 else find
        replacement_log.append(f"  [OK x{count}] '{short_find}'")
    else:
        short_find = (find[:70] + "...") if len(find) > 70 else find
        replacement_log.append(f"  [MISS]   '{short_find}'")

for entry in replacement_log:
    print(entry)

# ---------------------------------------------------------------------------
# Step 5 — PUT the new page with updated content
# ---------------------------------------------------------------------------

print(f"\nStep 5: Updating page {new_page_id} with replaced content...")
updated = wp_put(f"/wp-json/wp/v2/pages/{new_page_id}", {
    "content": updated_content,
})
print(f"  Update confirmed. Modified: {updated.get('modified', 'n/a')}")

# ---------------------------------------------------------------------------
# Step 6 — Report
# ---------------------------------------------------------------------------

final_link = updated.get("link", new_page_link)
print("\n=== RESULT ===")
print(f"  New page ID  : {new_page_id}")
print(f"  Slug         : {updated.get('slug', new_page_slug)}")
print(f"  Link         : {final_link}")
print(f"  Status       : {updated.get('status', 'unknown')}")
print("  Live website changed: NO (page is draft — not publicly visible)")
