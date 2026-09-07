import shutil
import subprocess
import sys

import pytest
from conftest import REPO
from test_m1 import metadata

from rctl.documents import RctlError, sections
from rctl.handoff import extract
from rctl.hooks.codex import handle
from rctl.maintenance import doctor, export_update


@pytest.mark.parametrize("verified", [False, True])
def test_relocated_evidence_keeps_status_and_reminders(
    task, cli, tmp_path_factory, monkeypatch, verified
):
    shutil.copytree(
        REPO / "examples/retained-comparison", task.path, dirs_exist_ok=True
    )
    metadata(
        task,
        lambda data: data["criteria"][0]["method"].update(
            argv=[sys.executable, "check_arithmetic.py"]
        ),
    )
    task.begin()
    path = "tasks/retained-comparison"
    if verified:
        cli("verify", path, "--reviews", f"{path}/reviews.json")
    task.file("state.md").write_text("## Next action\nInspect the retained results.\n")
    record = task.file(".rctl/record.json").read_bytes()
    evidence = task.path / "evidence"
    external = tmp_path_factory.mktemp("external") / "evidence"
    evidence.rename(external)
    evidence.symlink_to(external, target_is_directory=True)

    status = cli("status", path)["data"]
    assert status["phase"] == "active"
    assert status["title"] == "Inspect a synthetic retained error comparison"
    assert status["currentness"] == ("unknown" if verified else "not_checked")
    assert "Inspect the retained results." in cli("context", path)["data"]["context"]
    row = cli("task", "list")["data"]["tasks"][0]
    assert row["phase"] == "active" and row["error"] is None
    monkeypatch.setenv("RCTL_TASK_PATH", path)
    monkeypatch.delenv("RCTL_HOOK_LOG", raising=False)
    for event in ("SessionStart", "UserPromptSubmit"):
        output = handle(
            {"hook_event_name": event, "cwd": str(task.root)}, str(task.root)
        )["hookSpecificOutput"]["additionalContext"]
        assert "Inspect the retained results." in output
        assert "rctl context unavailable" not in output
    cli("verify", path, "--reviews", f"{path}/reviews.json", expected=2)
    assert task.file(".rctl/record.json").read_bytes() == record


@pytest.mark.parametrize("fence", ["```", "~~~~"])
def test_handoff_preserves_command_and_ignores_fenced_headings(task, fence):
    command = f"Run:\n\n{fence}sh\nuv run pytest -k retained\n## Blockers\n{fence}\n\nThen record the outcome."
    text = f"## Next action\n{command}\n\n## Blockers\nNone\n"
    assert extract(text) == ({"next_action": command, "blockers": "None"}, [])
    assert sections(text)["Next action"] == command
    task.begin()
    task.file("state.md").write_text(text)
    from rctl.context import context

    assert task.status()[0]["handoff"]["next_action"] == command
    for compact, budget in ((True, 2000), (False, 8000)):
        result = context(task, compact=compact, budget=budget)[0]
        assert command in result["context"]
        assert result["handoff"]["next_action"] == command


def test_inline_backticks_and_nonclosing_fences_preserve_handoff():
    action = "```command``` should be run.\nThen record the outcome."
    assert extract(f"## Next action\n{action}\n## Blockers\nNone") == (
        {"next_action": action, "blockers": "None"},
        [],
    )
    text = "```md\n```not a closing fence\n## Next action\nExample only\n```\n## Next action\nActual work"
    assert extract(text) == ({"next_action": "Actual work", "blockers": None}, [])
    assert sections(text) == {"Next action": "Actual work"}


def test_doctor_symlinked_skill_uses_logical_paths(cli, project):
    cli("init")
    skill = project / ".agents/skills/research-task"
    target = project / "shared/research-task"
    target.parent.mkdir()
    skill.rename(target)
    skill.symlink_to(target, target_is_directory=True)
    data = cli("doctor")["data"]
    assert not data["review_needed"]
    assert all(f["status"] == "current" for f in data["findings"])
    (target / "local.txt").write_text("Local instructions\n")
    extras = [f for f in cli("doctor")["data"]["findings"] if f["status"] == "extra"]
    assert [f["path"] for f in extras] == [".agents/skills/research-task/local.txt"]
    cli("update", "export", "candidate")
    assert not (project / "candidate/diffs").exists()
    assert (target / "local.txt").read_text() == "Local instructions\n"


def test_doctor_ignores_finder_metadata(cli, project):
    cli("init")
    metadata_file = project / ".agents/skills/research-task/.DS_Store"
    metadata_file.write_bytes(b"\xff\x00Finder metadata")
    assert not cli("doctor")["data"]["review_needed"]
    assert metadata_file.read_bytes() == b"\xff\x00Finder metadata"


def test_missing_entrypoint_preserves_diagnostics(cli, project, monkeypatch):
    cli("init", "--codex")
    (project / ".agents/skills/research-task/SKILL.md").write_text("Local edit\n")
    monkeypatch.setattr(sys, "executable", str(project / "missing-env/python"))
    data, _ = doctor(project, True)
    assert data["codex_inspected"] and data["review_needed"]
    assert any(
        f["path"].endswith("SKILL.md") and f["status"] == "different"
        for f in data["findings"]
    )
    assert any(
        f["path"] == "codex:entrypoint" and f["status"] == "unavailable"
        for f in data["findings"]
    )
    assert any("different rctl environment" in f["message"] for f in data["findings"])
    with pytest.raises(RctlError, match="entrypoint is unavailable"):
        export_update(project, "candidate", True)
    assert not (project / "candidate").exists()


def test_task_directory_collision_is_actionable(cli, project):
    (project / "tasks").write_text("A file, not a task directory")
    result = cli("task", "list", expected=2)
    assert "Expected directory: tasks" in result["error"]["message"]


def test_task_alias_has_one_canonical_identity(task, cli):
    task.begin()
    (task.path.parent / "alias").symlink_to(task.path, target_is_directory=True)
    rows = cli("task", "list")["data"]["tasks"]
    assert len(rows) == 1
    assert rows[0]["task_id"] == task.read_record()["task_id"]
    assert rows[0]["path"] == "tasks/retained-comparison"


def test_task_title_display_is_one_bounded_line(task, cli):
    title = "First line\nSecond line " + "long title " * 100
    metadata(task, lambda data: data.update(title=title))
    task.begin()
    assert cli("task", "list")["data"]["tasks"][0]["title"] == title
    result = subprocess.run(
        [sys.executable, "-m", "rctl", "--root", str(task.root), "task", "list"],
        capture_output=True,
        text=True,
        check=True,
    )
    rows = [line for line in result.stdout.splitlines() if not line.startswith("  ")]
    assert len(rows) == 1
    displayed = rows[0].split(" | ")[1]
    assert displayed.startswith("First line Second line ")
    assert len(displayed) == 160 and displayed.endswith("...")
