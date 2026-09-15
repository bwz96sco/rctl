#!/usr/bin/env python3
"""Behavioral tests for expand -> screen -> shortlist -> converge handoffs."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPO / "skills" / "research-idea-evaluation" / "scripts" / "validate-handoff.py"
)
EXPERIMENT_VALIDATOR = (
    REPO / "skills" / "research-experiment" / "scripts" / "validate-result.py"
)


IDEAS = """---
stage: expand_complete
target_question: "How should the system change?"
next_owner: research-idea-evaluation
---

# Idea portfolio

## C1: Problem-first route

- Mechanism: repair an observed failure.

## C2: Method-first route

- Mechanism: import a new control loop.

## C3: Dataset-first route

- Mechanism: use released interaction traces.

## C4: Mixed route

- Mechanism: combine the failure, loop, and traces.
"""


def screening(
    ids: tuple[str, ...] = ("C1", "C2", "C3", "C4"),
    *,
    signal: str = "advance",
) -> str:
    records = "\n\n".join(
        f"""## {candidate_id}: Screened route

- Closest-prior status: supplied prior inspected
- Surviving delta: bounded delta remains
- Asset feasibility: public data available
- Strongest concern: mechanism may not transfer
- Evidence: supplied ideas.md prior notes
- Screening signal: {signal}"""
        for candidate_id in ids
    )
    return f"""---
stage: screening_complete
portfolio: ideas.md
next_owner: human_shortlist
---

# Portfolio screening

{records}
"""


def shortlist(ids: str = "C1, C2, C3") -> str:
    return f"""---
stage: shortlist_complete
portfolio: ideas.md
screening: screening.md
selected_candidate_ids: [{ids}]
decision_recorded_by: human_confirmed
next_owner: research-idea-evaluation
---

# Human shortlist

## Human rationale

Keep these routes.
"""


def decision(
    *,
    status: str = "selected",
    selected: str = "C1",
    dispositions: tuple[str, ...] = ("C1", "C2", "C3"),
    briefs: tuple[str, ...] = ("C1",),
    next_owner: str | None = None,
) -> str:
    selected_ids = {item.strip() for item in selected.split(",") if item.strip()}
    rows = "\n".join(
        f"| {item} | {'selected' if item in selected_ids else 'rejected'} | reason |"
        for item in dispositions
    )
    brief_text = "\n".join(
        f"## Experiment Brief: {item}\n\n- Baseline: B0\n- Dataset: D0\n"
        for item in briefs
    )
    if next_owner is None:
        next_owner = "research-experiment" if status == "selected" else "none"
    return f"""---
stage: converge_complete
portfolio: ideas.md
shortlist: shortlist.md
decision_status: {status}
selected_candidate_ids: [{selected}]
next_owner: {next_owner}
---

# Idea evaluation decision

## Candidate Dispositions

| Candidate ID | Disposition | Reason |
| --- | --- | --- |
{rows}

{brief_text}
"""


def write_experiment(
    root: Path,
    *,
    origin_type="supplied",
    origin_id="existing-method",
    experiment_role="method_comparison",
    assessment="inconclusive",
    mechanism_tested="yes",
) -> None:
    root.mkdir(exist_ok=True)
    (root / "contract.md").write_text(
        f"""---
schema_version: 1
task_id: {root.name}
---
- Origin type: {origin_type}
- Origin ID: {origin_id}
- Experiment role: {experiment_role}
""",
        encoding="utf-8",
    )
    (root / "result.md").write_text(
        f"""---
schema_version: 1
task_id: {root.name}
contract_revision: 1
assessment: {assessment}
---
- Mechanism tested: {mechanism_tested}
- Supported claim: bounded by the frozen comparison
- Material amendments: none
- Actual run IDs: run-1
- Commands, configs, and code state: run-1/config.json
- Evidence references: run-1/metrics.json
- Failed or null runs: none
- Aggregation: single run
- Baseline relation: recorded in contract
- Comparability: comparable
- Deviations: none
- Claims not made: no broader claim
- Next action: stop
""",
        encoding="utf-8",
    )


class ResearchHandoffTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "ideas.md").write_text(IDEAS, encoding="utf-8")
        (self.root / "screening.md").write_text(screening(), encoding="utf-8")
        (self.root / "shortlist.md").write_text(shortlist(), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_validator(
        self,
        stage: str,
        root: Path | None = None,
        *extra: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), stage, str(root or self.root), *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def run_experiment_validator(
        self,
        root: Path,
        *extra: str,
        validator: Path = EXPERIMENT_VALIDATOR,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                "uv",
                "run",
                "--no-project",
                "--script",
                str(validator),
                str(root),
                *extra,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def write_attacks(self, *ids: str) -> None:
        attack_root = self.root / "attacks"
        attack_root.mkdir(exist_ok=True)
        for item in ids:
            (attack_root / f"{item}.md").write_text(f"# {item}\n", encoding="utf-8")

    def test_problem_method_dataset_and_mixed_candidates_need_no_checkpoint(
        self,
    ) -> None:
        result = self.run_validator("portfolio")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        for forbidden in ("problem-checkpoint.md", "synthesis.md", "readiness"):
            self.assertFalse((self.root / forbidden).exists())

    def test_portfolio_hands_full_slate_to_evaluation(self) -> None:
        (self.root / "ideas.md").write_text(
            IDEAS.replace("research-idea-evaluation", "human_shortlist"),
            encoding="utf-8",
        )
        result = self.run_validator("portfolio")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("next_owner must be research-idea-evaluation", result.stdout)

    def test_screening_covers_every_portfolio_candidate(self) -> None:
        result = self.run_validator("screening")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_screening_missing_candidate_is_rejected(self) -> None:
        (self.root / "screening.md").write_text(
            screening(("C1", "C2", "C3")), encoding="utf-8"
        )
        result = self.run_validator("screening")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("candidate coverage mismatch", result.stdout)
        self.assertIn("C4", result.stdout)

    def test_screening_duplicate_candidate_is_rejected(self) -> None:
        (self.root / "screening.md").write_text(
            screening(("C1", "C2", "C3", "C4", "C4")), encoding="utf-8"
        )
        result = self.run_validator("screening")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("duplicate candidate IDs", result.stdout)

    def test_screening_unknown_candidate_is_rejected(self) -> None:
        (self.root / "screening.md").write_text(
            screening(("C1", "C2", "C3", "C4", "C9")), encoding="utf-8"
        )
        result = self.run_validator("screening")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("candidate coverage mismatch", result.stdout)
        self.assertIn("C9", result.stdout)

    def test_invalid_screening_signal_is_rejected(self) -> None:
        (self.root / "screening.md").write_text(
            screening(signal="winner"), encoding="utf-8"
        )
        result = self.run_validator("screening")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("signal must be advance, hold, or reject", result.stdout)

    def test_screening_placeholder_evidence_is_rejected(self) -> None:
        text = screening().replace(
            "supplied ideas.md prior notes", "<paper IDs or artifact paths>", 1
        )
        (self.root / "screening.md").write_text(text, encoding="utf-8")
        result = self.run_validator("screening")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("has placeholder Evidence", result.stdout)

    def test_shortlist_requires_valid_screening(self) -> None:
        (self.root / "screening.md").unlink()
        result = self.run_validator("shortlist")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing screening.md", result.stdout)

    def test_shortlist_must_name_its_screening(self) -> None:
        text = shortlist().replace("screening: screening.md\n", "")
        (self.root / "shortlist.md").write_text(text, encoding="utf-8")
        result = self.run_validator("shortlist")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("screening must be", result.stdout)

    def test_explicit_shortlist_accepts_one_or_two_candidates(self) -> None:
        for ids in ("C1", "C1, C2"):
            with self.subTest(ids=ids):
                (self.root / "shortlist.md").write_text(
                    shortlist(ids), encoding="utf-8"
                )
                result = self.run_validator("shortlist")
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_shortlist_rejects_empty_duplicate_or_unconfirmed_selection(self) -> None:
        for text, error in (
            (shortlist(""), "at least one ID"),
            (shortlist("C1, C1"), "duplicate IDs"),
            (
                shortlist().replace("human_confirmed", "agent_inferred"),
                "human_confirmed",
            ),
        ):
            with self.subTest(error=error):
                (self.root / "shortlist.md").write_text(text, encoding="utf-8")
                result = self.run_validator("shortlist")
                self.assertNotEqual(0, result.returncode)
                self.assertIn(error, result.stdout)

    def test_shortlist_with_unknown_id_is_rejected(self) -> None:
        (self.root / "shortlist.md").write_text(
            shortlist("C1, C2, C9"), encoding="utf-8"
        )
        result = self.run_validator("shortlist")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("unknown candidate IDs", result.stdout)

    def test_explicit_human_selection_can_exceed_suggested_count(self) -> None:
        ideas = (
            IDEAS
            + """

## C5: Extra route

- Mechanism: test another route.

## C6: Another extra route

- Mechanism: test one more route.
"""
        )
        (self.root / "ideas.md").write_text(ideas, encoding="utf-8")
        (self.root / "screening.md").write_text(
            screening(("C1", "C2", "C3", "C4", "C5", "C6")), encoding="utf-8"
        )
        (self.root / "shortlist.md").write_text(
            shortlist("C1, C2, C3, C4, C5, C6"), encoding="utf-8"
        )
        result = self.run_validator("shortlist")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_empty_human_rationale_is_rejected(self) -> None:
        (self.root / "shortlist.md").write_text(
            shortlist().replace("Keep these routes.", ""), encoding="utf-8"
        )
        result = self.run_validator("shortlist")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Human rationale", result.stdout)

    def test_template_placeholder_is_not_human_rationale(self) -> None:
        (self.root / "shortlist.md").write_text(
            shortlist().replace("Keep these routes.", "<verbatim human wording>"),
            encoding="utf-8",
        )
        result = self.run_validator("shortlist")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Human rationale", result.stdout)

    def test_selected_decision_with_two_or_fewer_survivors_passes(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        (self.root / "decision.md").write_text(decision(), encoding="utf-8")
        result = self.run_validator("decision")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_single_candidate_can_handoff_to_pilot_or_formal_experiment(self) -> None:
        (self.root / "shortlist.md").write_text(shortlist("C1"), encoding="utf-8")
        self.write_attacks("C1")
        for owner in ("research-rapid-test", "research-experiment"):
            with self.subTest(owner=owner):
                (self.root / "decision.md").write_text(
                    decision(dispositions=("C1",), next_owner=owner), encoding="utf-8"
                )
                result = self.run_validator("decision")
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_decision_rejects_unknown_or_status_inconsistent_owner(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        for status, selected, briefs, owner in (
            ("selected", "C1", ("C1",), "research-writing"),
            ("selected", "C1", ("C1",), "none"),
            ("blocked", "", (), "research-rapid-test"),
            ("blocked", "", (), "research-experiment"),
        ):
            with self.subTest(status=status, owner=owner):
                (self.root / "decision.md").write_text(
                    decision(
                        status=status,
                        selected=selected,
                        briefs=briefs,
                        next_owner=owner,
                    ),
                    encoding="utf-8",
                )
                result = self.run_validator("decision")
                self.assertNotEqual(0, result.returncode)
                self.assertIn("next_owner", result.stdout)

    def test_rapid_handoff_still_requires_selected_brief_and_attack(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        path = self.root / "decision.md"
        path.write_text(
            decision(briefs=(), next_owner="research-rapid-test"), encoding="utf-8"
        )
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("briefs must cover", result.stdout)
        path.write_text(decision(next_owner="research-rapid-test"), encoding="utf-8")
        (self.root / "attacks/C1.md").unlink()
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("files must cover exactly", result.stdout)

    def test_blocked_decision_with_no_winner_passes(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        (self.root / "decision.md").write_text(
            decision(status="blocked", selected="", briefs=()), encoding="utf-8"
        )
        result = self.run_validator("decision")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_unshortlisted_attack_is_rejected(self) -> None:
        self.write_attacks("C1", "C2", "C3", "C4")
        (self.root / "decision.md").write_text(decision(), encoding="utf-8")
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("files must cover exactly the shortlist", result.stdout)

    def test_missing_disposition_is_rejected(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        (self.root / "decision.md").write_text(
            decision(dispositions=("C1", "C2")), encoding="utf-8"
        )
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("dispositions mismatch shortlist", result.stdout)

    def test_selected_id_must_have_selected_disposition(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        text = decision().replace("| C1 | selected |", "| C1 | rejected |")
        (self.root / "decision.md").write_text(text, encoding="utf-8")
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("disagree with Candidate Dispositions", result.stdout)

    def test_more_than_two_selected_is_rejected(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        (self.root / "decision.md").write_text(
            decision(selected="C1, C2, C3", briefs=("C1", "C2", "C3")),
            encoding="utf-8",
        )
        result = self.run_validator("decision")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("at most two", result.stdout)

    def test_method_experiment_requires_selected_candidate(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        decision_path = self.root / "decision.md"
        decision_path.write_text(decision(), encoding="utf-8")
        experiment = self.root / "experiment"
        write_experiment(experiment, origin_type="candidate", origin_id="C2")
        result = self.run_experiment_validator(
            experiment, "--decision", str(decision_path)
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("was not selected", result.stdout)

    def test_selected_candidate_and_native_yaml_comments_are_supported(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        decision_path = self.root / "decision.md"
        decision_path.write_text(decision(), encoding="utf-8")
        experiment = self.root / "experiment"
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        path = experiment / "result.md"
        path.write_text(
            path.read_text()
            .replace("task_id: experiment", "task_id: experiment # Native YAML comment")
            .replace(
                "contract_revision: 1", "contract_revision: 1 # Governing revision"
            )
            .replace(
                "bounded by the frozen comparison", "gain < 0.01; no broader claim"
            )
        )
        result = self.run_experiment_validator(
            experiment, "--decision", str(decision_path)
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_formal_followup_preserves_original_rapid_selection(self) -> None:
        (self.root / "shortlist.md").write_text(shortlist("C1"), encoding="utf-8")
        self.write_attacks("C1")
        decision_path = self.root / "decision.md"
        original = decision(dispositions=("C1",), next_owner="research-rapid-test")
        decision_path.write_text(original, encoding="utf-8")
        experiment = self.root / "formal-followup"
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        result = self.run_experiment_validator(
            experiment, "--decision", str(decision_path)
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(original, decision_path.read_text(encoding="utf-8"))
        write_experiment(experiment, origin_type="candidate", origin_id="C2")
        result = self.run_experiment_validator(
            experiment, "--decision", str(decision_path)
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("was not selected", result.stdout)

    def test_validators_work_from_nonstandard_install_directory(self) -> None:
        installed = self.root / "custom skill packages"
        for name in ("research-experiment", "research-idea-evaluation"):
            shutil.copytree(REPO / "skills" / name, installed / name)
        self.write_attacks("C1", "C2", "C3")
        decision_path = self.root / "decision.md"
        decision_path.write_text(decision(), encoding="utf-8")
        experiment = self.root / "relocated-experiment"
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        result = self.run_experiment_validator(
            experiment,
            "--decision",
            str(decision_path),
            validator=installed / "research-experiment/scripts/validate-result.py",
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_standalone_install_only_needs_peer_validator_for_candidate_origin(
        self,
    ) -> None:
        installed = self.root / "standalone" / "research-experiment"
        shutil.copytree(REPO / "skills/research-experiment", installed)
        validator = installed / "scripts/validate-result.py"
        experiment = self.root / "standalone-experiment"
        for origin, role in (
            ("supplied", "method_comparison"),
            ("problem", "problem_validation"),
        ):
            with self.subTest(origin=origin):
                write_experiment(experiment, origin_type=origin, experiment_role=role)
                result = self.run_experiment_validator(experiment, validator=validator)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.write_attacks("C1", "C2", "C3")
        decision_path = self.root / "decision.md"
        decision_path.write_text(decision(), encoding="utf-8")
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        result = self.run_experiment_validator(
            experiment,
            "--decision",
            str(decision_path),
            validator=validator,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "install research-idea-evaluation beside research-experiment", result.stdout
        )

    def test_method_experiment_rejects_invalid_decision_contract(self) -> None:
        self.write_attacks("C1", "C2", "C3")
        decision_path = self.root / "decision.md"
        decision_path.write_text(
            decision().replace("| C1 | selected |", "| C1 | rejected |"),
            encoding="utf-8",
        )
        experiment = self.root / "experiment"
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        result = self.run_experiment_validator(
            experiment, "--decision", str(decision_path)
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("disagree with Candidate Dispositions", result.stdout)

    def test_problem_validation_is_independent(self) -> None:
        experiment = self.root / "problem-experiment"
        write_experiment(
            experiment,
            origin_type="problem",
            origin_id="long-horizon-forgetting",
            experiment_role="problem_validation",
            assessment="not_supported",
        )
        result = self.run_experiment_validator(experiment)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_supplied_method_comparison_needs_no_idea_decision(self) -> None:
        experiment = self.root / "supplied-experiment"
        write_experiment(experiment, mechanism_tested="not_applicable")
        result = self.run_experiment_validator(experiment)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_result_requires_comparability_evidence(self) -> None:
        experiment = self.root / "incomplete-closeout"
        write_experiment(experiment)
        result_path = experiment / "result.md"
        result_path.write_text(
            result_path.read_text().replace(
                "- Comparability: comparable", "- Comparability:"
            )
        )
        result = self.run_experiment_validator(experiment)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("missing nonempty comparability", result.stdout)

    def test_unfilled_template_and_mismatched_identity_are_rejected(self) -> None:
        experiment = self.root / "draft"
        write_experiment(experiment, origin_id="<origin-id>")
        result = self.run_experiment_validator(experiment)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Origin ID", result.stdout)
        write_experiment(experiment)
        path = experiment / "result.md"
        path.write_text(
            path.read_text().replace("task_id: draft", "task_id: another-task")
        )
        result = self.run_experiment_validator(experiment)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("task_id differs", result.stdout)


if __name__ == "__main__":
    unittest.main()
