#!/usr/bin/env python3
"""Behavioral tests for the research-experiment result validator."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPERIMENT_VALIDATOR = (
    REPO / "skills" / "research-experiment" / "scripts" / "validate-result.py"
)


def write_experiment(
    root: Path,
    *,
    origin_type="supplied",
    origin_id="existing-method",
    experiment_role="method_comparison",
    assessment="inconclusive",
    mechanism_tested="yes",
) -> None:
    root.mkdir(parents=True, exist_ok=True)
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


class ExperimentResultTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_experiment_validator(
        self,
        root: Path,
        validator: Path = EXPERIMENT_VALIDATOR,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["uv", "run", "--no-project", "--script", str(validator), str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_native_yaml_comments_are_supported(self) -> None:
        experiment = self.root / "experiment"
        write_experiment(experiment)
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
        result = self.run_experiment_validator(experiment)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_standalone_install_needs_no_peer_package(self) -> None:
        installed = self.root / "custom skill packages" / "research-experiment"
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

    def test_retired_candidate_origin_is_rejected(self) -> None:
        experiment = self.root / "candidate-experiment"
        write_experiment(experiment, origin_type="candidate", origin_id="C1")
        result = self.run_experiment_validator(experiment)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Origin type must be one of", result.stdout)

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

    def test_supplied_method_comparison_passes(self) -> None:
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
