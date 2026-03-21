---
id: 04_initiatives__hillside_portfolio__business_projects__hbp_004_micro_saas_build_and_launch__executing__qa_checklist_md
title: Develop and Launch Micro SaaS (TariffLookup.ca) - QA Checklist
owner: ML1
status: active
created_date: 2026-03-20
last_updated: 2026-03-20
tags: [micro-saas, executing, qa]
---

# QA Checklist

Project ID: `HBP-004`
Stage: `Executing`

| Check | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Static bundle contains home page, styles, privacy, robots, sitemap, and 404 files | complete | `tarifflookup_site/` file set | Bundle is ready for upload |
| Landing page production render verified on live domain | pending | live domain review | Blocked by HostGator-side resolution |
| CTA and contact route verified in deployed environment | pending | live site review | Current CTA points to `hello@tarifflookup.ca` in bundle files |
| Privacy / SEO support files present in deployment bundle | complete | bundle files present | Production verification still pending |
| MVP lookup workflow returns valid structured tariff output | pending | application test evidence | Feature not yet live |
| Sampled accuracy review completed against approved sources | pending | QA sample review | Depends on MVP data and lookup flow |
| Launch-blocking issues reviewed before go-live | in progress | `PROJECT LOG.md` | Hosting blocker currently open |
