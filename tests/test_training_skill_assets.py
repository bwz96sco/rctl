"""Moved training resources must execute without the private source repository."""

import shutil
import subprocess
import sys

import pytest

from rctl.documents import resource_directory


@pytest.mark.parametrize(
    "name,validator,fixture,flags",
    [
        (
            "experiment-adapter-builder",
            "validate_adapter_skill.py",
            "demo-experiment-workflow",
            [],
        ),
        (
            "model-training-workflow",
            "validate_model_training_pack.py",
            "lora-wandb-tiny-overfit",
            [],
        ),
        (
            "model-training-workflow",
            "validate_model_training_pack.py",
            "training-collapse-diagnostic",
            ["--strict-diagnostics"],
        ),
    ],
)
def test_packaged_validator_accepts_fixture_and_rejects_missing_evidence(
    tmp_path, name, validator, fixture, flags
):
    root = resource_directory("skills") / name
    target = tmp_path / fixture
    shutil.copytree(root / "fixtures" / fixture, target)
    command = [sys.executable, str(root / "scripts" / validator), str(target), *flags]
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr

    missing = (
        "references/runners.md"
        if name == "experiment-adapter-builder"
        else "training_execution_log.md"
    )
    (target / missing).unlink()
    result = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 1
    assert f"missing required file: {missing}" in result.stdout + result.stderr
