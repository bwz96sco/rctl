"""The read Interface preserves facts while projections stay independent of I/O."""

import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from test_m2 import REVIEWS, TASK
from test_m2 import ready as ready
from test_m7 import guidance

from rctl.context import context, render
from rctl.project_context import read_project


def test_snapshot_and_nested_evidence_are_immutable(ready):
    ready.verify(REVIEWS)
    snapshot = ready.snapshot()
    with pytest.raises(FrozenInstanceError):
        snapshot.phase = "closed"
    with pytest.raises(TypeError):
        snapshot.handoff["next_action"] = "Invent progress"
    with pytest.raises(TypeError):
        snapshot.verification["checks"][0]["verdict"] = "fail"

    exported = snapshot.status()
    exported["verification"]["checks"][0]["evidence_refs"].clear()
    exported["verification"]["checks"].clear()
    assert snapshot.status()["verification"]["checks"][0]["evidence_refs"]
    assert json.loads(json.dumps(snapshot.status())) == snapshot.status()
    assert ready.read_record()["phase"] == "active"


def test_new_snapshot_refreshes_handoff_and_evidence_without_rewriting_old_view(
    ready, cli
):
    ready.verify(REVIEWS)
    earlier = ready.snapshot()
    ready.file("state.md").write_text("## Next action\nInspect the retained table.\n")
    handoff = ready.snapshot()
    assert handoff.handoff["next_action"] == "Inspect the retained table."
    assert handoff.currentness == earlier.currentness == "current"
    assert earlier.handoff["next_action"] != handoff.handoff["next_action"]

    ready.file("input.txt").write_text("Changed evidence needing verification")
    current = ready.snapshot()
    assert current.currentness == "stale"
    assert earlier.currentness == "current"
    assert cli("status", TASK)["data"] == current.status()
    assert context(ready)[0]["currentness"] == "stale"
    row = cli("task", "list")["data"]["tasks"][0]
    for key, value in current.discovery().items():
        assert row[key] == value
    cli("close", TASK, expected=4)


def test_projections_need_no_files_and_budgets_share_one_layout(ready, monkeypatch):
    guidance(ready.root)
    ready.file("state.md").write_text(
        "## Next action\nInspect the scoped result.\n\n## Blockers\nNone.\n"
    )
    ready.verify(REVIEWS)
    snapshot = ready.snapshot()
    project, warnings = read_project(ready.root)
    expected = snapshot.status()

    def no_io(*args, **kwargs):
        raise AssertionError("A projection attempted another filesystem read")

    monkeypatch.setattr(Path, "open", no_io)
    monkeypatch.setattr(Path, "stat", no_io)
    reminders = []
    for budget in (2000, 8000):
        data = render(
            ready.root,
            project,
            snapshot,
            list(snapshot.warnings) + warnings,
            None,
            True,
            budget,
            task_path=snapshot.path,
        )
        reminders.append(data["context"])
        assert data["question"] == snapshot.question
        assert data["verification"] == snapshot.verification_summary()
        assert len(data["context"]) <= budget
        assert "C: T/.rctl/record.json contracts[-1].text (accepted)" in data["context"]
    assert reminders[0] == reminders[1]
    assert "Governing contract (includes criteria)" not in reminders[0]
    assert snapshot.status() == expected
    assert snapshot.discovery()["currentness"] == "current"
