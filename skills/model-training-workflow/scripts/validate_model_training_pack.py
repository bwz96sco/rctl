#!/usr/bin/env python3
"""Validate model-training-workflow artifact packs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "source_skill_map.md",
    "training_plan.md",
    "preflight_report.md",
    "training_run_matrix.yaml",
    "training_execution_log.md",
    "model_training_handoff.md",
]

REQUIRED_SECTIONS = {
    "training_plan.md": [
        "objective",
        "model_family",
        "dataset_and_split",
        "baseline",
        "metric_contract",
        "adapter_discovery",
        "training_lineage_contract",
        "sanity_gates",
        "stop_go_rules",
        "project_adapter_decision",
    ],
    "preflight_report.md": [
        "data_checks",
        "tokenization_or_label_checks",
        "model_and_checkpoint_checks",
        "environment_checks",
        "metric_sanity",
        "blockers",
    ],
    "training_execution_log.md": [
        "run_id",
        "run_manifest",
        "command",
        "runner_route",
        "environment_snapshot",
        "changed_files_relevant_to_run",
        "training_lineage_contract",
        "experiment_code_review",
        "health_gate_verdict",
        "logs",
        "metrics",
        "raw_artifact_paths",
        "status",
    ],
    "model_training_handoff.md": [
        "verdict",
        "strongest_evidence",
        "weakest_evidence",
        "claims_supported",
        "claims_blocked",
        "next_action",
    ],
}

REQUIRED_SOURCE_FIELDS = [
    "training_problem",
    "source_repo",
    "source_checked_at",
    "selected_categories",
    "selected_source_files_or_urls",
    "local_targets",
    "command_authority",
]

REQUIRED_MATRIX_TOKENS = [
    "runs:",
    "run_id:",
    "variant:",
    "dataset:",
    "primary_metric:",
    "gate_class:",
    "health_gates:",
    "success_criterion:",
    "stop_go_gate:",
    "approval_policy:",
]

DIAGNOSTIC_SECTIONS = [
    "failure_layer",
    "failure_type",
    "observed_signal",
    "evidence_paths",
    "next_route",
    "claims_blocked",
]

NONEMPTY_SOURCE_FIELDS = [
    "training_problem",
    "source_repo",
    "source_checked_at",
    "selected_categories",
    "selected_source_files_or_urls",
    "local_targets",
    "command_authority",
]

NONEMPTY_SECTIONS = {
    "training_plan.md": [
        "objective",
        "dataset_and_split",
        "baseline",
        "metric_contract",
        "adapter_discovery",
        "training_lineage_contract",
        "sanity_gates",
        "stop_go_rules",
    ],
    "preflight_report.md": [
        "data_checks",
        "tokenization_or_label_checks",
        "model_and_checkpoint_checks",
        "environment_checks",
        "metric_sanity",
        "blockers",
    ],
    "training_execution_log.md": [
        "run_manifest",
        "command",
        "changed_files_relevant_to_run",
        "training_lineage_contract",
        "experiment_code_review",
        "logs",
        "metrics",
        "raw_artifact_paths",
        "status",
    ],
    "model_training_handoff.md": [
        "verdict",
        "strongest_evidence",
        "weakest_evidence",
        "claims_supported",
        "claims_blocked",
        "next_action",
    ],
}

STRICT_DIAGNOSTIC_NONEMPTY = [
    "failure_layer",
    "failure_type",
    "observed_signal",
    "evidence_paths",
    "next_route",
    "claims_blocked",
]

ALLOWED_VERDICTS = {
    "continue",
    "retry-with-delta",
    "debug",
    "scale",
    "compare",
    "handoff",
    "redesign",
    "park",
}

EMPTY_VALUES = {"", "todo", "tbd", "n/a", "na", "none", "unknown"}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text()


def has_heading_or_field(text: str, name: str) -> bool:
    raw = name.lower()
    normalized = name.lower().replace("_", " ")
    for line in text.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("#") and stripped.lstrip("#").strip() in {raw, normalized}:
            return True
        if stripped.startswith(f"{raw}:"):
            return True
        if stripped.startswith(f"{normalized}:"):
            return True
    return False


def normalize_name(name: str) -> str:
    return name.lower().replace("_", " ")


def clean_value(value: str) -> str:
    value = value.strip()
    while value.startswith(("-", "*", ">")):
        value = value[1:].strip()
    return value.strip()


def field_value(text: str, name: str) -> str:
    raw = name.lower()
    normalized = normalize_name(name)
    for line in text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        for prefix in (raw, normalized):
            if lowered.startswith(f"{prefix}:"):
                return clean_value(stripped.split(":", 1)[1])
    return ""


def heading_content(text: str, name: str) -> str:
    wanted = {name.lower(), normalize_name(name)}
    lines = text.splitlines()
    start: int | None = None
    start_level = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        title = stripped.lstrip("#").strip().lower()
        if title in wanted:
            start = index + 1
            start_level = len(stripped) - len(stripped.lstrip("#"))
            break
    if start is None:
        return field_value(text, name)
    content: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level <= start_level:
                break
        content.append(line)
    return "\n".join(content).strip()


def has_content(text: str, name: str) -> bool:
    value = heading_content(text, name) or field_value(text, name)
    normalized = clean_value(value).lower()
    return normalized not in EMPTY_VALUES


def has_matrix_gate(matrix_text: str) -> bool:
    return "health_gates:" in matrix_text and any(
        token in matrix_text.lower()
        for token in ["tiny_overfit", "tiny overfit", "one_batch", "one-batch", "smoke", "decode_sanity"]
    )


def artifact_paths_are_concrete(text: str) -> bool:
    value = heading_content(text, "raw_artifact_paths")
    lowered = value.lower()
    if any(marker in lowered for marker in ["fixture:", "unavailable:", "not_available:"]):
        return True
    return "/" in value or "." in value


def changed_files_are_present(text: str) -> bool:
    value = clean_value(heading_content(text, "changed_files_relevant_to_run"))
    lowered = value.lower()
    if not lowered:
        return False
    no_change_markers = (
        "none",
        "not_applicable",
        "not applicable",
        "no relevant",
        "unchanged",
        "fixture does not change",
    )
    return not any(lowered.startswith(marker) for marker in no_change_markers)


def validate_experiment_code_review(text: str) -> list[str]:
    errors: list[str] = []
    review = heading_content(text, "experiment_code_review")
    if "not_required" in review.lower():
        if not re.search(r"(?im)^\s*(?:[-*]\s*)?not_required:\s*\S+", review):
            errors.append("training_execution_log.md experiment_code_review not_required must include a reason")
        if changed_files_are_present(text):
            errors.append(
                "training_execution_log.md experiment_code_review cannot be not_required when changed_files_relevant_to_run is nonempty"
            )
    return errors


def handoff_verdict(text: str) -> str:
    value = clean_value(heading_content(text, "verdict"))
    if not value:
        value = clean_value(field_value(text, "verdict"))
    return value.split()[0].strip("`.,").lower()


def validate(root: Path, strict_diagnostics: bool) -> list[str]:
    errors: list[str] = []
    if not root.exists():
        return [f"root does not exist: {root}"]
    if not root.is_dir():
        return [f"root is not a directory: {root}"]

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required file: {rel}")
        elif not read_text(path).strip():
            errors.append(f"empty required file: {rel}")

    source_path = root / "source_skill_map.md"
    if source_path.is_file():
        source_text = read_text(source_path)
        for field in REQUIRED_SOURCE_FIELDS:
            if not has_heading_or_field(source_text, field):
                errors.append(f"source_skill_map.md missing {field}")
        for field in NONEMPTY_SOURCE_FIELDS:
            if not has_content(source_text, field):
                errors.append(f"source_skill_map.md has empty {field}")

    for rel, sections in REQUIRED_SECTIONS.items():
        path = root / rel
        if not path.is_file():
            continue
        text = read_text(path)
        for section in sections:
            if not has_heading_or_field(text, section):
                errors.append(f"{rel} missing {section}")
        for section in NONEMPTY_SECTIONS.get(rel, []):
            if not has_content(text, section):
                errors.append(f"{rel} has empty {section}")

    matrix_path = root / "training_run_matrix.yaml"
    if matrix_path.is_file():
        matrix_text = read_text(matrix_path)
        for token in REQUIRED_MATRIX_TOKENS:
            if token not in matrix_text:
                errors.append(f"training_run_matrix.yaml missing token {token}")
        if not has_matrix_gate(matrix_text):
            errors.append("training_run_matrix.yaml missing concrete sanity health gate")

    execution_path = root / "training_execution_log.md"
    if execution_path.is_file():
        execution_text = read_text(execution_path)
        if not artifact_paths_are_concrete(execution_text):
            errors.append("training_execution_log.md raw_artifact_paths must be concrete or marked unavailable/fixture")
        errors.extend(validate_experiment_code_review(execution_text))

    handoff_path = root / "model_training_handoff.md"
    if handoff_path.is_file():
        verdict = handoff_verdict(read_text(handoff_path))
        if verdict not in ALLOWED_VERDICTS:
            errors.append(
                "model_training_handoff.md verdict must be one of: "
                + ", ".join(sorted(ALLOWED_VERDICTS))
            )

    diagnostic_path = root / "training_diagnostic_report.md"
    if strict_diagnostics:
        if not diagnostic_path.is_file():
            errors.append("missing required file: training_diagnostic_report.md")
        elif not read_text(diagnostic_path).strip():
            errors.append("empty required file: training_diagnostic_report.md")
    if diagnostic_path.is_file():
        text = read_text(diagnostic_path)
        for section in DIAGNOSTIC_SECTIONS:
            if not has_heading_or_field(text, section):
                errors.append(f"training_diagnostic_report.md missing {section}")
        if strict_diagnostics:
            for section in STRICT_DIAGNOSTIC_NONEMPTY:
                if not has_content(text, section):
                    errors.append(f"training_diagnostic_report.md has empty {section}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument(
        "--strict-diagnostics",
        action="store_true",
        help="Require training_diagnostic_report.md for failed, suspicious, or collapsed runs",
    )
    args = parser.parse_args()

    errors = validate(args.root, args.strict_diagnostics)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
