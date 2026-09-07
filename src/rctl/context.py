"""Read-only reminders shared by terminal and host integration."""

from .documents import RctlError, read_text

DEFAULT_BUDGET = 8000


def bounded(text, budget, source):
    if len(text) <= budget:
        return text
    suffix = f"\n[Truncated; read {source}]"
    if len(suffix) >= budget:
        return "[Truncated]"[:budget]
    return text[: budget - len(suffix)] + suffix


def context(task, budget=DEFAULT_BUDGET, compact=False):
    status, warnings = task.status()
    record = task.read_record()
    report = status["verification"]
    verification = f"{report['id']}: {report['verdict']}" if report else "none"
    closure = status["historical_closure"]
    historical = (
        f"{closure['verification_id']} (cycle {closure['cycle']}, {closure['assessment']})"
        if closure
        else "none"
    )
    paths = {
        name: task.file(name)
        for name in ("contract.md", "state.md", "result.md", ".rctl/record.json")
    }
    identity = (
        f"Task: {status['task_id']}\n"
        f"Phase: {status['phase']}; governing revision: {status['contract_revision'] or 'none'}\n"
        f"Verification: {verification}; applicability: {status['currentness']}; "
        f"historical closure: {historical}\n"
    )
    sources = "\n".join(f"{name}: {path}" for name, path in paths.items()) + "\n"
    orientation = task.root / "research/README.md"
    if orientation.is_file():
        sources += f"Project orientation: {orientation}\n"
    # Reserve paths before excerpting any prose. Smaller caller budgets get a compact map.
    if len(identity + sources) > budget // 2:
        sources = f"Task directory: {task.path}\nSources: " + ", ".join(paths) + "\n"
    available = max(0, budget - len(identity + sources) - 5)
    limits = {
        "warnings": available // 4,
        "next_action": available // 4,
        "blockers": available // 8,
        "lifecycle": available // 8,
    }
    ended = status["phase"] in {"closed", "cancelled"}
    label = "Historical handoff" if ended else "Reported handoff"
    reported = status["handoff"]
    sections = [
        bounded(
            "\n".join(f"Warning: {w}" for w in warnings),
            limits["warnings"],
            "status TASK",
        ),
        bounded(
            f"{label} — Next action: {reported['next_action'] or 'Not recorded; read state.md.'}",
            limits["next_action"],
            paths["state.md"],
        ),
        bounded(
            f"{label} — Blockers: {reported['blockers'] or 'Not recorded.'}",
            limits["blockers"],
            paths["state.md"],
        ),
        bounded(
            f"Lifecycle action: {status['next_action']}",
            limits["lifecycle"],
            "status TASK",
        ),
    ]
    header = identity + "\n".join(sections) + "\n" + sources
    contract_text = (
        record["contracts"][-1]["text"] if record else read_text(paths["contract.md"])
    )
    handoff = "No handoff recorded."
    if paths["state.md"].exists():
        try:
            handoff = read_text(paths["state.md"])
        except RctlError:
            handoff = "Handoff unavailable; inspect state.md."
    labels = (
        "\nGoverning contract (includes criteria):\n",
        f"\n{label} (reported progress):\n",
    )
    remaining = budget - len(header) - sum(map(len, labels))
    if compact:
        reminder = bounded(header + labels[1] + handoff, budget, paths["state.md"])
    elif remaining < 100:
        reminder = bounded(header, budget, paths["contract.md"])
    else:
        contract_budget = min(len(contract_text), remaining // 2)
        handoff_budget = min(len(handoff), remaining - contract_budget)
        reminder = (
            header
            + labels[0]
            + bounded(contract_text, remaining - handoff_budget, paths["contract.md"])
        )
        reminder += labels[1] + bounded(handoff, handoff_budget, paths["state.md"])
    # Added JSON summaries must not bypass the reminder's bounds.
    status["handoff"] = {
        key: bounded(value, limits[key], paths["state.md"]) if value else None
        for key, value in reported.items()
    }
    status["title"] = bounded(status["title"], min(200, budget), paths["contract.md"])
    if report:
        status["verification"] = {
            key: report[key] for key in ("id", "verdict", "contract_revision", "cycle")
        }
    return {**status, "available": True, "context": reminder}, warnings
