import json
import subprocess
import sys

import pytest

from rctl.context import context
from rctl.handoff import extract
from rctl.maintenance import doctor, export_update
from rctl.records import Task


def snapshot(root):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file()
    }


def test_task_discovery_mixed_phases_damage_and_frozen_title(task, cli, project):
    task.begin()
    task.file("contract.md").write_text(
        task.file("contract.md").read_text().replace("title:", "proposed_title:")
    )
    cli(
        "task",
        "new",
        "tasks/draft",
        "--kind",
        "exploration",
        "--title",
        "Pending question",
    )
    cancelled = Task(project, project / "tasks/cancelled")
    cancelled.new("analysis", "To cancel")
    cancelled.file("contract.md").write_text(
        task.read_record()["contracts"][0]["text"].replace(
            "retained-comparison", "cancelled"
        )
    )
    cancelled.begin()
    cancelled.cancel("No further work")
    damaged = project / "tasks/damaged/.rctl"
    damaged.mkdir(parents=True)
    (damaged / "record.json").write_text("{")
    (project / "tasks/unrelated").mkdir()
    (project / "tasks/nested/tasks").mkdir(parents=True)
    (project / "tasks/nested/tasks/contract.md").write_text("not a top-level task")
    before = snapshot(project)
    rows = cli("task", "list")["data"]["tasks"]
    assert [r["task_id"] for r in rows] == [
        "cancelled",
        "damaged",
        "draft",
        "retained-comparison",
    ]
    assert rows[-1]["phase"] == "active" and rows[-1]["title"]
    assert rows[1]["phase"] is None and rows[1]["error"]["code"] == "RECORD_UNAVAILABLE"
    assert [
        r["task_id"] for r in cli("task", "list", "--phase", "active")["data"]["tasks"]
    ] == ["damaged", "retained-comparison"]
    assert snapshot(project) == before
    result = subprocess.run(
        [sys.executable, "-m", "rctl", "--root", str(project), "task", "list"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    for row in rows:
        assert row["path"] in result.stdout
        assert row["title"] is None or row["title"] in result.stdout
    assert "RECORD_UNAVAILABLE" in result.stdout


def test_empty_list_and_selection_independence(cli, project):
    assert cli("task", "list", env={"RCTL_TASK_PATH": "../bad"})["data"]["tasks"] == []
    (project / "tasks").mkdir()
    assert cli("task", "list")["data"]["tasks"] == []
    (project / "tasks/escape").symlink_to(project.parent, target_is_directory=True)
    assert cli("task", "list")["data"]["tasks"][0]["error"]["code"] == "INVALID_INPUT"


@pytest.mark.parametrize(
    "text,expected,blockers",
    [
        (
            "## Next action\n\n检查证据。\n保留结论。\n\n## Blockers\n\nWaiting for data.\n",
            "检查证据。\n保留结论。",
            "Waiting for data.",
        ),
        (
            "- Last verified progress: done\n- Next action: Inspect files.\n  Then summarize.\n- Blockers: None\n",
            "Inspect files.\n  Then summarize.",
            "None",
        ),
        ("Next action: Inspect metrics.\n\nOther narrative.", "Inspect metrics.", None),
        (
            "```md\n## Next action\nWrong example\n```\n## Next action\nActual work\n",
            "Actual work",
            None,
        ),
        ("~~~\nNext action: false\n~~~\nNo explicit step.", None, None),
        ("## Next action\n<One concrete continuation step.>\n", None, None),
        ("## Next action\nOne\n## Next action\nTwo\n", None, None),
        ("Next action: One\nNext action: Two\n", None, None),
    ],
)
def test_explicit_handoff_forms(text, expected, blockers):
    result, warnings = extract(text)
    assert result == {"next_action": expected, "blockers": blockers}
    assert bool(warnings) == (expected is None)


def test_late_handoff_survives_budgets_and_is_historical(task, cli, project):
    task.begin()
    state = (
        "# Handoff\n\n## Progress\n"
        + ("Old work.\n" * 2500)
        + "\n## Next action\nInspect the retained error table.\n\n## Blockers\nAwait the operator decision.\n"
    )
    source = project / "checkpoint.md"
    source.write_text(state)
    record = task.file(".rctl/record.json").read_bytes()
    cli("checkpoint", "tasks/retained-comparison", "--file", "checkpoint.md")
    assert task.file(".rctl/record.json").read_bytes() == record
    assert task.file("state.md").read_text() == state
    for compact, budget in ((True, 2000), (False, 8000)):
        response, _ = context(task, budget=budget, compact=compact)
        text = response["context"]
        assert len(text) <= budget
        assert "Next action: Inspect the retained error table." in text
        assert "Await the operator decision." in text
        assert "state.md" in text and "No verification" in text
        assert text.index("Inspect the retained") < text.index("Old work.")
    task.cancel("Pause route permanently")
    text = context(task, budget=2000, compact=True)[0]["context"]
    assert "Historical handoff — Next action:" in text
    assert "Reported handoff — Next action:" not in text
    assert "Reopen" in text


def test_handoff_does_not_smuggle_unbounded_json(task):
    task.begin()
    task.file("state.md").write_text(
        "## Next action\n" + "界" * 20000 + "\n## Blockers\n" + "文" * 20000
    )
    data = context(task, budget=2000, compact=True)[0]
    assert sum(len(v or "") for v in data["handoff"].values()) < 2000
    assert len(data["context"]) <= 2000
    task.file("state.md").write_bytes(b"\xff")
    status, warnings = task.status()
    assert status["phase"] == "active" and status["handoff"]["next_action"] is None
    assert any("unavailable" in warning for warning in warnings)


def test_doctor_customizations_and_candidate_export(cli, project):
    cli("init", "--vault", "notes", "--codex")
    assert not cli("doctor", "--codex")["data"]["review_needed"]
    assert not cli("doctor")["data"]["codex_inspected"]
    skill = project / ".agents/skills/research-task"
    (skill / "SKILL.md").write_text("Intentional local instructions\n")
    (skill / "local.txt").write_text("Keep me\n")
    before = snapshot(project)
    inspection = cli("doctor", "--codex")["data"]
    assert inspection["review_needed"]
    assert any(
        f["status"] == "different" and f["path"].endswith("SKILL.md")
        for f in inspection["findings"]
    )
    assert any(f["status"] == "extra" for f in inspection["findings"])
    cli("update", "export", ".work/candidates", "--codex")
    after = snapshot(project)
    assert {k: after[k] for k in before} == before
    assert all(k.startswith(".work/candidates/") for k in after.keys() - before.keys())
    bundle = project / ".work/candidates"
    assert (
        bundle / "candidates/.agents/skills/research-task/SKILL.md"
    ).read_text() != "Intentional local instructions\n"
    assert (
        "Intentional local instructions"
        in (bundle / "diffs/.agents/skills/research-task/SKILL.md.diff").read_text()
    )
    assert "MERGE FRAGMENTS" in (bundle / "README.md").read_text()
    cli("update", "export", ".work/candidates", expected=4)
    for destination in ("notes/update", "tasks/update", ".agents/update", "../update"):
        cli("update", "export", destination, expected=2)
    assert snapshot(project) == after


@pytest.mark.parametrize(
    "damage,fragment",
    [
        ("missing-skill", "unavailable"),
        ("json", "invalid"),
        ("toml", "invalid"),
        ("root", "command root"),
        ("executable", "executable is missing"),
        ("duplicate", "duplicate"),
        ("missing-hook", "missing"),
        ("disabled", "disabled"),
        ("wrapper", "unrecognized"),
    ],
)
def test_doctor_actionable_failures(cli, project, damage, fragment):
    cli("init", "--codex")
    hooks_file = project / ".codex/hooks.json"
    hooks = json.loads(hooks_file.read_text())
    handler = hooks["hooks"]["SessionStart"][0]["hooks"][0]
    if damage == "missing-skill":
        (project / ".agents/skills/research-task/SKILL.md").unlink()
    elif damage == "root":
        handler["command"] = handler["command"].replace(
            str(project), str(project.parent)
        )
    elif damage == "executable":
        handler["command"] = "/nonexistent/rctl --root " + str(project) + " hook codex"
    elif damage == "wrapper":
        handler["command"] = "custom-wrapper " + handler["command"]
    elif damage == "duplicate":
        hooks["hooks"]["SessionStart"].append(hooks["hooks"]["SessionStart"][0])
    elif damage == "missing-hook":
        del hooks["hooks"]["SessionStart"]
    elif damage == "disabled":
        (project / ".codex/config.toml").write_text("[features]\nhooks = false\n")
    hooks_file.write_text(json.dumps(hooks))
    if damage == "json":
        hooks_file.write_text("{")
    elif damage == "toml":
        (project / ".codex/config.toml").write_text("[")
    before = snapshot(project)
    data = cli("doctor", "--codex")["data"]
    assert data["review_needed"]
    assert any(fragment in f["status"] + f["message"] for f in data["findings"])
    assert snapshot(project) == before


def test_inline_hooks_and_unrelated_configuration(cli, project):
    cli("init", "--codex")
    from rctl.integration import inline_arguments

    hooks_file = project / ".codex/hooks.json"
    hooks = json.loads(hooks_file.read_text())
    inline = inline_arguments(hooks)
    (project / ".codex/config.toml").write_text(
        'model = "local-choice"\n' + "\n".join(inline[1::2])
    )
    hooks_file.write_text(
        json.dumps(
            {
                "hooks": {
                    "Stop": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "echo unrelated-preserved",
                                }
                            ]
                        }
                    ]
                }
            }
        )
    )
    data = cli("doctor", "--codex")["data"]
    assert not data["review_needed"]
    assert any(f["status"] == "inherited" for f in data["findings"])
    before = snapshot(project)
    cli("update", "export", "candidate", "--codex")
    for diff in (project / "candidate/diffs").rglob("*.diff"):
        assert "local-choice" not in diff.read_text()
        assert "unrelated-preserved" not in diff.read_text()
    assert all((project / p).read_bytes() == v for p, v in before.items())


def test_unavailable_binding_and_default_no_host_inspection(cli, project):
    cli("init", "--vault", "notes")
    (project / ".codex").mkdir()
    (project / ".codex/hooks.json").write_text("{")
    assert not cli("doctor")["data"]["review_needed"]
    (project / ".rctl/project.json").write_text("{")
    assert cli("doctor")["data"]["review_needed"]
    cli("update", "export", "candidate", expected=2)
    assert not (project / "candidate").exists()


def test_doctor_does_not_execute_hooks(cli, project):
    cli("init", "--codex")
    hooks = project / ".codex/hooks.json"
    data = json.loads(hooks.read_text())
    data["hooks"]["SessionStart"][0]["hooks"][0]["command"] = (
        "rctl --version; touch SHOULD_NOT_EXIST"
    )
    hooks.write_text(json.dumps(data))
    assert doctor(project, True)[0]["review_needed"]
    export_update(project, "candidate", True)
    assert not (project / "SHOULD_NOT_EXIST").exists()
