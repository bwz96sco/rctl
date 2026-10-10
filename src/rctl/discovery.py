"""A derived task list and the active-task scan used for reminder selection."""

import json

from .documents import RctlError, invalid, local_path, read_text
from .records import Task


def active_tasks(root):
    """Active task paths read from records; None when any record is unreadable.

    Reminders select the only active task automatically, so an unknown phase must
    not be treated as inactive: a damaged record could be the task being worked on.
    """
    directory = local_path(root, "tasks")
    if not directory.is_dir():
        return []
    found = {}
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        try:
            task = Task(root, path)
            record = task.file(".rctl/record.json")
            if not record.exists():
                continue
            phase = json.loads(read_text(record)).get("phase")
        except (RctlError, OSError, ValueError, AttributeError):
            return None
        if phase == "active":
            # Aliases resolve to one canonical task.
            found[task.path] = task.path.relative_to(root).as_posix()
    return sorted(found.values())


def list_tasks(root, phase=None):
    directory = local_path(root, "tasks")
    rows = []
    if not directory.exists():
        return {"tasks": rows}, []
    if not directory.is_dir():
        raise invalid("Expected directory: tasks.")
    seen = set()
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        row = {
            "task_id": path.name,
            "path": f"tasks/{path.name}",
            "title": None,
            "phase": None,
            "verification": None,
            "currentness": "unavailable",
            "goal_decision": None,
            "warnings": [],
            "error": None,
        }
        try:
            task = Task(root, path)
            if task.path in seen:
                continue
            seen.add(task.path)
            row.update(
                task_id=task.task_id, path=task.path.relative_to(root).as_posix()
            )
            if not task.path.is_dir() or not any(
                task.file(name).exists() or task.file(name).is_symlink()
                for name in ("contract.md", ".rctl/record.json")
            ):
                continue
            snapshot = task.snapshot()
            if phase is not None and snapshot.phase != phase:
                continue
            row.update(snapshot.discovery())
        except RctlError as error:
            row["error"] = {
                "code": error.code,
                "message": error.message,
                "next_action": error.next_action,
            }
        rows.append(row)
    return {"tasks": sorted(rows, key=lambda row: row["path"])}, []
