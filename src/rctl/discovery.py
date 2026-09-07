"""A derived task list; no index or implicit task selection."""

from .documents import RctlError, local_path
from .records import Task


def list_tasks(root, phase=None):
    directory = local_path(root, "tasks")
    rows = []
    if not directory.exists():
        return {"tasks": rows}, []
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        row = {
            "task_id": path.name,
            "path": f"tasks/{path.name}",
            "title": None,
            "phase": None,
            "verification": None,
            "currentness": "unavailable",
            "warnings": [],
            "error": None,
        }
        try:
            task = Task(root, path)
            if not task.path.is_dir() or not any(
                task.file(name).exists() or task.file(name).is_symlink()
                for name in ("contract.md", ".rctl/record.json")
            ):
                continue
            status, warnings = task.status()
            if phase is not None and status["phase"] != phase:
                continue
            row.update({key: status[key] for key in ("title", "phase", "currentness")})
            report = status["verification"]
            row["verification"] = (
                {key: report[key] for key in ("id", "verdict")} if report else None
            )
            row["warnings"] = warnings
        except RctlError as error:
            row["error"] = {
                "code": error.code,
                "message": error.message,
                "next_action": error.next_action,
            }
        rows.append(row)
    return {"tasks": rows}, []
