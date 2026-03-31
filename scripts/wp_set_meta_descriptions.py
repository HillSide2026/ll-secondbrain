#!/usr/bin/env python3
"""
wp_set_meta_descriptions.py

Sets RankMath meta descriptions on all F2 and F3 blog posts.
Uses /rankmath/v1/updateMeta endpoint.

Max 160 characters per description. Keyword-leading.
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

# ── Meta descriptions ─────────────────────────────────────────────────────────

META = {

    # ── F3 EO1 — MSB Registration ────────────────────────────────────────────
    1867: "MSB registration in Canada: who needs to register with FINTRAC, what the test is, and what happens if you're operating without registration.",
    1868: "Ongoing AML obligations for registered MSBs in Canada. What FINTRAC expects after registration and where compliance programs fall short.",
    1869: "What FINTRAC looks for in an MSB compliance review. How examiners assess your program and the gaps that most commonly trigger findings.",
    1870: "Cross-border payroll and contractor payments through Canadian MSBs. How payment flows are classified and what triggers MSB registration.",
    1871: "MSB registration requirements in Canada: the checklist of what FINTRAC requires, how to prepare, and what delays the process.",
    1872: "Do you need a Canadian entity to register as an MSB? When foreign businesses trigger FINTRAC registration and what structure is required.",
    1873: "How long MSB registration takes in Canada. Typical FINTRAC timelines, what causes delays, and how to manage the process.",
    1874: "What information FINTRAC requires on the MSB registration form. A practical walkthrough of the registration data requirements.",
    1875: "How to map a payment flow for MSB classification in Canada. The analysis FINTRAC applies and how to document your activity correctly.",
    1876: "Payment facilitator vs MSB in Canada: how the distinction is drawn, where platforms fall, and what triggers registration.",
    1877: "Crypto and stablecoin businesses as MSBs in Canada. How FINTRAC classifies virtual currency dealers and what registration requires.",
    1878: "MSB registration timeline and process delays in Canada. What to expect and how to avoid common bottlenecks with FINTRAC.",
    1879: "Remittance and money transfer licensing in Canada. The MSB rules that apply to remittance businesses operating in or into Canada.",
    1880: "Cross-border payment regulatory requirements in Canada. What payment flows trigger MSB registration and ongoing AML obligations.",
    1881: "Do payment processors need to register as MSBs in Canada? How FINTRAC classifies payment processing activity and where the line is.",
    1882: "Are marketplaces MSBs in Canada? When marketplace payment flows trigger FINTRAC registration and what the classification test is.",
    1883: "Banking partners and sponsor obligations for MSBs in Canada. What your bank expects from your AML program and how to meet it.",
    1884: "Operating without MSB registration in Canada. The penalties FINTRAC can impose and what enforcement actually looks like.",
    1903: "SaaS and embedded payments as MSBs in Canada. When software-enabled payment flows trigger FINTRAC registration obligations.",
    1904: "How banks assess MSB risk in Canada. What financial institutions look for before onboarding an MSB and what triggers rejection.",
    1905: "Designing payment flows to manage MSB risk in Canada. How payment architecture affects FINTRAC classification and banking relationships.",

    # ── F3 EO3 — AML Health Check ────────────────────────────────────────────
    1910: "AML compliance for MSBs in Canada: how risk actually shows up, what FINTRAC examines, and where most compliance programs fall short.",
    1911: "How to prepare for a FINTRAC examination as an MSB. What examiners review, how to organize your program, and what to expect.",
    1912: "Transaction monitoring failures in Canadian fintechs. The most common gaps in monitoring programs and how FINTRAC identifies them.",
    1913: "AML documentation requirements for MSBs in Canada. What records must be kept, how long, and what FINTRAC looks for in an audit.",
    1914: "Common AML program failures at Canadian MSBs. The structural weaknesses that FINTRAC finds most frequently and how to address them.",
    1915: "Why banks reject fintechs on AML grounds in Canada. What financial institutions assess and how to address the gaps that cause rejection.",
    1916: "What banks ask fintech clients during AML onboarding in Canada. The documentation, questions, and program requirements banks expect.",
    1917: "How banks assess AML risk for MSB clients in Canada. The risk factors that determine whether your business can get and keep banking.",
    1918: "What counts as a suspicious transaction in Canada. How FINTRAC defines suspicion and how MSBs should apply the standard.",
    1919: "When you have to file an STR in Canada. The FINTRAC reporting obligation, the timing rules, and what triggers a filing requirement.",
    1920: "Do all unusual transactions require an STR in Canada? How to distinguish unusual activity from reportable suspicion under FINTRAC.",
    1921: "What happens after you file an STR with FINTRAC. The process, confidentiality obligations, and what to expect following a filing.",

    # ── F3 EO2 — STR Triage ──────────────────────────────────────────────────
    1934: "The STR framework in Canada: how FINTRAC suspicious transaction reporting decisions are structured and what makes a filing defensible.",
    1935: "Suspicion vs reportability in Canada: what reasonable grounds to suspect actually means and how the threshold applies in practice.",
    1936: "When does an unusual transaction become reportable in Canada? How to apply the STR threshold and what tips the analysis toward filing.",
    1937: "Over-reporting vs under-reporting STRs in Canada. The real risk of each approach and how to build a consistent decision framework.",
    1938: "Why documentation matters more than filing in STR reporting. How FINTRAC assesses your reasoning and what records must support decisions.",
    1939: "Building a defensible STR narrative in Canada. What FINTRAC reviewers look for in the description and how to structure your reasoning.",
    1940: "What FINTRAC reviews when examining STR reporting at MSBs. The criteria examiners apply and how your program is assessed.",
    1941: "The internal escalation and STR review process. How decisions should flow through your organization before a report is filed.",
    1942: "When to seek STR triage support in Canada. The situations where internal processes are insufficient and outside review is warranted.",
    1943: "Controlled regulatory response vs reactive STR filing. How a structured approach produces better outcomes than filing under pressure.",
    1944: "STR reporting for crypto-enabled MSBs in Canada. How virtual currency activity is assessed under the FINTRAC suspicious transaction standard.",
    1945: "Cross-border payments and STR complexity in Canada. How international flows affect the suspicion analysis and reporting obligations.",
    1946: "What a mature STR framework looks like for Canadian MSBs. The structural elements of a program that withstands FINTRAC scrutiny.",
    1947: "The cost of inconsistent STR decisions in Canada. How unpredictable filing patterns create regulatory and legal exposure for MSBs.",
    1948: "STRs are about suspicion, not proof. Why the FINTRAC reporting standard does not require certainty and what that means in practice.",
    1949: "If you can't articulate the narrative, you're not ready to file. How the inability to explain suspicion signals a documentation problem.",
    1950: "One indicator is rarely enough for an STR. How FINTRAC expects MSBs to assess the totality of circumstances before filing.",

    # ── F3 EO4 — Crypto AML ──────────────────────────────────────────────────
    1951: "Crypto payments and AML risk in Canada: what changes under FINTRAC when value moves through virtual currency and what stays the same.",
    1952: "Stablecoins and AML assumptions in Canada: why price stability doesn't mean structural transparency and what monitoring must account for.",
    1953: "On-chain vs off-chain AML visibility in Canada. Where the fragmentation in crypto payment systems disrupts standard compliance analysis.",
    1954: "Wallet-based payments and counterparty identification in Canada. How AML analysis shifts when identity is not directly observable.",
    1944: "STR reporting for crypto-enabled MSBs in Canada. How virtual currency activity is assessed under the FINTRAC suspicious transaction standard.",
    1955: "Crypto payment flows and MSB classification in Canada. How control over value movement determines whether FINTRAC registration applies.",

    # ── F2 P1 — SHA ──────────────────────────────────────────────────────────
    2012: "Shareholder agreements in Ontario: what they actually control, how misalignment develops over time, and where they break under pressure.",
    2014: "The shotgun clause in Ontario: how it works, why financial asymmetry makes it unfair in practice, and what happens when it's triggered.",
    2008: "What happens to shares when a shareholder dies, becomes disabled, or goes insolvent in Ontario. The gaps most agreements leave open.",
    2013: "Private company share valuation in Ontario: why 'fair market value' without a defined methodology creates disputes instead of resolving them.",
    2010: "Founder terminated but still a shareholder in Ontario: the two-hat problem and why ending employment doesn't remove ownership rights.",
    2011: "Minority shareholder rights in Ontario: how vague governance thresholds give small shareholders functional veto power over business decisions.",
    2015: "Unanimous shareholder agreements in Ontario: the difference between form and substance, and how liability follows control under the OBCA.",
    2009: "When your shareholder agreement conflicts with your articles and by-laws in Ontario: which document controls and what that means in practice.",

    # ── F2 P2 — Contractor/Employee ──────────────────────────────────────────
    1980: "Contractor vs employee misclassification in Ontario: how liability develops over time and what CRA and common law tests actually measure.",
    1982: "The CRA test for contractors in Ontario: control, tools, profit/loss risk, and integration — how the analysis works in practice.",
    1983: "IP ownership when using contractors in Ontario: why payment doesn't transfer copyright and what assignment requires.",
    1984: "Non-compete agreements in Ontario after the 2021 ban: what still works, what doesn't, and how misclassification affects enforceability.",
    1985: "Termination clauses in Ontario employment contracts: why so many are unenforceable and what happens when they fail.",
    1981: "Converting a contractor to an employee in Ontario: what changes, what past exposure remains, and why documentation must be rebuilt.",

    # ── F2 P3 — Canadian Subsidiary ──────────────────────────────────────────
    1991: "Setting up a subsidiary in Canada: branch vs subsidiary, federal vs provincial incorporation, and why structure must precede operations.",
    1987: "Branch vs subsidiary in Canada: how the choice determines where liability sits, how tax applies, and what operational flexibility looks like.",
    1988: "Director residency requirements for Canadian corporations: what the CBCA and OBCA require and how governance works with non-resident directors.",
    1992: "Ongoing compliance for a Canadian subsidiary: what corporate records, annual filings, and resolutions are required and what gets missed.",
    1990: "Intercompany agreements between a foreign parent and Canadian subsidiary: why they must exist and what transfer pricing exposure they address.",
    1986: "Banking and regulatory setup for a Canadian subsidiary: account opening requirements, MSB considerations, and FINTRAC triggers.",
    1989: "Hiring in Canada through a subsidiary: how Ontario employment standards apply, how classification works, and what payroll requires.",

    # ── F2 P4 — Commercial Contracts ─────────────────────────────────────────
    1994: "Commercial contracts for Ontario businesses: how risk is allocated across key provisions and what to assess before you sign.",
    1998: "Personal guarantees in Ontario: how they create direct personal liability outside the company structure and what limits their scope.",
    1997: "Limitation of liability clauses in Ontario: what they cap, what they don't cover, and how indemnities can sit outside the limit.",
    1996: "Indemnity clauses in Ontario commercial contracts: how they shift risk beyond direct damages and why they often outweigh liability caps.",
    1993: "Auto-renewal clauses in Ontario contracts: how they extend agreements silently and why missing the notice window locks you in.",
    1995: "What happens to contracts when your Ontario business is sold or restructured: assignment restrictions and change-of-control triggers.",

    # ── F2 P5 — Transactions ─────────────────────────────────────────────────
    2000: "Buying or selling a business in Ontario: how the structure, diligence, and risk allocation decisions connect — and where deals break down.",
    2007: "Share purchase vs asset purchase in Ontario: what the structural choice determines about liability, contracts, and tax treatment.",
    1999: "Buying a business in Ontario from LOI to closing: how the stages overlap, where friction develops, and what drives the timeline.",
    2003: "The letter of intent in Ontario business sales: which provisions are binding, which aren't, and why the document still shapes outcomes.",
    2001: "Due diligence in Ontario business purchases: what gets reviewed, what commonly gets missed, and how gaps affect price and structure.",
    2005: "Representations and warranties in Ontario business sales: how they allocate risk, what inaccuracy triggers, and how claims are limited.",
    2002: "Earnout provisions in Ontario business sales: how deferred price mechanisms work and why the drafting determines how disputes are resolved.",
    2006: "Selling your business in Ontario: what records, ownership clarity, and contract consistency buyers expect to find in due diligence.",
    2004: "Non-compete agreements in Ontario business sales: why the employment ban doesn't apply and what scope and duration are enforceable.",
}


def set_meta(post_id, description):
    url = f"{BASE_URL}/wp-json/rankmath/v1/updateMeta"
    payload = {
        "objectID": post_id,
        "objectType": "post",
        "meta": {"description": description},
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ERROR {e.code}: {e.read().decode()[:150]}")
        return None


def main():
    ok = 0
    fail = 0
    for post_id, desc in META.items():
        length = len(desc)
        flag = " ⚠ LONG" if length > 160 else ""
        result = set_meta(post_id, desc)
        if result:
            print(f"  ✓ {post_id}  ({length} chars){flag}")
            ok += 1
        else:
            print(f"  ✗ {post_id}")
            fail += 1
    print(f"\nDone: {ok} updated, {fail} failed")


if __name__ == "__main__":
    main()
