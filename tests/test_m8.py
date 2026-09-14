"""Governing-question alignment regressions from the OR C15 scope-drift case."""

import json
import shutil
import sys

import pytest
from conftest import REPO
from test_m1 import metadata, rewrite
from test_m3 import hook

from rctl.context import context
from rctl.documents import resource_text

TASK = "tasks/retained-comparison"
REVIEWS = f"{TASK}/reviews.json"
QUESTION = "Does the supplied candidate meet the fixed improvement rule"
MECHANISM = "Combine complementary logical components across generated programs."
NON_CLAIM = "The broader cross-candidate mechanism is not decided."


def add_alignment(task, source="research/questions/C15.md#mechanism", extra=""):
    block = f"""## Question alignment

- Governing question source: {source}
- Governing mechanism: {MECHANISM}
- This task tests: The organization increment after both arms receive the same records.
- This task does not decide: {NON_CLAIM}
{extra}
"""
    rewrite(task, lambda text: text.replace("## Scope", block + "\n## Scope"))


def question_source(task):
    path = task.root / "research/questions/C15.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# C15\n\n## Mechanism\nCombine complementary logic.\n")
    return path


@pytest.fixture
def aligned(task):
    question_source(task)
    add_alignment(task)
    return task


@pytest.fixture
def aligned_ready(aligned):
    shutil.copytree(
        REPO / "examples/retained-comparison", aligned.path, dirs_exist_ok=True
    )
    add_alignment(aligned)
    aligned.file("check.py").write_text(
        "import pathlib\nprint(pathlib.Path('input.txt').read_text())\n"
    )
    aligned.file("input.txt").write_text("retained evidence")
    metadata(
        aligned,
        lambda data: data["criteria"][0]["method"].update(
            argv=[sys.executable, "check.py"],
            inputs=["check.py", "input.txt"],
            timeout_seconds=5,
        ),
    )
    aligned.begin()
    return aligned


def test_alignment_is_structural_and_legacy_contracts_remain_valid(aligned, task, cli):
    data = aligned.contract()[1]
    assert data["question"].startswith(QUESTION)
    assert data["question_alignment"] == {
        "source": "research/questions/C15.md#mechanism",
        "mechanism": MECHANISM,
        "tests": "The organization increment after both arms receive the same records.",
        "does_not_decide": NON_CLAIM,
    }
    response = cli("contract", "check", TASK)
    assert response["data"]["question_alignment"] == data["question_alignment"]

    rewrite(
        task,
        lambda text: (
            text.split("## Question alignment", 1)[0]
            + "## Scope"
            + text.split("## Scope", 1)[1]
        ),
    )
    assert task.contract()[1]["question_alignment"] is None


@pytest.mark.parametrize(
    ("change", "source"),
    [
        (lambda text: text.replace("- Governing mechanism:", "- Other field:"), None),
        (lambda text: text.replace(f"- Governing mechanism: {MECHANISM}\n", ""), None),
        (
            lambda text: text.replace(
                f"- Governing mechanism: {MECHANISM}",
                f"- Governing mechanism: {MECHANISM}\n- Governing mechanism: duplicate",
            ),
            None,
        ),
        (
            lambda text: text.replace("\n## Scope", "\nUnexpected prose.\n\n## Scope"),
            None,
        ),
        (lambda text: text.replace("Question alignment", "Question Alignment"), None),
        (lambda text: text, "/tmp/C15.md"),
        (lambda text: text, "https://example.com/C15.md"),
        (lambda text: text, "../outside.md"),
        (lambda text: text, "research/questions/missing.md"),
        (lambda text: text, "research/questions/C15.txt"),
    ],
)
def test_invalid_alignment_rejects_begin_without_record(task, cli, change, source):
    question_source(task)
    add_alignment(task, source=source or "research/questions/C15.md")
    rewrite(task, change)
    cli("begin", TASK, expected=2)
    assert not task.file(".rctl").exists()


def test_unreadable_alignment_source_rejects_draft(task, cli):
    path = task.root / "research/questions/unreadable.md"
    path.mkdir(parents=True)
    add_alignment(task, source="research/questions/unreadable.md")
    cli("contract", "check", TASK, expected=2)


@pytest.mark.parametrize("budget,compact", [(2000, True), (8000, False)])
def test_governing_question_precedes_mutable_guidance_and_survives_drift(
    aligned, budget, compact
):
    research = aligned.root / "research"
    (research / "PROGRAM.md").write_text(
        "## Goal\nRetain the actual question.\n\n## Current guidance\n"
        + "MUTABLE WRONG SUMMARY. " * 600
    )
    (research / "ROUTES.md").write_text(
        "## Reuse Rule\nRead the governing source before proposing work.\n"
    )
    aligned.begin()
    aligned.file("state.md").write_text(
        "## Next action\nInspect the scoped result.\n\n## Blockers\nNo blocker.\n"
    )
    rewrite(
        aligned,
        lambda text: text.replace("Does the supplied candidate", "DRIFTED QUESTION"),
    )

    data, warnings = context(aligned, budget=budget, compact=compact)
    reminder = data["context"]
    assert QUESTION in reminder
    assert "DRIFTED QUESTION" not in reminder
    assert reminder.index("Governing task question") < reminder.index(
        "Current guidance"
    )
    for value in (MECHANISM, NON_CLAIM, "Inspect the scoped result", "No blocker"):
        assert value in reminder
    assert data["question"].startswith(QUESTION)
    assert data["question_alignment"]["does_not_decide"] == NON_CLAIM
    assert any("AMENDMENT_REQUIRED" in warning for warning in warnings)
    assert len(reminder) <= budget


def test_verified_assessment_is_bound_to_task_question(aligned_ready, cli):
    cli("verify", TASK, "--reviews", REVIEWS)
    status = cli("status", TASK)["data"]
    assert status["question"].startswith(QUESTION)
    assert status["assessment"] == {
        "value": "not_supported",
        "verification_id": "V0001",
        "contract_revision": 1,
        "currentness": "current",
    }
    reminder = context(aligned_ready, budget=2000, compact=True)[0]["context"]
    assert "Task assessment: not_supported" in reminder
    assert "The broader cross-candidate mechanism is not decided" in reminder

    cli("close", TASK)
    question_source(aligned_ready).unlink()
    status_response = cli("status", TASK)
    assert status_response["data"]["phase"] == "closed"
    assert (
        status_response["data"]["historical_closure"]["assessment"] == "not_supported"
    )
    assert any(
        "Question alignment source unavailable" in item
        for item in status_response["warnings"]
    )


def test_alignment_source_can_be_declared_review_evidence(aligned_ready, cli):
    source_ref = "../../research/questions/C15.md"
    metadata(
        aligned_ready,
        lambda data: data["criteria"][1]["evidence_refs"].append(source_ref),
    )
    aligned_ready.amend("Review the governing-question relationship")
    aligned_ready.file("result.md").write_text(
        aligned_ready.file("result.md")
        .read_text()
        .replace("contract_revision: 1", "contract_revision: 2")
    )
    reviews_path = aligned_ready.file("reviews.json")
    reviews = json.loads(reviews_path.read_text())
    reviews["contract_revision"] = 2
    reviews["checks"][0]["evidence_refs"].append(source_ref)
    reviews_path.write_text(json.dumps(reviews))

    cli("verify", TASK, "--reviews", REVIEWS)
    question_source(aligned_ready).write_text("Changed governing question.\n")
    status = cli("status", TASK)["data"]
    assert status["assessment"]["currentness"] == "stale"
    assert status["currentness"] == "stale"


def test_legacy_task_has_question_without_invented_alignment_or_assessment(task, cli):
    task.begin()
    status = cli("status", TASK)["data"]
    assert status["question"].startswith(QUESTION)
    assert status["question_alignment"] is None
    assert status["assessment"] is None


@pytest.mark.parametrize("event", ["SessionStart", "UserPromptSubmit"])
def test_existing_hook_shape_delivers_governing_question(aligned, event):
    aligned.begin()
    payload = {
        "hook_event_name": event,
        "source": "compact" if event == "SessionStart" else "startup",
        "cwd": str(aligned.root),
    }
    response, stderr = hook(aligned, payload)
    assert not stderr
    output = response["hookSpecificOutput"]
    assert output["hookEventName"] == event
    assert QUESTION in output["additionalContext"]
    assert NON_CLAIM in output["additionalContext"]


def test_packaged_template_and_skill_explain_question_alignment():
    contract = resource_text("templates", "contract.md")
    template_guide = resource_text("templates", "README.md")
    skill = resource_text("skills", "research-task/SKILL.md")
    task_files = resource_text("skills", "research-task/references/task-files.md")
    assert "optional Question alignment" in contract
    for text in (template_guide, skill, task_files):
        assert "Governing question source" in text
        assert "This task does not decide" in text
        assert "review criterion" in text
