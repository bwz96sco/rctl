"""Run a built wheel in an isolated environment and non-Git project.

Usage: uv run scripts/smoke_package.py dist/rctl-0.2.0-py3-none-any.whl [--skills-root PATH]
"""

import argparse
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--skills-root", type=Path)
    args = parser.parse_args()
    wheel = args.wheel.resolve()
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

        cli("init", "--vault", "note/main", "--codex")
        assert (
            project / ".agents/skills/research-task/references/workspace.md"
        ).is_file()
        assert (project / "note/main/_templates/experiment-note.md").is_file()
        custom = project / "research/PROGRAM.md"
        custom.write_text("Preserved installed-wheel customization.\n")
        before = {p: p.read_bytes() for p in project.rglob("*") if p.is_file()}
        assert cli("init", "--codex")["data"]["created"] == []
        assert before == {p: p.read_bytes() for p in project.rglob("*") if p.is_file()}
        shared_record = None
        if args.skills_root:
            from smoke_shared_skills import walkthrough

            shared_record = walkthrough(
                cli, project, repo, args.skills_root.resolve(), python
            )
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
        shutil.copytree(repo / "examples/retained-comparison", task, dirs_exist_ok=True)
        (task / "contract.md").write_bytes(contract)
        cli("contract", "check", "tasks/retained-comparison")
        cli("begin", "tasks/retained-comparison")
        record = (task / ".rctl/record.json").read_bytes()
        (project / "handoff.md").write_text("Next action: inspect retained evidence.\n")
        cli("checkpoint", "tasks/retained-comparison", "--file", "handoff.md")
        assert (task / ".rctl/record.json").read_bytes() == record
        reminder = cli("context", "tasks/retained-comparison")["data"]["context"]
        assert "Next action: inspect retained evidence." in reminder
        hooks = json.loads((project / ".codex/hooks.json").read_text())
        hook_responses = {}
        for event, handlers in hooks["hooks"].items():
            hook_result = subprocess.run(
                shlex.split(handlers[0]["hooks"][0]["command"]),
                input=json.dumps({"hook_event_name": event, "cwd": str(project)}),
                cwd=project,
                env={**environment, "RCTL_TASK_PATH": "tasks/retained-comparison"},
                capture_output=True,
                text=True,
                check=True,
            )
            hook_response = json.loads(hook_result.stdout)
            assert "active" in hook_response["hookSpecificOutput"]["additionalContext"]
            hook_responses[event] = hook_response
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
        (task / "result.md").write_text(
            (task / "result.md")
            .read_text()
            .replace("contract_revision: 1", "contract_revision: 2")
        )
        reviews = json.loads((task / "reviews.json").read_text())
        reviews["contract_revision"] = 2
        (task / "reviews.json").write_text(json.dumps(reviews))
        cli("verify", "tasks/retained-comparison", expected=5)
        cli("close", "tasks/retained-comparison", expected=5)
        cli(
            "verify",
            "tasks/retained-comparison",
            "--reviews",
            "tasks/retained-comparison/reviews.json",
        )
        closure = cli("close", "tasks/retained-comparison")["data"]["closure"]
        assert closure["assessment"] == "not_supported"
        assert cli("status", "tasks/retained-comparison")["data"]["phase"] == "closed"
        cli(
            "reopen",
            "tasks/retained-comparison",
            "--reason",
            "Recheck retained evidence",
        )
        cli("close", "tasks/retained-comparison", expected=4)
        cli(
            "verify",
            "tasks/retained-comparison",
            "--reviews",
            "tasks/retained-comparison/reviews.json",
        )
        cli("close", "tasks/retained-comparison")
        assert cli("context", "tasks/retained-comparison")["data"]["phase"] == "closed"
        assert not (project / ".git").exists()
        cli("integration", "codex", "export", "host-bundle")
        assert (project / "host-bundle/research-task/SKILL.md").is_file()
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
        record = json.loads((task / ".rctl/record.json").read_text())
        execution_logs = {}
        reports = record["verifications"] + (
            shared_record["verifications"] if shared_record else []
        )
        for report in reports:
            for check in report["checks"]:
                if check.get("execution"):
                    for key in ("stdout_ref", "stderr_ref"):
                        ref = check["execution"][key]
                        execution_logs[ref] = (project / ref).read_text()
        print(
            json.dumps(
                {
                    "ok": True,
                    "python": platform.python_version(),
                    "platform": platform.platform(),
                    "wheel": wheel.name,
                    "versions": json.loads(resource_check.stdout),
                    "checks": results,
                    "shared_experiment_record": shared_record,
                    "generated_hook_adapter_responses": hook_responses,
                    "execution_logs": execution_logs,
                },
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
