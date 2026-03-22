---
id: mkt_skill_thrive_template_config
title: Thrive Template Configuration Skill
owner: ML1
status: active
created_date: 2026-03-21
last_updated: 2026-03-21
tags: [thrive, wordpress, theme-builder, templates]
---

# Skill: Thrive Template Configuration

## Purpose
Configure Thrive Theme Builder templates (header, footer, blog archive, single
post) and assign WordPress menus and Symbols to template regions.

## Inputs
- Template type to configure (header / footer / blog archive / single post /
  404 / search)
- Approved content and Symbol definitions
- WordPress menu structure

## Process
1. Identify the template type in Thrive Theme Builder.
2. Define the template structure (elements and their configuration).
3. Assign Symbols to template regions (e.g. LL_Global_Footer Symbol → footer
   template region).
4. Assign WordPress menus:
   - Header template → WordPress Appearance > Menus > [menu name] → assign to
     Primary Navigation location.
5. Configure sticky header: scroll trigger, height change on scroll, background
   color change.
6. Configure mobile header: hamburger menu trigger, mobile menu style, close
   behavior.
7. Configure blog archive: post grid or list layout, posts per page, category
   filter, pagination style.
8. Configure single post template: content area, sidebar (if applicable), related
   posts, author box.

## Outputs
- Template configuration spec per template type:
  - Template name and type
  - Element structure and configuration
  - Symbol assignments
  - Menu assignments
  - Responsive behavior

## Constraints
- Template changes affect all pages using that template. Document impact before
  recommending changes to existing templates.

## Invocation
Used when setting up or updating Thrive Theme Builder template structure.
