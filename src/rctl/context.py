"""Read-only reminders shared by terminal and future host integration."""

from .documents import RctlError, read_text

DEFAULT_BUDGET = 8000


def bounded(text, budget, source):
    if len(text) <= budget:
        return text
    suffix = f"\n[Truncated; read {source}]"
    if len(suffix) >= budget:
        return "[Truncated]"[:budget]
    return text[: budget - len(suffix)] + suffix


def context(task, budget=DEFAULT_BUDGET):
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
    lines = [
        f"Task: {status['task_id']}",
        f"Phase: {status['phase']}; governing revision: {status['contract_revision'] or 'none'}",
        f"Verification: {verification}; applicability: {status['currentness']}; historical closure: {historical}",
        *[f"Warning: {warning}" for warning in warnings],
        f"Next action: {status['next_action']}",
    ]
    lines.extend(f"{name}: {path}" for name, path in paths.items())
    orientation = task.root / "research/README.md"
    if orientation.is_file():
        lines.append(f"Project orientation: {orientation}")
    # Prefer the retained agreement when a proposed edit is incomplete or invalid.
    contract_text = (
        record["contracts"][-1]["text"] if record else read_text(paths["contract.md"])
    )
    handoff = "No handoff recorded."
    if paths["state.md"].exists():
        try:
            handoff = read_text(paths["state.md"])
        except RctlError:
            warning = "Handoff unavailable; inspect state.md."
            warnings.append(warning)
            lines.insert(3, f"Warning: {warning}")
            handoff = warning
    header = "\n".join(lines) + "\n"
    labels = (
        "\nGoverning contract (includes criteria):\n",
        "\nHandoff (reported progress):\n",
    )
    remaining = budget - len(header) - sum(map(len, labels))
    if remaining < 100:
        reminder = bounded(header, budget, paths["contract.md"])
    else:
        contract_budget = min(len(contract_text), remaining // 2)
        handoff_budget = min(len(handoff), remaining - contract_budget)
        contract_budget = remaining - handoff_budget
        reminder = (
            header
            + labels[0]
            + bounded(contract_text, contract_budget, paths["contract.md"])
        )
        reminder += labels[1] + bounded(handoff, handoff_budget, paths["state.md"])
    # Context's JSON surface must not smuggle the unbounded report/result into a reminder.
    if report:
        status["verification"] = {
            key: report[key] for key in ("id", "verdict", "contract_revision", "cycle")
        }
    return {**status, "available": True, "context": reminder}, warnings
