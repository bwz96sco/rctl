"""Run one actual fresh host session for the frozen release-analysis task."""

import json
import os
import subprocess
import sys
from pathlib import Path

from rctl.integration import inline_arguments


def main():
    stage = sys.argv[1]
    if stage not in {"first", "second"}:
        raise SystemExit("Expected first or second")
    repo = Path(__file__).resolve().parents[1]
    root = repo / ".work/release-task"
    evidence = repo / "docs/evidence/release-sessions" / stage
    evidence.mkdir(parents=True, exist_ok=False)
    hooks = json.loads((root / "bundle/hooks.json").read_text())
    executable = repo / ".work/release-venv/bin/rctl"
    common = f"""Use $research-task from .agents/skills/research-task/SKILL.md for the selected task. The working root is {root}. The installed CLI is {executable}; use this exact executable for all rctl operations. Read the governing task contract, optional handoff, and status. Work only inside this root and the task's frozen budget. This is an actual analysis of retained real-host delivery observations, not a request to implement or change rctl. Use uv for Python file runs; no network or new host probes. Do not delegate or start more agents. Preserve raw input evidence, contract, and the supplied independent checker. Follow the current contract revision.
"""
    if stage == "first":
        prompt = (
            common
            + """Perform the initial retained-evidence analysis. Inspect the actual launch arguments, receipts, host event streams, and final model outputs. Implement task-local analyze.py and derive evidence/analysis.json according to the frozen contract; use your own analysis implementation rather than importing the independent checker. Save an accurate task state.md using rctl checkpoint with concrete observed progress and the next action for a fresh session. Pause with the task active. Leave result.md, reviews.json, verification, and closeout for the next session. In your final response give the saved handoff and what remains unresolved; do not claim closure.
"""
        )
    else:
        prompt = (
            "Before any tool call, state the concrete progress and next action supplied by the rctl hook handoff in your context, or state that no handoff was delivered.\n"
            + common
            + """Continue the existing analysis from the delivered handoff and source files. Independently inspect the cited raw evidence and the derived analysis; write the current-revision result.md and evidence-based reviews.json. Run the declared verification and inspect its outcome. Close only when the rctl guard succeeds, otherwise leave the precise unresolved state. Keep the final response bounded to the actual finding and verification. Do not amend the contract or expand the comparison merely to obtain a favorable conclusion.
"""
        )
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
        "--enable",
        "hooks",
        "--skip-git-repo-check",
        "--ephemeral",
        "--sandbox",
        "workspace-write",
        "--dangerously-bypass-hook-trust",
        *inline_arguments(hooks),
        "--cd",
        str(root),
        "--json",
        "--color",
        "never",
        "--output-last-message",
        str(evidence / "final.txt"),
        "-",
    ]
    env = dict(os.environ)
    env.update(
        RCTL_PROJECT_ROOT=str(root),
        RCTL_TASK_PATH="tasks/hook-loading-compatibility",
        RCTL_HOOK_LOG=f"receipts-{stage}.jsonl",
    )
    (evidence / "prompt.txt").write_text(prompt)
    (evidence / "launch.json").write_text(
        json.dumps(
            {
                "argv": command,
                "cwd": str(root),
                "host_version": subprocess.check_output(
                    ["codex", "--version"], text=True
                ).strip(),
                "environment_overrides": {
                    k: env[k]
                    for k in ("RCTL_PROJECT_ROOT", "RCTL_TASK_PATH", "RCTL_HOOK_LOG")
                },
                "trust_scope": "Reviewed exported hooks; invocation-only trust; workspace-write; user config/apps/plugins disabled.",
            },
            indent=2,
        )
    )
    with (
        (evidence / "events.jsonl").open("w") as out,
        (evidence / "stderr.txt").open("w") as err,
    ):
        result = subprocess.run(
            command, input=prompt, text=True, cwd=root, env=env, stdout=out, stderr=err
        )
    for source, destination in (
        (root / f"receipts-{stage}.jsonl", evidence / "receipts.jsonl"),
        (root / "tasks/hook-loading-compatibility/state.md", evidence / "handoff.md"),
    ):
        if source.exists():
            destination.write_bytes(source.read_bytes())
    summary = {
        "stage": stage,
        "exit_code": result.returncode,
        "final": (evidence / "final.txt").read_text()
        if (evidence / "final.txt").exists()
        else None,
    }
    (evidence / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
