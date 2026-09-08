"""Project guidance and short-reminder regressions from the Pinyin VSR pilot."""

import json

import pytest
from test_m3 import hook

from rctl.context import context, load_context
from rctl.documents import RctlError
from rctl.project_context import read_project
from rctl.records import Task


def guidance(root, current="Coverage does not substitute for lower error."):
    directory = root / "research"
    directory.mkdir(exist_ok=True)
    (directory / "PROGRAM.md").write_text(
        "# Program\n\n## Goal\nReduce comparable error.\n\n## Current guidance\n"
        + current
        + "\n\n## Old interpretations\nOld content is not current guidance.\n"
    )
    (directory / "ROUTES.md").write_text(
        "# Routes\n\n## Reuse Rule\nRead related mechanisms and cite their reopen condition.\n"
        "\n## Routes\n### R01\nHistorical route details stay here.\n"
    )


def test_no_selection_and_bad_selection_preserve_project(cli, project, task):
    guidance(project)
    task.begin()
    before = task.file(".rctl/record.json").read_bytes()
    data = cli("context")["data"]
    assert data["available"] and data["project"]["available"]
    assert not data["task_selected"] and not data["task_available"]
    assert "phase" not in data
    assert "Reduce comparable error." in data["context"]
    assert "Historical route details" not in data["context"]
    for selection, code in (("missing", 3), ("../outside", 2), ("", 3)):
        response = cli("context", selection, expected=code)
        assert response["data"]["available"]
        assert response["data"]["task_selected"]
        assert not response["data"]["task_available"]
        assert "Reduce comparable error." in response["data"]["context"]
        assert response["error"]["code"] in response["data"]["context"]
    assert task.file(".rctl/record.json").read_bytes() == before


def test_damaged_record_keeps_guidance_and_original_error(cli, project, task):
    guidance(project)
    task.begin()
    task.file(".rctl/record.json").write_text("{")
    response = cli("context", "tasks/retained-comparison", expected=3)
    assert response["error"]["code"] == "RECORD_UNAVAILABLE"
    assert response["data"]["project"]["current_guidance"].startswith("Coverage")
    assert response["warnings"] == []
    assert task.file(".rctl/record.json").read_text() == "{"


def test_missing_project_files_do_not_break_task(cli, task):
    task.begin()
    response = cli("context", "tasks/retained-comparison")
    assert response["data"]["task_available"]
    assert not response["data"]["project"]["available"]
    assert response["data"]["phase"] == "active"
    assert any("PROGRAM.md" in warning for warning in response["warnings"])


@pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
def test_hooks_keep_project_without_task_and_refresh(task, event):
    guidance(task.root)
    payload = {"hook_event_name": event, "source": "compact", "cwd": str(task.root)}
    first, _ = hook(task, payload, selection=False)
    assert "Coverage does not" in first["hookSpecificOutput"]["additionalContext"]
    guidance(
        task.root, "CURRENT: the new result supersedes the earlier coverage claim."
    )
    second, _ = hook(task, payload, extra_env={"RCTL_TASK_PATH": "missing"})
    text = second["hookSpecificOutput"]["additionalContext"]
    assert "CURRENT:" in text and "Coverage does not" not in text
    assert "Task context unavailable" in text
    assert "NOT_FOUND" in text


@pytest.mark.parametrize(
    "bad", ["duplicate", "placeholder", "invalid-utf8", "directory", "escape"]
)
def test_bad_project_source_does_not_poison_other_source(project, bad):
    guidance(project)
    path = project / "research/PROGRAM.md"
    if bad == "duplicate":
        path.write_text(path.read_text() + "\n## Goal\nConflicting goal.\n")
    elif bad == "placeholder":
        path.write_text(
            "## Goal\n<State goal.>\n## Current guidance\n<Add guidance.>\n"
        )
    elif bad == "invalid-utf8":
        path.write_bytes(b"\xff")
    elif bad == "directory":
        path.unlink()
        path.mkdir()
    else:
        path.unlink()
        path.symlink_to(project.parent / "outside-guidance.md")
    data, warnings = read_project(project)
    assert data["goal"] is None and data["current_guidance"] is None
    assert data["reuse_rule"].startswith("Read related mechanisms")
    assert warnings


def test_fenced_headings_are_content_and_not_guidance(project):
    guidance(project)
    path = project / "research/PROGRAM.md"
    path.write_text(
        "# Program\n```md\n## Goal\nFake goal.\n```\n"
        "## Goal\nActual goal.\n## Current guidance\nRun:\n"
        "```sh\necho retained\n## Goal\n```\nThen inspect.\n"
    )
    data, warnings = read_project(project)
    assert data["goal"] == "Actual goal."
    assert "echo retained\n## Goal" in data["current_guidance"]
    assert not warnings


@pytest.mark.parametrize("budget,compact", [(2000, True), (8000, False)])
def test_long_reminder_keeps_real_content_and_is_readonly(task, budget, compact):
    guidance(
        task.root,
        "CORRECTION: preserve comparable error as the objective. " + "Detail. " * 100,
    )
    long_path = task.root / "tasks" / ("research-task-" + "x" * 65)
    task.path.rename(long_path)
    # Keep the task identity consistent in the draft before begin.
    path = long_path / "contract.md"
    path.write_text(path.read_text().replace("retained-comparison", long_path.name))
    task = Task(task.root, long_path)
    task.begin()
    task.file("state.md").write_text(
        "## Progress\n"
        + "OLD_PROGRESS " * 2000
        + "\n## Next action\nNEXT: inspect the exported judgments. "
        + "Details. " * 500
        + "\n## Blockers\nBLOCKED: no matching export is available. "
        + "Details. " * 500
    )
    before = {p: p.read_bytes() for p in task.root.rglob("*") if p.is_file()}
    data, _ = context(task, budget, compact)
    text = data["context"]
    assert len(text) <= budget
    for value in (
        "Reduce comparable error.",
        "CORRECTION:",
        "NEXT:",
        "BLOCKED:",
        "No verification",
    ):
        assert value in text
    assert "T/state.md" in text and "P: research/PROGRAM.md" in text
    assert text.count(str(task.root)) == 1
    assert sum(len(v or "") for v in data["handoff"].values()) < budget
    assert (
        sum(
            len(data["project"][k] or "")
            for k in ("goal", "current_guidance", "reuse_rule")
        )
        < budget
    )
    assert (
        ("OLD_PROGRESS" not in text)
        if compact
        else (text.index("BLOCKED:") < text.index("OLD_PROGRESS"))
    )
    assert {p: p.read_bytes() for p in task.root.rglob("*") if p.is_file()} == before


def test_short_fields_release_space_and_tiny_budget_is_nullable(project):
    guidance(project, "Review the revised source. " * 40)
    data, _ = load_context(project, budget=2000, compact=True)
    assert "Truncated" not in data["project"]["current_guidance"]
    data, _ = load_context(project, budget=10, compact=True)
    assert len(data["context"]) <= 10
    assert data["project"]["current_guidance"] is None


def test_unavailable_task_exception_retains_bounded_context(project):
    guidance(project)
    with pytest.raises(RctlError) as caught:
        load_context(project, "missing", budget=2000, compact=True)
    data = caught.value.data
    assert data["task_available"] is False
    assert len(data["context"]) <= 2000
    assert "Reduce comparable error" in json.dumps(data)
