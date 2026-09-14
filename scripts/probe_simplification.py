"""Run a bounded Astra acceptance session against a chosen installed rctl.

Run stages first, resume, compact, stale in order in a fresh .work/ project.
Keep the same fixtures and prompts for the baseline and candidate executables.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

import yaml

from rctl.integration import inline_arguments

TASK = "tasks/retained-comparison"
REFRESHED = (
    "Planning update: only a matched component-removal comparison would answer "
    "the remaining complementarity question."
)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def prepare(repo, root, executable, cli):
    cli("init")
    # Give the fixture its own project boundary, excluding development AGENTS.md.
    subprocess.run(["git", "init", "--quiet", str(root)], check=True)
    (root / "research/PROGRAM.md").write_text(
        "# Synthetic research program\n\n## Goal\n"
        "Determine whether combining complementary components can lower error.\n\n"
        "## Current guidance\nRecover accepted evidence before choosing a follow-up.\n"
    )
    (root / "research/ROUTES.md").write_text(
        "# Routes\n\n## Reuse Rule\nCite related mechanisms and the decision new evidence changes.\n\n"
        "## Organization-only comparison\nBoth arms received the same candidate records. "
        "The synthetic organization change has error 0.23 versus 0.20. It does not "
        "isolate complementary components. See ../tasks/retained-comparison/evidence/metrics.json "
        "and questions/Q.md. Reopen that question only with an intervention that "
        "isolates component complementarity at a matched budget.\n"
    )
    question = root / "research/questions/Q.md"
    question.parent.mkdir()
    question.write_text(
        "# Component complementarity\n\n## Mechanism\n"
        "Combining complementary logical components may improve generated programs. "
        "An organization-only comparison with the same supplied records does not "
        "isolate this mechanism. A matched component-removal control could do so.\n"
    )
    task = root / TASK
    shutil.copytree(repo / "examples/retained-comparison", task)
    contract = (task / "contract.md").read_text()
    front, body = contract[4:].split("\n---\n", 1)
    data = yaml.safe_load(front)
    data["criteria"][0]["method"]["argv"] = [
        "uv",
        "run",
        "--offline",
        "--no-project",
        "--no-cache",
        "--python",
        str(executable.with_name("python")),
        "--script",
        "check_arithmetic.py",
    ]
    data["criteria"][1]["evidence_refs"].append("../../research/questions/Q.md")
    data["criteria"][1]["requirement"] += (
        " Its organization-only result does not decide the broader complementarity mechanism."
    )
    alignment = """## Question alignment

- Governing question source: research/questions/Q.md#mechanism
- Governing mechanism: Combining complementary logical components may improve generated programs.
- This task tests: The organization increment after both arms receive the same records.
- This task does not decide: Whether complementary components improve generated programs.

"""
    body = body.replace("## Scope", alignment + "## Scope")
    (task / "contract.md").write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False) + "---\n" + body
    )
    reviews = json.loads((task / "reviews.json").read_text())
    reviews["checks"][0]["evidence_refs"].append("../../research/questions/Q.md")
    write_json(task / "reviews.json", reviews)
    (root / "handoff-history.md").write_text(
        "## Earlier inspection notes\n\n"
        + "".join(
            f"Entry {i:03d}: supplied aggregates retained; prediction-level evidence is outside this task.\n"
            for i in range(120)
        )
    )
    cli("begin", TASK)
    cli("integration", "codex", "export", "bundle")
    (root / "prepare_compact.py").write_text(
        "from pathlib import Path\n"
        "root = Path(__file__).parent\n"
        "program = root / 'research/PROGRAM.md'\n"
        "program.write_text(program.read_text().split('## Current guidance')[0] "
        f"+ '## Current guidance\\n' + {REFRESHED!r} + '\\n')\n"
        "for i in range(1400):\n"
        "    print(f'Compaction fixture row {i:04d}: local delivery diagnostic only; no research observation.')\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("first", "resume", "compact", "stale"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--rctl", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    root, executable = args.root.resolve(), args.rctl.absolute()
    if not root.is_relative_to(repo / ".work") or root == repo / ".work":
        parser.error(
            "Use a distinct disposable project under this repository's .work/."
        )
    if args.stage == "first":
        root.mkdir(parents=True, exist_ok=False)
    evidence = root / "probe-evidence" / args.stage
    evidence.mkdir(parents=True, exist_ok=False)
    env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"VIRTUAL_ENV", "PYTHONPATH"} and not key.startswith("RCTL_")
    }
    env["PATH"] = str(executable.parent) + os.pathsep + env["PATH"]
    calls = []

    def cli(*arguments, expected=0):
        command = [str(executable), "--root", str(root), "--format", "json", *arguments]
        result = subprocess.run(
            command, env=env, capture_output=True, text=True, check=False
        )
        response = json.loads(result.stdout)
        calls.append(
            {"argv": command, "exit_code": result.returncode, "response": response}
        )
        write_json(evidence / "cli.json", calls)
        if result.returncode != expected:
            raise RuntimeError(result.stdout + result.stderr)
        return response["data"]

    if args.stage == "first":
        prepare(repo, root, executable, cli)
    if args.stage == "stale":
        cli(
            "reopen",
            TASK,
            "--reason",
            "Exercise the same evidence in a fresh acceptance cycle",
        )
        cli("verify", TASK, "--reviews", f"{TASK}/reviews.json")
        before = cli("status", TASK)
        (root / "stale-handoff.md").write_text(
            "## Next action\nInspect the result annotation and refresh verification before closure.\n"
            "\n## Blockers\nThe result annotation may need a fresh check.\n"
        )
        cli("checkpoint", TASK, "--file", "stale-handoff.md")
        after_handoff = cli("status", TASK)
        assert before["currentness"] == after_handoff["currentness"] == "current"
        result = root / TASK / "result.md"
        result.write_text(
            result.read_text()
            + "\nEditorial note: all observations remain synthetic.\n"
        )
        assert cli("status", TASK)["currentness"] == "stale"
        cli("close", TASK, expected=4)

    common = (
        "Use $research-task from .agents/skills/research-task/SKILL.md for the selected task. "
        f"The installed CLI is {executable}; use it for rctl operations. "
        "Work only in this disposable project using the supplied synthetic evidence. "
        "Keep its scientific question, inputs, budget, and criteria fixed. "
        "Use uv for Python runs. Do not start other agents or remote work.\n"
    )
    prompts = {
        "first": common
        + (
            "Inspect the supplied evidence and draft result. Prepare a handoff for a fresh session "
            "to finish the assessment. Save it through checkpoint with a concrete next action and "
            "blockers first, then retain handoff-history.md as its earlier inspection notes. "
            "Pause with the task active; verification and closure belong to the next session."
        ),
        "resume": common
        + (
            "Before tools, state the next action supplied by the hook handoff, or say none arrived. "
            "Continue from that handoff to finish this task: inspect the sources, finalize the result "
            "and evidence-based review, verify, and close when permitted. Report the scoped finding."
        ),
        "compact": common
        + (
            "Use the completed result and related history to propose one distinct follow-up question "
            "and the decision it would change, without executing the proposed research. "
            "Then exercise the supplied infrastructure helper exactly once: "
            f"uv run --offline --no-project --no-cache --python {executable.with_name('python')} "
            "--script prepare_compact.py . Its rows are delivery diagnostics, not scientific evidence. "
            "After that command, use no further tools. Report the proposal, the accepted task scope, "
            "what its result does not decide, and the latest project guidance delivered by rctl. "
            "If no updated reminder arrives, say so."
        ),
        "stale": common
        + (
            "The result received an editorial annotation after verification. Inspect the reported "
            "state and carry the required corrective work through to closure when permitted. "
            "Preserve the accepted question and supplied evidence. Report the verification used."
        ),
    }
    hooks = json.loads((root / "bundle/hooks.json").read_text())
    for handlers in hooks["hooks"].values():
        expected = str(executable)
        assert expected in handlers[0]["hooks"][0]["command"]
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
        "--disable",
        "multi_agent",
        "--enable",
        "hooks",
        "--skip-git-repo-check",
        "--ephemeral",
        "--sandbox",
        "workspace-write",
        "--dangerously-bypass-hook-trust",
        "--model",
        "gpt-6-astra",
        "-c",
        'model_reasoning_effort="medium"',
        *inline_arguments(hooks),
        "--cd",
        str(root),
        "--json",
        "--color",
        "never",
        "--output-last-message",
        str(evidence / "final.txt"),
    ]
    if args.stage == "compact":
        command += [
            "-c",
            "model_auto_compact_token_limit=3000",
            "-c",
            'model_auto_compact_token_limit_scope="body_after_prefix"',
        ]
    command.append("-")
    env.update(
        RCTL_PROJECT_ROOT=str(root),
        RCTL_TASK_PATH=TASK,
        RCTL_HOOK_LOG=f"probe-evidence/{args.stage}/receipts.jsonl",
    )
    (evidence / "prompt.txt").write_text(prompts[args.stage])
    write_json(
        evidence / "launch.json",
        {
            "argv": command,
            "host_version": subprocess.check_output(
                ["codex", "--version"], text=True
            ).strip(),
            "model": "gpt-6-astra",
            "reasoning_effort": "medium",
            "rctl": str(executable),
            "trust_scope": "Reviewed generated rctl hooks only; invocation-only trust; workspace-write sandbox.",
        },
    )
    with (
        (evidence / "events.jsonl").open("w") as out,
        (evidence / "stderr.txt").open("w") as err,
    ):
        try:
            result = subprocess.run(
                command,
                input=prompts[args.stage],
                text=True,
                env=env,
                cwd=root,
                stdout=out,
                stderr=err,
                timeout=300,
                check=False,
            )
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            exit_code = 124
    status = cli("status", TASK)
    receipts_path = evidence / "receipts.jsonl"
    receipts = (
        [json.loads(line) for line in receipts_path.read_text().splitlines()]
        if receipts_path.exists()
        else []
    )
    summary = {
        "stage": args.stage,
        "exit_code": exit_code,
        "phase": status["phase"],
        "currentness": status["currentness"],
        "verification": status["verification"]["id"]
        if status["verification"]
        else None,
        "receipts": [
            {
                "event": r["event"],
                "source": r["source"],
                "characters": len(r["context"]),
            }
            for r in receipts
        ],
        "refreshed_compact": any(
            r["source"] == "compact" and REFRESHED in r["context"] for r in receipts
        ),
        "final": (evidence / "final.txt").read_text()
        if (evidence / "final.txt").exists()
        else None,
    }
    write_json(evidence / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    if exit_code:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
