"""A task cannot omit the declared goal judgment or confuse it with local pass."""

import json
import re
import shutil
import socket
from contextlib import contextmanager
from threading import Thread

import pytest
from conftest import REPO
from test_m1 import metadata

from rctl.context import context
from rctl.documents import RctlError
from rctl.records import Task

TASK = "tasks/retained-comparison"
REVIEWS = f"{TASK}/reviews.json"
CONTRIBUTION = {
    "obligation": "Determine whether this candidate supports lower comparable error.",
    "expected_output": "A checked fixed-threshold comparison and scoped investment decision.",
    "decision_use": "Promote only supported improvement; stop this candidate on a worse result.",
    "review_criterion": "AC-03",
}
IMPACT = {
    "claim_effect": "contradicts",
    "claim_reason": "The synthetic candidate is worse by 0.03; arithmetic correctness supplies no improvement.",
    "remaining_gap": "No real-data benefit or general method conclusion is established.",
    "next_decision": "stop",
    "decision_reason": "The frozen candidate fails its improvement rule; no renewed run is justified.",
}


def write_goal(root):
    path = root / "research/PROGRAM.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Program\n\n## Goal\nEstablish lower comparable error.\n", encoding="utf-8")
    return path


def add_goal(task):
    def change(data):
        data["goal_contribution"] = CONTRIBUTION.copy()
        data["criteria"].append({
            "id": "AC-03",
            "requirement": "Review what the result establishes for the project goal and next investment.",
            "evidence_refs": ["result.md", "evidence/metrics.json"],
            "failure_action": "Supply the missing judgment; do not promote a local pass to goal support.",
            "method": {"type": "review", "reviewer": "either"},
        })
    metadata(task, change)


def add_review(task):
    path = task.file("reviews.json")
    data = json.loads(path.read_text())
    data["checks"].append({
        "criterion_id": "AC-03",
        "verdict": "pass",
        "reviewer": "agent",
        "rationale": "Inspected the goal, fixed inputs, arithmetic and scoped result; an honest negative completes this decision task.",
        "evidence_refs": ["result.md", "evidence/metrics.json"],
        "goal_impact": IMPACT.copy(),
    })
    path.write_text(json.dumps(data), encoding="utf-8")


@pytest.fixture
def goal_task(task):
    shutil.copytree(REPO / "examples/retained-comparison", task.path, dirs_exist_ok=True)
    write_goal(task.root)
    add_goal(task)
    add_review(task)
    return task


@contextmanager
def edit_program_during_check(task, replacement):
    """Synchronize a cooperating editor with a real read-only command check."""
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(10)
        port = listener.getsockname()[1]
        checker = task.file("check_arithmetic.py")
        checker.write_text(
            "import socket\n"
            f"with socket.create_connection(('127.0.0.1', {port}), timeout=10) as channel:\n"
            "    channel.sendall(b'C')\n"
            "    assert channel.recv(1) == b'1'\n"
            + checker.read_text()
        )
        errors = []

        def edit():
            try:
                channel, _ = listener.accept()
                with channel:
                    channel.settimeout(10)
                    assert channel.recv(1) == b"C"
                    program = task.root / "research/PROGRAM.md"
                    if replacement is None:
                        program.unlink()
                    else:
                        program.write_text(replacement, encoding="utf-8")
                    channel.sendall(b"1")
            except Exception as error:
                errors.append(error)

        editor = Thread(target=edit)
        editor.start()
        try:
            yield
        finally:
            editor.join(timeout=12)
            assert not editor.is_alive(), "Program editor did not finish."
            if errors:
                raise errors[0]


def test_new_work_cannot_omit_goal_review(task, cli):
    write_goal(task.root)
    for args in (("contract", "check", TASK), ("begin", TASK)):
        response = cli(*args, expected=2)
        assert "goal_contribution" in response["error"]["message"]
    assert task.read_record() is None
    # Read-only discovery of an incomplete draft remains possible.
    assert cli("status", TASK)["data"]["phase"] == "draft"


@pytest.mark.parametrize("field", ["obligation", "expected_output", "decision_use", "review_criterion"])
def test_incomplete_entry_rejected(goal_task, cli, field):
    metadata(goal_task, lambda d: d["goal_contribution"].pop(field))
    cli("begin", TASK, expected=2)
    assert goal_task.read_record() is None


@pytest.mark.parametrize("change", [
    lambda d: d["goal_contribution"].update(review_criterion="AC-99"),
    lambda d: d["goal_contribution"].update(review_criterion="AC-01"),
    lambda d: d["criteria"][-1].update(evidence_refs=["evidence/metrics.json"]),
    lambda d: d["criteria"][-1].update(evidence_refs=["result.md"]),
    lambda d: d["criteria"][-1].update(evidence_refs=["../../research/PROGRAM.md", "result.md"]),
])
def test_goal_entry_requires_real_review_and_evidence(goal_task, cli, change):
    metadata(goal_task, change)
    cli("begin", TASK, expected=2)
    assert goal_task.read_record() is None


def test_missing_goal_review_blocks_close_even_with_other_passes(goal_task, cli):
    goal_task.begin()
    path = goal_task.file("reviews.json")
    data = json.loads(path.read_text())
    data["checks"].pop()
    path.write_text(json.dumps(data))
    response = cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    checks = response["data"]["checks"]
    assert [c["verdict"] for c in checks] == ["pass", "pass", "unknown"]
    cli("close", TASK, expected=5)
    assert goal_task.read_record()["phase"] == "active"


@pytest.mark.parametrize("field", [None, "claim_effect", "claim_reason", "remaining_gap", "next_decision", "decision_reason"])
def test_incomplete_closeout_rejected_before_checks(goal_task, cli, field):
    goal_task.begin()
    path = goal_task.file("reviews.json")
    data = json.loads(path.read_text())
    check = data["checks"][-1]
    if field is None:
        check.pop("goal_impact")
    else:
        check["goal_impact"].pop(field)
    path.write_text(json.dumps(data))
    cli("verify", TASK, "--reviews", REVIEWS, expected=2)
    assert not goal_task.read_record()["verifications"]


def test_negative_goal_decision_closes_without_becoming_goal_support(goal_task, cli):
    goal_task.begin()
    response = cli("verify", TASK, "--reviews", REVIEWS)
    assert response["data"]["verdict"] == "pass"
    assert response["data"]["checks"][-1]["goal_impact"] == IMPACT
    assert response["data"]["checks"][-1]["reviewed_goal"] == "Establish lower comparable error."
    cli("close", TASK)
    status = cli("status", TASK)["data"]
    assert status["phase"] == "closed" and status["currentness"] == "current"
    assert status["assessment"]["value"] == "not_supported"
    assert status["goal_contribution"] == CONTRIBUTION
    assert status["goal_impact"]["claim_effect"] == "contradicts"
    assert status["goal_impact"]["next_decision"] == "stop"
    assert status["goal_impact"]["review_verdict"] == "pass"
    for budget in (2000, 8000):
        data, _ = context(goal_task, budget)
        assert len(data["context"]) <= budget
        assert data["goal_impact"]["next_decision"] == "stop"
        assert "investment: stop" in data["context"]
        assert "contradicts" in data["context"]


def test_changed_goal_prevents_close(goal_task, cli):
    goal_task.begin()
    cli("verify", TASK, "--reviews", REVIEWS)
    path = goal_task.root / "research/PROGRAM.md"
    path.write_text(path.read_text().replace("lower comparable error", "lower cost"))
    assert cli("status", TASK)["data"]["goal_impact"]["currentness"] == "stale"
    response = cli("close", TASK, expected=4)
    assert "Project Goal changed" in response["error"]["message"]


@pytest.mark.parametrize("review_first", [False, True])
def test_goal_change_during_verify_retains_original_goal_and_blocks_close(goal_task, cli, review_first):
    if review_first:
        metadata(goal_task, lambda d: d["criteria"].insert(0, d["criteria"].pop()))
    replacement = "# Program\n\n## Goal\nEstablish lower execution cost.\n"
    with edit_program_during_check(goal_task, replacement):
        goal_task.begin()
        response = cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    checks = {c["criterion_id"]: c for c in response["data"]["checks"]}
    assert checks["AC-01"]["verdict"] == "pass"
    assert checks["AC-03"]["verdict"] == "unknown"
    assert checks["AC-03"]["reviewed_goal"] == "Establish lower comparable error."
    assert "during verification" in checks["AC-03"]["rationale"]
    report = cli("status", TASK)["data"]["verification"]
    assert report["subject_issues"] and report["verdict"] == "unknown"
    assert json.loads(report["review_input_text"])["checks"][-1]["goal_impact"] == IMPACT
    cli("close", TASK, expected=4)
    assert goal_task.read_record()["phase"] == "active"
    write_goal(goal_task.root)
    # Restoring the Goal cannot turn the interrupted judgment into a pass.
    cli("close", TASK, expected=5)


@pytest.mark.parametrize(("replacement", "close_exit"), [
    (None, 4),
    ("# Program\n\n## Goal\n<Goal>\n", 4),
    ("## Goal\nOriginal goal.\n\n## Goal\nDuplicate goal.\n", 5),
])
def test_goal_unavailable_during_verify_keeps_original_goal_and_unknown_review(goal_task, cli, replacement, close_exit):
    with edit_program_during_check(goal_task, replacement):
        goal_task.begin()
        response = cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    check = response["data"]["checks"][-1]
    assert check["verdict"] == "unknown"
    assert check["reviewed_goal"] == "Establish lower comparable error."
    assert "during verification" in check["rationale"]
    cli("close", TASK, expected=close_exit)


@pytest.mark.parametrize("replacement", [
    "# Program\n\n## Goal\nEstablish lower\n  comparable error.\n",
    "# Program\n\n## Goal\nEstablish lower comparable error.\n\n## Current guidance\nStop this candidate.\n",
])
def test_goal_reflow_or_guidance_edit_during_verify_keeps_review_current(goal_task, cli, replacement):
    with edit_program_during_check(goal_task, replacement):
        goal_task.begin()
        response = cli("verify", TASK, "--reviews", REVIEWS)
    check = response["data"]["checks"][-1]
    assert check["verdict"] == "pass"
    assert check["reviewed_goal"] == "Establish lower comparable error."
    status = cli("status", TASK)["data"]
    assert status["goal_impact"]["currentness"] == "current"
    assert status["verification"]["subject_issues"] == []
    cli("close", TASK)


def test_guidance_edits_keep_goal_review_current(goal_task, cli):
    # Corrections and closeout promotion edit PROGRAM outside its Goal section.
    goal_task.begin()
    cli("verify", TASK, "--reviews", REVIEWS)
    path = goal_task.root / "research/PROGRAM.md"
    path.write_text(path.read_text() + "\n## Current guidance\nA new correction.\n")
    cli("close", TASK)
    path.write_text(path.read_text() + "Promoted: stop this candidate.\n")
    status = cli("status", TASK)["data"]
    assert status["currentness"] == "current"
    assert status["goal_impact"]["currentness"] == "current"
    row = cli("task", "list")["data"]["tasks"][0]
    assert row["goal_decision"] == {
        "next_decision": "stop", "claim_effect": "contradicts", "currentness": "current"
    }


def test_cited_program_stales_task_but_not_goal_decision(goal_task, cli):
    # A reviewer naturally cites the PROGRAM file it read for the Goal.
    path = goal_task.file("reviews.json")
    data = json.loads(path.read_text())
    data["checks"][-1]["evidence_refs"].append("../../research/PROGRAM.md")
    path.write_text(json.dumps(data))
    goal_task.begin()
    cli("verify", TASK, "--reviews", REVIEWS)
    program = goal_task.root / "research/PROGRAM.md"
    program.write_text(program.read_text() + "\n## Current guidance\nA new correction.\n")
    # Closure still follows report-wide observation of cited files.
    cli("close", TASK, expected=4)
    cli("verify", TASK, "--reviews", REVIEWS)
    cli("close", TASK)
    program.write_text(program.read_text() + "Promoted: stop this candidate.\n")
    status = cli("status", TASK)["data"]
    assert status["currentness"] == "stale"
    assert status["goal_impact"]["currentness"] == "current"
    assert cli("task", "list")["data"]["tasks"][0]["goal_decision"]["currentness"] == "current"
    assert "V0002 / current / pass" in context(goal_task, 2000)[0]["context"]


def test_reflowed_goal_keeps_review_current(goal_task, cli):
    goal_task.begin()
    cli("verify", TASK, "--reviews", REVIEWS)
    path = goal_task.root / "research/PROGRAM.md"
    path.write_text(path.read_text().replace("lower comparable", "lower\n  comparable"))
    assert cli("status", TASK)["data"]["goal_impact"]["currentness"] == "current"
    cli("close", TASK)


def test_unavailable_goal_leaves_goal_review_unknown(goal_task, cli):
    goal_task.begin()
    (goal_task.root / "research/PROGRAM.md").write_text("# Program\n\n## Goal\n<Goal>\n")
    response = cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    check = response["data"]["checks"][-1]
    assert check["verdict"] == "unknown" and "Project Goal unavailable" in check["rationale"]
    assert "reviewed_goal" not in check


def test_missing_goal_evidence_blocks_close(goal_task, cli):
    ref = "evidence/goal-observation.json"
    goal_task.file(ref).write_text('{"observation": "retained"}')
    metadata(goal_task, lambda d: d["criteria"][-1]["evidence_refs"].append(ref))
    path = goal_task.file("reviews.json")
    data = json.loads(path.read_text())
    data["checks"][-1]["evidence_refs"].append(ref)
    path.write_text(json.dumps(data))
    goal_task.begin()
    goal_task.file(ref).unlink()
    response = cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    assert [c["verdict"] for c in response["data"]["checks"]] == ["pass", "pass", "unknown"]
    cli("close", TASK, expected=4)


def test_amendment_does_not_project_previous_goal_review_as_current(goal_task, cli):
    goal_task.begin()
    cli("verify", TASK, "--reviews", REVIEWS)
    metadata(goal_task, lambda d: d["goal_contribution"].update(obligation="A newly bounded obligation."))
    cli("amend", TASK, "--reason", "Specify a different bounded goal obligation")
    status = cli("status", TASK)["data"]
    assert status["goal_contribution"]["obligation"] == "A newly bounded obligation."
    assert status["goal_impact"] is None
    assert status["currentness"] == "stale"
    assert context(goal_task, 2000)[0]["goal_impact"] is None


def test_old_agreement_survives_but_new_amendment_requires_goal(task, cli):
    shutil.copytree(REPO / "examples/retained-comparison", task.path, dirs_exist_ok=True)
    task.begin()
    write_goal(task.root)
    cli("contract", "check", TASK)
    cli("verify", TASK, "--reviews", REVIEWS)
    cli("close", TASK)
    status = cli("status", TASK)["data"]
    assert status["goal_impact"] is None
    assert status["goal_contribution"] is None
    assert status["historical_closure"]
    assert cli("task", "list")["data"]["tasks"][0]["goal_decision"] is None
    cli("reopen", TASK, "--reason", "A new planned increment")
    path = task.file("contract.md")
    path.write_text(path.read_text() + "\nNew scoped work.\n")
    cli("contract", "check", TASK, expected=2)
    cli("amend", TASK, "--reason", "Declare the next work", expected=2)


def test_new_project_draft_scaffolds_goal_and_required_review(project, cli):
    write_goal(project)
    cli("task", "new", "tasks/new-work", "--kind", "analysis", "--title", "Bounded work")
    task = Task(project, project / "tasks/new-work")
    data = task.contract()[1]
    assert data["goal_contribution"]["review_criterion"] == "AC-02"
    assert data["criteria"][-1]["method"]["type"] == "review"
    assert data["criteria"][-1]["evidence_refs"] == ["result.md", "<Primary task evidence file>"]
    with pytest.raises(RctlError, match="authoring placeholders"):
        task.begin()


def test_standalone_task_still_works_without_project_goal(task):
    assert task.contract()[1]["goal_contribution"] is None
    task.begin()


@pytest.mark.parametrize("has_goal", [False, True])
def test_fully_authored_generated_draft_can_begin(project, cli, has_goal):
    if has_goal:
        write_goal(project)
    cli("task", "new", "tasks/new-work", "--kind", "analysis", "--title", "Bounded work")
    task = Task(project, project / "tasks/new-work")
    path = task.file("contract.md")
    # Author the active fields; instructional comments must not leave a hidden
    # bundled placeholder which blocks a completed agreement.
    path.write_text("\n".join(
        line if line.startswith("# ") else re.sub(r"<[^<>]+>", "Declared agreement", line)
        for line in path.read_text().splitlines()
    ) + "\n")
    task.begin()
    assert task.read_record()["phase"] == "active"
