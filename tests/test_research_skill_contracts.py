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
    "research-rapid-test",
    "research-review-case",
    "research-slides",
    "research-synthesis",
    "research-theory",
    "research-writing",
}


class ResearchSkillContractTest(unittest.TestCase):
    def test_discovery_literature_synthesis_boundaries(self) -> None:
        discovery = (SKILLS / "paper-discovery/SKILL.md").read_text(encoding="utf-8")
        literature = (SKILLS / "research-literature/SKILL.md").read_text(
            encoding="utf-8"
        )
        note_template = (SKILLS / "research-literature/note-template.md").read_text(
            encoding="utf-8"
        )
        synthesis = (SKILLS / "research-synthesis/SKILL.md").read_text(encoding="utf-8")
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
            "exactly one Zotero collection",
            "zotero-collection.md",
            "$zotero-cli",
            "$paper-search-cli",
            "$smart-search-cli",
            "entire Zotero library",
            "persistent identifiers first",
            "Search coverage",
            "zotero_key",
            "closest_candidate",
            "metadata_status",
            "$research-literature",
        ):
            self.assertIn(marker, discovery)
        for marker in (
            "$paper-discovery",
            "One clean reader may take one paper or a small batch",
            "full-text read or explicitly blocked",
            "$research-synthesis",
        ):
            self.assertIn(marker, literature)
        self.assertNotIn("paper-search-cli", literature)
        self.assertNotIn("Search coverage", literature)
        for marker in (
            "Metadata status: verified | conflicting | unverified",
            "Access: full_pdf | partial_text | abstract_only",
            "the sample size, and the uncertainty",
            "`limitation` records quote the authors verbatim",
            "[null]",
            "[defect: <assumption|evaluation|mechanism|scope>, <observed|inferred>]",
            "[test] for R5:",
            "closest_candidate",
            "final closest-prior selection belongs to `$research-synthesis`",
        ):
            self.assertIn(marker, note_template)
        defect_record = next(
            line for line in note_template.splitlines() if line.startswith("R5 [defect")
        )
        self.assertIn("<anchor> — <basis>, <confidence>", defect_record)
        for marker in (
            "closest prior work",
            "exact overlap and differentiators",
            "paper IDs and record IDs",
            "$paper-discovery",
            "$research-literature",
        ):
            self.assertIn(marker, synthesis)
        self.assertIn("Evidence-backed open problems", synthesis)
        self.assertIn("not a novelty verdict", synthesis)
        self.assertIn("start without synthesis", synthesis)

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

    def test_experiment_response_contract_is_mode_free(self) -> None:
        text = (
            (SKILLS / "research-experiment" / "SKILL.md")
            .read_text(encoding="utf-8")
            .lower()
        )
        for marker in (
            "one compact run matrix",
            "no more than six stop/kill/relaunch/fallback rules",
            "one bounded claim contract",
            "fixed-wording mechanical transformation",
            "adds no experimental judgment",
            "minimum trust-bearing evidence",
        ):
            self.assertIn(marker, text)
        for heading in ("## direct", "## pack", "## deep", "## campaign"):
            self.assertNotIn(heading, text)

    def test_experiment_resources_are_reachable(self) -> None:
        root = SKILLS / "research-experiment"
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        for relative in ("assets/experiment-contract.md", "assets/result-template.md"):
            self.assertTrue((root / relative).is_file())
            self.assertIn(relative, text)


if __name__ == "__main__":
    unittest.main()
