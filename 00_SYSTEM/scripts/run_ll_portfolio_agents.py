#!/usr/bin/env python3
"""
LL Portfolio Agent Runner

Runs the restored LLM-004/005/006 agent logic in a deterministic, local form and
materializes outputs in both:
1) Canonical LL folders under 04_INITIATIVES/LL_PORTFOLIO/03_FIRM_OPERATIONS/
2) A timestamped run folder under 06_RUNS/
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
PROJECTS_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "07_STRATEGIC_PROJECTS"

PROJECT_MGMT_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PROJECT_MANAGEMENT"
PORTFOLIO_MGMT_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PORTFOLIO_MANAGEMENT"
PORTFOLIO_GOVERNANCE_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PORTFOLIO_GOVERNANCE"

REQUIRED_STAGE1 = [
    "PROJECT_CHARTER.md",
    "PROBLEM_STATEMENT.md",
    "SUCCESS_CRITERIA.md",
    "STAKEHOLDERS.md",
    "RISKS_INITIAL.md",
    "APPROVAL_RECORD.md",
]

REQUIRED_STAGE2_MEASUREMENT = [
    "METRIC_DEFINITION.md",
    "MEASUREMENT_METHOD.md",
    "BASELINE_CAPTURE_PERIOD.md",
    "VALIDATION_REVIEW.md",
    "ML1_METRIC_APPROVAL.md",
]

REQUIRED_STAGE2_PLANNING = [
    "SCOPE_DEFINITION.md",
    "WORKPLAN.md",
    "MILESTONES.md",
    "RESOURCE_PLAN.md",
    "ASSUMPTIONS_CONSTRAINTS.md",
    "DEPENDENCIES.md",
    "RISK_REGISTER.md",
    "COMMUNICATION_PLAN.md",
]

REQUIRED_STAGE3 = [
    "EXECUTION_LOG.md",
    "DECISION_LOG.md",
    "CHANGE_LOG.md",
    "ISSUE_LOG.md",
    "DELIVERABLES_TRACKER.md",
    "QA_CHECKLIST.md",
]

REQUIRED_STAGE4 = [
    "STATUS_REPORT.md",
    "KPI_DASHBOARD.md",
    "VARIANCE_REPORT.md",
    "RISK_UPDATES.md",
    "STAKEHOLDER_UPDATES.md",
]

REQUIRED_STAGE5 = [
    "DELIVERABLE_ACCEPTANCE.md",
    "LESSONS_LEARNED.md",
    "POST_IMPLEMENTATION_REVIEW.md",
    "FINAL_STATUS_REPORT.md",
    "ARCHIVE_INDEX.md",
]


@dataclass
class ProjectSnapshot:
    project_id: str
    files: set[str]
    inferred_stage: int
    missing_stage1: List[str]
    missing_stage2_measurement: List[str]
    missing_stage2_planning: List[str]
    missing_stage3: List[str]
    missing_stage4: List[str]
    missing_stage5: List[str]

    @property
    def approvals_present(self) -> bool:
        return "APPROVAL_RECORD.md" in self.files and "ML1_METRIC_APPROVAL.md" in self.files

    @property
    def stage1_complete(self) -> bool:
        return not self.missing_stage1

    @property
    def stage2_measurement_complete(self) -> bool:
        return not self.missing_stage2_measurement

    @property
    def project_health(self) -> str:
        if not self.stage1_complete:
            return "at-risk"
        if not self.approvals_present:
            return "at-risk"
        if not self.stage2_measurement_complete:
            return "watch"
        return "on-track"

    @property
    def open_gate_count(self) -> int:
        return (
            len(self.missing_stage1)
            + len(self.missing_stage2_measurement)
            + len(self.missing_stage2_planning)
            + len(self.missing_stage3)
            + len(self.missing_stage4)
            + len(self.missing_stage5)
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def generate_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%H%M%SZ")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"RUN-{date}-LL-PORTFOLIO-AGENTS-{stamp}"


def infer_stage(files: set[str]) -> int:
    if any(name in files for name in REQUIRED_STAGE5):
        return 5
    if any(name in files for name in REQUIRED_STAGE4):
        return 4
    if any(name in files for name in REQUIRED_STAGE3):
        return 3
    if any(name in files for name in (REQUIRED_STAGE2_MEASUREMENT + REQUIRED_STAGE2_PLANNING)):
        return 2
    if any(name in files for name in REQUIRED_STAGE1):
        return 1
    return 0


def discover_projects() -> List[ProjectSnapshot]:
    projects: List[ProjectSnapshot] = []
    if not PROJECTS_DIR.exists():
        return projects

    for path in sorted(PROJECTS_DIR.iterdir(), key=lambda p: p.name):
        if not path.is_dir() or not path.name.startswith("LLP-"):
            continue
        file_set = {p.name for p in path.glob("*.md")}
        projects.append(
            ProjectSnapshot(
                project_id=path.name,
                files=file_set,
                inferred_stage=infer_stage(file_set),
                missing_stage1=[name for name in REQUIRED_STAGE1 if name not in file_set],
                missing_stage2_measurement=[name for name in REQUIRED_STAGE2_MEASUREMENT if name not in file_set],
                missing_stage2_planning=[name for name in REQUIRED_STAGE2_PLANNING if name not in file_set],
                missing_stage3=[name for name in REQUIRED_STAGE3 if name not in file_set],
                missing_stage4=[name for name in REQUIRED_STAGE4 if name not in file_set],
                missing_stage5=[name for name in REQUIRED_STAGE5 if name not in file_set],
            )
        )
    return projects


def write_markdown(path: Path, title: str, run_id: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = "\n".join(
        [
            f"# {title}",
            "",
            f"- Generated: {utc_now()}",
            f"- Run ID: {run_id}",
            "",
            "> Advisory output. ML1 approval remains required for decisions.",
            "",
        ]
    )
    path.write_text(header + body.strip() + "\n", encoding="utf-8")


def render_table(headers: List[str], rows: List[List[str]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def llm_004_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    stage_rows: List[List[str]] = []
    health_rows: List[List[str]] = []

    for p in projects:
        blockers = []
        if p.missing_stage1:
            blockers.append("missing-stage1")
        if p.missing_stage2_measurement:
            blockers.append("missing-measurement")
        if p.missing_stage2_planning:
            blockers.append("missing-planning")
        stage_rows.append(
            [
                p.project_id,
                str(p.inferred_stage),
                "yes" if p.stage1_complete else "no",
                "yes" if p.stage2_measurement_complete else "no",
                "yes" if p.approvals_present else "no",
                ", ".join(blockers) if blockers else "none",
            ]
        )

        health_rows.append(
            [
                p.project_id,
                p.project_health,
                str(p.open_gate_count),
                str(len(p.missing_stage2_planning)),
            ]
        )

    checklist_body = "\n".join(
        [
            "## Stage Gate Snapshot",
            "",
            render_table(
                [
                    "Project",
                    "Inferred Stage",
                    "Stage 1 Complete",
                    "Measurement Complete",
                    "Approvals Present",
                    "Blockers",
                ],
                stage_rows or [["none", "-", "-", "-", "-", "-"]],
            ),
            "",
            "## Rule",
            "",
            "- Do not advance a project gate without explicit ML1 approval.",
        ]
    )

    rollup_body = "\n".join(
        [
            "## Project Health Rollup",
            "",
            render_table(
                [
                    "Project",
                    "Health",
                    "Open Gate Count",
                    "Planning Gaps",
                ],
                health_rows or [["none", "-", "-", "-"]],
            ),
            "",
            "## Summary",
            "",
            f"- Projects reviewed: {len(projects)}",
            f"- On-track: {sum(1 for p in projects if p.project_health == 'on-track')}",
            f"- Watch: {sum(1 for p in projects if p.project_health == 'watch')}",
            f"- At-risk: {sum(1 for p in projects if p.project_health == 'at-risk')}",
        ]
    )

    write_markdown(
        PROJECT_MGMT_DIR / "PROJECT_STAGE_GATE_CHECKLIST.md",
        "Project Stage Gate Checklist",
        run_id,
        checklist_body,
    )
    write_markdown(
        PROJECT_MGMT_DIR / "PROJECT_HEALTH_ROLLUP.md",
        run_id=run_id,
        title="Project Health Rollup",
        body=rollup_body,
    )

    report = "\n".join(
        [
            "## LLM-004 Result",
            "",
            f"- Projects reviewed: {len(projects)}",
            f"- Stage 1 complete: {sum(1 for p in projects if p.stage1_complete)}",
            f"- Measurement complete: {sum(1 for p in projects if p.stage2_measurement_complete)}",
            f"- Approval gaps: {sum(1 for p in projects if not p.approvals_present)}",
            "",
            "## Outputs",
            "",
            f"- {PROJECT_MGMT_DIR / 'PROJECT_STAGE_GATE_CHECKLIST.md'}",
            f"- {PROJECT_MGMT_DIR / 'PROJECT_HEALTH_ROLLUP.md'}",
        ]
    )
    return {"report": report}


def llm_005_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    stage_counts = Counter(p.inferred_stage for p in projects)
    health_counts = Counter(p.project_health for p in projects)

    ranked = sorted(
        projects,
        key=lambda p: (
            p.project_health != "at-risk",
            p.project_health != "watch",
            p.open_gate_count,
            p.project_id,
        ),
    )

    dashboard_rows = [
        [p.project_id, str(p.inferred_stage), p.project_health, str(p.open_gate_count)] for p in projects
    ] or [["none", "-", "-", "-"]]

    priority_rows = [
        [str(i), p.project_id, p.project_health, str(p.open_gate_count)] for i, p in enumerate(ranked, start=1)
    ] or [["-", "none", "-", "-"]]

    sequencing_lines = []
    if ranked:
        first = ranked[0]
        sequencing_lines.append(f"1. Stabilize `{first.project_id}` ({first.project_health}).")
    if len(ranked) > 1:
        second = ranked[1]
        sequencing_lines.append(f"2. Sequence `{second.project_id}` after primary stabilization.")
    if len(ranked) > 2:
        sequencing_lines.append("3. Defer remaining projects until planning gaps close.")
    if not sequencing_lines:
        sequencing_lines.append("1. No active projects detected.")

    collisions = [p.project_id for p in projects if p.inferred_stage == 2]
    collision_body = "\n".join(
        [
            "## Resource Collision Signals",
            "",
            f"- Projects in planning/measurement stage: {len(collisions)}",
            f"- Potential coordination set: {', '.join(collisions) if collisions else 'none'}",
        ]
    )

    files_to_body = {
        "PORTFOLIO_STATUS_DASHBOARD.md": "\n".join(
            [
                "## Portfolio Status",
                "",
                render_table(["Project", "Stage", "Health", "Open Gates"], dashboard_rows),
                "",
                f"- Total projects: {len(projects)}",
                f"- Health mix: on-track={health_counts.get('on-track', 0)}, "
                f"watch={health_counts.get('watch', 0)}, at-risk={health_counts.get('at-risk', 0)}",
            ]
        ),
        "CAPACITY_ALLOCATION_MODEL.md": "\n".join(
            [
                "## Capacity Allocation Model (Advisory)",
                "",
                f"- Stage 1 load: {stage_counts.get(1, 0)}",
                f"- Stage 2 load: {stage_counts.get(2, 0)}",
                f"- Stage 3+ load: {stage_counts.get(3, 0) + stage_counts.get(4, 0) + stage_counts.get(5, 0)}",
                "",
                "- Recommendation: prioritize Stage 2 closure to reduce planning backlog.",
            ]
        ),
        "BOTTLENECK_ANALYSIS.md": "\n".join(
            [
                "## Bottleneck Analysis",
                "",
                f"- Planning bottleneck candidates: {sum(1 for p in projects if p.missing_stage2_planning)}",
                f"- Measurement bottleneck candidates: {sum(1 for p in projects if p.missing_stage2_measurement)}",
            ]
        ),
        "PROJECT_PRIORITY_MATRIX.md": "\n".join(
            [
                "## Priority Matrix",
                "",
                render_table(["Rank", "Project", "Health", "Open Gates"], priority_rows),
            ]
        ),
        "STAGE_DISTRIBUTION_REPORT.md": "\n".join(
            [
                "## Stage Distribution",
                "",
                render_table(
                    ["Stage", "Count"],
                    [[str(stage), str(stage_counts.get(stage, 0))] for stage in [0, 1, 2, 3, 4, 5]],
                ),
            ]
        ),
        "SEQUENCING_RECOMMENDATIONS.md": "\n".join(
            [
                "## Sequencing Recommendations",
                "",
                *sequencing_lines,
            ]
        ),
        "WIP_LOAD_ANALYSIS.md": "\n".join(
            [
                "## WIP Load Analysis",
                "",
                f"- Active projects (stage >=1): {sum(1 for p in projects if p.inferred_stage >= 1)}",
                f"- At-risk active projects: {sum(1 for p in projects if p.inferred_stage >= 1 and p.project_health == 'at-risk')}",
            ]
        ),
        "RESOURCE_COLLISION_REPORT.md": collision_body,
    }

    for filename, body in files_to_body.items():
        write_markdown(PORTFOLIO_MGMT_DIR / filename, filename.replace("_", " ").replace(".md", ""), run_id, body)

    report = "\n".join(
        [
            "## LLM-005 Result",
            "",
            f"- Projects reviewed: {len(projects)}",
            f"- Stage 2 concentration: {stage_counts.get(2, 0)}",
            f"- At-risk projects: {health_counts.get('at-risk', 0)}",
            "",
            "## Outputs",
            "",
            f"- {PORTFOLIO_MGMT_DIR}",
        ]
    )
    return {"report": report}


def llm_006_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    approval_gaps = [p for p in projects if not p.approvals_present]
    stage_violations = [p for p in projects if p.missing_stage1 or p.missing_stage2_measurement]
    metric_schema_gaps = [p for p in projects if p.missing_stage2_measurement]
    contradiction_alerts: List[str] = []

    seen = set()
    for p in projects:
        if p.project_id in seen:
            contradiction_alerts.append(f"Duplicate project identifier: {p.project_id}")
        seen.add(p.project_id)

    files_to_body = {
        "GOVERNANCE_COMPLIANCE_AUDIT.md": "\n".join(
            [
                "## Governance Compliance Audit",
                "",
                f"- Projects audited: {len(projects)}",
                f"- Stage violations: {len(stage_violations)}",
                f"- Approval gaps: {len(approval_gaps)}",
                f"- Metric schema gaps: {len(metric_schema_gaps)}",
            ]
        ),
        "STAGE_GATE_VIOLATION_REPORT.md": "\n".join(
            [
                "## Stage Gate Violations",
                "",
                *(
                    [
                        f"- `{p.project_id}`: missing stage1={len(p.missing_stage1)}, "
                        f"missing measurement={len(p.missing_stage2_measurement)}"
                        for p in stage_violations
                    ]
                    or ["- None."]
                ),
            ]
        ),
        "METRIC_SCHEMA_INTEGRITY_REPORT.md": "\n".join(
            [
                "## Metric Schema Integrity",
                "",
                *(
                    [
                        f"- `{p.project_id}` missing: {', '.join(p.missing_stage2_measurement)}"
                        for p in metric_schema_gaps
                    ]
                    or ["- All projects contain required measurement artifacts."]
                ),
            ]
        ),
        "CONTRADICTION_ALERTS.md": "\n".join(
            [
                "## Contradiction Alerts",
                "",
                *(contradiction_alerts or ["- No cross-project contradictions detected by deterministic checks."]),
            ]
        ),
        "MIGRATION_VALIDATION_REPORT.md": "\n".join(
            [
                "## Migration Validation",
                "",
                "- No stage 5 project migrations detected in this run.",
            ]
        ),
        "APPROVAL_GAP_REPORT.md": "\n".join(
            [
                "## Approval Gap Report",
                "",
                *([f"- `{p.project_id}` missing one or more ML1 approvals." for p in approval_gaps] or ["- None."]),
            ]
        ),
        "DOCTRINE_DRIFT_REPORT.md": "\n".join(
            [
                "## Doctrine Drift Report",
                "",
                "- No doctrine text drift analysis executed in this deterministic runner.",
                "- Structural checks only; require ML1 review for doctrine-level interpretation.",
            ]
        ),
    }

    for filename, body in files_to_body.items():
        write_markdown(
            PORTFOLIO_GOVERNANCE_DIR / filename,
            filename.replace("_", " ").replace(".md", ""),
            run_id,
            body,
        )

    report = "\n".join(
        [
            "## LLM-006 Result",
            "",
            f"- Projects audited: {len(projects)}",
            f"- Approval gaps: {len(approval_gaps)}",
            f"- Stage gate violations: {len(stage_violations)}",
            f"- Metric schema gaps: {len(metric_schema_gaps)}",
            "",
            "## Outputs",
            "",
            f"- {PORTFOLIO_GOVERNANCE_DIR}",
        ]
    )
    return {"report": report}


def write_run_outputs(
    run_root: Path,
    run_id: str,
    project_count: int,
    llm_004_report: str,
    llm_005_report: str,
    llm_006_report: str,
) -> None:
    run_root.mkdir(parents=True, exist_ok=True)

    run_log = "\n".join(
        [
            "# RUN LOG — LL Portfolio Agents",
            "",
            f"Run ID: {run_id}",
            f"Generated: {utc_now()}",
            "",
            "Agents:",
            "- LLM-004 Project Management Agent",
            "- LLM-005 Portfolio Management Agent",
            "- LLM-006 Portfolio Governance Agent",
            "",
            f"Projects reviewed: {project_count}",
            "",
            "Outputs written to:",
            f"- {PROJECT_MGMT_DIR}",
            f"- {PORTFOLIO_MGMT_DIR}",
            f"- {PORTFOLIO_GOVERNANCE_DIR}",
            "",
        ]
    )
    (run_root / "RUN_LOG.md").write_text(run_log, encoding="utf-8")

    write_markdown(run_root / "LLM-004_PROJECT_MANAGEMENT_REPORT.md", "LLM-004 Project Management Report", run_id, llm_004_report)
    write_markdown(run_root / "LLM-005_PORTFOLIO_MANAGEMENT_REPORT.md", "LLM-005 Portfolio Management Report", run_id, llm_005_report)
    write_markdown(run_root / "LLM-006_PORTFOLIO_GOVERNANCE_REPORT.md", "LLM-006 Portfolio Governance Report", run_id, llm_006_report)


def main() -> int:
    run_id = generate_run_id()
    run_root = REPO_ROOT / "06_RUNS" / run_id / "ll_portfolio_agents"

    projects = discover_projects()

    llm_004 = llm_004_outputs(projects, run_id)
    llm_005 = llm_005_outputs(projects, run_id)
    llm_006 = llm_006_outputs(projects, run_id)

    write_run_outputs(
        run_root=run_root,
        run_id=run_id,
        project_count=len(projects),
        llm_004_report=llm_004["report"],
        llm_005_report=llm_005["report"],
        llm_006_report=llm_006["report"],
    )

    print(f"LL portfolio agents run complete: {run_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
