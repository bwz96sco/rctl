"""Per-session task pointers, so concurrent host sessions keep their own task.

`begin`, `reopen` and `task use` point the calling host session at a task; reminders
read the pointer through the session ID in the hook payload. Pointers live in a
self-ignored runtime directory, never in task records.
"""

import json
import os
import re

from .documents import RctlError, local_path, read_text
from .records import atomic_write, now

DIRECTORY = ".rctl/sessions"
# Each host exports its own session ID to the shell commands it runs; the hook
# payload carries the same value as `session_id`.
SHELL_VARIABLES = {"claude": "CLAUDE_CODE_SESSION_ID", "codex": "CODEX_THREAD_ID"}
SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


def pointer(root, host, session_id):
    if not isinstance(session_id, str) or not SESSION_ID.fullmatch(session_id):
        return None
    return root / DIRECTORY / f"{host}-{session_id}.json"


def shell_session():
    """The (host, session ID) running this command, else None and the reason."""
    found = [
        (host, os.environ[name].strip())
        for host, name in SHELL_VARIABLES.items()
        if os.environ.get(name, "").strip()
    ]
    if len(found) > 1:
        # A host launched from another inherits the outer ID; neither is knowable.
        return None, "both CLAUDE_CODE_SESSION_ID and CODEX_THREAD_ID are set"
    if not found:
        return None, "no Claude Code or Codex session ID in this shell"
    return found[0], None


def remember(task):
    """Point the calling session at TASK; returns the pointer name, else None."""
    session, reason = shell_session()
    path = pointer(task.root, *session) if session else None
    if path is None:
        return None, reason or "the session ID is not a plain identifier"
    ignore = path.parent / ".gitignore"
    if not ignore.exists():
        atomic_write(ignore, "*\n")
    record = {
        "task": task.path.relative_to(task.root).as_posix(),
        "host": session[0],
        "session_id": session[1],
        "updated_at": now(),
    }
    atomic_write(path, json.dumps(record, indent=2) + "\n")
    return path.stem, None


def session_task(root, host, session_id):
    """This session's task path and a note when its pointer cannot be used."""
    path = pointer(root, host, session_id)
    if path is None or not path.exists():
        return None, ""
    try:
        task = json.loads(read_text(path))["task"]
        exists = local_path(root, task).is_dir()
    except (RctlError, OSError, ValueError, TypeError, KeyError):
        return None, f"Session task pointer {DIRECTORY}/{path.name} is unreadable.\n"
    if not exists:
        return None, f"This session's task {task} no longer exists.\n"
    return task, ""


def forget(task):
    """Remove every session pointer to TASK once it has ended."""
    directory = task.root / DIRECTORY
    target = task.path.relative_to(task.root).as_posix()
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        try:
            if json.loads(read_text(path)).get("task") == target:
                path.unlink()
        except (RctlError, OSError, ValueError, AttributeError):
            continue
