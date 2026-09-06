"""Derive the frozen three-route comparison from retained host observations."""

import json
from collections import Counter
from pathlib import Path


EVIDENCE = Path(__file__).resolve().parent / "evidence"


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def analyze_route(name):
    directory = EVIDENCE / name
    summary = json.loads((directory / "summary.json").read_text())
    host_events = read_rows(directory / "events.jsonl")
    receipts = read_rows(directory / "receipts.jsonl")
    final = (directory / "final.txt").read_text()
    session_ids = sorted({
        event["thread_id"]
        for event in host_events
        if event.get("type") == "thread.started"
    })
    counts = dict(sorted(Counter(receipt["event"] for receipt in receipts).items()))
    reports_task = all(
        token in final for token in ("retained-comparison", "active", "B0", "C1")
    )
    bound_to_launch = len(session_ids) == 1 and all(
        receipt.get("session_id") == session_ids[0] for receipt in receipts
    )
    complete = (
        summary["exit_code"] == 0
        and counts.get("SessionStart", 0) > 0
        and counts.get("UserPromptSubmit", 0) > 0
        and bound_to_launch
        and reports_task
    )
    return {
        "exit_code": summary["exit_code"],
        "receipts_total": len(receipts),
        "events": counts,
        "session_ids": session_ids,
        "model_reports_task": reports_task,
        "delivery_complete": complete,
    }, final


def main():
    routes = {}
    finals = {}
    for name in ("inline", "project", "none"):
        routes[name], finals[name] = analyze_route(name)

    control_valid = (
        routes["none"]["exit_code"] == 0
        and routes["none"]["receipts_total"] == 0
        and "NO_RCTL_REMINDER" in finals["none"]
    )
    assessment = "inconclusive"
    if routes["inline"]["delivery_complete"] and control_valid:
        if routes["project"]["delivery_complete"]:
            assessment = "supported"
        elif routes["project"]["exit_code"] == 0:
            assessment = "not_supported"

    analysis = {"routes": routes, "assessment": assessment}
    output = json.dumps(analysis, indent=2) + "\n"
    (EVIDENCE / "analysis.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
