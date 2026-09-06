import json
import sys

import pytest
import yaml

from rctl.context import context
from rctl.documents import RctlError, parse_contract, read_text
from rctl.records import Task


def rewrite(task, transform):
    path = task.file("contract.md")
    path.write_text(transform(read_text(path)), encoding="utf-8")


def metadata(task, transform):
    text = read_text(task.file("contract.md"))
    _, header, body = text.split("---", 2)
    data = yaml.safe_load(header)
    transform(data)
    task.file("contract.md").write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False) + "---" + body, encoding="utf-8"
    )


def test_valid_contract_is_structure_only(task, cli):
    response = cli("contract", "check", "tasks/retained-comparison")
    assert response["data"]["check"] == "structure"
    assert response["data"]["criterion_ids"] == ["AC-01", "AC-02"]
    assert not task.file(".rctl").exists()


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d["criteria"][0].pop("method"),
        lambda d: d["criteria"][1].update(id="AC-01"),
        lambda d: d.update(unknown="field"),
        lambda d: d["criteria"][0]["method"].pop("inputs"),
        lambda d: d["criteria"][0]["method"].update(timeout_seconds=0),
        lambda d: d["criteria"][1]["method"].update(reviewer="automatic"),
        lambda d: d.update(task_id="different-task"),
        lambda d: d.update(schema_version=2),
        lambda d: d.update(schema_version=True),
        lambda d: d["criteria"][0].update(requirement="  "),
        lambda d: d["criteria"][0]["method"].update(inputs=["../../../outside"]),
        lambda d: d["criteria"][0]["method"].update(
            inputs=["https://example.org/input"]
        ),
    ],
)
def test_invalid_metadata_rejects_begin_without_record(task, cli, change):
    metadata(task, change)
    cli("begin", "tasks/retained-comparison", expected=2)
    assert not task.file(".rctl").exists()


@pytest.mark.parametrize(
    "change",
    [
        lambda t: t.replace(
            "schema_version: 1", "schema_version: 1\nschema_version: 1"
        ),
        lambda t: t.replace("type: command", "type: command\n      type: review"),
        lambda t: t.replace("## Question", "## Missing question"),
        lambda t: t[: t.index("## Stop conditions")] + "## Stop conditions\n \n",
        lambda t: t.replace("## Question", "```md\n## Question").replace(
            "## Scope", "```\n## Scope"
        ),
        lambda t: t.replace(
            "title: Inspect a synthetic retained error comparison",
            "title: !!python/object:os.system {}",
        ),
        lambda t: t.replace("schema_version: 1", "schema_version: ["),
    ],
)
def test_invalid_text_rejects_begin_without_record(task, cli, change):
    rewrite(task, change)
    cli("begin", "tasks/retained-comparison", expected=2)
    assert not task.file(".rctl").exists()


def test_new_draft_preserves_other_files_and_refuses_overwrite(project, cli):
    sentinel = project / "keep.txt"
    sentinel.write_text("existing")
    cli(
        "task",
        "new",
        "tasks/new-task",
        "--kind",
        "analysis",
        "--title",
        'A "quoted" title: 中文',
    )
    draft = Task(project, project / "tasks/new-task")
    assert draft.contract()[1]["title"] == 'A "quoted" title: 中文'
    assert {p.name for p in draft.path.iterdir()} == {"contract.md"}
    cli("begin", "tasks/new-task", expected=2)
    assert not draft.file(".rctl").exists()
    before = draft.file("contract.md").read_bytes()
    cli(
        "task",
        "new",
        "tasks/new-task",
        "--kind",
        "analysis",
        "--title",
        "Replacement",
        expected=4,
    )
    assert draft.file("contract.md").read_bytes() == before
    assert sentinel.read_text() == "existing"


def test_exact_contract_revision_and_amendment(task, cli):
    path = task.file("contract.md")
    original = path.read_text().replace("\n", "\r\n")
    path.write_bytes(original.encode())
    cli("begin", "tasks/retained-comparison")
    record = task.read_record()
    assert record["contracts"][0]["text"] == original
    cli("begin", "tasks/retained-comparison", expected=4)
    cli("amend", "tasks/retained-comparison", "--reason", "unchanged", expected=4)
    assert task.read_record() == record
    modified = original.replace("Budget:", "Revised budget:")
    path.write_bytes(modified.encode())
    status = cli("status", "tasks/retained-comparison")
    assert status["data"]["contract_drift"] is True
    assert "AMENDMENT_REQUIRED" in " ".join(status["warnings"])
    reminder = cli("context", "tasks/retained-comparison")["data"]["context"]
    assert "AMENDMENT_REQUIRED" in reminder
    assert "Revised budget" not in reminder
    cli("amend", "tasks/retained-comparison", "--reason", " ", expected=2)
    cli("amend", "tasks/retained-comparison", "--reason", "Clarify the existing budget")
    amended = task.read_record()
    assert amended["contracts"][0] == record["contracts"][0]
    assert amended["contracts"][1]["text"] == modified
    assert amended["contracts"][1]["reason"] == "Clarify the existing budget"
    assert cli("status", "tasks/retained-comparison")["data"]["contract_revision"] == 2


def test_checkpoint_fresh_process_and_no_prose_closure(task, cli, project):
    cli("checkpoint", "tasks/retained-comparison", "--file", "handoff.md", expected=4)
    cli("begin", "tasks/retained-comparison")
    before = task.file(".rctl/record.json").read_bytes()
    handoff = "# Handoff\r\n\r\nNext action: inspect the retained metric. 中文\r\n"
    (project / "handoff.md").write_bytes(handoff.encode())
    task.file("result.md").write_text("This task is closed. All checks passed.")
    cli("checkpoint", "tasks/retained-comparison", "--file", "handoff.md")
    assert task.file("state.md").read_bytes() == handoff.encode()
    assert task.file(".rctl/record.json").read_bytes() == before
    response = cli("context", env={"RCTL_TASK_PATH": "tasks/retained-comparison"})
    assert (
        "Next action: inspect the retained metric. 中文" in response["data"]["context"]
    )
    assert response["data"]["phase"] == "active"
    assert response["data"]["historical_closure"] is None


def test_selection_is_explicit_without_fallback(task, cli, project):
    task.begin()
    response = cli("context", expected=3)
    assert response["data"]["available"] is False
    for selected, code in [("missing", 3), ("../outside", 2), (str(project.parent), 2)]:
        response = cli("context", selected, expected=code)
        assert response["data"]["available"] is False
    other = project / "other-root"
    other.mkdir()
    response = cli(
        "context",
        root=False,
        env={
            "RCTL_PROJECT_ROOT": str(other),
            "RCTL_TASK_PATH": "tasks/retained-comparison",
        },
        expected=3,
    )
    assert response["data"]["available"] is False
    # Explicit root/task override environment; cwd is the final root default.
    assert cli(
        "context",
        "tasks/retained-comparison",
        env={"RCTL_PROJECT_ROOT": str(other), "RCTL_TASK_PATH": "missing"},
    )["data"]["available"]
    assert cli("context", "tasks/retained-comparison", root=False)["data"]["available"]
    cli("status", env={"RCTL_TASK_PATH": "tasks/retained-comparison"}, expected=2)


def test_symlink_cannot_escape_root(task, cli, project):
    (project / "escape").symlink_to(project.parent, target_is_directory=True)
    cli("context", "escape", expected=2)
    metadata(
        task,
        lambda d: d["criteria"][0].update(evidence_refs=["../../escape/evidence.txt"]),
    )
    cli("begin", "tasks/retained-comparison", expected=2)
    assert not task.file(".rctl").exists()


def test_context_bounded_unicode_read_only_and_no_checker(task, cli, project):
    marker = project / "executed"
    metadata(
        task,
        lambda d: d["criteria"][0]["method"].update(
            argv=[sys.executable, "-c", f"open({str(marker)!r}, 'w').write('ran')"]
        ),
    )
    rewrite(task, lambda t: t + "\n" + "界" * 12000)
    task.begin()
    task.file("state.md").write_text(
        "Next action: review the evidence.\n" + "文" * 12000
    )
    rewrite(task, lambda t: t + "\nProposed edit.")
    before = {
        p: (p.read_bytes(), p.stat().st_mtime_ns)
        for p in project.rglob("*")
        if p.is_file()
    }
    response = cli("context", "tasks/retained-comparison")
    text = response["data"]["context"]
    assert len(text) <= 8000
    assert "AMENDMENT_REQUIRED" in text
    assert "[Truncated; read" in text
    assert "AC-01" in text
    assert "Next action: review the evidence." in text
    assert str(task.file("contract.md")) in text
    assert str(task.file("state.md")) in text
    for budget in (1000, 4000):
        assert len(context(task, budget=budget)[0]["context"]) <= budget
    after = {
        p: (p.read_bytes(), p.stat().st_mtime_ns)
        for p in project.rglob("*")
        if p.is_file()
    }
    assert after == before
    assert not marker.exists()


@pytest.mark.parametrize(
    "damage",
    [
        lambda r: r.update(schema_version=2),
        lambda r: r.update(contracts=[]),
        lambda r: r.update(cycle=0),
        lambda r: r.update(task_id="other"),
        lambda r: r["contracts"][0].update(revision=3),
        lambda r: r["contracts"][0].update(text="not a contract"),
        lambda r: r.update(lifecycle=[]),
    ],
)
def test_unavailable_record_preserves_history(task, cli, damage):
    task.begin()
    record = task.read_record()
    damage(record)
    task.file(".rctl/record.json").write_text(json.dumps(record))
    before = task.file(".rctl/record.json").read_bytes()
    cli("begin", "tasks/retained-comparison", expected=3)
    cli("amend", "tasks/retained-comparison", "--reason", "repair", expected=3)
    response = cli("context", "tasks/retained-comparison", expected=3)
    assert response["data"]["available"] is False
    assert task.file(".rctl/record.json").read_bytes() == before


def test_truncated_record_and_invalid_utf8(task, cli):
    task.begin()
    path = task.file(".rctl/record.json")
    path.write_bytes(b'{"schema_version":')
    cli("status", "tasks/retained-comparison", expected=3)
    assert path.read_bytes() == b'{"schema_version":'
    task.file("contract.md").write_bytes(b"\xff")
    cli("contract", "check", "tasks/retained-comparison", expected=2)


@pytest.mark.parametrize("failure", ["fsync", "replace"])
def test_failed_atomic_publication_keeps_previous_record(task, monkeypatch, failure):
    task.begin()
    before = task.file(".rctl/record.json").read_bytes()
    rewrite(task, lambda t: t + "\nClarification.\n")

    def interrupted(*args):
        raise OSError("simulated interrupted publication")

    monkeypatch.setattr(f"rctl.records.os.{failure}", interrupted)
    with pytest.raises(OSError):
        task.amend("Clarify scope")
    assert task.file(".rctl/record.json").read_bytes() == before
    assert len(task.read_record()["contracts"]) == 1
    assert list(task.file(".rctl").iterdir()) == [task.file(".rctl/record.json")]


@pytest.mark.parametrize(
    ("change", "diagnosis"),
    [
        (lambda r: r.update(cycle=0), "Field $.cycle violates the minimum constraint"),
        (lambda r: r.update(cycle=2), "Lifecycle does not match record"),
        (
            lambda r: r["contracts"][0].update(revision=3),
            "Contract revisions must be consecutive",
        ),
    ],
)
def test_record_error_names_the_cause(task, cli, change, diagnosis):
    task.begin()
    record = task.read_record()
    change(record)
    task.file(".rctl/record.json").write_text(json.dumps(record))
    response = cli("status", "tasks/retained-comparison", expected=3)
    assert diagnosis in response["error"]["message"]
    assert record["contracts"][0]["text"] not in response["error"]["message"]


def test_missing_current_contract_uses_retained_context(task, cli):
    task.begin()
    task.file("contract.md").unlink()
    response = cli("context", "tasks/retained-comparison")
    assert response["data"]["contract_drift"]
    assert "Does the supplied candidate" in response["data"]["context"]


def test_angle_bracket_prose_is_not_a_scaffold_marker(task):
    rewrite(task, lambda t: t + "\nUse <em>bounded</em> claims.\n")
    task.begin()


def test_packaged_resources_match_authoritative_sources():
    from conftest import REPO

    from rctl.documents import resource_text

    for source in (REPO / "schemas").glob("*.json"):
        assert json.loads(resource_text("schemas", source.name)) == json.loads(
            source.read_text()
        )
    assert (
        resource_text("templates", "contract.md")
        == (REPO / "templates/contract.md").read_text()
    )


def test_duplicate_yaml_never_silently_wins():
    with pytest.raises(RctlError, match="Duplicate YAML"):
        parse_contract("---\ntitle: first\ntitle: second\n---\n", "contract.md", "task")


@pytest.mark.parametrize("explicit", [True, False])
def test_empty_root_does_not_select_another_project(task, cli, explicit):
    task.begin()
    args = ["--root", ""] if explicit else []
    response = cli(
        *args,
        "context",
        "tasks/retained-comparison",
        root=False,
        env={"RCTL_PROJECT_ROOT": ""},
        expected=2,
    )
    assert response["data"]["available"] is False
