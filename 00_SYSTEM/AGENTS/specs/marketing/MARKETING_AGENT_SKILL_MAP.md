---
id: 00_system__agents__specs__marketing__agent_skill_map_md
title: Marketing Agent Skill Map
owner: ML1
status: draft
created_date: 2026-03-08
last_updated: 2026-03-21
tags: [marketing, agents, skills, mapping]
---

# Marketing Agent Skill Map

Canonical mapping of marketing agents to their declared skill files.
Skill files are stored under `00_SYSTEM/AGENTS/specs/marketing/skills/`.

## Implementation Status (2026-03-21)
- Implemented meta-skill files for `MKT_CHIEF_MARKETING_OFFICER_AGENT`.
- Implemented skill files: all original eight core agents.
- Implemented skill files: all optional specialist agent skills.
- Added 2026-03-21: `MKT_UX_DESIGN_AGENT` and `MKT_THRIVE_THEMES_AGENT` activated
  as core agents with full skill files.
- Runtime activation approved by ML1 on `2026-03-21` for full suite including
  `MKT_UX_DESIGN_AGENT` and `MKT_THRIVE_THEMES_AGENT`.

## MKT_CHIEF_MARKETING_OFFICER_AGENT
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
- `keyword_mapping.skill.md`
- `cta_design.skill.md`
- `conversion_path_design.skill.md`
- `landing_flow_optimization.skill.md`
- `market_feedback_analysis.skill.md`

Meta-execution chain:
1. Objective
2. `task_decomposition.skill.md`
3. `skill_selection.skill.md`
4. `context_assembly.skill.md`
5. `operational_skill`
6. `execution_validation.skill.md`
7. `artifact_promotion.skill.md`

## MKT_MARKETING_STRATEGY_AGENT
- `campaign_design.skill.md`
- `funnel_architecture.skill.md`
- `audience_segmentation.skill.md`
- `channel_strategy.skill.md`
- `campaign_brief_generation.skill.md`
- `offer_engineering.skill.md`
- `demand_capture.skill.md`

## MKT_CONTENT_PRODUCTION_AGENT
- `long_form_content_generation.skill.md`
- `short_form_content_generation.skill.md`
- `landing_page_copywriting.skill.md`
- `email_marketing_copy.skill.md`
- `content_adaptation.skill.md`

## MKT_DESIGN_PRODUCTION_AGENT
- `design_brief_translation.skill.md`
- `template_slot_selection.skill.md`
- `canva_design_instantiation.skill.md`
- `canva_autofill_binding.skill.md`
- `brand_kit_enforcement.skill.md`
- `legal_disclaimer_insertion.skill.md`
- `banned_claims_guard.skill.md`
- `design_variant_generation.skill.md`
- `design_preflight_qc.skill.md`
- `design_metadata_registration.skill.md`
- `design_handoff_packet.skill.md`

## MKT_EDITORIAL_QA_AGENT
- `brand_voice_validation.skill.md`
- `doctrine_alignment_check.skill.md`
- `factual_claim_validation.skill.md`
- `marketing_policy_compliance.skill.md`
- `editorial_quality_review.skill.md`

## MKT_WEBSITE_IMPLEMENTATION_AGENT
- `landing_page_copywriting.skill.md`
- `conversion_path_design.skill.md`
- `landing_flow_optimization.skill.md`
- `on_page_optimization.skill.md`
- `brand_kit_enforcement.skill.md`
- `integration_workflow_execution.skill.md`
- `asset_format_transformation.skill.md`

## MKT_DISTRIBUTION_ORCHESTRATION_AGENT
- `channel_asset_packaging.skill.md`
- `distribution_schedule_design.skill.md`
- `integration_workflow_execution.skill.md`
- `asset_format_transformation.skill.md`

## MKT_MARKET_SIGNAL_AGENT
- `engagement_data_collection.skill.md`
- `market_feedback_analysis.skill.md`
- `positioning_drift_detection.skill.md`
- `performance_signal_reporting.skill.md`
- `revenue_attribution.skill.md`

## MKT_REPOSITORY_ASSET_GOVERNANCE_AGENT
- `artifact_classification.skill.md`
- `asset_version_management.skill.md`
- `artifact_state_management.skill.md`
- `marketing_repository_indexing.skill.md`

## MKT_UX_DESIGN_AGENT
- `information_architecture.skill.md`
- `user_flow_design.skill.md`
- `wireframe_production.skill.md`
- `ui_pattern_selection.skill.md`
- `visual_hierarchy_optimization.skill.md`
- `responsive_design_specification.skill.md`
- `interaction_and_state_specification.skill.md`
- `forms_and_conversion_ux.skill.md`
- `accessibility_audit_and_remediation.skill.md`
- `platform_aware_design_constraints.skill.md`
- `design_system_translation.skill.md`
- `design_to_implementation_handoff.skill.md`
- `ux_audit.skill.md`
- `component_design.skill.md`

## MKT_THRIVE_THEMES_AGENT
- `thrive_element_mapping.skill.md`
- `thrive_build_packet.skill.md`
- `thrive_symbol_design.skill.md`
- `thrive_css_override.skill.md`
- `thrive_responsive_config.skill.md`
- `thrive_template_config.skill.md`
- `wordpress_page_setup.skill.md`
- `thrive_audit.skill.md`

## Optional Specialists

### MKT_SEO_DISCOVERABILITY_AGENT
- `keyword_mapping.skill.md`
- `search_intent_clustering.skill.md`
- `seo_gap_analysis.skill.md`
- `on_page_optimization.skill.md`

### MKT_SOCIAL_NARRATIVE_AGENT
- `social_thread_design.skill.md`
- `platform_voice_calibration.skill.md`
- `short_form_narrative_structuring.skill.md`

### MKT_OFFER_FUNNEL_AGENT
- `cta_design.skill.md`
- `conversion_path_design.skill.md`
- `lead_magnet_structuring.skill.md`
- `landing_flow_optimization.skill.md`
- `offer_engineering.skill.md`
- `demand_capture.skill.md`

### MKT_COMPETITIVE_POSITIONING_AGENT
- `competitor_message_analysis.skill.md`
- `market_position_mapping.skill.md`
- `differentiation_detection.skill.md`
