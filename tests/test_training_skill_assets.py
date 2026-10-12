"""Consolidated experiment helpers retain earlier formats and bounded checks."""

import shutil
import subprocess
import sys

import pytest

from rctl.documents import resource_directory


@pytest.mark.parametrize(
    "validator,fixture,flags",
    [
        (
            "validate-adapter.py",
            "project-adapter",
            [],
        ),
        (
            "validate-training.py",
            "lora-wandb-tiny-overfit",
            [],
        ),
        (
            "validate-training.py",
            "training-collapse-diagnostic",
            ["--strict-diagnostics"],
        ),
    ],
)
def test_packaged_validator_accepts_fixture_and_rejects_missing_evidence(
    tmp_path, validator, fixture, flags
):
    root = resource_directory("skills") / "research-experiment"
    target = tmp_path / fixture
    shutil.copytree(root / "fixtures" / fixture, target)
    entrypoint = target / "entrypoint.md"
    if entrypoint.is_file():
        entrypoint.rename(target / "SKILL.md")
    command = [sys.executable, str(root / "scripts" / validator), str(target), *flags]
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr

    missing = (
        "references/runners.md"
        if validator == "validate-adapter.py"
        else "model_training_handoff.md"
    )
    (target / missing).unlink()
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 1
    message = result.stdout + result.stderr
    if validator == "validate-adapter.py":
        assert f"references missing file: {missing}" in message
    else:
        assert f"missing required file: {missing}" in message


def test_adapter_reuses_project_documents_without_fixed_reference_tree(tmp_path):
    skill = resource_directory("skills") / "research-experiment"
    target = tmp_path / ".agents/skills/demo-experiment-workflow"
    target.mkdir(parents=True)
    (tmp_path / "README.md").write_text(
        "Fixture command: uv run python train.py from the project root. "
        "Outputs: runs/. Source: this supplied synthetic project protocol.\n"
    )
    manifest = tmp_path / "run-manifest.md"
    manifest.write_text("Fixture project-owned run record format.\n")
    (target / "SKILL.md").write_text(
        "---\nname: demo-experiment-workflow\n"
        "description: Run the supplied demo project.\n---\n\n"
        "Use [project commands and sources](../../../README.md). "
        "Retain outputs using the [project manifest](../../../run-manifest.md).\n"
    )
    command = [
        sys.executable,
        str(skill / "scripts/validate-adapter.py"),
        str(target),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not (target / "references").exists()
    assert not (target / "templates").exists()

    manifest.unlink()
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 1
    assert "references missing file: ../../../run-manifest.md" in result.stderr

    # A missing description cannot consume the next frontmatter field as its value.
    (target / "SKILL.md").write_text(
        "---\nname: demo-experiment-workflow\ndescription:\nlicense: MIT\n---\n"
        "Use the supplied project command.\n"
    )
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 1
    assert "missing nonempty description" in result.stderr


def test_training_summary_reuses_run_records_without_a_six_file_pack(tmp_path):
    skill = resource_directory("skills") / "research-experiment"
    summary = tmp_path / "model_training_handoff.md"
    text = """# Training evidence

## verdict
Continue within the existing allowance.
## strongest_evidence
The supplied fixture log records finite loss; no generalization claim.
## claims_supported
The reported fixture run reached its declared step count.
## claims_blocked
Model quality is unassessed.
## next_action
Inspect retained predictions against the task's evaluator.
## run_manifest
manifest_path: runs/manifest.md
## raw_artifact_paths
runs/log.txt and runs/predictions.json
## status
Recorded completed; scientific validity unassessed.
"""
    summary.write_text(text)
    command = [
        sys.executable,
        str(skill / "scripts/validate-training.py"),
        str(tmp_path),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "model_training_handoff.md"
    ]

    summary.write_text(text.replace("manifest_path: runs/manifest.md", ""))
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 1
    assert "missing completed run_manifest" in result.stdout

    summary.write_text(text)
    result = subprocess.run(
        command + ["--strict-diagnostics"], capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "missing required file: training_diagnostic_report.md" in result.stdout
