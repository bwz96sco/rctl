import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from rctl.records import Task

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def project(tmp_path):
    return tmp_path


@pytest.fixture
def task(project):
    path = project / "tasks/retained-comparison"
    path.mkdir(parents=True)
    (path / "contract.md").write_bytes(
        (REPO / "examples/retained-comparison/contract.md").read_bytes()
    )
    return Task(project, path)


@pytest.fixture
def cli(project):
    def run(*args, root=True, env=None, expected=0):
        environment = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("RCTL_")
        }
        environment.update(env or {})
        command = [sys.executable, "-m", "rctl", "--format", "json"]
        if root:
            command += ["--root", str(project)]
        result = subprocess.run(
            command + list(args),
            cwd=project,
            env=environment,
            capture_output=True,
            text=True,
        )
        assert result.returncode == expected, result.stderr + result.stdout
        response = json.loads(result.stdout)
        assert set(response) == {"schema_version", "ok", "data", "error", "warnings"}
        assert isinstance(response["data"], dict)
        assert isinstance(response["warnings"], list)
        assert response["ok"] == (expected == 0)
        if expected:
            assert response["error"]["code"] in result.stderr
        else:
            assert response["error"] is None
        return response

    return run
