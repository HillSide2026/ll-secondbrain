---
id: mkt_skill_wordpress_page_setup
title: WordPress Page Setup Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [wordpress, page-setup, seo, menu, permalinks]
---

# Skill: WordPress Page Setup

## Purpose
Produce a complete WordPress page setup checklist for ML1 to execute before
building in Thrive Architect.

## Inputs
- Page title, slug, level (Level 2 / Level 3)
- Parent page (if Level 3)
- Menu name and position
- SEO title and meta description
- Canonical URL

## Process
Produce checklist:

### WordPress Page Settings
- [ ] Page title: [title]
- [ ] URL slug: [/slug] — confirm via Settings > Permalinks (must be "Post name")
- [ ] Parent page: [parent title] (Level 3 pages only; leave blank for Level 2)
- [ ] WordPress page template: Full Width / No Sidebar (for Thrive Architect pages)
- [ ] Page status: Draft (do not publish until content is approved by ML1)
- [ ] Thrive Architect: click "Launch Thrive Architect" to enter editor

### Menu Assignment
- [ ] WordPress Appearance > Menus > [menu name]
- [ ] Add page to menu at position [n]
- [ ] Set menu item label: [label]
- [ ] If Level 3: nest under correct Level 2 menu item

### SEO Plugin (Yoast or RankMath)
- [ ] SEO title: [title tag — under 60 characters]
- [ ] Meta description: [160 characters max]
- [ ] Canonical URL: [full URL]
- [ ] Robots: Index, Follow (default; change only if page should not be indexed)

### Post-build checks
- [ ] All internal links verified in Thrive editor
- [ ] CTA buttons link to correct targets
- [ ] Page previews correctly on mobile (use Thrive responsive preview)
- [ ] No broken image slots

### ML1 Publish Step
This page is a Draft. To publish: confirm all content and links in Thrive
Architect, change Status from Draft to Published in WordPress page settings,
and verify menu item is active and links correctly.

## Outputs
- Complete WordPress page setup checklist (as above)

## Constraints
- Page must remain in Draft status until ML1 explicitly approves publication.
- INV-0002 applies: no autonomous publish.

## Invocation
Used as part of every Thrive build packet, before the ML1 publish step.
