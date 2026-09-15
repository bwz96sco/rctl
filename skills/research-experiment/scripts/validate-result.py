#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Validate a research-experiment result structure and optional candidate lineage."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

ORIGIN_TYPES = {"supplied", "problem", "candidate"}
ASSESSMENTS = {"supported", "not_supported", "inconclusive", "not_applicable"}
MECHANISM_VALUES = {"yes", "no", "not_applicable"}
CANDIDATE_ID = re.compile(r"C[1-9][0-9]*")
REQUIRED_BODY_FIELDS = (
    "material amendments",
    "actual run IDs",
    "commands, configs, and code state",
    "evidence references",
    "failed or null runs",
    "aggregation",
    "baseline relation",
    "comparability",
    "deviations",
    "claims not made",
    "next action",
)


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path.name}: unterminated YAML frontmatter")
    try:
        result = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise ValueError(f"{path.name}: invalid YAML frontmatter") from exc
    if not isinstance(result, dict):
        raise ValueError(f"{path.name}: frontmatter must be a mapping")
    return result


def scalar(fields: dict, key: str, path: Path) -> str:
    value = fields.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path.name}: {key} must be a nonempty scalar")
    return value


def validate_candidate(origin_id: str, decision: Path | None) -> None:
    if not CANDIDATE_ID.fullmatch(origin_id):
        raise ValueError("contract.md: candidate origin requires a C# origin_id")
    if decision is None or not decision.is_file() or decision.name != "decision.md":
        raise ValueError("candidate origin requires --decision pointing to decision.md")

    idea_validator = (
        Path(__file__).resolve().parents[2]
        / "research-idea-evaluation"
        / "scripts"
        / "validate-handoff.py"
    )
    if not idea_validator.is_file():
        raise ValueError(
            "candidate validation requires the peer handoff validator; "
            "install research-idea-evaluation beside research-experiment "
            f"under the same skills root (expected {idea_validator})"
        )
    result = subprocess.run(
        [sys.executable, str(idea_validator), "decision", str(decision.parent)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stdout.strip() or result.stderr.strip()
        raise ValueError(f"invalid candidate decision: {detail}")

    selected = frontmatter(decision).get("selected_candidate_ids")
    if not isinstance(selected, list) or origin_id not in selected:
        raise ValueError(f"contract.md: {origin_id} was not selected in decision.md")


def body_field(text: str, label: str) -> str:
    matches = re.findall(rf"(?im)^-[ \t]*{re.escape(label)}[ \t]*:[ \t]*(.*)$", text)
    if (
        len(matches) != 1
        or not matches[0].strip()
        or re.search(r"<[^>\n]+>", matches[0])
    ):
        raise ValueError(f"missing nonempty {label} (one completed value required)")
    return matches[0].strip()


def validate_result(root: Path, decision: Path | None) -> None:
    contract = root / "contract.md"
    result = root / "result.md"
    contract_fields = frontmatter(contract)
    fields = frontmatter(result)
    if scalar(fields, "task_id", result) != scalar(
        contract_fields, "task_id", contract
    ):
        raise ValueError("result.md: task_id differs from contract.md")
    if scalar(fields, "assessment", result) not in ASSESSMENTS:
        raise ValueError("result.md: assessment must use the native rctl vocabulary")
    revision = fields.get("contract_revision")
    if type(revision) is not int or revision < 1:
        raise ValueError("result.md: contract_revision must be positive")
    contract_body = contract.read_text(encoding="utf-8").split("\n---\n", 1)[1]
    origin_type = body_field(contract_body, "Origin type")
    origin_id = body_field(contract_body, "Origin ID")
    role = body_field(contract_body, "Experiment role")
    if origin_type not in ORIGIN_TYPES:
        raise ValueError(
            f"contract.md: Origin type must be one of {sorted(ORIGIN_TYPES)}"
        )
    if (origin_type == "problem") != (role == "problem_validation"):
        raise ValueError(
            "contract.md: problem origin requires problem_validation and vice versa"
        )
    if origin_type == "candidate":
        validate_candidate(origin_id, decision)
    body = result.read_text(encoding="utf-8").split("\n---\n", 1)[1]
    if body_field(body, "Mechanism tested") not in MECHANISM_VALUES:
        raise ValueError(
            "result.md: Mechanism tested must be yes, no, or not_applicable"
        )
    body_field(body, "Supported claim")
    for label in REQUIRED_BODY_FIELDS:
        body_field(body, label)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--decision", type=Path)
    args = parser.parse_args()
    try:
        validate_result(args.root, args.decision)
    except (OSError, TypeError, ValueError) as exc:
        print(f"FAIL {exc}")
        return 1
    print(
        "OK experiment structure and candidate lineage only; rctl verify and evidence review remain required"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
