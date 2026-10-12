#!/usr/bin/env python3
"""Static regression tests for repaired research workflow boundaries."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
SKILLS = REPO / "skills"
ACTIVE_RESEARCH_SKILLS = {
    "research-experiment",
    "research-figure",
    "research-literature",
    "research-slides",
    "research-writing",
}


class ResearchSkillContractTest(unittest.TestCase):
    def test_paper_records_retain_the_citable_evidence_format(self) -> None:
        note_template = (SKILLS / "research-literature/note-template.md").read_text(
            encoding="utf-8"
        )
        for removed in (
            "## Overview",
            "## Field map and gap",
            "## Method",
            "## Analyst: reflection",
            "Zotero key:",
            "Successor work addressing it",
        ):
            self.assertNotIn(removed, note_template)
        for marker in (
            "Metadata status: verified | conflicting | unverified",
            "Access: full_pdf | partial_text | abstract_only",
            "the sample size, and the uncertainty",
            "`limitation` records quote the authors verbatim",
            "[null]",
            "[defect: <assumption|evaluation|mechanism|scope>, <observed|inferred>]",
            "[test] for R5:",
            "closest_candidate",
        ):
            self.assertIn(marker, note_template)
        defect_record = next(
            line for line in note_template.splitlines() if line.startswith("R5 [defect")
        )
        self.assertIn("<anchor> — <basis>, <confidence>", defect_record)

    def test_consolidated_entrypoints_and_routes_are_retired(self) -> None:
        retired = (
            "experiment-adapter-builder",
            "model-training-workflow",
            "research-rapid-test",
            "research-synthesis",
            "research-theory",
            "research-review-case",
        )
        for name in retired:
            self.assertFalse((SKILLS / name).exists())
        names = "(?:" + "|".join(map(re.escape, retired)) + ")"
        routes = re.compile(rf"\${names}\b|skills/{names}(?:/|\b)|`{names}`")
        for root in (SKILLS, REPO / "templates"):
            for path in root.rglob("*"):
                if path.suffix in {".md", ".yaml"}:
                    self.assertIsNone(routes.search(path.read_text()), path)

    def test_retired_quest_packages_and_references_are_absent(self) -> None:
        retired_pattern = re.compile(
            r"(?i)(?:\bresearch-quest-admin\b|(?<![a-z0-9])_quest(?:/|\b)|\bquest\b)"
        )
        self.assertFalse((SKILLS / "research-quest").exists())
        self.assertFalse((SKILLS / "research-quest-admin").exists())
        for skill_name in ACTIVE_RESEARCH_SKILLS:
            with self.subTest(skill=skill_name):
                skill_root = SKILLS / skill_name
                for path in skill_root.rglob("*"):
                    relative_path = path.relative_to(skill_root)
                    self.assertIsNone(retired_pattern.search(relative_path.as_posix()))
                    if path.is_file():
                        text = path.read_text(encoding="utf-8", errors="ignore")
                        self.assertIsNone(retired_pattern.search(text))

    def test_retired_ideation_packages_and_routes_are_absent(self) -> None:
        retired = ("research-ideation", "research-question", "research-idea-evaluation")
        retired_pattern = re.compile("|".join(map(re.escape, retired)))
        for name in retired:
            self.assertFalse((SKILLS / name).exists())
        for skill_name in ACTIVE_RESEARCH_SKILLS | {"research-task"}:
            with self.subTest(skill=skill_name):
                for path in (SKILLS / skill_name).rglob("*"):
                    if path.is_file():
                        text = path.read_text(encoding="utf-8", errors="ignore")
                        self.assertIsNone(retired_pattern.search(text), path)

    def test_research_skills_allow_implicit_invocation(self) -> None:
        roots = sorted(
            path.parent
            for path in SKILLS.glob("research-*/SKILL.md")
            if path.parent.name != "research-task"
        )
        self.assertEqual(ACTIVE_RESEARCH_SKILLS, {root.name for root in roots})
        for root in roots:
            with self.subTest(skill=root.name):
                skill = (root / "SKILL.md").read_text(encoding="utf-8")
                projection = (root / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertNotIn("disable-model-invocation: true", skill)
                self.assertTrue(
                    yaml.safe_load(projection)
                    .get("policy", {})
                    .get("allow_implicit_invocation", True)
                )

    def test_experiment_resources_are_reachable(self) -> None:
        root = SKILLS / "research-experiment"
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        for relative in ("assets/experiment-contract.md", "assets/result-template.md"):
            self.assertTrue((root / relative).is_file())
            self.assertIn(relative, text)


if __name__ == "__main__":
    unittest.main()
