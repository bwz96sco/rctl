"""Codex SessionStart and UserPromptSubmit adapter."""

import json
import os
import sys
from pathlib import Path

from ..context import bounded, context
from ..documents import RctlError, invalid, local_path
from ..records import Task, now, project_root, select_task

BUDGETS = {"SessionStart": 8000, "UserPromptSubmit": 2000}


def handle(payload, root_argument=None):
    if not isinstance(payload, dict):
        raise invalid("Codex hook input must be a JSON object.")
    event = payload.get("hook_event_name")
    if event not in BUDGETS:
        return {}
    root = None
    try:
        if root_argument is None and not os.environ.get("RCTL_PROJECT_ROOT"):
            raise invalid("Set RCTL_PROJECT_ROOT or supply --root for the reminder.")
        root = project_root(root_argument)
        cwd = payload.get("cwd")
        if not isinstance(cwd, str) or not Path(cwd).is_absolute():
            raise invalid(
                "Hook cwd must be an absolute path inside the selected project."
            )
        local_path(root, cwd)
        task = Task(root, select_task(root))
        text = context(
            task, budget=BUDGETS[event], compact=event == "UserPromptSubmit"
        )[0]["context"]
    except (RctlError, OSError, ValueError) as error:
        text = "rctl context unavailable: " + str(error)
        if isinstance(error, RctlError):
            text += "\n" + error.next_action
    text = bounded(text, BUDGETS[event], "the selected task files")
    receipt = os.environ.get("RCTL_HOOK_LOG")
    if receipt and root is not None:
        try:
            path = local_path(root, receipt)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as stream:
                stream.write(
                    json.dumps(
                        {
                            "event": event,
                            "source": payload.get("source"),
                            "session_id": payload.get("session_id"),
                            "task_path": os.environ.get("RCTL_TASK_PATH"),
                            "timestamp": now(),
                            "context": text,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        except (RctlError, OSError) as error:
            print(f"rctl hook receipt unavailable: {error}", file=sys.stderr)
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def main(root_argument=None):
    try:
        response = handle(json.load(sys.stdin), root_argument)
    except (ValueError, RctlError) as error:
        print(f"rctl hook: invalid event input: {error}", file=sys.stderr)
        response = {}
    except Exception as error:
        # A reminder failure must not stop ordinary conversation.
        print(f"rctl hook unavailable: {type(error).__name__}", file=sys.stderr)
        response = {}
    print(json.dumps(response, ensure_ascii=False))
    return 0
