# Artifact Schemas

All markdown files in this repository MUST begin with YAML frontmatter.

## Required Fields (All Artifacts)

---
id:
title:
owner: ML1
status: draft | proposed | approved | deprecated
created_date:
last_updated:
tags: []
---

## Additional Fields (Doctrine)

---
effective_date:
supersedes:
provenance:
  decided_by: ML1
  decided_on:
  context:
---

## Matter

Matter = {
  overview,
  facts,
  Records (documents + communications including email)
  analysis,
  Outputs
  actions,
}
