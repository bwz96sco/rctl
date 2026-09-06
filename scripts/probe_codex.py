"""Launch disposable real-host delivery probes with reviewed rctl hooks.

uv run scripts/probe_codex.py inline|project|none
Runs asynchronously from the agent's terminal tool; stdout reports a compact result.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from rctl.integration import export_codex, inline_arguments
from rctl.records import Task


def main():
    mode = sys.argv[1]
    if mode not in {"inline", "project", "none"}:
        raise SystemExit("Expected inline, project, or none")
    repo = Path(__file__).resolve().parents[1]
    root = repo / ".work" / f"host-{mode}"
    root.mkdir(parents=True, exist_ok=False)
    evidence = repo / "docs/evidence/host-probes" / mode
    evidence.mkdir(parents=True, exist_ok=False)
    task_path = root / "tasks/retained-comparison"
    shutil.copytree(repo / "examples/retained-comparison", task_path)
    task = Task(root, task_path)
    task.begin()
    task.file("state.md").write_text(
        "Next action: inspect retained baseline B0 and candidate C1 before interpretation.\n"
    )
    export_codex(root, "bundle")
    shutil.copytree(
        root / "bundle/research-task", root / ".agents/skills/research-task"
    )
    hooks = json.loads((root / "bundle/hooks.json").read_text())
    command = [
        "codex",
        "-a",
        "never",
        "exec",
        "--ignore-user-config",
        "--disable",
        "plugins",
        "--disable",
        "apps",
        "--skip-git-repo-check",
        "--ephemeral",
        "--sandbox",
        "workspace-write",
        "--cd",
        str(root),
        "--json",
        "--color",
        "never",
        "--output-last-message",
        str(evidence / "final.txt"),
    ]
    if mode != "none":
        command += ["--enable", "hooks", "--dangerously-bypass-hook-trust"]
        if mode == "inline":
            command += inline_arguments(hooks)
        else:
            (root / ".codex").mkdir()
            shutil.copyfile(root / "bundle/hooks.json", root / ".codex/hooks.json")
            command += ["-c", f'projects.{json.dumps(str(root))}.trust_level="trusted"']
    else:
        command += ["--disable", "hooks"]
    command += ["-"]
    env = dict(os.environ)
    env.update(
        RCTL_PROJECT_ROOT=str(root),
        RCTL_TASK_PATH="tasks/retained-comparison",
        RCTL_HOOK_LOG="hook-receipts.jsonl",
    )
    prompt = "This is a bounded reminder-delivery probe. Before any tool use, report the task identity, phase, and next action supplied by an rctl hook reminder in your context. If none was delivered, reply NO_RCTL_REMINDER. Do not inspect files, use tools, or perform the research task."
    (evidence / "prompt.txt").write_text(prompt)
    version = subprocess.check_output(["codex", "--version"], text=True).strip()
    (evidence / "launch.json").write_text(
        json.dumps(
            {
                "argv": command,
                "cwd": str(root),
                "host_version": version,
                "environment_overrides": {
                    k: env[k]
                    for k in ("RCTL_PROJECT_ROOT", "RCTL_TASK_PATH", "RCTL_HOOK_LOG")
                },
                "trust_scope": "Reviewed generated hooks; invocation-only hook trust; no shared config modified.",
            },
            indent=2,
        )
    )
    with (
        (evidence / "events.jsonl").open("w") as out,
        (evidence / "stderr.txt").open("w") as err,
    ):
        process = subprocess.run(
            command, input=prompt, text=True, cwd=root, env=env, stdout=out, stderr=err
        )
    receipts = root / "hook-receipts.jsonl"
    if receipts.exists():
        shutil.copyfile(receipts, evidence / "receipts.jsonl")
    summary = {
        "mode": mode,
        "exit_code": process.returncode,
        "receipt_count": len(receipts.read_text().splitlines())
        if receipts.exists()
        else 0,
        "final": (evidence / "final.txt").read_text()
        if (evidence / "final.txt").exists()
        else None,
    }
    (evidence / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
