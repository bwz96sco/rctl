"""Read-only project and task reminders shared by terminal and host integration."""

import os
import re

from .documents import RctlError
from .project_context import read_project
from .records import Task, select_task

DEFAULT_BUDGET = 8000
FIELD_VISIBILITY = 96
AUTOMATIC = "selected automatically as the only active task"
# Per-prompt caps keep each line a whole sentence instead of a fragment.
PROMPT_CAPS = {"next_action": 400, "blockers": 200, "warning": 200, "sentence": 300}


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
    note="",
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
    identity = bounded(note + identity, min(400, budget // 4), "status TASK")
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


def first_sentence(text):
    text = " ".join(text.split())
    match = re.search(r"[.!?。！？](?=\s|$)", text)
    return text[: match.end()] if match else text


def prompt_reminder(snapshot, project, warnings, task_path, budget, automatic=False):
    """Selected-task state for every prompt; SessionStart carries the full reminder."""
    report = snapshot.verification
    verification = f"{report['id']} {report['verdict']}" if report else "not verified"
    head = (
        f"Task: {snapshot.task_id} | {snapshot.phase} | {verification} "
        f"({snapshot.currentness})"
    )
    if automatic:
        head += f" | {AUTOMATIC}"
    tail = f"Full reminder: rctl context {task_path}"
    sentence = PROMPT_CAPS["sentence"]
    # (display order, label, text, cap, source), listed by priority for space.
    lines = [
        (1, "Warning", warning, PROMPT_CAPS["warning"], f"rctl status {task_path}")
        for warning in warnings[:3]
    ]
    impact, contribution = snapshot.goal_impact, snapshot.goal_contribution
    if impact is not None:
        decision = (
            f"{impact['claim_effect']}; investment: {impact['next_decision']} "
            f"({impact['currentness']})"
        )
        lines.append((8, "Goal decision (reviewed)", decision, sentence, "status TASK"))
    elif contribution is not None:
        lines.append(
            (
                8,
                "Goal obligation (declared)",
                first_sentence(contribution["obligation"]),
                sentence,
                "C / goal_contribution",
            )
        )
    if project["goal"]:
        lines.append(
            (9, "Project goal (reported)", first_sentence(project["goal"]), sentence, "P / Goal")
        )
    if snapshot.phase in {"draft", "active"}:
        lines.append(
            (
                5,
                "Reported handoff — Next action",
                snapshot.handoff["next_action"],
                PROMPT_CAPS["next_action"],
                "T/state.md",
            )
        )
    lines.append(
        (3, "Governing task question", first_sentence(snapshot.question), sentence, "C / Question")
    )
    if snapshot.question_alignment is not None:
        lines.append(
            (
                4,
                "This task does not decide (declared)",
                first_sentence(snapshot.question_alignment["does_not_decide"]),
                sentence,
                "C / Question alignment",
            )
        )
    lines.append((7, "Lifecycle action", snapshot.next_action, sentence, "status TASK"))
    if snapshot.phase in {"draft", "active"}:
        lines.append(
            (
                6,
                "Reported handoff — Blockers",
                snapshot.handoff["blockers"],
                PROMPT_CAPS["blockers"],
                "T/state.md",
            )
        )
    if len(warnings) > 3:
        lines.append(
            (2, "Warnings", f"{len(warnings) - 3} more; read rctl status {task_path}.", 100, "status TASK")
        )
    room = budget - len(head) - len(tail) - 2
    kept = []
    for order, label, text, cap, source in lines:
        space = min(cap, room - len(label) - 3)
        # Skip a line that would only fit a fragment; the pointer remains.
        if not text or space < min(len(text), 40):
            continue
        line = f"{label}: {bounded(text, space, source)}"
        kept.append((order, line))
        room -= len(line) + 1
    body = [line for _, line in sorted(kept, key=lambda item: item[0])]
    return "\n".join([head, *body, tail])


def context(task, budget=DEFAULT_BUDGET):
    """Read one concise reminder from the selected task."""
    return load_context(task.root, task=task, budget=budget)


def load_context(
    root, selection=None, *, task=None, budget=DEFAULT_BUDGET, prompt=False
):
    project, project_warnings = read_project(root)
    selected = (
        task is not None
        or selection is not None
        or bool(os.environ.get("RCTL_TASK_PATH"))
    )
    # Without an explicit task, a reminder uses the only active task; several
    # active tasks are listed instead of guessed.
    automatic, note = False, ""
    if not selected:
        from .discovery import active_tasks

        try:
            active = active_tasks(root)
        except RctlError:
            active = None
        if active is None:
            note = (
                "Automatic task selection unavailable: a task record is unreadable; "
                "run rctl task list.\n"
            )
        elif len(active) == 1:
            selection, selected, automatic = active[0], True, True
            note = f"Task {AUTOMATIC}.\n"
        elif active:
            note = f"Active tasks (none selected): {', '.join(active)}.\n"
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
        note=note,
    )
    data["task_selection"] = (
        "automatic" if automatic else "explicit" if selected else None
    )
    if error:
        error.data = {**data, "context_warnings": warnings}
        raise error
    if prompt and snapshot is not None:
        data["context"] = prompt_reminder(
            snapshot,
            project,
            warnings,
            task.path.relative_to(root).as_posix(),
            budget,
            automatic,
        )
    return data, warnings
