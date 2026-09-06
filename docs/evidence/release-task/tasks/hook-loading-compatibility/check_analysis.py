"""Independent consistency check against retained host observations."""

import collections
import json
import re
from pathlib import Path


def expected_route(mode):
    root = Path("evidence") / mode
    summary = json.loads((root / "summary.json").read_text())
    events = [json.loads(line) for line in (root / "events.jsonl").read_text().splitlines()]
    sessions = sorted({event["thread_id"] for event in events if event.get("type") == "thread.started"})
    receipt_path = root / "receipts.jsonl"
    receipts = [json.loads(line) for line in receipt_path.read_text().splitlines()] if receipt_path.exists() else []
    counts = dict(collections.Counter(receipt["event"] for receipt in receipts))
    final = (root / "final.txt").read_text()
    model_reports_task = all(value in final for value in ("retained-comparison", "active", "B0", "C1"))
    complete = (summary["exit_code"] == 0 and counts.get("SessionStart", 0) > 0
                and counts.get("UserPromptSubmit", 0) > 0
                and all(receipt["session_id"] in sessions for receipt in receipts) and model_reports_task)
    return dict(exit_code=summary["exit_code"], receipts_total=len(receipts), events=counts,
                session_ids=sessions, model_reports_task=model_reports_task, delivery_complete=complete)


def main():
    actual = json.loads(Path("evidence/analysis.json").read_text())
    expected = {mode: expected_route(mode) for mode in ("inline", "project", "none")}
    assert actual["routes"] == expected, "Derived route observations differ from raw evidence"
    control = (expected["none"]["exit_code"] == 0 and expected["none"]["receipts_total"] == 0
               and "NO_RCTL_REMINDER" in Path("evidence/none/final.txt").read_text())
    assessment = "inconclusive"
    if expected["inline"]["delivery_complete"] and control:
        if expected["project"]["delivery_complete"]:
            assessment = "supported"
        elif expected["project"]["exit_code"] == 0:
            assessment = "not_supported"
    assert actual["assessment"] == assessment, "Assessment differs from fixed comparison rule"
    result = Path("result.md").read_text()
    assert re.search(r"^assessment: " + assessment + r"$", result, re.MULTILINE), "Result assessment differs"
    print(f"PASS retained real-host analysis: {assessment}; receipts=" + str({k: v['receipts_total'] for k, v in expected.items()}))


if __name__ == "__main__":
    main()
