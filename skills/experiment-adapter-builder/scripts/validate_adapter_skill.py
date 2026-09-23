#!/usr/bin/env python3
"""Validate a generated project-local experiment adapter skill."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "references/runners.md",
    "references/preflight-health.md",
    "references/queue-and-concurrency.md",
    "references/monitoring.md",
    "references/profiling.md",
    "references/result-validation.md",
    "references/adapter-sources.md",
    "templates/run-manifest.md",
    "templates/experiment-campaign.md",
    "templates/experiment-code-review.md",
    "templates/result-ledger.csv",
]

REFERENCE_PATTERNS = {
    "references/runners.md": [
        "command_authority",
        "working_directory",
        "environment_manager",
        "runner_selection",
        "canonical_output_root",
    ],
    "references/preflight-health.md": [
        "data_checks",
        "checkpoint_checks",
        "baseline_checks",
        "environment_checks",
        "gpu_memory_checks",
    ],
    "references/queue-and-concurrency.md": [
        "queue_authority",
        "max_parallel",
        "grid_spec",
        "job_state_machine",
        "completion detection",
        "phase_chaining",
        "retry_policy",
        "stale_job_cleanup",
        "wave_transition_gate",
        "crash_recovery",
        "known_failure_modes",
        "shared_state_hazards",
    ],
    "references/monitoring.md": [
        "backend_status_checks",
        "logs",
        "metrics",
        "structured_outputs",
        "raw_numbers_summary",
    ],
    "references/profiling.md": [
        "profiling_triggers",
        "target_types",
        "tools",
        "instrumentation_policy",
        "profile_output_root",
        "report_structure",
        "instrumentation_changelog_required",
        "cleanup_policy",
    ],
    "references/result-validation.md": [
        "expected_outputs",
        "metric_parsing",
        "experiment_code_review",
        "EXPERIMENT_CODE_REVIEW.md",
        "baseline_comparison",
        "failure_classes",
        "paper_valid_evidence_gate",
        "eval_integrity",
        "claim_boundary",
    ],
    "references/adapter-sources.md": [
        "fact_sources",
        "update_history",
        "open_questions",
    ],
}

RUN_MANIFEST_PATTERNS = [
    "identity",
    "command",
    "code_state",
    "environment",
    "data_contract",
    "model_contract",
    "training_contract",
    "eval_contract",
    "expected_outputs",
    "launch_guard",
    "result_summary",
]

FORBIDDEN_RUNTIME_FIELDS = [
    "current_run_id",
    "current_campaign_status",
    "today_failures",
    "temporary_blockers",
    "live_queue_status",
    "latest_result",
    "raw_log_excerpt",
    "checkpoint_blob",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_name(name: str) -> str:
    return name.lower().replace("_", " ")


def clean_marker_prefix(value: str) -> str:
    value = value.strip().lower()
    while value.startswith(("-", "*", ">")):
        value = value[1:].strip()
    return value


def has_heading_or_field(text: str, name: str) -> bool:
    raw = name.lower()
    normalized = normalize_name(name)
    for line in text.splitlines():
        stripped = clean_marker_prefix(line)
        if stripped.startswith("#") and stripped.lstrip("#").strip() in {raw, normalized}:
            return True
        if stripped.startswith(f"{raw}:") or stripped.startswith(f"{normalized}:"):
            return True
    return False


def validate_required_files(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing required file: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"empty required file: {rel}")
    return errors


def validate_skill_md(root: Path) -> list[str]:
    path = root / "SKILL.md"
    if not path.is_file():
        return []
    text = read_text(path)
    errors: list[str] = []
    if not re.search(r"^name:\s+", text, re.MULTILINE):
        errors.append("SKILL.md missing name frontmatter")
    if not re.search(r"^description:\s+", text, re.MULTILINE):
        errors.append("SKILL.md missing description frontmatter")
    line_count = len(text.splitlines())
    if line_count > 100:
        errors.append(f"SKILL.md too long: {line_count} lines")
    return errors


def validate_reference_patterns(root: Path) -> list[str]:
    errors: list[str] = []
    for rel, labels in REFERENCE_PATTERNS.items():
        path = root / rel
        if not path.is_file():
            continue
        text = read_text(path)
        missing = [
            label
            for label in labels
            if (label.lower() not in text.lower() if "." in label else not has_heading_or_field(text, label))
        ]
        if missing:
            errors.append(f"{rel} missing fields: {', '.join(missing)}")
    return errors


def validate_run_manifest_patterns(root: Path) -> list[str]:
    path = root / "templates/run-manifest.md"
    if not path.is_file():
        return []
    text = read_text(path)
    missing = [label for label in RUN_MANIFEST_PATTERNS if not has_heading_or_field(text, label)]
    if missing:
        return [f"templates/run-manifest.md missing fields: {', '.join(missing)}"]
    return []


def validate_no_runtime_state(root: Path) -> list[str]:
    errors: list[str] = []
    scan_paths = [root / "SKILL.md", *sorted((root / "references").glob("*.md"))]
    for path in scan_paths:
        if not path.is_file():
            continue
        text = read_text(path).lower()
        for field in FORBIDDEN_RUNTIME_FIELDS:
            if field.lower() in text:
                rel = path.relative_to(root)
                errors.append(f"{rel} contains mutable runtime field: {field}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adapter_dir", type=Path, help="Generated project experiment adapter directory")
    args = parser.parse_args()

    root = args.adapter_dir.resolve()
    if not root.is_dir():
        print(f"FAIL adapter dir is not a directory: {root}", file=sys.stderr)
        return 1

    errors: list[str] = []
    errors.extend(validate_required_files(root))
    errors.extend(validate_skill_md(root))
    errors.extend(validate_reference_patterns(root))
    errors.extend(validate_run_manifest_patterns(root))
    errors.extend(validate_no_runtime_state(root))

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1

    print(f"OK experiment adapter skill: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
