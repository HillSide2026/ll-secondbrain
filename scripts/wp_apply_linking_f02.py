#!/usr/bin/env python3
"""
wp_apply_linking_f02.py

Sets slugs, applies internal linking architecture, and applies tags
across all Funnel 02 blog posts (WP IDs 1980-2015).

Architecture: pillar links down to all supporting posts
Each supporting post: 1 link up (pillar) + 1 link forward (next in flow)

Flows:
  P1 SHA (pillar: 2012):
    2014 → 2008 → 2013 → 2010 → 2011 → 2015 → 2009 → back to 2012

  P2 Contractor/Employee (pillar: 1980):
    1982 → 1980 (pillar)
    1983 → 1985
    1984 → 1980 (pillar)
    1985 → 1981
    1981 → 1980 (pillar)

  P3 Canadian Subsidiary (pillar: 1991):
    1987 → 1988 → 1992 → 1990 → 1986 → 1989 → back to 1991

  P4 Commercial Contracts (pillar: 1994):
    1998 → 1997 → 1996 → 1993 → 1995 → back to 1994

  P5 Transactions (pillar: 2000):
    2007 → 1999 → 2003 → 2001 → 2005 → 2002 → 2006 → 2004 → back to 2000

  P6 Commercial Lending (pillar: 3001 — PLACEHOLDER IDs, replace after WP publish):
    3002 → 3003 → 3004 → 3005 → 3006 → 3007 → 3008 → back to 3001

Tags: pillar-based + topic-based from frontmatter (filtered to SEO-relevant terms)
"""

import base64
import json
import os
import re
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

# ── Post registry ─────────────────────────────────────────────────────────────

# Tags: skip internal/system tags, keep SEO-relevant ones
SKIP_TAGS = {"funnel-02", "blog", "pillar", "supporting", "p1", "p2", "p3", "p4", "p5", "p6", "sha"}

POSTS = {
    # P1 — SHA
    2012: {
        "slug": "shareholder-agreements-ontario-what-they-actually-control",
        "title": "Shareholder Agreements in Ontario: What They Actually Control — and Where They Break",
        "anchor": "shareholder agreements in Ontario",
        "role": "pillar",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["shareholder-agreement", "ontario", "corporate"],
    },
    2014: {
        "slug": "shotgun-clause-ontario",
        "title": "The Shotgun Clause in Ontario: When It Stops Being Fair",
        "anchor": "the shotgun clause in Ontario",
        "role": "post",
        "forward": 2008,
        "forward_anchor": "when shares pass to the wrong hands",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["shotgun-clause", "shareholder-agreement", "ontario", "corporate"],
    },
    2008: {
        "slug": "death-disability-insolvency-shareholder-shares-ontario",
        "title": "Death, Disability, and Insolvency: When Shares Pass to the Wrong Hands",
        "anchor": "when shares pass to the wrong hands",
        "role": "post",
        "forward": 2013,
        "forward_anchor": "where share valuation agreements become ambiguous",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["death", "disability", "insolvency", "shareholder-agreement", "ontario", "corporate"],
    },
    2013: {
        "slug": "private-company-share-valuation-ontario",
        "title": "Private Company Share Valuation in Ontario: Where Agreements Become Ambiguous",
        "anchor": "where share valuation agreements become ambiguous",
        "role": "post",
        "forward": 2010,
        "forward_anchor": "what happens when a founder is terminated but keeps their shares",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["valuation", "shareholder-agreement", "ontario", "corporate"],
    },
    2010: {
        "slug": "founder-terminated-still-shareholder-ontario",
        "title": "Founder Terminated, Still a Shareholder: The Problem No One Plans For",
        "anchor": "what happens when a founder is terminated but keeps their shares",
        "role": "post",
        "forward": 2011,
        "forward_anchor": "how minority veto power emerges",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["founder", "employment", "shareholder-agreement", "ontario", "corporate"],
    },
    2011: {
        "slug": "minority-shareholder-rights-ontario",
        "title": "Minority Shareholder Rights in Ontario: How Veto Power Emerges",
        "anchor": "how minority veto power emerges",
        "role": "post",
        "forward": 2015,
        "forward_anchor": "the difference between a USA and a regular shareholder agreement",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["minority-shareholder", "veto", "shareholder-agreement", "ontario", "corporate"],
    },
    2015: {
        "slug": "unanimous-shareholder-agreement-ontario",
        "title": "Unanimous Shareholder Agreements in Ontario: Form vs Substance",
        "anchor": "the difference between a USA and a regular shareholder agreement",
        "role": "post",
        "forward": 2009,
        "forward_anchor": "when your shareholder agreement conflicts with your articles and by-laws",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["unanimous-shareholder-agreement", "usa", "ontario", "corporate"],
    },
    2009: {
        "slug": "shareholder-agreement-articles-by-laws-ontario",
        "title": "Shareholder Agreements vs. Articles and By-Laws in Ontario: When the Documents Don't Match",
        "anchor": "when your shareholder agreement conflicts with your articles and by-laws",
        "role": "post",
        "forward": 2012,
        "forward_anchor": "shareholder agreements in Ontario",
        "pillar_tags": ["shareholder-agreement"],
        "topic_tags": ["shareholder-agreement", "articles", "by-laws", "ontario", "corporate"],
    },

    # P2 — Contractor/Employee
    1980: {
        "slug": "contractor-employee-misclassification-ontario",
        "title": "Contractor vs Employee in Ontario: Where Misclassification Actually Creates Liability",
        "anchor": "contractor vs employee misclassification in Ontario",
        "role": "pillar",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["contractor", "employee", "misclassification", "ontario", "employment"],
    },
    1982: {
        "slug": "cra-test-contractors-ontario",
        "title": "The CRA Test for Contractors in Ontario: How Risk Actually Shows Up",
        "anchor": "the CRA test for contractors in Ontario",
        "role": "post",
        "forward": 1980,
        "forward_anchor": "contractor vs employee misclassification in Ontario",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["cra", "contractor", "classification", "ontario", "employment"],
    },
    1983: {
        "slug": "ip-ownership-contractor-ontario",
        "title": "Who Owns the IP When You Use a Contractor in Ontario",
        "anchor": "who owns the IP when you use a contractor",
        "role": "post",
        "forward": 1985,
        "forward_anchor": "why termination clauses in Ontario often don't work",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["ip", "intellectual-property", "contractor", "ontario", "employment"],
    },
    1984: {
        "slug": "non-compete-agreements-ontario-employer",
        "title": "Non-Compete Agreements in Ontario: What Still Works After the Ban",
        "anchor": "non-compete agreements in Ontario after the ban",
        "role": "post",
        "forward": 1980,
        "forward_anchor": "contractor vs employee misclassification in Ontario",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["non-compete", "restrictive-covenant", "ontario", "employment"],
    },
    1985: {
        "slug": "termination-clauses-ontario-unenforceable",
        "title": "Termination Clauses in Ontario: Why Many Don't Work",
        "anchor": "why termination clauses in Ontario often don't work",
        "role": "post",
        "forward": 1981,
        "forward_anchor": "what actually changes when you convert a contractor to an employee",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["termination-clause", "ontario", "employment"],
    },
    1981: {
        "slug": "contractor-to-employee-conversion-ontario",
        "title": "Converting a Contractor to an Employee: What Actually Changes",
        "anchor": "what actually changes when you convert a contractor to an employee",
        "role": "post",
        "forward": 1980,
        "forward_anchor": "contractor vs employee misclassification in Ontario",
        "pillar_tags": ["contractor-employee"],
        "topic_tags": ["contractor", "employee", "conversion", "ontario", "employment"],
    },

    # P3 — Canadian Subsidiary
    1991: {
        "slug": "setting-up-subsidiary-canada",
        "title": "Setting Up a Subsidiary in Canada: What Foreign Businesses Need to Know",
        "anchor": "setting up a subsidiary in Canada",
        "role": "pillar",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["subsidiary", "canada", "ontario", "foreign-business", "corporate"],
    },
    1987: {
        "slug": "branch-vs-subsidiary-canada",
        "title": "Branch vs Subsidiary in Canada: Which Structure Actually Fits",
        "anchor": "branch vs subsidiary in Canada",
        "role": "post",
        "forward": 1988,
        "forward_anchor": "director residency requirements in Canada",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["branch", "subsidiary", "canada", "corporate"],
    },
    1988: {
        "slug": "director-residency-requirements-canada",
        "title": "Director Residency Requirements in Canada: What Has Changed",
        "anchor": "director residency requirements in Canada",
        "role": "post",
        "forward": 1992,
        "forward_anchor": "what ongoing compliance a Canadian subsidiary requires",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["director-residency", "canada", "cbca", "obca", "corporate"],
    },
    1992: {
        "slug": "canadian-subsidiary-compliance-obligations",
        "title": "Ongoing Compliance for a Canadian Subsidiary: What Gets Missed",
        "anchor": "what ongoing compliance a Canadian subsidiary requires",
        "role": "post",
        "forward": 1990,
        "forward_anchor": "intercompany agreements between a foreign parent and Canadian subsidiary",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["compliance", "subsidiary", "canada", "corporate"],
    },
    1990: {
        "slug": "intercompany-agreements-foreign-parent-canadian-subsidiary",
        "title": "Intercompany Agreements Between a Foreign Parent and Canadian Subsidiary",
        "anchor": "intercompany agreements between a foreign parent and Canadian subsidiary",
        "role": "post",
        "forward": 1986,
        "forward_anchor": "banking and regulatory setup for a Canadian subsidiary",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["intercompany", "transfer-pricing", "subsidiary", "canada", "corporate"],
    },
    1986: {
        "slug": "banking-regulatory-setup-canadian-subsidiary",
        "title": "Banking and Regulatory Setup for a Canadian Subsidiary",
        "anchor": "banking and regulatory setup for a Canadian subsidiary",
        "role": "post",
        "forward": 1989,
        "forward_anchor": "what changes when you hire in Canada through a subsidiary",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["banking", "regulatory", "subsidiary", "canada", "corporate"],
    },
    1989: {
        "slug": "hiring-canada-through-subsidiary",
        "title": "Hiring in Canada Through a Subsidiary: What Actually Changes",
        "anchor": "what changes when you hire in Canada through a subsidiary",
        "role": "post",
        "forward": 1991,
        "forward_anchor": "setting up a subsidiary in Canada",
        "pillar_tags": ["canadian-subsidiary"],
        "topic_tags": ["hiring", "employment", "subsidiary", "canada", "ontario", "corporate"],
    },

    # P4 — Commercial Contracts
    1994: {
        "slug": "commercial-contracts-ontario-businesses",
        "title": "Commercial Contracts for Ontario Businesses: What to Review Before You Sign",
        "anchor": "commercial contracts for Ontario businesses",
        "role": "pillar",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["commercial-contracts", "ontario", "corporate"],
    },
    1998: {
        "slug": "personal-guarantees-ontario-business",
        "title": "Personal Guarantees in Ontario: What Business Owners Are Actually Agreeing To",
        "anchor": "personal guarantees in Ontario",
        "role": "post",
        "forward": 1997,
        "forward_anchor": "what limitation of liability clauses actually protect",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["personal-guarantee", "ontario", "corporate", "contracts"],
    },
    1997: {
        "slug": "limitation-of-liability-clauses-ontario",
        "title": "Limitation of Liability Clauses in Ontario: What They Actually Protect",
        "anchor": "what limitation of liability clauses actually protect",
        "role": "post",
        "forward": 1996,
        "forward_anchor": "what indemnity clauses are actually covering",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["limitation-of-liability", "ontario", "corporate", "contracts"],
    },
    1996: {
        "slug": "indemnity-clauses-ontario",
        "title": "Indemnity Clauses in Ontario: What Is Actually Being Covered",
        "anchor": "what indemnity clauses are actually covering",
        "role": "post",
        "forward": 1993,
        "forward_anchor": "how auto-renewal clauses extend contracts without notice",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["indemnity", "ontario", "corporate", "contracts"],
    },
    1993: {
        "slug": "auto-renewal-clauses-ontario-contracts",
        "title": "Auto-Renewal Clauses in Ontario Contracts: When the Agreement Doesn't End",
        "anchor": "how auto-renewal clauses extend contracts without notice",
        "role": "post",
        "forward": 1995,
        "forward_anchor": "what happens to contracts when your business is sold",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["auto-renewal", "ontario", "corporate", "contracts"],
    },
    1995: {
        "slug": "contracts-business-sold-restructured-ontario",
        "title": "What Happens to Your Contracts When Your Business Is Sold or Restructured",
        "anchor": "what happens to contracts when your business is sold",
        "role": "post",
        "forward": 1994,
        "forward_anchor": "commercial contracts for Ontario businesses",
        "pillar_tags": ["commercial-contracts"],
        "topic_tags": ["assignment", "sale", "restructure", "ontario", "corporate", "contracts"],
    },

    # P6 — Commercial Lending
    # WP IDs are placeholders — replace with real IDs after publishing
    3001: {
        "slug": "commercial-loan-agreement-ontario",
        "title": "Commercial Lending in Ontario: What the Legal Documents Actually Say",
        "anchor": "what commercial loan documents actually contain",
        "role": "pillar",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["commercial-lending", "ppsa", "ontario", "corporate"],
    },
    3002: {
        "slug": "ppsa-security-registration-ontario",
        "title": "PPSA Security in Ontario: What It Means When a Lender Registers Against a Business",
        "anchor": "what a PPSA registration means for a business",
        "role": "post",
        "forward": 3003,
        "forward_anchor": "what personal guarantees cover in commercial lending",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["ppsa", "commercial-lending", "ontario", "corporate"],
    },
    3003: {
        "slug": "personal-guarantee-commercial-loan-ontario",
        "title": "Personal Guarantees in Commercial Lending: What Ontario Business Owners Are Actually Signing",
        "anchor": "what personal guarantees cover in commercial lending",
        "role": "post",
        "forward": 3004,
        "forward_anchor": "how private lending differs from bank lending in Ontario",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["personal-guarantee", "commercial-lending", "ontario", "corporate"],
    },
    3004: {
        "slug": "private-lender-ontario",
        "title": "Private Lenders in Ontario: What Borrowers Need to Know Before They Sign",
        "anchor": "how private lending differs from bank lending in Ontario",
        "role": "post",
        "forward": 3005,
        "forward_anchor": "legal requirements for private mortgage lending in Ontario",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["private-lending", "commercial-lending", "ontario", "corporate"],
    },
    3005: {
        "slug": "private-mortgage-lending-ontario",
        "title": "Private Mortgage Lending in Ontario: Legal Requirements for Lenders and Borrowers",
        "anchor": "legal requirements for private mortgage lending in Ontario",
        "role": "post",
        "forward": 3006,
        "forward_anchor": "how commercial lenders enforce against Ontario businesses",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["private-lending", "private-mortgage", "ontario", "corporate"],
    },
    3006: {
        "slug": "commercial-loan-default-enforcement-ontario",
        "title": "What Happens When a Commercial Lender Enforces Against an Ontario Business",
        "anchor": "how commercial lenders enforce against Ontario businesses",
        "role": "post",
        "forward": 3007,
        "forward_anchor": "the legal risks of crypto-backed lending in Ontario",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["commercial-lending", "ppsa", "enforcement", "default", "ontario", "corporate"],
    },
    3007: {
        "slug": "crypto-backed-lending-ontario",
        "title": "Crypto-Backed Lending in Ontario: What Borrowers Need to Know About Using Digital Assets as Collateral",
        "anchor": "the legal risks of crypto-backed lending in Ontario",
        "role": "post",
        "forward": 3008,
        "forward_anchor": "how to structure a private lending operation in Ontario",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["crypto", "digital-assets", "ppsa", "commercial-lending", "ontario", "corporate"],
    },
    3008: {
        "slug": "set-up-private-lending-ontario",
        "title": "Setting Up a Private Lending Operation in Ontario: Legal Structure and Documentation Requirements",
        "anchor": "how to structure a private lending operation in Ontario",
        "role": "post",
        "forward": 3001,
        "forward_anchor": "what commercial loan documents actually contain",
        "pillar_tags": ["commercial-lending"],
        "topic_tags": ["private-lending", "ppsa", "ontario", "corporate"],
    },

    # P5 — Transactions
    2000: {
        "slug": "buying-selling-business-ontario",
        "title": "Buying or Selling a Business in Ontario: How Deals Actually Come Together — and Where They Break",
        "anchor": "buying or selling a business in Ontario",
        "role": "pillar",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["buying-business", "selling-business", "ontario", "transactions", "corporate"],
    },
    2007: {
        "slug": "share-purchase-vs-asset-purchase-ontario",
        "title": "Share Purchase vs Asset Purchase in Ontario: What Actually Changes",
        "anchor": "share purchase vs asset purchase in Ontario",
        "role": "post",
        "forward": 1999,
        "forward_anchor": "the steps from letter of intent to closing in Ontario",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["share-purchase", "asset-purchase", "ontario", "transactions", "corporate"],
    },
    1999: {
        "slug": "buying-business-ontario-loi-to-closing",
        "title": "Buying a Business in Ontario: From Letter of Intent to Closing",
        "anchor": "the steps from letter of intent to closing in Ontario",
        "role": "post",
        "forward": 2003,
        "forward_anchor": "what is and isn't binding in a letter of intent",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["buying-business", "loi", "closing", "ontario", "transactions", "corporate"],
    },
    2003: {
        "slug": "letter-of-intent-ontario-business",
        "title": "The Letter of Intent in Ontario: What Is Binding and What Is Not",
        "anchor": "what is and isn't binding in a letter of intent",
        "role": "post",
        "forward": 2001,
        "forward_anchor": "what due diligence actually reviews in Ontario business purchases",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["letter-of-intent", "loi", "ontario", "transactions", "corporate"],
    },
    2001: {
        "slug": "due-diligence-ontario-business-purchases",
        "title": "Due Diligence in Ontario Business Purchases: What Gets Reviewed",
        "anchor": "what due diligence actually reviews in Ontario business purchases",
        "role": "post",
        "forward": 2005,
        "forward_anchor": "how representations and warranties allocate risk in Ontario business sales",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["due-diligence", "ontario", "transactions", "corporate"],
    },
    2005: {
        "slug": "representations-warranties-ontario-business-sales",
        "title": "Representations and Warranties in Ontario Business Sales",
        "anchor": "how representations and warranties allocate risk in Ontario business sales",
        "role": "post",
        "forward": 2002,
        "forward_anchor": "how earnout provisions work in Ontario business sales",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["representations", "warranties", "ontario", "transactions", "corporate"],
    },
    2002: {
        "slug": "earnout-provisions-ontario-business-sales",
        "title": "Earnout Provisions in Ontario Business Sales",
        "anchor": "how earnout provisions work in Ontario business sales",
        "role": "post",
        "forward": 2006,
        "forward_anchor": "what needs to be ready when selling your business in Ontario",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["earnout", "ontario", "transactions", "corporate"],
    },
    2006: {
        "slug": "selling-business-ontario-what-needs-to-be-ready",
        "title": "Selling Your Business in Ontario: What Needs to Be Ready",
        "anchor": "what needs to be ready when selling your business in Ontario",
        "role": "post",
        "forward": 2004,
        "forward_anchor": "non-compete agreements in Ontario business sales",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["selling-business", "ontario", "transactions", "corporate"],
    },
    2004: {
        "slug": "non-compete-agreements-ontario-business-sales",
        "title": "Non-Compete Agreements in Ontario Business Sales",
        "anchor": "non-compete agreements in Ontario business sales",
        "role": "post",
        "forward": 2000,
        "forward_anchor": "buying or selling a business in Ontario",
        "pillar_tags": ["business-transactions"],
        "topic_tags": ["non-compete", "business-sale", "ontario", "transactions", "corporate"],
    },
}

# Map: post_id → pillar_id for each pillar
PILLAR_MAP = {
    2012: [2014, 2008, 2013, 2010, 2011, 2015, 2009],
    1980: [1982, 1983, 1984, 1985, 1981],
    1991: [1987, 1988, 1992, 1990, 1986, 1989],
    1994: [1998, 1997, 1996, 1993, 1995],
    2000: [2007, 1999, 2003, 2001, 2005, 2002, 2006, 2004],
    3001: [3002, 3003, 3004, 3005, 3006, 3007, 3008],  # P6 — placeholder IDs
}

# Build reverse: post → pillar
POST_TO_PILLAR = {}
for pillar_id, children in PILLAR_MAP.items():
    POST_TO_PILLAR[pillar_id] = pillar_id  # pillar maps to itself
    for child in children:
        POST_TO_PILLAR[child] = pillar_id


# ── Tag helpers ───────────────────────────────────────────────────────────────

_tag_cache = {}

def get_or_create_tag(name):
    if name in _tag_cache:
        return _tag_cache[name]
    # Search first
    url = f"{BASE_URL}/wp-json/wp/v2/tags?search={urllib.request.quote(name)}&per_page=20"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        tags = json.loads(resp.read().decode())
    for t in tags:
        if t["slug"] == name or t["name"].lower() == name.lower():
            _tag_cache[name] = t["id"]
            return t["id"]
    # Create
    url = f"{BASE_URL}/wp-json/wp/v2/tags"
    data = json.dumps({"name": name, "slug": name}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            t = json.loads(resp.read().decode())
            _tag_cache[name] = t["id"]
            return t["id"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "term_exists" in body:
            import re as _re
            m = _re.search(r'"term_id":(\d+)', body)
            if m:
                tid = int(m.group(1))
                _tag_cache[name] = tid
                return tid
        print(f"    Tag error '{name}': {body[:100]}")
        return None


# ── WordPress helpers ─────────────────────────────────────────────────────────

def wp_get(post_id):
    url = f"{BASE_URL}/wp-json/wp/v2/posts/{post_id}?status=any"
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


def url_for(post_id):
    slug = POSTS[post_id]["slug"]
    return f"{BASE_URL}/{slug}/"


def link(post_id, anchor):
    return f'<a href="{url_for(post_id)}">{anchor}</a>'


# ── Build related-links block ─────────────────────────────────────────────────

def build_related_block(post_id):
    p = POSTS[post_id]
    pillar_id = POST_TO_PILLAR[post_id]

    if p["role"] == "pillar":
        children = PILLAR_MAP[post_id]
        html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
        for child_id in children:
            html += f'  <li>{link(child_id, POSTS[child_id]["anchor"])}</li>\n'
        html += '</ul>\n'
        return html

    # Supporting post: 1 up + 1 forward
    forward_id = p["forward"]
    forward_anchor = p["forward_anchor"]

    html = '\n<hr>\n<h2>Related</h2>\n<ul>\n'
    html += f'  <li>{link(pillar_id, POSTS[pillar_id]["anchor"])}</li>\n'
    html += f'  <li>{link(forward_id, forward_anchor)}</li>\n'
    html += '</ul>\n'
    return html


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Pre-creating all tags...")
    all_tag_names = set()
    for p in POSTS.values():
        all_tag_names.update(p.get("pillar_tags", []))
        all_tag_names.update(p.get("topic_tags", []))
    tag_ids = {}
    for name in sorted(all_tag_names):
        tid = get_or_create_tag(name)
        tag_ids[name] = tid
        print(f"  tag '{name}' → {tid}")

    print("\nUpdating posts...")
    for post_id, meta in POSTS.items():
        print(f"Post {post_id}: {meta['title'][:55]}...")

        post = wp_get(post_id)
        current_content = post.get("content", {}).get("rendered", "")

        if "<hr>" in current_content:
            current_content = current_content[:current_content.rfind("<hr>")]

        related_block = build_related_block(post_id)
        new_content = current_content.strip() + related_block

        all_tags = set(meta.get("pillar_tags", []) + meta.get("topic_tags", []))
        tag_id_list = [tag_ids[t] for t in all_tags if t in tag_ids and tag_ids[t]]

        result = wp_patch(post_id, {
            "slug": meta["slug"],
            "content": new_content,
            "tags": tag_id_list,
        })

        if result:
            print(f"  ✓ slug={result.get('slug')}  tags={len(tag_id_list)}")
        else:
            print(f"  ✗ failed")


if __name__ == "__main__":
    main()
