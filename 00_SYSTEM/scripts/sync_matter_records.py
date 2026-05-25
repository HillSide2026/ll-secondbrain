#!/usr/bin/env python3
"""
sync_matter_records.py

Backfill canonical matter-management fields into MATTER.yaml, reconcile
matter-local README status blocks with MATTER.yaml, and regenerate the
hand-maintained matter registry from local matter records.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
MATTERS_ROOT = ROOT / "05_MATTERS"
REGISTRY_PATH = MATTERS_ROOT / "MATTER_REGISTRY.md"
FOLDER_ORDER = ["ESSENTIAL", "STRATEGIC", "STANDARD", "NORMAL"]

CLIENT_NAME_OVERRIDES = {
    "22-194-00006": "Rousseau Mazzuca LLP",
    "23-194-00013": "Rousseau Mazzuca LLP",
    "24-256-00001": "Aspire Infusions Inc",
    "24-256-00002": "Aspire Infusions Inc",
    "24-256-00003": "Aspire Infusions Inc",
    "24-256-00004": "Aspire Infusions Inc",
    "24-256-00005": "Aspire Infusions Inc",
    "25-194-00059": "Rousseau Mazzuca LLP",
    "26-1631-00001": "1713425 Ontario Inc.",
    "26-1637-00001": "MRKT",
}

INSTRUCTING_OFFICER_OVERRIDES = {
    "22-194-00006": "Michael Mazzuca",
    "23-169-00003": "Kato Wake",
    "23-194-00013": "Michael Mazzuca",
    "24-336-00004": "Max Hill",
    "24-646-00001": "Nicolas Rousseau",
    "24-256-00001": "Sy",
    "24-256-00002": "Sy",
    "24-256-00003": "Sy",
    "24-256-00004": "Sy",
    "24-256-00005": "Sy",
    "25-1024-00001": "Mark",
    "25-1185-00001": "Alexander Klys",
    "25-1231-00001": "Charmaine Spiteri",
    "25-1318-00001": "Zelko Culibrk",
    "25-1363-00001": "Raevan Joy Sambrano",
    "25-192-00003": "Paige",
    "25-845-00001": "Abhishek Shah",
    "25-845-00002": "Abhishek Shah",
    "25-927-00003": "Harry Bedi",
    "25-1538-00002": "Georgiana Nicoară",
    "25-1588-00001": "Gregory Popov",
    "25-174-00001": "Danielle Thompson",
    "25-194-00059": "Michael Mazzuca",
    "25-822-00001": "Majid Hajibeigy",
    "26-1630-00001": "Marcela Hernandez",
    "26-1639-00001": "Diego Ures",
    "26-1639-00002": "Diego Ures",
    "26-1639-00003": "Carolina Ures-Saldanha",
    "26-1631-00001": "Tejvir Boparai",
    "26-1637-00001": "Nilabh Anand",
    "26-927-00004": "Harry Bedi",
}

DESCRIPTION_OVERRIDES = {
    "22-194-00006": "Commercial Leasing",
    "23-194-00013": "Corporate Matters - Legacy",
    "25-194-00059": "Training Centre",
}

PLACEHOLDER_VALUES = {
    "",
    "[Brief description of the matter]",
    "(Plain-language description of what this matter is about.)",
}

TOP_LEVEL_ORDER = [
    "matter_id",
    "clio_matter_id",
    "matter_name",
    "client_name",
    "instructing_officer_name",
    "matter_description",
    "status",
    "delivery_status",
    "delivery_stage",
    "fulfillment_status",
    "engagement_date",
    "created_date",
    "closed_date",
    "practice_area",
    "previous_reference",
    "services",
    "solutions",
    "strategies",
]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a mapping")
    return data


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def is_placeholder(value: str | None) -> bool:
    if value is None:
        return True
    return normalize_whitespace(value) in PLACEHOLDER_VALUES


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_readme_title(path: Path) -> str | None:
    text = read_text(path)
    for line in text.splitlines():
        if line.startswith("# "):
            return normalize_whitespace(line[2:])
    return None


def read_section_value(path: Path, headings: list[str]) -> str | None:
    text = read_text(path)
    if not text:
        return None

    lines = text.splitlines()
    capture = False
    collected: list[str] = []

    for line in lines:
        if line.strip() in headings:
            capture = True
            collected = []
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.strip():
            collected.append(normalize_whitespace(line))

    if not collected:
        return None

    candidate = collected[0]
    if is_placeholder(candidate):
        return None
    return candidate


def infer_client_name(matter_id: str, data: dict[str, Any], readme_title: str | None) -> str | None:
    if matter_id in CLIENT_NAME_OVERRIDES:
        return CLIENT_NAME_OVERRIDES[matter_id]

    existing = data.get("client_name")
    if isinstance(existing, str) and existing.strip():
        return normalize_whitespace(existing)

    matter_name = normalize_whitespace(str(data.get("matter_name") or ""))
    if " — " in matter_name:
        return matter_name.split(" — ", 1)[0].strip()

    if readme_title and readme_title not in PLACEHOLDER_VALUES:
        if matter_id not in {"26-1639-00001", "26-1639-00002", "26-1639-00003"}:
            return readme_title

    return matter_name or None


def infer_instructing_officer(matter_id: str, data: dict[str, Any]) -> str | None:
    if matter_id in INSTRUCTING_OFFICER_OVERRIDES:
        return INSTRUCTING_OFFICER_OVERRIDES[matter_id]

    existing = data.get("instructing_officer_name")
    if isinstance(existing, str) and existing.strip():
        return normalize_whitespace(existing)

    return None


def infer_description(matter_id: str, data: dict[str, Any], readme_path: Path) -> str | None:
    existing = data.get("matter_description")
    if isinstance(existing, str) and existing.strip() and not is_placeholder(existing):
        return normalize_whitespace(existing)

    if matter_id in DESCRIPTION_OVERRIDES:
        return DESCRIPTION_OVERRIDES[matter_id]

    candidate = read_section_value(readme_path, ["## Description", "## Overview"])
    if candidate:
        return candidate

    return None


def infer_engagement_date(data: dict[str, Any]) -> str | None:
    for key in ("engagement_date", "created_date"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return normalize_whitespace(value)
    return None


def canonical_delivery_status(value: str | None, matter_dir: Path) -> str:
    if not value:
        return matter_dir.parent.name.title()
    token = normalize_whitespace(value)
    if token.lower() == "parked":
        return "Normal"
    return token[0].upper() + token[1:] if token else matter_dir.parent.name.title()


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def render_yaml(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(render_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(item)}")
        return lines

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, child in item.items():
                    child_prefix = f"{prefix}- " if first else f"{prefix}  "
                    if isinstance(child, (dict, list)):
                        lines.append(f"{child_prefix}{key}:")
                        lines.extend(render_yaml(child, indent + 4))
                    else:
                        lines.append(f"{child_prefix}{key}: {yaml_scalar(child)}")
                    first = False
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
        return lines

    lines.append(f"{prefix}{yaml_scalar(value)}")
    return lines


def build_ordered_record(data: dict[str, Any]) -> dict[str, Any]:
    ordered: dict[str, Any] = {}
    for key in TOP_LEVEL_ORDER:
        if key in data:
            ordered[key] = data[key]
    for key, value in data.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    text = "\n".join(render_yaml(data)) + "\n"
    path.write_text(text, encoding="utf-8")


def sync_readme_status_block(readme_path: Path, data: dict[str, Any], matter_dir: Path) -> bool:
    if not readme_path.exists():
        return False

    original = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(r"(^## Status\n)(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    match = pattern.search(original)
    if not match:
        return False

    status_lines = [
        "## Status",
        f"- **Clio Status:** {data.get('status', 'Open')}",
        f"- **Delivery Status:** {canonical_delivery_status(data.get('delivery_status'), matter_dir)}",
    ]

    delivery_stage = data.get("delivery_stage")
    if isinstance(delivery_stage, str) and delivery_stage.strip():
        status_lines.append(f"- **Delivery Stage:** {normalize_whitespace(delivery_stage)}")

    status_lines.append(f"- **Fulfillment Status:** {data.get('fulfillment_status', 'active')}")

    replacement = "\n".join(status_lines) + "\n\n"
    updated = original[: match.start()] + replacement + original[match.end() :]

    if updated == original:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True


def generate_registry(rows: list[dict[str, str]]) -> str:
    lines = [
        "# Matter Registry",
        "",
        "| Matter ID | Matter Name | Delivery Status |",
        "|---|---|---|",
    ]

    for folder in FOLDER_ORDER:
        folder_rows = [row for row in rows if row["folder"] == folder]
        folder_rows.sort(key=lambda row: row["matter_id"])
        for row in folder_rows:
            lines.append(
                f"| {row['matter_id']} | {row['matter_name']} | {row['delivery_status']} |"
            )

    lines.append("")
    return "\n".join(lines)


def matter_dirs() -> list[Path]:
    return sorted(path.parent for path in MATTERS_ROOT.rglob("MATTER.yaml"))


def main() -> int:
    yaml_updates = 0
    readme_updates = 0
    registry_rows: list[dict[str, str]] = []

    for matter_dir in matter_dirs():
        yaml_path = matter_dir / "MATTER.yaml"
        readme_path = matter_dir / "README.md"
        data = load_yaml(yaml_path)

        matter_id = str(data.get("matter_id") or matter_dir.name)
        readme_title = read_readme_title(readme_path)

        data["matter_id"] = matter_id
        data["clio_matter_id"] = matter_id
        data["client_name"] = infer_client_name(matter_id, data, readme_title)
        data["instructing_officer_name"] = infer_instructing_officer(matter_id, data)
        data["matter_description"] = infer_description(matter_id, data, readme_path)
        data["engagement_date"] = infer_engagement_date(data)
        data["closed_date"] = data.get("closed_date")

        ordered = build_ordered_record(data)
        rendered = "\n".join(render_yaml(ordered)) + "\n"
        current = yaml_path.read_text(encoding="utf-8")
        if rendered != current:
            yaml_path.write_text(rendered, encoding="utf-8")
            yaml_updates += 1

        if sync_readme_status_block(readme_path, ordered, matter_dir):
            readme_updates += 1

        registry_rows.append(
            {
                "folder": matter_dir.parent.name,
                "matter_id": matter_id,
                "matter_name": str(ordered.get("matter_name") or ordered.get("client_name") or matter_id),
                "delivery_status": canonical_delivery_status(
                    str(ordered.get("delivery_status") or matter_dir.parent.name),
                    matter_dir,
                ),
            }
        )

    registry_text = generate_registry(registry_rows)
    current_registry = REGISTRY_PATH.read_text(encoding="utf-8")
    if registry_text != current_registry:
        REGISTRY_PATH.write_text(registry_text, encoding="utf-8")

    print(f"Updated MATTER.yaml files: {yaml_updates}")
    print(f"Updated README status blocks: {readme_updates}")
    print(f"Regenerated registry: {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
