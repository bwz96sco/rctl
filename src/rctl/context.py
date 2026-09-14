"""Read-only project and task reminders shared by terminal and host integration."""

import os

from .documents import RctlError
from .project_context import read_project
from .records import Task, select_task

DEFAULT_BUDGET = 8000
FIELD_VISIBILITY = 96


def bounded(text, budget, source):
    if len(text) <= budget:
        return text
    suffix = f"\n[Truncated; read {source}]"
    if len(suffix) >= budget:
        return "[Truncated]" if budget >= len("[Truncated]") else ""
    return text[: budget - len(suffix)] + suffix


def allocate(texts, budget):
    """Share space between fields, redistributing space unused by short fields."""
    limits = [0] * len(texts)
    pending = list(range(len(texts)))
    while pending and budget > 0:
        share = max(1, budget // len(pending))
        for i in pending[:]:
            amount = min(share, len(texts[i]) - limits[i], budget)
            limits[i] += amount
            budget -= amount
            if limits[i] == len(texts[i]):
                pending.remove(i)
    return limits


def render(
    root,
    project,
    snapshot,
    warnings,
    error,
    selected,
    budget,
    *,
    task_path=None,
    orientation=False,
):
    # Short aliases avoid repeating absolute paths in every truncation marker.
    sources = f"Root: {root}\nP: research/PROGRAM.md; R: research/ROUTES.md\n"
    if orientation:
        sources += "Orientation: research/README.md\n"
    if task_path is not None:
        sources += f"T: {task_path}\nT files: contract.md, state.md, result.md\n"
    if snapshot is not None:
        sources += f"C: {snapshot.contract_source}\n"
    sources = bounded(sources, min(500, budget // 4), "--root and selected task")
    identity = "No task selected. Supply TASK or set RCTL_TASK_PATH for task context.\n"
    if error:
        identity = "Task context unavailable.\n"
    elif snapshot is not None:
        identity = snapshot.identity()
    identity = bounded(identity, min(400, budget // 4), "status TASK")
    # key, label, value, source; values are budgeted independently of labels.
    fields = snapshot.task_fields() if snapshot is not None else []
    task_context_keys = {field[0] for field in fields}
    for key, label, source in (
        ("goal", "Project goal (reported)", "P / Goal"),
        ("current_guidance", "Current guidance (reported)", "P / Current guidance"),
        ("reuse_rule", "History reuse", "R / Reuse Rule"),
    ):
        if project[key]:
            fields.append((key, label, project[key], source))
    if warnings:
        fields.append(
            ("warnings", "Warning", "\nWarning: ".join(warnings), "status TASK; P; R")
        )
    if error:
        fields.append(
            (
                "error",
                "Task error",
                f"{error.code}: {error.message}\n{error.next_action}",
                "selected task",
            )
        )
    if snapshot is not None:
        fields.extend(snapshot.handoff_fields())
    overhead = len(sources) + len(identity) + sum(len(f[1]) + 3 for f in fields) + 2
    remaining = max(0, budget - overhead)
    visible = [min(FIELD_VISIBILITY, len(field[2])) for field in fields]
    if sum(visible) > remaining:
        limits = allocate([field[2] for field in fields], remaining)
    else:
        limits = visible
        remaining -= sum(limits)
        # Give the accepted task relationship its remaining space before mutable
        # guidance, without displacing warnings, handoff, or guidance completely.
        priority = [
            i
            for i, field in enumerate(fields)
            if field[0] in task_context_keys and limits[i] < len(field[2])
        ]
        allocated = allocate([fields[i][2][limits[i] :] for i in priority], remaining)
        for index, limit in zip(priority, allocated):
            limits[index] += limit
        remaining -= sum(allocated)
        rest = [
            i
            for i, field in enumerate(fields)
            if field[0] not in task_context_keys and limits[i] < len(field[2])
        ]
        allocated = allocate([fields[i][2][limits[i] :] for i in rest], remaining)
        for index, limit in zip(rest, allocated):
            limits[index] += limit
    values = {f[0]: bounded(f[2], limit, f[3]) for f, limit in zip(fields, limits)}
    task_context = "\n".join(
        f"{field[1]}: {values[field[0]]}"
        for field in fields
        if field[0] in task_context_keys
    )
    guidance = "\n".join(
        f"{field[1]}: {values[field[0]]}" for field in fields if field[0] in project
    )
    other = "\n".join(
        f"{field[1]}: {values[field[0]]}"
        for field in fields
        if field[0] not in project and field[0] not in task_context_keys
    )
    reminder = "\n".join(
        part
        for part in (identity.rstrip(), task_context, guidance, other, sources)
        if part
    )
    data = (
        snapshot.context_data(
            values, bounded(snapshot.title, min(200, budget), "C") or None
        )
        if snapshot is not None
        else {}
    )
    data.update(
        {
            "available": project["available"] or snapshot is not None,
            "task_selected": selected,
            "task_available": snapshot is not None,
            "project": {
                **project,
                **{
                    key: values.get(key) or None
                    for key in ("goal", "current_guidance", "reuse_rule")
                },
            },
            "context": bounded(reminder, budget, "project and task sources"),
        }
    )
    return data


def context(task, budget=DEFAULT_BUDGET):
    """Read one concise reminder from the selected task."""
    return load_context(task.root, task=task, budget=budget)


def load_context(root, selection=None, *, task=None, budget=DEFAULT_BUDGET):
    project, project_warnings = read_project(root)
    selected = (
        task is not None
        or selection is not None
        or bool(os.environ.get("RCTL_TASK_PATH"))
    )
    snapshot, warnings, error = None, [], None
    if selected:
        try:
            task = task or Task(root, select_task(root, selection))
            snapshot = task.snapshot()
            warnings = list(snapshot.warnings)
        except RctlError as caught:
            error = caught
        except (OSError, ValueError) as caught:
            error = RctlError(
                "NOT_FOUND",
                str(caught),
                "Inspect the selected task path and permissions.",
                3,
            )
    warnings = warnings + project_warnings
    data = render(
        root,
        project,
        snapshot,
        warnings,
        error,
        selected,
        budget,
        task_path=task.path.relative_to(root).as_posix() if task is not None else None,
        orientation=(root / "research/README.md").is_file(),
    )
    if error:
        error.data = {**data, "context_warnings": warnings}
        raise error
    return data, warnings
