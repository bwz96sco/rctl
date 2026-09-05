"""Run a built wheel in an isolated environment and non-Git project.

Usage: uv run scripts/smoke_package.py dist/rctl-0.1.0a1-py3-none-any.whl
"""

import json
import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    wheel = Path(sys.argv[1]).resolve()
    repo = Path(__file__).resolve().parents[1]
    work = repo / ".work"
    work.mkdir(exist_ok=True)
    results = []
    with tempfile.TemporaryDirectory(prefix="wheel-smoke-", dir=work) as directory:
        directory = Path(directory)
        environment = {
            key: value
            for key, value in os.environ.items()
            if key not in {"PYTHONPATH", "VIRTUAL_ENV"} and not key.startswith("RCTL_")
        }
        venv = directory / "venv"
        python = venv / "bin/python"
        for command in (
            ["uv", "venv", "--python", sys.executable, str(venv)],
            ["uv", "pip", "install", "--offline", "--python", str(python), str(wheel)],
        ):
            subprocess.run(
                command, env=environment, check=True, capture_output=True, text=True
            )
        project = directory / "project"
        project.mkdir()
        executable = venv / "bin/rctl"

        def cli(*args, expected=0):
            result = subprocess.run(
                [str(executable), "--format", "json", *args],
                cwd=project,
                env=environment,
                capture_output=True,
                text=True,
            )
            assert result.returncode == expected, result.stdout + result.stderr
            response = json.loads(result.stdout)
            results.append(
                {
                    "argv": list(args),
                    "exit_code": result.returncode,
                    "response": response,
                }
            )
            return response

        cli(
            "task",
            "new",
            "tasks/retained-comparison",
            "--kind",
            "analysis",
            "--title",
            "Installed wheel smoke",
        )
        cli("begin", "tasks/retained-comparison", expected=2)
        task = project / "tasks/retained-comparison"
        contract = (repo / "examples/retained-comparison/contract.md").read_bytes()
        (task / "contract.md").write_bytes(contract)
        cli("contract", "check", "tasks/retained-comparison")
        cli("begin", "tasks/retained-comparison")
        record = (task / ".rctl/record.json").read_bytes()
        (project / "handoff.md").write_text("Next action: inspect retained evidence.\n")
        cli("checkpoint", "tasks/retained-comparison", "--file", "handoff.md")
        assert (task / ".rctl/record.json").read_bytes() == record
        reminder = cli("context", "tasks/retained-comparison")["data"]["context"]
        assert "Next action: inspect retained evidence." in reminder
        (task / "contract.md").write_bytes(contract + b"\nBudget clarification.\n")
        assert cli("status", "tasks/retained-comparison")["data"]["contract_drift"]
        cli(
            "amend",
            "tasks/retained-comparison",
            "--reason",
            "Clarify the existing budget",
        )
        assert (
            cli("status", "tasks/retained-comparison")["data"]["contract_revision"] == 2
        )
        assert not (project / ".git").exists()
        resource_check = subprocess.run(
            [
                str(python),
                "-c",
                (
                    "import json, rctl; from pathlib import Path; "
                    "from importlib.resources import files; "
                    "from importlib.metadata import version; "
                    f"assert Path(rctl.__file__).is_relative_to({str(venv)!r}); "
                    "assert files('rctl').joinpath('schemas/contract.schema.json').is_file(); "
                    "assert files('rctl').joinpath('templates/contract.md').is_file(); "
                    "print(json.dumps({name: version(name) for name in ['rctl', 'PyYAML', 'jsonschema']}))"
                ),
            ],
            cwd=project,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )
        print(
            json.dumps(
                {
                    "ok": True,
                    "python": platform.python_version(),
                    "platform": platform.platform(),
                    "wheel": wheel.name,
                    "versions": json.loads(resource_check.stdout),
                    "checks": results,
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
