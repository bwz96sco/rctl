"""Probe project-file discovery with scoped trust; never edit shared configuration."""

import json
import os
import selectors
import shutil
import subprocess
import sys
import time
from pathlib import Path

from rctl.integration import export_codex
from rctl.records import Task


def discover(root, arguments):
    process = subprocess.Popen(
        [
            "codex",
            "app-server",
            "--disable",
            "plugins",
            "--disable",
            "apps",
            *arguments,
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)

    def request(identifier, method, params):
        process.stdin.write(
            json.dumps({"id": identifier, "method": method, "params": params}) + "\n"
        )
        process.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if selector.select(1):
                line = process.stdout.readline()
                if not line:
                    raise RuntimeError("Discovery server exited")
                message = json.loads(line)
                if message.get("id") == identifier:
                    if "error" in message:
                        raise RuntimeError(message["error"])
                    return message["result"]
        raise TimeoutError(method)

    try:
        request(
            0,
            "initialize",
            {
                "clientInfo": {"name": "rctl_probe", "version": "0.1.0"},
                "capabilities": {"experimentalApi": True},
            },
        )
        process.stdin.write('{"method":"initialized"}\n')
        process.stdin.flush()
        return request(1, "hooks/list", {"cwds": [str(root)]})["data"][0]
    finally:
        selector.close()
        process.terminate()
        process.wait(timeout=10)


def main():
    stage = sys.argv[1]
    if stage not in {
        "leaf-trust",
        "repo-trust",
        "untrusted",
        "trusted",
        "updated",
        "disabled",
        "repo-bypass",
        "config-layer",
        "normal-bypass",
        "normal-ignore",
    }:
        raise SystemExit(
            "Expected leaf-trust, repo-trust, untrusted, trusted, updated, or disabled"
        )
    repo = Path(__file__).resolve().parents[1]
    root = repo / ".work/project-auto-probe"
    evidence = repo / "docs/evidence/project-auto" / stage
    evidence.mkdir(parents=True, exist_ok=False)
    if not root.exists():
        root.mkdir()
        shutil.copytree(
            repo / "examples/retained-comparison", root / "tasks/retained-comparison"
        )
        Task(root, root / "tasks/retained-comparison").begin()
        export_codex(root, "bundle")
        (root / ".codex").mkdir()
        shutil.copy2(root / "bundle/hooks.json", root / ".codex/hooks.json")
        (root / "tasks/retained-comparison/state.md").write_text(
            "Delivery marker: COPPER-ORCHID-73. Next action: inspect the retained delivery table.\n"
        )
    if stage == "updated":
        (root / "tasks/retained-comparison/state.md").write_text(
            "Delivery marker: SILVER-MAPLE-29. Next action: compare the amended handoff with the receipt.\n"
        )
    if stage == "config-layer":
        (root / ".codex/config.toml").write_text("[features]\nhooks = true\n")
    discovery = discover(root, [])
    project_hooks = [
        hook
        for hook in discovery["hooks"]
        if hook["sourcePath"] == str(root / ".codex/hooks.json")
    ]
    if len(project_hooks) != 2:
        raise RuntimeError("Expected both project hooks in normal discovery")
    (evidence / "discovery.json").write_text(
        json.dumps(
            {
                **discovery,
                "hooks": project_hooks,
                "unrelated_hook_count": len(discovery["hooks"]) - len(project_hooks),
            },
            indent=2,
        )
    )
    arguments = []
    if stage in {"leaf-trust", "repo-trust", "repo-bypass", "config-layer"}:
        arguments += [
            "--ignore-user-config",
            "-c",
            f'projects.{json.dumps(str(root if stage == "leaf-trust" else repo))}.trust_level="trusted"',
        ]
    elif stage == "trusted":
        for hook in discovery["hooks"]:
            if hook not in project_hooks:
                arguments += [
                    "-c",
                    f"hooks.state.{json.dumps(hook['key'])}.enabled=false",
                ]
    if stage in {"leaf-trust", "repo-trust", "trusted", "repo-bypass", "config-layer"}:
        for hook in project_hooks:
            arguments += [
                "-c",
                f"hooks.state.{json.dumps(hook['key'])}.trusted_hash={json.dumps(hook['currentHash'])}",
            ]
    if stage in {
        "repo-bypass",
        "config-layer",
        "normal-bypass",
        "normal-ignore",
        "updated",
    }:
        arguments += ["--dangerously-bypass-hook-trust"]
    if stage == "normal-ignore":
        arguments += ["--ignore-user-config"]
    if stage == "disabled":
        arguments += ["--disable", "hooks"]
    command = [
        "codex",
        "-a",
        "never",
        "exec",
        "--disable",
        "plugins",
        "--disable",
        "apps",
        "--disable",
        "multi_agent",
        "--enable",
        "hooks",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--cd",
        str(root),
        "--json",
        "--color",
        "never",
        "--output-last-message",
        str(evidence / "final.txt"),
        *arguments,
        "-",
    ]
    prompt = "This is a reminder-delivery test. Without calling any tools or inspecting files, report the task identity, phase, delivery marker, and next action supplied by an rctl hook in your current context. If no rctl reminder was delivered, reply NO_RCTL_REMINDER. Do not perform the task or start other agents."
    env = dict(os.environ)
    selected = {
        "RCTL_PROJECT_ROOT": str(root),
        "RCTL_TASK_PATH": "tasks/retained-comparison",
        "RCTL_HOOK_LOG": f"receipts-{stage}.jsonl",
    }
    env.update(selected)
    (evidence / "launch.json").write_text(
        json.dumps(
            {
                "argv": command,
                "cwd": str(root),
                "git_root": subprocess.check_output(
                    ["git", "rev-parse", "--show-toplevel"], cwd=root, text=True
                ).strip(),
                "host_version": subprocess.check_output(
                    ["codex", "--version"], text=True
                ).strip(),
                "environment_overrides": selected,
                "trust_scope": "See argv for invocation-only trust bypass or attempted state overrides. hooks.state overrides did not change native trust/enabled state in this host version. Normal configuration may run existing user hooks. No hook definitions injected and no shared config writes.",
            },
            indent=2,
        )
    )
    (evidence / "prompt.txt").write_text(prompt)
    shutil.copy2(root / ".codex/hooks.json", evidence / "hooks.json")
    if (root / ".codex/config.toml").exists():
        shutil.copy2(root / ".codex/config.toml", evidence / "config.toml")
    shutil.copy2(root / "tasks/retained-comparison/state.md", evidence / "handoff.md")
    with (
        (evidence / "events.jsonl").open("w") as out,
        (evidence / "stderr.txt").open("w") as err,
    ):
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            env=env,
            cwd=root,
            stdout=out,
            stderr=err,
            timeout=120,
        )
    receipts = root / selected["RCTL_HOOK_LOG"]
    if receipts.exists():
        shutil.copy2(receipts, evidence / "receipts.jsonl")
    summary = {
        "stage": stage,
        "exit_code": result.returncode,
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
