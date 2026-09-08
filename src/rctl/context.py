"""Read-only project and task reminders shared by terminal and host integration."""

import os

from .documents import RctlError, read_text
from .project_context import read_project
from .records import Task, select_task

DEFAULT_BUDGET = 8000


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


def render(root, project, task, status, warnings, error, selected, budget, compact):
    # Short aliases avoid repeating absolute paths in every truncation marker.
    sources = f"Root: {root}\nP: research/PROGRAM.md; R: research/ROUTES.md\n"
    sources += "Orientation: research/README.md\n"
    if task is not None:
        sources += (
            f"T: {task.path.relative_to(root)}\n"
            "T files: contract.md, state.md, result.md, .rctl/record.json\n"
        )
    sources = bounded(sources, min(500, budget // 4), "--root and selected task")
    identity = "No task selected. Supply TASK or set RCTL_TASK_PATH for task context.\n"
    if error:
        identity = "Task context unavailable.\n"
    elif status is not None:
        report = status["verification"]
        verification = f"{report['id']}: {report['verdict']}" if report else "none"
        closure = status["historical_closure"]
        historical = (
            f"{closure['verification_id']} (cycle {closure['cycle']}, {closure['assessment']})"
            if closure
            else "none"
        )
        identity = (
            f"Task: {status['task_id']}\n"
            f"Phase: {status['phase']}; governing revision: {status['contract_revision'] or 'none'}\n"
            f"Verification: {verification}; applicability: {status['currentness']}; "
            f"historical closure: {historical}\n"
        )
    identity = bounded(identity, min(400, budget // 4), "status TASK")
    # key, label, value, source; values are budgeted independently of labels.
    fields = []
    for key, label, source in (
        ("goal", "Project goal (reported)", "P / Goal"),
        ("current_guidance", "Current guidance (reported)", "P / Current guidance"),
        ("reuse_rule", "History reuse", "R / Reuse Rule"),
    ):
        if project[key]:
            fields.append((key, label, project[key], source))
    if warnings:
        fields.append(("warnings", "Warning", "\n".join(warnings), "status TASK; P; R"))
    if error:
        fields.append(
            (
                "error",
                "Task error",
                f"{error.code}: {error.message}\n{error.next_action}",
                "selected task",
            )
        )
    label = "Reported handoff"
    if status is not None:
        label = (
            "Historical handoff"
            if status["phase"] in {"closed", "cancelled"}
            else label
        )
        for key, title in (("blockers", "Blockers"), ("next_action", "Next action")):
            value = status["handoff"][key] or "Not recorded; read T/state.md."
            fields.append((key, f"{label} — {title}", value, "T/state.md"))
        fields.append(
            ("lifecycle", "Lifecycle action", status["next_action"], "status TASK")
        )
    overhead = len(sources) + len(identity) + sum(len(f[1]) + 3 for f in fields) + 2
    # Leave extended reminders room for governing contract and handoff excerpts.
    core_budget = budget if compact else min(budget, 3200)
    limits = allocate([f[2] for f in fields], max(0, core_budget - overhead))
    values = {f[0]: bounded(f[2], limit, f[3]) for f, limit in zip(fields, limits)}
    guidance = "\n".join(f"{f[1]}: {values[f[0]]}" for f in fields if f[0] in project)
    other = "\n".join(f"{f[1]}: {values[f[0]]}" for f in fields if f[0] not in project)
    reminder = guidance + "\n" + identity + other + "\n" + sources
    if not compact and status is not None:
        record = task.read_record()
        contract = (
            record["contracts"][-1]["text"]
            if record
            else read_text(task.file("contract.md"))
        )
        try:
            handoff = read_text(task.file("state.md"))
        except RctlError:
            handoff = "Handoff unavailable; inspect T/state.md."
        labels = (
            "\nGoverning contract (includes criteria):\n",
            f"\n{label} (reported progress):\n",
        )
        remaining = max(0, budget - len(reminder) - sum(map(len, labels)))
        for text, heading, source, limit in zip(
            (contract, handoff),
            labels,
            ("T/contract.md", "T/state.md"),
            allocate([contract, handoff], remaining),
        ):
            if limit:
                reminder += heading + bounded(text, limit, source)
    data = dict(status or {})
    if status is not None:
        data["handoff"] = {
            key: (values.get(key) or None) if value else None
            for key, value in status["handoff"].items()
        }
        data["title"] = (
            bounded(status["title"], min(200, budget), "T/contract.md") or None
        )
        if status["verification"]:
            data["verification"] = {
                key: status["verification"][key]
                for key in ("id", "verdict", "contract_revision", "cycle")
            }
    data.update(
        {
            "available": project["available"] or status is not None,
            "task_selected": selected,
            "task_available": status is not None,
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


def context(task, budget=DEFAULT_BUDGET, compact=False):
    """Compatibility entry for callers that already hold a selected Task."""
    return load_context(task.root, task=task, budget=budget, compact=compact)


def load_context(
    root, selection=None, *, task=None, budget=DEFAULT_BUDGET, compact=False
):
    project, project_warnings = read_project(root)
    selected = (
        task is not None
        or selection is not None
        or bool(os.environ.get("RCTL_TASK_PATH"))
    )
    status, warnings, error = None, [], None
    if selected:
        try:
            task = task or Task(root, select_task(root, selection))
            status, warnings = task.status()
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
        root, project, task, status, warnings, error, selected, budget, compact
    )
    if error:
        error.data = {**data, "context_warnings": warnings}
        raise error
    return data, warnings
