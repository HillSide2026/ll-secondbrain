---
id: financial_services__market_structure_framework
title: Financial Services — Market Structure Framework
owner: ML1
status: approved
approved_by: ML1
approved_date: 2026-04-17
version: 1.2
tags: [financial-services, market-structure, practice-area, scope]
---

# Financial Services — Market Structure Framework

## Purpose

This document defines the canonical five-level structural map of financial
services activity. It establishes where Levine Law operates, where it does
not, and why. All solutions, strategies, and agents in this practice area
inherit their scope boundaries from this framework.

This is a reference document, not a binding policy. It does not constrain
agent behavior directly — it governs scope decisions for strategies and
solutions built on top of it.

---

## The Five-Level Stack

| Level | Function | Risk Type | Who Bears It |
|---|---|---|---|
| 1 | Move money | Operational | Almost nobody (in theory) |
| 2 | Lend money | Credit | You |
| 3 | Hold money | Liability / insolvency | You (but disguised) |
| 4 | Create money (banking) | Systemic | You + regulator |
| 5 | Define money | Sovereign | State |

---

## RPAA Payment Functions — Statutory Reference

The five payment functions under s. 2 of the *Retail Payment Activities Act*,
SC 2021, c. 23 (exact statutory language):

| # | Payment Function |
|---|---|
| (a) | The provision or maintenance of an account that, in relation to an electronic funds transfer, is held on behalf of one or more end users |
| (b) | The holding of funds on behalf of an end user until they are withdrawn or transferred |
| (c) | The initiation of an electronic funds transfer at the request of an end user |
| (d) | The authorization of an electronic funds transfer or the transmission, reception or facilitation of an instruction in relation to an electronic funds transfer |
| (e) | The provision of clearing or settlement services |

### The (a)/(b) Distinction — Structural Key

Functions (a) and (b) are legally separate and this separation is architecturally
significant.

Function (a) — *providing or maintaining the account* — is an infrastructure
role. The PSP maintains the account as a record or ledger. The account can be
provided without the PSP controlling the funds held in it. The money may sit
with a bank sponsor or other institution while the PSP operates the account
layer above it.

Function (b) — *holding funds* — is where the PSP takes actual custody of
end-user money. The funds are in the PSP's control until withdrawn or
transferred.

A PSP can perform (a) without (b). This is the structural design of most
pass-through and bank-sponsored fintech models: the PSP provides the account
layer; the bank holds the underlying funds. The PSP is Level 1 with no fund
control.

**The moment a PSP holds the balance itself, it has moved into (b) — and that
is where the Level 1 / Level 3 boundary begins.**

The safeguarding obligation under the RPAA attaches only to PSPs performing
function (b). A PSP performing only (a), (c), (d), or (e) without holding
funds has no safeguarding obligation (though all other operational risk
requirements apply).

---

## Level Definitions

### Level 1 — Payment Execution (Flow Layer)

**What it is:** Moving money without controlling it.

Defined by the RPAA payment functions. Level 1 operators perform one or more of:
- **(a)** Provision or maintenance of a payment account — without necessarily
  controlling the funds in it
- **(c)** Initiation of EFTs at the request of an end user
- **(d)** Authorization of EFTs, or transmission, reception, facilitation of
  payment instructions
- **(e)** Clearing or settlement services

A Level 1 operator may also perform **(b)** (holding funds) — but only
transiently, in the course of executing a payment function. When the holding
becomes structural (an ongoing balance, a stored value product), the operator
has moved into Level 3.

No balance sheet risk in theory. Operators in this layer pretend not to
touch money. They do — but try not to own it.

Participants:
- Payment processors
- PSPs under the RPAA
- MSBs (money transmission aspect)
- Card programs (program manager layer)
- FX execution (non-principal)

Core legal focus:
- Safeguarding / segregation (RPAA — function (b) only)
- Operational risk
- AML/ATF (PCMLTFA)
- Agency vs principal characterization
- Account provision vs fund control (the (a)/(b) distinction)

**LL position:** Core practice area. Fully built. Commoditized but
compliance-heavy — clients need a lawyer, not a consultant.

---

### Level 2 — Balance Sheet Lite (Credit Intermediation)

**What it is:** Taking risk on who pays back, but not creating money.

Participants:
- Private lenders
- Factoring / receivables financing
- Merchant cash advance
- Crypto-backed lending
- Trade finance (non-bank)

Core legal focus:
- Credit risk allocation
- Security / collateral
- Priority (PPSA)
- True sale vs secured loan characterization

Key distinction from Level 1: you now care about repayment, not just movement.

**LL position:** In scope. Legal value is real — structure and enforcement
questions are genuinely complex. Solutions not yet built in this playbook.
Content exists in Funnel 2 (P6 pillar) but has not been formalized as
practice area solutions.

---

### Level 3 — Client Fund Holding

**What it is:** Holding of client funds as an ongoing structural obligation —
not transiently in the course of a payment, but as a product feature or
core business model.

This is RPAA function (b) in its structural form: the PSP holds funds on
behalf of end users not merely to move them, but as a persistent balance
or stored value. The holding itself is the product.

Participants:
- Wallets / stored value accounts
- Prepaid programs
- EMI-style models (UK/EU concept)
- Fiat-backed stablecoins (functionally similar)

Core legal tension (Canada specifically):
- Is this a deposit substitute?
- Are you creating a monetary liability?
- Canada actively suppresses this layer — the Bank Act resists recognizing
  non-bank monetary liabilities.

Core legal focus:
- Custody vs deposit characterization
- Trust vs beneficial ownership
- Insolvency treatment
- Safeguarding (structurally different from Level 1 — the obligation is
  ongoing, not transient)

**LL position:** Highest strategic value in the stack. Regulatory friction
is high — which is exactly where legal advisory is most valuable. No
solutions currently built. The characterization analysis (especially the
Canada-specific Bank Act constraint) is the core intellectual product at
this layer.

---

### Level 4 — Regulated Lending + Deposit-Taking (Banking Core)

**What it is:** Full balance sheet intermediation.

Participants:
- Banks
- Credit unions
- Deposit-taking institutions

Core functions: take deposits, make loans, create money via lending.

Legal regime: prudential regulation (OSFI), capital requirements, liquidity
coverage, deposit insurance (CDIC).

**LL position:** Soft wall. A charter is required to operate at Level 4, and
no amount of legal advisory confers one. However, LL can advise clients
navigating toward Level 4 — readiness work, structural preparation, and
questions that arise at the boundary between Level 3 and Level 4.
The wall is soft and unspoken: no statute prohibits the conversation, but
the commercial reality is that the gate is regulatory, not legal.

---

### Level 5 — Monetary Sovereign / Infrastructure Layer

**What it is:** Control of the system itself. A categorically different
universe from Levels 1–4.

Participants:
- Central banks (Bank of Canada)
- Payment clearing and settlement systems

Core powers: issue base money, final settlement, system stability.

**LL position:** No role. No wall is needed — there is no door. The answer
to "can a client operate here" is 100% political, not legal. Sovereign
discretion governs. LL has nothing to say at Level 5 and should not
represent otherwise.

---

## LL Operating Map

| Level | LL Position | Playbook Status |
|---|---|---|
| 1 — Payment Execution | Core practice area | Fully built (PAYMENTS) |
| 2 — Credit Intermediation | In scope | Not yet built — gap |
| 3 — Client Fund Holding | In scope — highest strategic value | Not yet built — gap |
| 4 — Regulated Deposit-Taking | Boundary advisory only; soft wall | No solutions; correctly limited |
| 5 — Monetary Sovereign | Out of scope entirely | Correctly absent |

---

## Scope Inheritance

Solutions and strategies built in this practice area must identify which
level(s) they serve. A solution that spans levels must make the
characterization question explicit — the answer often determines the
entire regulatory path.

Agents operating in this practice area must refuse to advise on Level 5
matters and must flag Level 4 matters as boundary cases requiring ML1
judgment before proceeding.

---

## Open Build Priorities

1. **Level 2 solutions** — private lending, factoring, PPSA, crypto-backed
   lending
2. **Level 3 framework** — characterization analysis, Bank Act constraints,
   stablecoin positioning, Canada-specific client fund holding doctrine

---

## First Order Principles

Foundational interpretive positions that govern how this practice area
approaches ambiguous characterization questions. These are not safe harbours —
they are the starting points for analysis.

---

### FOP-001 — The Technology Provider Ambiguity

**Principle:**
A software vendor, ledger provider, or white-label infrastructure operator
that "maintains" account records for another entity is sitting in ambiguous
territory under the RPAA.

**Analysis:**
The Act as written would arguably capture such an operator under payment
function (a) — provision or maintenance of an account held on behalf of end
users. The account records are being maintained; end users are the ultimate
beneficiaries.

However, the PSP definition contains a carve-out: a person or entity is only
a PSP if it performs payment functions "as a service or business activity that
is not incidental to another service or business activity." A pure technology
provider whose core product is infrastructure — not payments — may fall outside
the definition on this basis. The payment function would be incidental to the
software business, not the business itself.

**Why it matters:**
The carve-out is unlitigated. The Bank of Canada has not issued guidance
specifically addressing where the technology provider line falls. The online
marketplaces supervisory policy (December 2025) is the closest published
guidance on intermediary/infrastructure roles, but it targets marketplace
platforms, not pure ledger or white-label operators.

**Implication for practice:**
Any client operating as a white-label payment infrastructure provider,
ledger-as-a-service, or technology intermediary for a licensed PSP must
analyze both sides of this principle before concluding they are out of scope.
Assuming the incidental carve-out applies without that analysis is a
compliance risk. Assuming the Act captures them without testing the carve-out
is an over-registration risk.

**Status:** Unlitigated. Bank of Canada interpretive guidance pending.

---

### FOP-002 — Account Provision/Maintenance Does Not Trigger Safeguarding

**Principle:**
Neither the provision nor the maintenance of a payment account — function (a)
alone — triggers the safeguarding obligation under the RPAA.

**Analysis:**
The safeguarding obligation attaches exclusively to PSPs that perform payment
function (b): holding funds on behalf of an end user until they are withdrawn
or transferred. A PSP that provisions or maintains a payment account without
holding the underlying funds is performing function (a) only. The safeguarding
framework — trust account, insurance/guarantee, or prescribed method — does
not apply to that operator.

The account and the funds in it are legally separable. The entity that
maintains the account record is not necessarily the entity that holds the
money. In a bank-sponsored or pass-through model, the sponsoring bank holds
the funds; the PSP maintains the account layer. Only the bank (or whichever
entity holds the funds) is subject to the safeguarding obligation.

**Why it matters:**
Mischaracterizing an account-layer operator as a fund-holder exposes the
client to over-compliance costs and misdirected regulatory posture. Conversely,
a client that holds funds but characterizes its activity as mere account
maintenance to avoid the safeguarding regime is in violation — the Bank of
Canada treats safeguarding failures as the highest AMP severity tier.

**Implication for practice:**
The first question in any RPAA safeguarding analysis is always: does this
client actually hold end-user funds, or does it provide/maintain the account
while funds sit elsewhere? The answer determines whether the safeguarding
framework applies at all.

**Status:** Settled by statute. RPAA s. 2, functions (a) and (b).
