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
    "research-idea-evaluation",
    "research-ideation",
    "research-literature",
    "research-rapid-test",
    "research-review-case",
    "research-slides",
    "research-synthesis",
    "research-theory",
    "research-writing",
}


class ResearchSkillContractTest(unittest.TestCase):
    def test_ideation_evaluation_handoff_preserves_owner_boundary(self) -> None:
        ideation = (SKILLS / "research-ideation/SKILL.md").read_text(encoding="utf-8")
        evaluation = (SKILLS / "research-idea-evaluation/SKILL.md").read_text(
            encoding="utf-8"
        )
        evaluation_policy = (
            SKILLS / "research-idea-evaluation/agents/openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("$research-idea-evaluation", ideation)
        self.assertIn("next_owner: research-idea-evaluation", ideation)
        self.assertIn("portfolio <idea-root>", ideation)
        self.assertNotIn("human_shortlist", ideation)
        self.assertNotIn("shortlist.md", ideation)
        self.assertIn("screening <idea-root>", evaluation)
        self.assertIn("attack-template.md", evaluation)
        self.assertIn("disable-model-invocation: true", evaluation)
        self.assertIn("allow_implicit_invocation: false", evaluation_policy)

    def test_ideation_evaluation_handoff_fields_match(self) -> None:
        generation = (
            (SKILLS / "research-ideation/SKILL.md").read_text(encoding="utf-8").lower()
        )
        evaluation = "\n".join(
            (SKILLS / "research-idea-evaluation" / name)
            .read_text(encoding="utf-8")
            .lower()
            for name in ("SKILL.md", "attack-template.md")
        )
        for marker in ("candidate", "falsification", "kill", "major uncertainty"):
            self.assertIn(marker, generation)
        for marker in ("candidate", "falsification", "closest prior", "method flaw"):
            self.assertIn(marker, evaluation)

    def test_discovery_literature_ideation_boundaries(self) -> None:
        discovery = (SKILLS / "paper-discovery/SKILL.md").read_text(encoding="utf-8")
        literature = (SKILLS / "research-literature/SKILL.md").read_text(
            encoding="utf-8"
        )
        note_template = (SKILLS / "research-literature/note-template.md").read_text(
            encoding="utf-8"
        )
        synthesis = (SKILLS / "research-synthesis/SKILL.md").read_text(encoding="utf-8")
        ideation = (SKILLS / "research-ideation/SKILL.md").read_text(encoding="utf-8")
        ideas_template = (SKILLS / "research-ideation/ideas-template.md").read_text(
            encoding="utf-8"
        )
        evaluation = (SKILLS / "research-idea-evaluation/SKILL.md").read_text(
            encoding="utf-8"
        )
        screening_template = (
            SKILLS / "research-idea-evaluation/screening-template.md"
        ).read_text(encoding="utf-8")
        shortlist_template = (
            SKILLS / "research-idea-evaluation/shortlist-template.md"
        ).read_text(encoding="utf-8")
        decision_template = (
            SKILLS / "research-idea-evaluation/decision-template.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Analyst: evidence-backed defects", note_template)
        self.assertNotIn("Successor work addressing it", note_template)
        self.assertNotIn("Still open:", note_template)
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
            "one clean subagent per paper",
            "full-text read or explicitly blocked",
            "$research-synthesis",
        ):
            self.assertIn(marker, literature)
        self.assertNotIn("paper-search-cli", literature)
        self.assertNotIn("Search coverage", literature)
        for marker in (
            "## Key results",
            "Zotero key:",
            "Metadata status: verified | conflicting | unverified",
            "Access: full_pdf | partial_text | abstract_only",
            "Sample size / seeds / uncertainty",
            "Evidence basis: text | figure | table | equation",
            "Confidence / caveat",
            "closest_candidate",
            "final closest-prior selection belongs to `$research-synthesis`",
        ):
            self.assertIn(marker, note_template)
        defect_fields = note_template.split("## Analyst: evidence-backed defects", 1)[
            1
        ].split("## Analyst: relation to target question", 1)[0]
        self.assertIn("Evidence basis:", defect_fields)
        self.assertIn("Confidence / caveat:", defect_fields)
        for marker in (
            "closest prior work",
            "exact overlap and differentiators",
            "paper IDs and note anchors",
            "$paper-discovery",
            "$research-literature",
        ):
            self.assertIn(marker, synthesis)
        self.assertIn("Evidence-backed open problems", synthesis)
        self.assertIn("not a novelty verdict", synthesis)
        self.assertIn("start without synthesis", synthesis)
        for input_mode in ("problem-first", "method-first", "dataset-first"):
            self.assertIn(input_mode, ideation)
        self.assertIn("stage: expand_complete", ideas_template)
        self.assertIn("next_owner: research-idea-evaluation", ideas_template)
        self.assertFalse((SKILLS / "research-ideation/shortlist-template.md").exists())
        self.assertIn("stage: screening_complete", screening_template)
        self.assertIn("advance | hold | reject", screening_template)
        self.assertIn("selected_candidate_ids", shortlist_template)
        self.assertIn("screening: screening.md", shortlist_template)
        self.assertIn("decision_recorded_by: human_confirmed", shortlist_template)
        self.assertIn("decision-template.md", evaluation)
        self.assertIn("stage: converge_complete", decision_template)
        self.assertIn("Experiment Brief", decision_template)
        self.assertIn("Do not invent exact performance targets", ideation)
        for removed in (
            "problem-checkpoint",
            "opportunity-board",
            "problem-decision",
            "h1_decision",
            "h2_decision",
        ):
            self.assertNotIn(removed, ideation.lower())

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

    def test_exact_research_invocation_policy_split(self) -> None:
        explicit = {"research-idea-evaluation"}
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
                if root.name in explicit:
                    self.assertIn("disable-model-invocation: true", skill)
                    self.assertIn("allow_implicit_invocation: false", projection)
                else:
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
