# IMPLEMENTATION WORKPLAN

Project ID: MHS-2D-MICRO-SAAS-001
Project Path: 04_INITIATIVES/HillSide_PORTFOLIO/MATTHEW_HOLDINGS_17513721_CANADA_INC/2D_MICRO_SAAS_BUILD_AND_SALE
Stage: Implementation

## Objective
Deliver one Micro SaaS product through build, launch, and stabilization under approved scope and budget constraints.

## Decision Use
Use this file as the canonical implementation execution plan, including scope control, sequence, and evidence requirements.

## Stage Entry Rule
Implementation starts only when ML1 records Planning -> Implementation approval in `../APPROVAL_RECORD.md`.
Concept, ICP, and workflow scope must already be frozen in planning artifacts.

## Implementation Method (9-Step Sequence)

| Step | Implementation Action | Owner | Completion Evidence |
| --- | --- | --- | --- |
| IM-01 Project Structure Setup | Create and validate `frontend/` and `backend/` structure, with environment/bootstrap docs. | Project Owner | Repository structure and setup notes |
| IM-02 Frontend Foundation | Bootstrap frontend with Vite + React + TypeScript + Tailwind; implement baseline UI shells (login, dashboard, profile, settings). | Matthew | Running frontend and route shell screenshots |
| IM-03 Routing | Implement route model (`/login`, `/dashboard`, `/profile`, `/settings`) and route guards for auth states. | Matthew | Route map and guard test notes |
| IM-04 Authentication | Implement auth flow (default stack: Supabase) with enforced redirect logic for authenticated/unauthenticated users. | Project Owner | Auth acceptance test results |
| IM-05 Data Model + RLS | Create initial table (`id`, `user_id`, `main_data_field`, `created_at`) and RLS policies for per-user read/write isolation. | Project Owner | DB schema export and RLS policy evidence |
| IM-06 Core Feature Loop | Implement server-side OpenAI processing loop: input -> backend processing -> DB storage -> frontend display. | Project Owner | API test logs and persisted sample records |
| IM-07 Debug and Hardening | Resolve setup/runtime defects (env, dependency, API, RLS, syntax) and close critical blockers. | Project Owner | Defect log and closure evidence |
| IM-08 Setup Billing | Implement Stripe subscription model and backend enforcement of active-subscription access control. | Project Owner | Billing flow test results and entitlement checks |
| IM-09 Post-Launch Quality Pass | Improve UX clarity, error handling, loading states, and design consistency without expanding scope. | Project Owner | Change log and QA sign-off |

## Workstreams

| Workstream | Scope | Owner | Evidence |
| --- | --- | --- | --- |
| IW-01 Build Foundation | IM-01 through IM-03 | Matthew | Frontend/backend baseline operational |
| IW-02 Platform and Data Controls | IM-04 through IM-05 | Project Owner | Auth and RLS controls validated |
| IW-03 Core Value Delivery | IM-06 through IM-07 | Project Owner | Feature loop working and blockers cleared |
| IW-04 Commercialization Controls | IM-08 | Project Owner | Subscription gating active |
| IW-05 Launch Stabilization | IM-09 + first 30 days operations | Project Owner | KPI and issue stability packet |

## Milestones

| Milestone | Target | Status | Evidence |
| --- | --- | --- | --- |
| I1 - Build foundation complete | 2026-04-05 | pending | IM-01..IM-03 closed |
| I2 - Auth and data controls complete | 2026-04-08 | pending | IM-04..IM-05 closed |
| I3 - Core feature and billing complete | 2026-04-10 | pending | IM-06..IM-08 closed |
| I4 - MVP launch and 14-day stabilization checkpoint | 2026-04-24 | pending | Launch evidence + blocker report |
| I5 - 30-day validation checkpoint | 2026-05-10 | pending | OKR snapshot and review packet |

## Controls
- Scope control: no feature expansion outside approved scope without ML1 approval.
- Budget control: maintain variance within approved threshold from `planning/ML1_METRIC_APPROVAL.md`.
- Schedule control: escalate any milestone slip over 5 days.
- Security control: API keys remain backend only and must never be exposed in frontend code.
- Data control: all user data access must be enforced by RLS and validated with test cases.

## Exit Rule
Implementation stage is complete when product launch is live, stabilization thresholds are met, and evidence for OKR checkpoints is recorded.
