---
id: 00_system__agents__specs__marketing__single_layer_marketing_agent_stack_md
title: Single-Layer Marketing Agent Stack
owner: ML1
status: draft
created_date: 2026-03-22
last_updated: 2026-04-03
tags: [marketing, agents, consolidated, skills]
---

# Single-Layer Marketing Agent Stack

## Purpose

Create one flat operating view of the LL marketing system by merging:
- the initiative-level funnel agents tracked in `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/AGENT_ROSTER.md`
- the system-level website, design, and implementation agents tracked in `00_SYSTEM/AGENTS/specs/marketing/`

This artifact is a consolidation layer.
It does not replace the source charters or source activation records.

## Consolidation Rules

- `MKT_CHIEF_MARKETING_OFFICER_AGENT` orchestrates the stack.
- `SE-01` remains the mandatory strategic and coherence gate before ML1 approval.
- No agent publishes autonomously.
- Each agent in this consolidated layer carries a minimum operating bundle of 10 skills.
- If a source charter already lists more than 10 skills, that source charter still stands.
- If a source charter does not yet declare a 10-skill bundle, the bundle below is the consolidated minimum operating bundle.

## Flat Roster

| Agent | Role | Status | Source Layer |
| --- | --- | --- | --- |
| `MKT_CHIEF_MARKETING_OFFICER_AGENT` | Marketing system orchestration | active | system marketing suite |
| `SE-01` | Strategic coherence and positioning gate | active - lightweight mode | initiative funnel roster |
| `SEO-01` | SEO intelligence and keyword analytics | active - limited scope | initiative funnel roster |
| `SPE-01` | Top-of-funnel authority hooks | blocked | initiative funnel roster |
| `BSE-01` | Long-form SEO and authority content | blocked | initiative funnel roster |
| `CA-01` | Conversion optimization | blocked | initiative funnel roster |
| `MKT_DESIGN_PRODUCTION_AGENT` | Draft visual asset production | active | system marketing suite |
| `MKT_UX_DESIGN_AGENT` | UI/UX specification and handoff | active | system marketing suite |
| `MKT_THRIVE_THEMES_AGENT` | Thrive Architect build-packet generation | active | system marketing suite |
| `MKT_WEBSITE_IMPLEMENTATION_AGENT` | Website implementation and release prep | active | system marketing suite |
| `MKT_MUGGAH_SECURITIES_AGENT` | Funnel 3 securities-adjacent perimeter specialist | draft | system marketing suite |
| `MKT_MUGGAH_MONEY_SERVICES_AGENT` | Funnel 3 money-services perimeter specialist | draft | system marketing suite |
| `MKT_MUGGAH_PAYMENT_SERVICES_AGENT` | Funnel 3 payment-services perimeter specialist | draft | system marketing suite |

## Agent Skill Bundles

### `MKT_CHIEF_MARKETING_OFFICER_AGENT`

Role: orchestration, sequencing, dependency management, and funnel execution control.

Minimum skill bundle:
- `task_decomposition.skill.md`
- `skill_selection.skill.md`
- `context_assembly.skill.md`
- `execution_validation.skill.md`
- `artifact_promotion.skill.md`
- `campaign_design.skill.md`
- `funnel_architecture.skill.md`
- `offer_engineering.skill.md`
- `demand_capture.skill.md`
- `revenue_attribution.skill.md`

### `SE-01`

Role: final strategic editor and coherence gate across all outward-facing artifacts.

Minimum skill bundle:
- `doctrine_alignment_check.skill.md`
- `brand_voice_validation.skill.md`
- `editorial_quality_review.skill.md`
- `factual_claim_validation.skill.md`
- `marketing_policy_compliance.skill.md`
- `positioning_drift_detection.skill.md`
- `differentiation_detection.skill.md`
- `market_position_mapping.skill.md`
- `audience_segmentation.skill.md`
- `banned_claims_guard.skill.md`

### `SEO-01`

Role: keyword discovery, intent analysis, and search-performance interpretation.

Minimum skill bundle:
- `keyword_mapping.skill.md`
- `search_intent_clustering.skill.md`
- `seo_gap_analysis.skill.md`
- `on_page_optimization.skill.md`
- `market_feedback_analysis.skill.md`
- `performance_signal_reporting.skill.md`
- `revenue_attribution.skill.md`
- `audience_segmentation.skill.md`
- `competitor_message_analysis.skill.md`
- `campaign_brief_generation.skill.md`

### `SPE-01`

Role: high-signal top-of-funnel hooks for LinkedIn and authority-led outreach.

Minimum skill bundle:
- `short_form_content_generation.skill.md`
- `short_form_narrative_structuring.skill.md`
- `social_thread_design.skill.md`
- `platform_voice_calibration.skill.md`
- `audience_segmentation.skill.md`
- `demand_capture.skill.md`
- `cta_design.skill.md`
- `market_position_mapping.skill.md`
- `differentiation_detection.skill.md`
- `doctrine_alignment_check.skill.md`

### `BSE-01`

Role: structured long-form SEO and authority-content production.

Minimum skill bundle:
- `long_form_content_generation.skill.md`
- `content_adaptation.skill.md`
- `keyword_mapping.skill.md`
- `search_intent_clustering.skill.md`
- `on_page_optimization.skill.md`
- `seo_gap_analysis.skill.md`
- `brand_voice_validation.skill.md`
- `doctrine_alignment_check.skill.md`
- `editorial_quality_review.skill.md`
- `cta_design.skill.md`

### `CA-01`

Role: conversion-path optimization across diagnostic, remediation, and retainer flow.

Minimum skill bundle:
- `conversion_path_design.skill.md`
- `landing_flow_optimization.skill.md`
- `demand_capture.skill.md`
- `offer_engineering.skill.md`
- `revenue_attribution.skill.md`
- `performance_signal_reporting.skill.md`
- `engagement_data_collection.skill.md`
- `forms_and_conversion_ux.skill.md`
- `cta_design.skill.md`
- `landing_page_copywriting.skill.md`

### `MKT_DESIGN_PRODUCTION_AGENT`

Role: governed draft design production from approved copy and templates.

Minimum skill bundle:
- `frontend_design.skill.md`
- `design_brief_translation.skill.md`
- `template_slot_selection.skill.md`
- `canva_design_instantiation.skill.md`
- `canva_autofill_binding.skill.md`
- `brand_kit_enforcement.skill.md`
- `legal_disclaimer_insertion.skill.md`
- `banned_claims_guard.skill.md`
- `design_variant_generation.skill.md`
- `design_preflight_qc.skill.md`
- `design_handoff_packet.skill.md`

### `MKT_UX_DESIGN_AGENT`

Role: transform approved content into wireframes, interaction specs, and implementation handoff.

Minimum skill bundle:
- `frontend_design.skill.md`
- `information_architecture.skill.md`
- `user_flow_design.skill.md`
- `wireframe_production.skill.md`
- `ui_pattern_selection.skill.md`
- `visual_hierarchy_optimization.skill.md`
- `responsive_design_specification.skill.md`
- `interaction_and_state_specification.skill.md`
- `forms_and_conversion_ux.skill.md`
- `accessibility_audit_and_remediation.skill.md`
- `design_to_implementation_handoff.skill.md`

### `MKT_THRIVE_THEMES_AGENT`

Role: translate approved UX/page specifications into exact Thrive Architect build packets.

Minimum skill bundle:
- `frontend_design.skill.md`
- `thrive_element_mapping.skill.md`
- `thrive_build_packet.skill.md`
- `thrive_symbol_design.skill.md`
- `thrive_css_override.skill.md`
- `thrive_responsive_config.skill.md`
- `thrive_template_config.skill.md`
- `wordpress_page_setup.skill.md`
- `thrive_audit.skill.md`
- `design_to_implementation_handoff.skill.md`
- `platform_aware_design_constraints.skill.md`

### `MKT_WEBSITE_IMPLEMENTATION_AGENT`

Role: implement or package approved website and landing-page changes for execution.

Minimum skill bundle:
- `frontend_design.skill.md`
- `landing_page_copywriting.skill.md`
- `conversion_path_design.skill.md`
- `landing_flow_optimization.skill.md`
- `on_page_optimization.skill.md`
- `brand_kit_enforcement.skill.md`
- `integration_workflow_execution.skill.md`
- `asset_format_transformation.skill.md`
- `wordpress_page_setup.skill.md`
- `accessibility_audit_and_remediation.skill.md`
- `design_to_implementation_handoff.skill.md`

### `MKT_MUGGAH_SECURITIES_AGENT`

Role: securities-adjacent issue spotting, claim-boundary control, and client-risk
rating for Funnel 3 token, stablecoin, marketplace, and exempt-distribution
fact patterns.

Minimum skill bundle:
- `securities_law_knowledge.skill.md`
- `securities_law_analysis.skill.md`
- `securities_law_document_review.skill.md`
- `doctrine_alignment_check.skill.md`
- `market_position_mapping.skill.md`
- `offer_tightening_and_polishing.skill.md`
- `campaign_brief_tightening_and_polishing.skill.md`
- `audience_segmentation.skill.md`
- `differentiation_detection.skill.md`
- `competitor_message_analysis.skill.md`

### `MKT_MUGGAH_MONEY_SERVICES_AGENT`

Role: money-services issue spotting, claim-boundary control, and client-risk
rating for Funnel 3 MSB, virtual-currency, remittance, foreign-exchange, and
AML/reporting fact patterns.

Minimum skill bundle:
- `money_services_law_knowledge.skill.md`
- `money_services_law_analysis.skill.md`
- `money_services_law_document_review.skill.md`
- `doctrine_alignment_check.skill.md`
- `market_position_mapping.skill.md`
- `offer_tightening_and_polishing.skill.md`
- `campaign_brief_tightening_and_polishing.skill.md`
- `audience_segmentation.skill.md`
- `differentiation_detection.skill.md`
- `competitor_message_analysis.skill.md`

### `MKT_MUGGAH_PAYMENT_SERVICES_AGENT`

Role: payment-services issue spotting, claim-boundary control, and client-risk
rating for Funnel 3 PSP, RPAA, safeguarding, and payment-function fact patterns.

Minimum skill bundle:
- `payment_services_law_knowledge.skill.md`
- `payment_services_law_analysis.skill.md`
- `payment_services_law_document_review.skill.md`
- `doctrine_alignment_check.skill.md`
- `market_position_mapping.skill.md`
- `offer_tightening_and_polishing.skill.md`
- `campaign_brief_tightening_and_polishing.skill.md`
- `audience_segmentation.skill.md`
- `differentiation_detection.skill.md`
- `competitor_message_analysis.skill.md`

## Operating Sequence

1. `MKT_CHIEF_MARKETING_OFFICER_AGENT` sequences the run.
2. Strategy, SEO, provocation, and content generation produce draft upstream assets.
3. `MKT_DESIGN_PRODUCTION_AGENT` and `MKT_UX_DESIGN_AGENT` convert approved direction into design and page structure.
4. `MKT_THRIVE_THEMES_AGENT` and `MKT_WEBSITE_IMPLEMENTATION_AGENT` turn approved specs into executable implementation packets.
5. `SE-01` performs the mandatory coherence gate.
6. ML1 approves, executes, or publishes where required.
7. `SEO-01` and `CA-01` interpret downstream performance and conversion signals.

## Source References

- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/AGENT_ROSTER.md`
- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/06_AGENTS/STRATEGIC_EDITOR/AGENT_SPEC-STRATEGIC_EDITOR_V2.md`
- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/06_AGENTS/SEO_METRICS_MASTER/AGENT_SPEC-SEO_METRICS_MASTER_V2.md`
- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/06_AGENTS/SELECTIVE_PROVOCATION_ENGINE/AGENT_SPEC-SELECTIVE_PROVOCATION_ENGINE_V2.md`
- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/06_AGENTS/BLOG_SEO_ENGINE/AGENT_SPEC-BLOG_SEO_ENGINE_V2.md`
- `04_INITIATIVES/LL_PORTFOLIO/08_MARKETING/06_AGENTS/CONVERSION_ARCHITECT/AGENT_SPEC-CONVERSION_ARCHITECT_AGENT_V1.md`
- `00_SYSTEM/AGENTS/specs/marketing/README.md`
- `00_SYSTEM/AGENTS/specs/marketing/MARKETING_AGENT_SKILL_MAP.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_CHIEF_MARKETING_OFFICER_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_DESIGN_PRODUCTION_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_UX_DESIGN_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_THRIVE_THEMES_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_WEBSITE_IMPLEMENTATION_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_MUGGAH_SECURITIES_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_MUGGAH_MONEY_SERVICES_AGENT.md`
- `00_SYSTEM/AGENTS/specs/marketing/MKT_MUGGAH_PAYMENT_SERVICES_AGENT.md`
