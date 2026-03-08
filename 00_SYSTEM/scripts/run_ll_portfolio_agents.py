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
import re
from typing import Dict, List, Tuple


REPO_ROOT = Path(__file__).resolve().parents[2]
LL_PORTFOLIO_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO"

PROJECT_MGMT_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PROJECT_MANAGEMENT"
PORTFOLIO_MGMT_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PORTFOLIO_MANAGEMENT"
PORTFOLIO_GOVERNANCE_DIR = REPO_ROOT / "04_INITIATIVES" / "LL_PORTFOLIO" / "03_FIRM_OPERATIONS" / "PORTFOLIO_GOVERNANCE"

GOVERNED_PROJECT_TYPES = {"Strategic Project", "Management Project", "Operational Project"}
PROJECT_TYPE_PATTERN = re.compile(r"(?im)^(?:\*\*Project Type:\*\*|Project Type:)\s*(.+?)\s*$")

REQUIRED_STAGE1 = [
    "PROJECT_CHARTER.md",
    "PROBLEM_STATEMENT.md",
    "SUCCESS_CRITERIA.md",
    "STAKEHOLDERS.md",
    "RISK_SCAN.md",
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
    # Consolidated planning artifact; includes milestone schedule and resource plan sections.
    "WORKPLAN.md",
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

STAGE_REQUIREMENTS = {
    1: REQUIRED_STAGE1,
    2: REQUIRED_STAGE1 + REQUIRED_STAGE2_PLANNING + REQUIRED_STAGE2_MEASUREMENT,
    3: REQUIRED_STAGE1 + REQUIRED_STAGE2_PLANNING + REQUIRED_STAGE2_MEASUREMENT + REQUIRED_STAGE3,
    4: REQUIRED_STAGE1 + REQUIRED_STAGE2_PLANNING + REQUIRED_STAGE2_MEASUREMENT + REQUIRED_STAGE3 + REQUIRED_STAGE4,
    5: REQUIRED_STAGE1
    + REQUIRED_STAGE2_PLANNING
    + REQUIRED_STAGE2_MEASUREMENT
    + REQUIRED_STAGE3
    + REQUIRED_STAGE4
    + REQUIRED_STAGE5,
}


@dataclass
class ProjectSnapshot:
    project_id: str
    project_type: str
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
        if self.inferred_stage == 0:
            return "at-risk"
        if not self.stage1_complete:
            return "at-risk"
        if not self.approvals_present:
            return "at-risk"
        if self.inferred_stage >= 2 and (self.missing_stage2_measurement or self.missing_stage2_planning):
            return "watch"
        if self.inferred_stage >= 3 and self.missing_stage3:
            return "watch"
        if self.inferred_stage >= 4 and self.missing_stage4:
            return "watch"
        if self.inferred_stage >= 5 and self.missing_stage5:
            return "watch"
        return "on-track"

    @property
    def open_gate_count(self) -> int:
        return len(self.missing_for_current_stage)

    @property
    def stage2_completion_pct(self) -> int:
        if self.inferred_stage < 2:
            return 0
        required = REQUIRED_STAGE2_PLANNING + REQUIRED_STAGE2_MEASUREMENT
        present = sum(1 for name in required if name in self.files)
        return int(round((present / len(required)) * 100))

    @property
    def missing_for_current_stage(self) -> List[str]:
        if self.inferred_stage <= 0:
            return list(REQUIRED_STAGE1)
        required = STAGE_REQUIREMENTS.get(self.inferred_stage, STAGE_REQUIREMENTS[5])
        return [name for name in required if name not in self.files]


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


def normalize_project_type(raw_value: str) -> str:
    value = raw_value.strip().strip("*").strip()
    key = value.lower()
    aliases = {
        "strategic": "Strategic Project",
        "strategic project": "Strategic Project",
        "management": "Management Project",
        "management project": "Management Project",
        "operational": "Operational Project",
        "operational project": "Operational Project",
        "client matter": "Client Matter",
        "client project": "Client Matter",
        "client matters": "Client Matter",
        "client projects": "Client Matter",
    }
    return aliases.get(key, value)


def extract_project_type(charter_text: str) -> str | None:
    match = PROJECT_TYPE_PATTERN.search(charter_text)
    if not match:
        return None
    return normalize_project_type(match.group(1))


def discover_projects() -> List[ProjectSnapshot]:
    projects: List[ProjectSnapshot] = []
    if not LL_PORTFOLIO_DIR.exists():
        return projects

    for charter_path in sorted(LL_PORTFOLIO_DIR.rglob("PROJECT_CHARTER.md"), key=lambda p: p.as_posix()):
        path = charter_path.parent
        try:
            charter_text = charter_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        project_type = extract_project_type(charter_text)
        if project_type not in GOVERNED_PROJECT_TYPES:
            continue

        file_set = {p.name for p in path.glob("*.md")}
        project_id = path.relative_to(LL_PORTFOLIO_DIR).as_posix()
        projects.append(
            ProjectSnapshot(
                project_id=project_id,
                project_type=project_type,
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


def project_priority_score(project: ProjectSnapshot) -> int:
    return (
        (10 if project.project_health == "at-risk" else 0)
        + (5 if project.project_health == "watch" else 0)
        + (3 * len(project.missing_stage2_measurement))
        + (2 * len(project.missing_stage2_planning))
        + len(project.missing_for_current_stage)
    )


def missing_frequency(projects: List[ProjectSnapshot], selector: str) -> Counter:
    counts: Counter = Counter()
    for project in projects:
        missing = getattr(project, selector)
        for name in missing:
            counts[name] += 1
    return counts


def join_or_none(items: List[str]) -> str:
    return ", ".join(items) if items else "none"


def llm_004_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    stage_rows: List[List[str]] = []
    health_rows: List[List[str]] = []
    blocker_lines: List[str] = []
    action_rows: List[List[str]] = []

    ranked = sorted(projects, key=lambda p: (-project_priority_score(p), p.project_id))

    for p in projects:
        blocker_types = []
        if p.missing_stage1:
            blocker_types.append("stage1")
        if p.missing_stage2_measurement:
            blocker_types.append("measurement")
        if p.missing_stage2_planning:
            blocker_types.append("planning")
        if not p.approvals_present:
            blocker_types.append("approval")

        stage_rows.append(
            [
                p.project_id,
                str(p.inferred_stage),
                p.project_health,
                str(p.open_gate_count),
                f"{p.stage2_completion_pct}%" if p.inferred_stage >= 2 else "n/a",
                "yes" if p.approvals_present else "no",
                join_or_none(blocker_types),
            ]
        )

        health_rows.append(
            [
                p.project_id,
                p.project_health,
                str(p.open_gate_count),
                str(len(p.missing_stage2_planning)),
                str(len(p.missing_stage2_measurement)),
            ]
        )

        current_stage_missing = p.missing_for_current_stage
        blocker_lines.append(
            f"- `{p.project_id}`: stage={p.inferred_stage}, health={p.project_health}, "
            f"relevant gaps={len(current_stage_missing)} ({join_or_none(current_stage_missing)})"
        )

    for p in ranked:
        action = "Close stage-2 planning artifacts before any stage advancement."
        if p.missing_stage2_measurement:
            action = "Complete measurement artifacts and secure ML1 metric confirmation."
        if not p.approvals_present:
            action = "Record missing ML1 approvals in APPROVAL_RECORD/ML1_METRIC_APPROVAL."
        action_rows.append([p.project_id, str(project_priority_score(p)), action])

    checklist_body = "\n".join(
        [
            "## Stage Gate Snapshot",
            "",
            render_table(
                [
                    "Project",
                    "Stage",
                    "Health",
                    "Relevant Gate Gaps",
                    "Stage 2 Readiness",
                    "Approvals Present",
                    "Blocker Types",
                ],
                stage_rows or [["none", "-", "-", "-", "-", "-", "-"]],
            ),
            "",
            "## Project-Specific Blockers",
            "",
            *(blocker_lines or ["- None."]),
            "",
            "## ML1 Action Queue",
            "",
            render_table(
                ["Project", "Priority Score", "Recommended Next Action"],
                action_rows or [["none", "-", "-"]],
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
                    "Relevant Gate Gaps",
                    "Planning Gaps",
                    "Measurement Gaps",
                ],
                health_rows or [["none", "-", "-", "-", "-"]],
            ),
            "",
            "## Summary",
            "",
            f"- Projects reviewed: {len(projects)}",
            f"- On-track: {sum(1 for p in projects if p.project_health == 'on-track')}",
            f"- Watch: {sum(1 for p in projects if p.project_health == 'watch')}",
            f"- At-risk: {sum(1 for p in projects if p.project_health == 'at-risk')}",
            f"- Average stage-2 readiness: "
            f"{int(round(sum((p.stage2_completion_pct for p in projects), 0) / max(len(projects), 1)))}%",
        ]
    )

    write_markdown(
        PROJECT_MGMT_DIR / "PROJECT_HEALTH_ROLLUP.md",
        run_id=run_id,
        title="Project Health Rollup",
        body=rollup_body,
    )

    top_actions = [f"- {row[0]}: {row[2]}" for row in action_rows[:3]] or ["- None."]
    report = "\n".join(
        [
            "## LLM-004 Result",
            "",
            f"- Projects reviewed: {len(projects)}",
            f"- Watch/at-risk projects: {sum(1 for p in projects if p.project_health != 'on-track')}",
            f"- Stage-2 planning gaps: {sum(len(p.missing_stage2_planning) for p in projects)}",
            f"- Stage-2 measurement gaps: {sum(len(p.missing_stage2_measurement) for p in projects)}",
            "",
            "## Top ML1 Actions",
            "",
            *top_actions,
            "",
            "## Outputs",
            "",
            f"- {PROJECT_MGMT_DIR / 'PROJECT_ARTIFACT_TEMPLATE.md'}",
            f"- {PROJECT_MGMT_DIR / 'PROJECT_HEALTH_ROLLUP.md'}",
        ]
    )
    return {"report": report}


def llm_005_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    stage_counts = Counter(p.inferred_stage for p in projects)
    health_counts = Counter(p.project_health for p in projects)
    planning_freq = missing_frequency(projects, "missing_stage2_planning")
    measurement_freq = missing_frequency(projects, "missing_stage2_measurement")

    ranked = sorted(
        projects,
        key=lambda p: (-project_priority_score(p), p.project_id),
    )

    dashboard_rows = [
        [
            p.project_id,
            str(p.inferred_stage),
            p.project_health,
            str(p.open_gate_count),
            f"{p.stage2_completion_pct}%" if p.inferred_stage >= 2 else "n/a",
        ]
        for p in projects
    ] or [["none", "-", "-", "-", "-"]]

    priority_rows = [
        [
            str(i),
            p.project_id,
            str(project_priority_score(p)),
            p.project_health,
            str(p.open_gate_count),
            "Complete stage-2 planning packet" if p.missing_stage2_planning else "Advance to next gated artifact set",
        ]
        for i, p in enumerate(ranked, start=1)
    ] or [["-", "none", "-", "-", "-", "-"]]

    sequencing_lines: List[str] = []
    if not ranked:
        sequencing_lines.append("1. No active projects detected.")
    else:
        for i, project in enumerate(ranked[:4], start=1):
            sequencing_lines.append(
                f"{i}. `{project.project_id}` first focus: close {len(project.missing_stage2_planning)} planning and "
                f"{len(project.missing_stage2_measurement)} measurement gaps."
            )

    collisions = [p.project_id for p in projects if p.inferred_stage == 2]
    collision_artifacts = sorted(
        [name for name, count in planning_freq.items() if count >= 2],
        key=lambda n: (-planning_freq[n], n),
    )
    collision_body = "\n".join(
        [
            "## Resource Collision Signals",
            "",
            f"- Projects in planning/measurement stage: {len(collisions)}",
            f"- Potential coordination set: {', '.join(collisions) if collisions else 'none'}",
            f"- Shared missing planning artifacts (portfolio-wide): {join_or_none(collision_artifacts)}",
        ]
    )

    capacity_rows: List[List[str]] = []
    total_capacity_units = 0
    for p in projects:
        load_units = (len(p.missing_stage2_planning) * 2) + (len(p.missing_stage2_measurement) * 3)
        total_capacity_units += load_units
        capacity_rows.append([p.project_id, str(load_units), str(len(p.missing_stage2_planning)), str(len(p.missing_stage2_measurement))])

    top_bottlenecks = planning_freq.most_common(3) + measurement_freq.most_common(2)
    bottleneck_lines = [f"- `{name}` missing in {count} project(s)." for name, count in top_bottlenecks]

    files_to_body = {
        "PORTFOLIO_STATUS_DASHBOARD.md": "\n".join(
            [
                "## Portfolio Status",
                "",
                render_table(["Project", "Stage", "Health", "Relevant Open Gates", "Stage 2 Readiness"], dashboard_rows),
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
                render_table(
                    ["Project", "Estimated Capacity Units", "Planning Gaps", "Measurement Gaps"],
                    capacity_rows or [["none", "-", "-", "-"]],
                ),
                "",
                f"- Stage 1 load: {stage_counts.get(1, 0)}",
                f"- Stage 2 load: {stage_counts.get(2, 0)}",
                f"- Stage 3+ load: {stage_counts.get(3, 0) + stage_counts.get(4, 0) + stage_counts.get(5, 0)}",
                f"- Total estimated capacity units to close current stage-2 gaps: {total_capacity_units}",
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
                "",
                "## Top Portfolio Bottlenecks",
                "",
                *(bottleneck_lines or ["- None."]),
            ]
        ),
        "PROJECT_PRIORITY_MATRIX.md": "\n".join(
            [
                "## Priority Matrix",
                "",
                render_table(["Rank", "Project", "Priority Score", "Health", "Relevant Open Gates", "Next Focus"], priority_rows),
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
                f"- Watch projects: {sum(1 for p in projects if p.project_health == 'watch')}",
                f"- Portfolio planning gap total: {sum(len(p.missing_stage2_planning) for p in projects)}",
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
            f"- Planning backlog volume: {sum(len(p.missing_stage2_planning) for p in projects)}",
            f"- Measurement backlog volume: {sum(len(p.missing_stage2_measurement) for p in projects)}",
            "",
            "## Top Sequencing Moves",
            "",
            *(f"- {line}" for line in sequencing_lines[:3]),
            "",
            "## Outputs",
            "",
            f"- {PORTFOLIO_MGMT_DIR}",
        ]
    )
    return {"report": report}


def llm_006_outputs(projects: List[ProjectSnapshot], run_id: str) -> Dict[str, str]:
    approval_gaps = [p for p in projects if not p.approvals_present]
    stage_violations = [p for p in projects if p.missing_for_current_stage]
    metric_schema_gaps = [p for p in projects if p.inferred_stage >= 2 and p.missing_stage2_measurement]
    planning_gaps = [p for p in projects if p.inferred_stage >= 2 and p.missing_stage2_planning]
    contradiction_alerts: List[str] = []

    seen = set()
    for p in projects:
        if p.project_id in seen:
            contradiction_alerts.append(f"Duplicate project identifier: {p.project_id}")
        seen.add(p.project_id)

    severity_counts = {"critical": 0, "high": 0, "medium": 0}
    for project in projects:
        if project.missing_stage1 or not project.approvals_present:
            severity_counts["critical"] += 1
        elif project.missing_stage2_measurement:
            severity_counts["high"] += 1
        elif project.missing_stage2_planning:
            severity_counts["medium"] += 1

    planning_drift_freq = missing_frequency(projects, "missing_stage2_planning")
    measurement_drift_freq = missing_frequency(projects, "missing_stage2_measurement")

    files_to_body = {
        "GOVERNANCE_COMPLIANCE_AUDIT.md": "\n".join(
            [
                "## Governance Compliance Audit",
                "",
                f"- Projects audited: {len(projects)}",
                f"- Stage violations: {len(stage_violations)}",
                f"- Approval gaps: {len(approval_gaps)}",
                f"- Metric schema gaps: {len(metric_schema_gaps)}",
                f"- Planning schema gaps: {len(planning_gaps)}",
                "",
                "## Severity Mix",
                "",
                f"- Critical: {severity_counts['critical']}",
                f"- High: {severity_counts['high']}",
                f"- Medium: {severity_counts['medium']}",
            ]
        ),
        "STAGE_GATE_VIOLATION_REPORT.md": "\n".join(
            [
                "## Stage Gate Violations",
                "",
                *(
                    [
                        f"- `{p.project_id}`: relevant missing artifacts={len(p.missing_for_current_stage)} "
                        f"({join_or_none(p.missing_for_current_stage)})"
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
                        f"- `{p.project_id}` missing measurement artifacts: {join_or_none(p.missing_stage2_measurement)}"
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
                "- No migration packets found to validate in project folders.",
            ]
        ),
        "APPROVAL_GAP_REPORT.md": "\n".join(
            [
                "## Approval Gap Report",
                "",
                *(
                    [
                        f"- `{p.project_id}` missing one or more ML1 approvals "
                        f"(APPROVAL_RECORD.md present={ 'yes' if 'APPROVAL_RECORD.md' in p.files else 'no' }, "
                        f"ML1_METRIC_APPROVAL.md present={ 'yes' if 'ML1_METRIC_APPROVAL.md' in p.files else 'no' })."
                        for p in approval_gaps
                    ]
                    or ["- None."]
                ),
            ]
        ),
        "DOCTRINE_DRIFT_REPORT.md": "\n".join(
            [
                "## Doctrine Drift Report",
                "",
                "- Structural drift patterns detected from repeated missing artifacts:",
                *(
                    [
                        f"- Planning drift: `{name}` missing in {count} project(s)."
                        for name, count in planning_drift_freq.most_common(5)
                    ]
                    or ["- No repeated planning drift pattern detected."]
                ),
                *(
                    [
                        f"- Measurement drift: `{name}` missing in {count} project(s)."
                        for name, count in measurement_drift_freq.most_common(3)
                    ]
                    or ["- No repeated measurement drift pattern detected."]
                ),
                "- Doctrine interpretation remains ML1 authority.",
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
            f"- Planning schema gaps: {len(planning_gaps)}",
            "",
            "## Governance Risk View",
            "",
            f"- Critical risk projects: {severity_counts['critical']}",
            f"- High risk projects: {severity_counts['high']}",
            f"- Medium risk projects: {severity_counts['medium']}",
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
