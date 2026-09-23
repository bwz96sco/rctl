#!/usr/bin/env python3
"""Audit Orchestra AI Research Skills for model-training integration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


TRAINING_CORE_PREFIXES = {
    "01-model-architecture": "training-core",
    "02-tokenization": "training-core",
    "03-fine-tuning": "training-core",
    "06-post-training": "training-core",
    "08-distributed-training": "training-core",
    "10-optimization": "training-core",
    "11-evaluation": "training-core",
    "13-mlops": "training-core",
    "18-multimodal": "training-core",
    "19-emerging-techniques": "training-core",
}

TRAINING_ADJACENT_PREFIXES = {
    "04-mechanistic-interpretability": "training-adjacent",
    "05-data-processing": "training-adjacent",
    "09-infrastructure": "training-adjacent",
    "12-inference-serving": "training-adjacent",
    "17-observability": "training-adjacent",
}

RESEARCH_PREFIXES = {
    "0-autoresearch-skill": "research-orchestration",
    "21-research-ideation": "research-orchestration",
    "22-agent-native-research-artifact": "research-orchestration",
}

WRITING_PREFIXES = {
    "20-ml-paper-writing": "writing/figure",
}

TOOL_PREFIXES = {
    "07-safety-alignment": "tool-wrapper",
    "14-agents": "tool-wrapper",
    "15-rag": "tool-wrapper",
    "16-prompt-engineering": "tool-wrapper",
}

KEYWORDS = {
    "model",
    "train",
    "fine-tun",
    "lora",
    "qlora",
    "token",
    "gpu",
    "distributed",
    "evaluation",
    "benchmark",
    "mlops",
    "checkpoint",
    "inference",
    "multimodal",
    "rl",
    "optimization",
}


def first_path_part(path: str) -> str:
    return path.split("/", 1)[0]


def classify(path: str) -> str:
    prefix = first_path_part(path)
    if prefix in TRAINING_CORE_PREFIXES:
        return TRAINING_CORE_PREFIXES[prefix]
    if prefix in TRAINING_ADJACENT_PREFIXES:
        return TRAINING_ADJACENT_PREFIXES[prefix]
    if prefix in RESEARCH_PREFIXES:
        return RESEARCH_PREFIXES[prefix]
    if prefix in WRITING_PREFIXES:
        return WRITING_PREFIXES[prefix]
    if prefix in TOOL_PREFIXES:
        return TOOL_PREFIXES[prefix]
    return "ignore"


def category(path: str) -> str:
    parts = path.split("/")
    if len(parts) <= 2:
        return parts[0]
    return parts[0]


def source_name(path: str) -> str:
    parts = path.split("/")
    if len(parts) >= 2:
        return parts[-2]
    return Path(path).stem


def extract_refs(text: str) -> list[str]:
    refs: list[str] = []
    for line in text.splitlines():
        if "references/" in line or "templates/" in line or line.strip().startswith("- ["):
            refs.extend(re.findall(r"[A-Za-z0-9_./-]*(?:references|templates)/[A-Za-z0-9_./-]+", line))
    return sorted(set(refs))


def extract_io_hints(text: str) -> tuple[list[str], list[str]]:
    inputs: set[str] = set()
    outputs: set[str] = set()
    for line in text.splitlines():
        lower = line.lower()
        if any(word in lower for word in ["input", "requires", "prerequisite", "before you"]):
            inputs.update(re.findall(r"`([^`]+)`", line))
        if any(word in lower for word in ["output", "write", "create", "generate", "artifact", "report"]):
            outputs.update(re.findall(r"`([^`]+)`", line))
    return sorted(inputs), sorted(outputs)


def relevance_score(description: str, text: str, cls: str) -> int:
    score = 0
    haystack = f"{description}\n{text[:4000]}".lower()
    for keyword in KEYWORDS:
        if keyword in haystack:
            score += 1
    if cls == "training-core":
        score += 4
    elif cls == "training-adjacent":
        score += 2
    return score


def local_target(cls: str) -> str:
    if cls == "training-core":
        return "candidate: model-training-workflow source-routing/preflight/failure taxonomy/adapter handoff"
    if cls == "training-adjacent":
        return "candidate: model-training-workflow source-routing or experiment-adapter-builder"
    if cls == "research-orchestration":
        return "existing research-ideation/research-experiment; no model-training import by default"
    if cls == "writing/figure":
        return "existing research-writing/research-figure; no model-training import"
    if cls == "tool-wrapper":
        return "tool-specific skill or existing source catalog; no model-training import by default"
    return "waived: not relevant to model-training workflow"


def load_source_text(source_root: Path, rel_path: str) -> str:
    path = source_root / rel_path
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def build_audit(skills: list[dict[str, Any]], source_root: Path, expected_commit: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    commits = {str(skill.get("source_commit", "")) for skill in skills}
    if expected_commit and commits != {expected_commit}:
        raise ValueError(f"source commit mismatch: found {sorted(commits)} expected {expected_commit}")

    for skill in sorted(skills, key=lambda item: item.get("path", "")):
        path = str(skill.get("path", ""))
        text = load_source_text(source_root, path)
        cls = classify(path)
        inputs, outputs = extract_io_hints(text)
        refs = extract_refs(text)
        description = str(skill.get("description", "")).strip()
        score = relevance_score(description, text, cls)
        records.append(
            {
                "skill_id": skill.get("skill_id", ""),
                "name": skill.get("name", ""),
                "source_path": path,
                "category": category(path),
                "source_commit": skill.get("source_commit", ""),
                "classification": cls,
                "training_relevance_score": score,
                "description": description,
                "reference_paths": refs,
                "input_hints": inputs,
                "output_hints": outputs,
                "local_target": local_target(cls),
                "integration_status": "pending_manual_review" if cls in {"training-core", "training-adjacent"} else "waived_or_existing_owner",
            }
        )

    return {
        "source": "Orchestra AI Research Skills",
        "source_url": "https://github.com/Orchestra-Research/AI-Research-SKILLs.git",
        "source_commit": expected_commit or next(iter(commits), ""),
        "checked_at": date.today().isoformat(),
        "record_count": len(records),
        "classification_counts": dict(Counter(record["classification"] for record in records)),
        "category_counts": dict(Counter(record["category"] for record in records)),
        "records": records,
    }


def write_markdown(audit: dict[str, Any], path: Path) -> None:
    counts = audit["classification_counts"]
    lines = [
        "# Orchestra AI Research Skills Model-Training Source Audit",
        "",
        f"Source: `{audit['source_url']}`",
        f"Commit: `{audit['source_commit']}`",
        f"Checked at: `{audit['checked_at']}`",
        f"Records: `{audit['record_count']}`",
        "",
        "## Status",
        "",
        "This is a source-inspection audit, not a distillation approval. `model-training-workflow` remains local draft until selected records receive manual source read, local target mapping, package validation, and repository validation.",
        "",
        "## Classification Counts",
        "",
    ]
    for key in sorted(counts):
        lines.append(f"- `{key}`: {counts[key]}")
    lines.extend(
        [
            "",
            "## Training-Core And Adjacent Sources",
            "",
            "| classification | category | skill | path | score | local target |",
            "|---|---|---|---|---:|---|",
        ]
    )
    for record in audit["records"]:
        if record["classification"] not in {"training-core", "training-adjacent"}:
            continue
        lines.append(
            "| {classification} | {category} | {name} | `{source_path}` | {training_relevance_score} | {local_target} |".format(
                **record
            )
        )
    lines.extend(
        [
            "",
            "## Full Inventory",
            "",
            "| classification | category | skill | path | status |",
            "|---|---|---|---|---|",
        ]
    )
    for record in audit["records"]:
        lines.append(
            "| {classification} | {category} | {name} | `{source_path}` | {integration_status} |".format(
                **record
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-json", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--min-records", type=int, default=98)
    args = parser.parse_args()

    skills = json.loads(args.skills_json.read_text(encoding="utf-8"))
    audit = build_audit(skills, args.source_root, args.expected_commit)
    if audit["record_count"] < args.min_records:
        print(f"FAIL record_count {audit['record_count']} < {args.min_records}", file=sys.stderr)
        return 1
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(audit, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(audit, args.out_md)
    print(f"OK records={audit['record_count']} commit={audit['source_commit']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
