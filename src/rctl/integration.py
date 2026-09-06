"""Export reviewable host files without modifying a live host configuration."""

import json
import shlex
import sys
from pathlib import Path

from .documents import RctlError, local_path, resource_tree
from .records import state_error


def toml_value(value):
    if isinstance(value, dict):
        return (
            "{"
            + ", ".join(
                f"{json.dumps(key)} = {toml_value(item)}" for key, item in value.items()
            )
            + "}"
        )
    if isinstance(value, list):
        return "[" + ", ".join(map(toml_value, value)) + "]"
    return json.dumps(value, ensure_ascii=False)


def inline_arguments(hooks):
    arguments = []
    for event, handlers in hooks["hooks"].items():
        arguments += ["-c", f"hooks.{event}={toml_value(handlers)}"]
    return arguments


def codex_hooks(root):
    entrypoint = Path(sys.executable).parent / "rctl"
    if not entrypoint.is_file():
        raise RctlError(
            "NOT_FOUND",
            "Installed rctl console entrypoint is unavailable.",
            "Install rctl in this Python environment before exporting.",
            3,
        )
    command = shlex.join([str(entrypoint), "--root", str(root), "hook", "codex"])
    hooks = {
        "hooks": {
            event: [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": command,
                            "timeout": 10,
                            "additionalContextLimit": budget,
                        }
                    ]
                }
            ]
            for event, budget in (("SessionStart", 8000), ("UserPromptSubmit", 2000))
        }
    }
    return hooks, entrypoint


def export_codex(root, destination):
    path = local_path(root, destination)
    if path.exists():
        raise state_error("Integration destination already exists; choose a new directory.")
    hooks, entrypoint = codex_hooks(root)
    launch = shlex.join(
        ["codex", "--enable", "hooks", *inline_arguments(hooks), "--cd", str(root)]
    )
    readme = f"""# rctl Codex reminder bundle

Target and tested release route: Codex CLI 0.153.4, invocation-local inline hook configuration. Only SessionStart startup and UserPromptSubmit delivery are claimed by the release evidence. Other host versions, resume/compact delivery, and persisted project installation need their own delivery evidence.

## Load and select a task

Inspect `hooks.json` and the generated skill before use. Copy `research-task/` into this project's `.agents/skills/` only when that destination is unused. The skill also works through an explicit path in a prompt. Select the task for each launch:

```sh
export RCTL_TASK_PATH=tasks/your-task
{launch}
```

Use Codex `/hooks` to review and trust the exact definitions. Hook trust is owned by Codex. Exporting this directory does not grant trust or install configuration. Existing host hook sources may also run; inspect them in `/hooks`. For isolated automation, the release smoke used `--ignore-user-config`, disabled apps/plugins, and the host's invocation-only hook-trust bypass after reviewing these generated definitions; that bypass is not part of the normal launch above.

The hook command fixes project root `{root}` and uses installed entrypoint `{entrypoint}`. Re-export after moving/replacing that environment. Optional `RCTL_HOOK_LOG` selects a receipt JSONL path inside this project; leave it unset for no receipts. Receipts contain delivered task context and stay local. Export does not execute task checks or launch Codex.

## Remove

Stop using the inline arguments and unset `RCTL_TASK_PATH` and `RCTL_HOOK_LOG` in that shell. Remove only the skill directory you copied and this exported bundle when no longer needed. Task contracts, results, handoffs, and machine records remain usable from the terminal.

## Evidence boundary

The release verification record in the rctl source repository contains the actual host version, exact launch arguments, receipts, and two-session task evidence. A copied hook file or a direct adapter invocation alone does not demonstrate model-visible delivery. Ordinary persisted `.codex/hooks.json` loading is reported separately there. Protocol reference: https://developers.openai.com/codex/hooks
"""
    path.mkdir(parents=True, exist_ok=False)
    (path / "hooks.json").write_text(
        json.dumps(hooks, indent=2) + "\n", encoding="utf-8"
    )
    skill = path / "research-task"
    skill_files = resource_tree("skills/research-task")
    for name, content in skill_files.items():
        target = skill / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    (path / "README.md").write_text(readme, encoding="utf-8")
    return {
        "directory": str(path),
        "host": "codex",
        "entrypoint": str(entrypoint),
        "files": [
            "hooks.json",
            *[f"research-task/{name}" for name in skill_files],
            "README.md",
        ],
    }
