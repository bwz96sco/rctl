#!/usr/bin/env python3
"""Check an optional training evidence summary; scientific validity stays with review."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

SUMMARY_FIELDS = (
    "verdict",
    "strongest_evidence",
    "claims_supported",
    "claims_blocked",
    "next_action",
)
RUN_FIELDS = ("run_manifest", "raw_artifact_paths", "status")
DIAGNOSTIC_FIELDS = (
    "failure_layer",
    "failure_type",
    "observed_signal",
    "evidence_paths",
    "next_route",
    "claims_blocked",
)


def content(text: str, name: str) -> str:
    names = {name.lower(), name.lower().replace("_", " ")}
    lines = text.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r"^(#+)\s+(.+?)\s*$", line)
        if heading and heading[2].lower() in names:
            values = []
            for following in lines[index + 1 :]:
                next_heading = re.match(r"^(#+)\s+", following)
                if next_heading and len(next_heading[1]) <= len(heading[1]):
                    break
                values.append(following)
            return "\n".join(values).strip()
        field = re.match(r"^\s*(?:[-*]\s*)?([^:]+):\s*(.*)$", line)
        if field and field[1].strip().lower() in names:
            return field[2].strip()
    return ""


def complete(value: str) -> bool:
    return (
        bool(value.strip())
        and value.strip().lower() not in {"todo", "tbd"}
        and not re.search(r"<[^>\n]+>", value)
    )


def require_fields(path: Path, fields: tuple[str, ...], errors: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    for field in fields:
        if not complete(content(text, field)):
            errors.append(f"{path.name} missing completed {field}")
    return text


def validate(root: Path, strict_diagnostics: bool) -> list[str]:
    if not root.is_dir():
        return [f"root is not a directory: {root}"]
    errors: list[str] = []
    summary = root / "model_training_handoff.md"
    if not summary.is_file():
        return ["missing required file: model_training_handoff.md"]
    require_fields(summary, SUMMARY_FIELDS, errors)

    # Reuse an earlier pack's execution log or put run references in the summary.
    execution = root / "training_execution_log.md"
    run_source = execution if execution.is_file() else summary
    run_text = require_fields(run_source, RUN_FIELDS, errors)
    paths = content(run_text, "raw_artifact_paths")
    unavailable = re.search(
        r"(?im)^\s*(?:[-*]\s*)?(?:unavailable|not_available|fixture):\s*\S", paths
    )
    if complete(paths) and not unavailable and "/" not in paths and "." not in paths:
        errors.append(
            f"{run_source.name} raw_artifact_paths need paths or an explained unavailable marker"
        )

    diagnostic = root / "training_diagnostic_report.md"
    if strict_diagnostics and not diagnostic.is_file():
        errors.append("missing required file: training_diagnostic_report.md")
    if diagnostic.is_file():
        require_fields(diagnostic, DIAGNOSTIC_FIELDS, errors)

    for name in (
        "training_plan.md",
        "preflight_report.md",
        "source_skill_map.md",
        "training_run_matrix.yaml",
    ):
        path = root / name
        if path.is_file() and not path.read_text(encoding="utf-8").strip():
            errors.append(f"empty optional file: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument(
        "--strict-diagnostics",
        action="store_true",
        help="Require the requested diagnostic report",
    )
    args = parser.parse_args()
    try:
        errors = validate(args.root, args.strict_diagnostics)
    except (OSError, UnicodeError) as error:
        errors = [f"Cannot inspect training evidence: {error}"]
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print("OK training summary structure; execution and scientific validity unassessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
