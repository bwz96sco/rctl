import json
import os
import shutil
import signal
import subprocess
import sys
import time

import pytest
from conftest import REPO
from test_m1 import metadata, rewrite

from rctl import __version__
from rctl.documents import RctlError, read_text
from rctl.records import Task

TASK = "tasks/retained-comparison"
REVIEWS = f"{TASK}/reviews.json"


@pytest.fixture
def ready(task):
    example = REPO / "examples/retained-comparison"
    shutil.copytree(example, task.path, dirs_exist_ok=True)
    task.file("check.py").write_text(
        "import pathlib, sys\n"
        "print('actual stdout: ' + pathlib.Path('input.txt').read_text())\n"
        "print('actual stderr', file=sys.stderr)\n"
    )
    task.file("input.txt").write_text("retained evidence")
    metadata(
        task,
        lambda d: d["criteria"][0]["method"].update(
            argv=[sys.executable, "check.py"],
            inputs=["check.py", "input.txt"],
            timeout_seconds=5,
        ),
    )
    task.begin()
    return task


def report(task):
    return task.read_record()["verifications"][-1]


def review_edit(task, change):
    path = task.file("reviews.json")
    data = json.loads(path.read_text())
    change(data)
    path.write_text(json.dumps(data))


def verify_pass(task, cli):
    response = cli("verify", TASK, "--reviews", REVIEWS)
    assert response["data"]["verdict"] == "pass"
    return report(task)


def test_real_execution_negative_close_and_history(ready, cli):
    result = ready.file("result.md").read_bytes().replace(b"\n", b"\r\n")
    ready.file("result.md").write_bytes(result)
    reviews = ready.file("reviews.json").read_bytes()
    saved = verify_pass(ready, cli)
    assert saved["result_text"].encode() == result
    assert saved["review_input_text"].encode() == reviews
    assert saved["rctl_version"] == __version__
    assert saved["subject_issues"] == []
    execution = saved["checks"][0]["execution"]
    assert execution["argv"] == [sys.executable, "check.py"]
    assert execution["cwd"] == TASK
    assert execution["exit_code"] == 0
    assert execution["timed_out"] is False
    assert (
        ready.root / execution["stdout_ref"]
    ).read_text() == "actual stdout: retained evidence\n"
    assert (ready.root / execution["stderr_ref"]).read_text() == "actual stderr\n"
    observed = {item["path"] for item in saved["observed_files"]}
    assert {
        f"{TASK}/input.txt",
        f"{TASK}/check.py",
        execution["stdout_ref"],
        execution["stderr_ref"],
    } <= observed
    closure = cli("close", TASK)["data"]["closure"]
    assert closure["assessment"] == "not_supported"
    assert closure["verification_id"] == saved["id"]
    before = ready.file(".rctl/record.json").read_bytes()
    cli("close", TASK, expected=4)
    assert ready.file(".rctl/record.json").read_bytes() == before
    assert cli("status", TASK)["data"]["currentness"] == "current"


@pytest.mark.parametrize("assessment", ["supported", "inconclusive", "not_applicable"])
def test_assessment_is_separate_from_completion(ready, cli, assessment):
    path = ready.file("result.md")
    path.write_text(path.read_text().replace("not_supported", assessment))
    verify_pass(ready, cli)
    assert cli("close", TASK)["data"]["closure"]["assessment"] == assessment


@pytest.mark.parametrize(
    "subject", ["result.md", "input.txt", "check.py", "evidence/metrics.json", "stdout"]
)
def test_edited_verified_material_prevents_close(ready, cli, subject):
    saved = verify_pass(ready, cli)
    path = (
        ready.root / saved["checks"][0]["execution"]["stdout_ref"]
        if subject == "stdout"
        else ready.file(subject)
    )
    path.write_bytes(path.read_bytes() + b"\nchanged\n")
    assert cli("status", TASK)["data"]["currentness"] == "stale"
    response = cli("close", TASK, expected=4)
    assert response["error"]["code"] == "VERIFICATION_STALE"
    assert ready.read_record()["phase"] == "active"


def test_checkpoint_preserves_applicability(ready, cli):
    verify_pass(ready, cli)
    (ready.root / "handoff.md").write_text(
        "Next action: close using the recorded evidence."
    )
    cli("checkpoint", TASK, "--file", "handoff.md")
    assert cli("status", TASK)["data"]["currentness"] == "current"
    cli("close", TASK)


def test_later_failure_cannot_reuse_old_pass_and_collects_reviews(ready, cli):
    first = verify_pass(ready, cli)
    ready.file("check.py").write_text("import sys\nprint('FAILED')\nsys.exit(7)\n")
    response = cli("verify", TASK, "--reviews", REVIEWS, expected=4)
    assert response["data"]["verification_id"] == "V0002"
    assert response["error"]["code"] == "VERIFICATION_FAILED"
    assert "AC-01" in response["error"]["message"]
    assert "Correct the derived arithmetic" in response["error"]["next_action"]
    latest = report(ready)
    assert latest["checks"][0]["execution"]["exit_code"] == 7
    assert latest["checks"][1]["verdict"] == "pass"
    assert ready.read_record()["verifications"][0] == first
    cli("close", TASK, expected=4)
    assert cli("status", TASK)["data"]["currentness"] == "current"


@pytest.mark.parametrize(
    "missing", ["executable", "input", "review", "review-evidence"]
)
def test_missing_execution_or_evidence_saves_unknown(ready, cli, missing):
    if missing == "executable":
        metadata(
            ready,
            lambda d: d["criteria"][0]["method"].update(
                argv=["rctl-nonexistent-check-executable"]
            ),
        )
        ready.amend("Test unavailable checker")
        ready.file("result.md").write_text(
            ready.file("result.md")
            .read_text()
            .replace("contract_revision: 1", "contract_revision: 2")
        )
        review_edit(ready, lambda d: d.update(contract_revision=2))
    elif missing == "input":
        ready.file("input.txt").unlink()
    elif missing == "review-evidence":
        ready.file("evidence/metrics.json").unlink()
    args = [] if missing == "review" else ["--reviews", REVIEWS]
    response = cli("verify", TASK, *args, expected=5)
    assert response["data"]["verification_id"] == "V0001"
    assert report(ready)["verdict"] == "unknown"
    if missing in {"input", "executable"}:
        assert report(ready)["checks"][0]["execution"] is None
    cli("close", TASK, expected=4 if missing in {"input", "review-evidence"} else 5)
    assert ready.read_record()["phase"] == "active"


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d.update(task_id="other"),
        lambda d: d.update(contract_revision=2),
        lambda d: d["checks"].append(d["checks"][0].copy()),
        lambda d: d["checks"][0].update(criterion_id="AC-01"),
        lambda d: d["checks"][0].update(criterion_id="AC-99"),
        lambda d: d["checks"][0].update(evidence_refs=["result.md"]),
        lambda d: d["checks"][0].update(rationale=" "),
        lambda d: d["checks"][0].update(unknown="field"),
        lambda d: d["checks"][0]["evidence_refs"].append("../../../escaped.txt"),
    ],
)
def test_invalid_review_executes_nothing(ready, cli, change):
    review_edit(ready, change)
    before = ready.file(".rctl/record.json").read_bytes()
    cli("verify", TASK, "--reviews", REVIEWS, expected=2)
    assert ready.file(".rctl/record.json").read_bytes() == before
    assert not ready.file(".rctl/checks").exists()


@pytest.mark.parametrize("document", ["result.md", "reviews.json"])
def test_malformed_documents_execute_nothing(ready, cli, document):
    ready.file(document).write_text("not valid frontmatter or JSON")
    cli("verify", TASK, "--reviews", REVIEWS, expected=2)
    assert not ready.file(".rctl/checks").exists()
    assert ready.read_record()["verifications"] == []


def test_operator_source_and_extra_references(ready, cli):
    metadata(ready, lambda d: d["criteria"][1]["method"].update(reviewer="operator"))
    ready.amend("Require operator judgment")
    ready.file("result.md").write_text(
        ready.file("result.md")
        .read_text()
        .replace("contract_revision: 1", "contract_revision: 2")
    )
    review_edit(ready, lambda d: d.update(contract_revision=2))
    cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    assert report(ready)["checks"][1]["reviewer"] == "agent"
    ready.file("attachment.txt").write_text("Reviewed versioned source.")
    review_edit(
        ready,
        lambda d: d["checks"][0].update(
            reviewer="operator",
            evidence_refs=d["checks"][0]["evidence_refs"]
            + ["attachment.txt", "https://example.invalid/version-1"],
        ),
    )
    saved = verify_pass(ready, cli)
    assert saved["checks"][1]["reviewer"] == "operator"
    assert saved["external_refs"] == ["https://example.invalid/version-1"]
    assert f"{TASK}/attachment.txt" in {o["path"] for o in saved["observed_files"]}
    ready.file("attachment.txt").unlink()
    cli("close", TASK, expected=4)


def test_contract_amendment_guards_and_revision_binding(ready, cli):
    verify_pass(ready, cli)
    rewrite(ready, lambda t: t + "\nClarify scope.\n")
    for command in ("verify", "close"):
        assert cli(command, TASK, expected=4)["error"]["code"] == "AMENDMENT_REQUIRED"
    ready.amend("Clarify scope")
    assert cli("close", TASK, expected=4)["error"]["code"] == "VERIFICATION_STALE"
    response = cli("verify", TASK, expected=2)
    assert (
        "revision 1" in response["error"]["message"]
        and "revision 2" in response["error"]["message"]
    )
    assert len(ready.read_record()["verifications"]) == 1


def test_close_without_result_or_report_does_not_claim_closure(ready, cli):
    ready.file("result.md").unlink()
    cli("close", TASK, expected=4)
    cli("verify", TASK, expected=3)
    assert ready.read_record()["closures"] == []


def test_reopen_requires_new_cycle_and_retains_history(ready, cli):
    verify_pass(ready, cli)
    closed = cli("close", TASK)["data"]["closure"]
    ready.file("result.md").write_bytes(
        ready.file("result.md").read_bytes() + b"\nUpdated interpretation.\n"
    )
    status = cli("status", TASK)["data"]
    assert status["phase"] == "closed" and status["currentness"] == "stale"
    assert status["historical_closure"] == closed
    reminder = cli("context", TASK)["data"]["context"]
    assert (
        "historical closure: V0001" in reminder and "differs from verified" in reminder
    )
    for command, args in [
        ("verify", []),
        ("amend", ["--reason", "edit"]),
        ("checkpoint", ["--file", REVIEWS]),
        ("cancel", ["--reason", "stop"]),
    ]:
        cli(command, TASK, *args, expected=4)
    cli("reopen", TASK, "--reason", " ", expected=2)
    cli("reopen", TASK, "--reason", "Revise interpretation")
    assert ready.read_record()["cycle"] == 2
    cli("close", TASK, expected=4)
    verify_pass(ready, cli)
    cli("close", TASK)
    record = ready.read_record()
    assert record["closures"][0] == closed
    assert record["closures"][1]["cycle"] == 2


def test_cancel_and_reopen_without_closure(ready, cli):
    cli("cancel", TASK, "--reason", " ", expected=2)
    cli("cancel", TASK, "--reason", "Evidence unavailable")
    assert ready.read_record()["closures"] == []
    cli("verify", TASK, expected=4)
    cli("cancel", TASK, "--reason", "duplicate", expected=4)
    cli("reopen", TASK, "--reason", "Evidence recovered")
    assert ready.read_record()["cycle"] == 2
    verify_pass(ready, cli)
    cli("close", TASK)


def test_version_change_needs_verification(ready, cli, monkeypatch):
    verify_pass(ready, cli)
    monkeypatch.setattr("rctl.verification.__version__", "future-version")
    with pytest.raises(RctlError) as exc:
        ready.close()
    assert exc.value.code == "VERIFICATION_STALE"


@pytest.mark.parametrize("changed", ["input.txt", "contract.md", "result.md"])
def test_material_change_during_real_check_is_unknown(ready, cli, changed):
    ready.file("check.py").write_text(
        f"from pathlib import Path\np=Path({changed!r})\np.write_bytes(p.read_bytes()+b'\\nchanged during check\\n')\n"
    )
    cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    assert report(ready)["subject_issues"]
    assert report(ready)["verdict"] == "unknown"
    cli("close", TASK, expected=4 if changed != "input.txt" else 5)


def test_record_change_during_real_check_refuses_publication(ready, cli):
    ready.file("check.py").write_text(
        "import subprocess, sys\n"
        "subprocess.run([sys.executable, '-m', 'rctl', '--root', '../..', 'cancel', 'tasks/retained-comparison', '--reason', 'Intervening operator action'], check=True)\n"
    )
    response = cli("verify", TASK, "--reviews", REVIEWS, expected=6)
    assert response["error"]["code"] == "RECORD_CHANGED"
    assert ready.read_record()["phase"] == "cancelled"
    assert ready.read_record()["verifications"] == []
    assert list(ready.file(".rctl/checks").rglob("*.stdout"))


def test_timeout_kills_descendant_group(ready, cli):
    metadata(ready, lambda d: d["criteria"][0]["method"].update(timeout_seconds=1))
    ready.amend("Use a bounded timeout")
    ready.file("result.md").write_text(
        ready.file("result.md")
        .read_text()
        .replace("contract_revision: 1", "contract_revision: 2")
    )
    review_edit(ready, lambda d: d.update(contract_revision=2))
    ready.file("check.py").write_text(
        "import subprocess, sys, time\n"
        'p=subprocess.Popen([sys.executable, \'-c\', \'import time; time.sleep(2); open("survived", "w").write("bad")\'])\n'
        "print(p.pid, flush=True)\n"
        "time.sleep(30)\n"
    )
    cli("verify", TASK, "--reviews", REVIEWS, expected=5)
    execution = report(ready)["checks"][0]["execution"]
    assert execution["timed_out"] and execution["exit_code"] < 0
    assert "Timed out" in execution["error"]
    time.sleep(2.1)
    assert not ready.file("survived").exists()
    cli("close", TASK, expected=5)


def test_interrupt_keeps_prior_record_and_orphan_logs_are_not_a_pass(ready, cli):
    verify_pass(ready, cli)
    before = ready.file(".rctl/record.json").read_bytes()
    ready.file("check.py").write_text(
        "from pathlib import Path\nimport time\nPath('started').write_text('ready')\ntime.sleep(30)\n"
    )
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "rctl",
            "--root",
            str(ready.root),
            "--format",
            "json",
            "verify",
            TASK,
            "--reviews",
            REVIEWS,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        deadline = time.monotonic() + 5
        while not ready.file("started").exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert ready.file("started").exists()
        process.send_signal(signal.SIGINT)
        process.communicate(timeout=5)
        assert process.returncode != 0
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)
    assert ready.file(".rctl/record.json").read_bytes() == before
    orphans = set(ready.file(".rctl/checks").rglob("*.stdout"))
    assert len(orphans) == 2
    cli("close", TASK, expected=4)
    ready.file("check.py").write_text("print('replacement check')\n")
    verify_pass(ready, cli)
    assert report(ready)["id"] == "V0002"
    assert orphans < set(ready.file(".rctl/checks").rglob("*.stdout"))


def test_interrupted_report_publication_after_real_execution(ready, monkeypatch):
    before = ready.file(".rctl/record.json").read_bytes()

    def fail(*args):
        raise OSError("interrupted publication")

    monkeypatch.setattr("rctl.records.os.replace", fail)
    with pytest.raises(OSError):
        ready.verify(REVIEWS)
    assert ready.file(".rctl/record.json").read_bytes() == before
    assert list(ready.file(".rctl/checks").rglob("*.stdout"))
    assert ready.read_record()["verifications"] == []


def test_copy_task_and_project_relative_evidence(ready, cli):
    runs = ready.root / "runs"
    runs.mkdir()
    (runs / "retained.txt").write_text("shared input")
    metadata(
        ready,
        lambda d: d["criteria"][0]["method"]["inputs"].append(
            "../../runs/retained.txt"
        ),
    )
    ready.amend("Declare project-relative input")
    ready.file("result.md").write_text(
        ready.file("result.md")
        .read_text()
        .replace("contract_revision: 1", "contract_revision: 2")
    )
    review_edit(ready, lambda d: d.update(contract_revision=2))
    verify_pass(ready, cli)
    cli("close", TASK)
    destination = ready.root / "relocated"
    shutil.copytree(ready.path, destination / TASK)
    shutil.copytree(runs, destination / "runs")
    relocated = Task(destination, destination / TASK)
    assert relocated.status()[0]["historical_closure"]["verification_id"] == "V0001"
    relocated.reopen("Verify the copied task here")
    relocated.verify(REVIEWS)
    relocated.close()
    assert relocated.read_record()["phase"] == "closed"
    assert ready.read_record()["cycle"] == 1


def test_unreadable_evidence_cannot_close(ready, cli):
    verify_pass(ready, cli)
    path = ready.file("input.txt")
    path.chmod(0)
    try:
        if os.access(path, os.R_OK):
            pytest.skip("Runtime bypasses file permission checks")
        assert cli("close", TASK, expected=5)["error"]["code"] == "VERIFICATION_UNKNOWN"
        cli("verify", TASK, "--reviews", REVIEWS, expected=5)
        assert report(ready)["checks"][0]["execution"] is None
    finally:
        path.chmod(0o600)


def test_full_synthetic_example_closes(ready, cli):
    # Exercise the documented uv-based arithmetic checker, not only test check.py.
    original = (REPO / "examples/retained-comparison/contract.md").read_text()
    ready.file("contract.md").write_text(original)
    ready.amend("Use the documented synthetic arithmetic checker")
    ready.file("result.md").write_text(
        ready.file("result.md")
        .read_text()
        .replace("contract_revision: 1", "contract_revision: 2")
    )
    review_edit(ready, lambda d: d.update(contract_revision=2))
    saved = verify_pass(ready, cli)
    assert "gain=-0.03; promote=False" in read_text(
        ready.root / saved["checks"][0]["execution"]["stdout_ref"]
    )
    assert cli("close", TASK)["data"]["closure"]["assessment"] == "not_supported"


def test_fail_takes_precedence_over_missing_review(ready, cli):
    ready.file("check.py").write_text("raise SystemExit(1)\n")
    response = cli("verify", TASK, expected=4)
    assert response["data"]["verdict"] == "fail"
    assert [check["verdict"] for check in report(ready)["checks"]] == [
        "fail",
        "unknown",
    ]


def test_negative_review_is_recorded_failure(ready, cli):
    review_edit(
        ready,
        lambda d: d["checks"][0].update(
            verdict="fail",
            rationale="The interpretation overstates the supplied observations.",
        ),
    )
    cli("verify", TASK, "--reviews", REVIEWS, expected=4)
    cli("close", TASK, expected=4)
    assert report(ready)["checks"][1]["verdict"] == "fail"


@pytest.mark.parametrize(
    "change",
    [
        lambda r: r["verifications"][0]["checks"][0]["execution"].pop("exit_code"),
        lambda r: r["verifications"][0].update(observed_files=[]),
        lambda r: r["verifications"][0].pop("review_input_text"),
        lambda r: r["verifications"][0].update(verdict="fail"),
    ],
)
def test_malformed_reports_are_unavailable_and_preserved(ready, cli, change):
    verify_pass(ready, cli)
    record = ready.read_record()
    change(record)
    ready.file(".rctl/record.json").write_text(json.dumps(record))
    before = ready.file(".rctl/record.json").read_bytes()
    assert cli("close", TASK, expected=3)["error"]["code"] == "RECORD_UNAVAILABLE"
    assert not cli("context", TASK, expected=3)["data"]["available"]
    assert ready.file(".rctl/record.json").read_bytes() == before


def test_deleted_log_prevents_close(ready, cli):
    saved = verify_pass(ready, cli)
    (ready.root / saved["checks"][0]["execution"]["stdout_ref"]).unlink()
    assert cli("close", TASK, expected=4)["error"]["code"] == "VERIFICATION_STALE"


def test_repointed_input_symlink_is_reobserved(ready, cli):
    ready.file("original.txt").write_text("original data")
    ready.file("new.txt").write_text("different retained data")
    (ready.path / "input.txt").unlink()
    (ready.path / "input.txt").symlink_to("original.txt")
    verify_pass(ready, cli)
    (ready.path / "input.txt").unlink()
    (ready.path / "input.txt").symlink_to("new.txt")
    assert cli("close", TASK, expected=4)["error"]["code"] == "VERIFICATION_STALE"


@pytest.mark.parametrize("option", ["--help", "--version"])
def test_informational_options_use_json_envelope(cli, option):
    assert cli(option)["data"]["message"]


def test_unexpected_internal_failure_uses_exit_70(monkeypatch, capsys):
    from rctl.cli import main

    def fail(*args):
        raise RuntimeError("injected internal failure")

    monkeypatch.setattr("rctl.cli.dispatch", fail)
    assert main(["--format", "json", "status", TASK]) == 70
    captured = capsys.readouterr()
    assert json.loads(captured.out)["error"]["code"] == "INTERNAL_ERROR"
    assert "INTERNAL_ERROR" in captured.err


def test_text_output_preserves_verification_outcome(ready, capsys):
    from rctl.cli import main

    assert main(["--root", str(ready.root), "verify", TASK, "--reviews", REVIEWS]) == 0
    captured = capsys.readouterr()
    assert "verification_id: V0001" in captured.out
    assert "verdict: pass" in captured.out
    assert "actual stdout" not in captured.out


@pytest.mark.parametrize("exists", [True, False])
def test_verify_distinguishes_draft_from_missing_task(task, cli, exists):
    if exists:
        response = cli("verify", TASK, expected=4)
        assert response["error"]["code"] == "STATE_REJECTED"
        assert "begin" in response["error"]["message"]
    else:
        cli("verify", "tasks/missing", expected=3)
