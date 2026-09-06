import json
import os
import shlex
import subprocess
import sys
import tomllib

import pytest
import yaml

from rctl.integration import inline_arguments


def hook(task, payload, *, root=True, selection=True, logging=None, extra_env=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("RCTL_")}
    if selection:
        env["RCTL_TASK_PATH"] = "tasks/retained-comparison"
    if logging:
        env["RCTL_HOOK_LOG"] = logging
    env.update(extra_env or {})
    args = [sys.executable, "-m", "rctl"]
    if root:
        args += ["--root", str(task.root)]
    args += ["hook", "codex"]
    result = subprocess.run(
        args,
        input=payload if isinstance(payload, str) else json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=task.root,
        env=env,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout), result.stderr


@pytest.mark.parametrize(
    "event,budget", [("SessionStart", 8000), ("UserPromptSubmit", 2000)]
)
def test_real_adapter_is_bounded_readonly_and_receipts_optional(task, event, budget):
    task.begin()
    task.file("state.md").write_text(
        "Next action: inspect the retained evidence.\n" + "界" * 12000
    )
    before = {p: p.read_bytes() for p in task.path.rglob("*") if p.is_file()}
    payload = {
        "hook_event_name": event,
        "source": "startup",
        "session_id": "fixture",
        "cwd": str(task.root),
    }
    response, stderr = hook(task, payload)
    assert not stderr
    output = response["hookSpecificOutput"]
    assert output["hookEventName"] == event
    assert len(output["additionalContext"]) <= budget
    assert "Next action: inspect the retained evidence." in output["additionalContext"]
    assert "Truncated" in output["additionalContext"]
    assert {p: p.read_bytes() for p in task.path.rglob("*") if p.is_file()} == before
    if event == "UserPromptSubmit":
        assert "Does the supplied candidate" not in output["additionalContext"]
    response, stderr = hook(task, payload, logging="receipts.jsonl")
    receipt = json.loads((task.root / "receipts.jsonl").read_text())
    assert receipt["context"] == response["hookSpecificOutput"]["additionalContext"]
    assert receipt["event"] == event and receipt["session_id"] == "fixture"
    assert receipt["task_path"] == "tasks/retained-comparison"


@pytest.mark.parametrize("payload", ["{", "[]", "null"])
def test_malformed_payload_never_blocks(task, payload):
    response, stderr = hook(task, payload)
    assert response == {} and "invalid event input" in stderr


def test_unsupported_event_has_no_output_or_receipt(task):
    response, _ = hook(
        task,
        {"hook_event_name": "Stop", "cwd": str(task.root)},
        logging="receipt.jsonl",
    )
    assert response == {}
    assert not (task.root / "receipt.jsonl").exists()


@pytest.mark.parametrize(
    "case",
    ["no-root", "no-task", "missing", "wrong-cwd", "relative-cwd", "malformed-record"],
)
def test_unavailable_selection_is_visible_without_fallback(task, case):
    task.begin()
    payload = {"hook_event_name": "SessionStart", "cwd": str(task.root)}
    if case == "wrong-cwd":
        payload["cwd"] = str(task.root.parent)
    if case == "relative-cwd":
        payload["cwd"] = "."
    if case == "malformed-record":
        task.file(".rctl/record.json").write_text("{")
    response, _ = hook(
        task,
        payload,
        root=case != "no-root",
        selection=case != "no-task",
        extra_env={"RCTL_TASK_PATH": "missing"} if case == "missing" else {},
    )
    assert "unavailable" in response["hookSpecificOutput"]["additionalContext"]


def test_environment_root_and_changed_handoff_are_fresh(task):
    task.begin()
    payload = {"hook_event_name": "UserPromptSubmit", "cwd": str(task.root)}
    task.file("state.md").write_text("Next action: first observation.")
    first, _ = hook(
        task, payload, root=False, extra_env={"RCTL_PROJECT_ROOT": str(task.root)}
    )
    task.file("state.md").write_text("Next action: revised observation.")
    second, _ = hook(
        task, payload, root=False, extra_env={"RCTL_PROJECT_ROOT": str(task.root)}
    )
    assert "first observation" in first["hookSpecificOutput"]["additionalContext"]
    assert "revised observation" in second["hookSpecificOutput"]["additionalContext"]


def test_receipt_failure_does_not_block_context(task):
    task.begin()
    response, stderr = hook(
        task,
        {"hook_event_name": "SessionStart", "cwd": str(task.root)},
        logging="../outside.jsonl",
    )
    assert "Phase: active" in response["hookSpecificOutput"]["additionalContext"]
    assert "receipt unavailable" in stderr


def test_export_is_reviewable_runnable_and_preserves_existing_config(task, cli):
    task.begin()
    config = task.root / ".codex/config.toml"
    config.parent.mkdir()
    config.write_text("# Existing host configuration\n")
    response = cli("integration", "codex", "export", "bundle with spaces")
    bundle = task.root / "bundle with spaces"
    hooks = json.loads((bundle / "hooks.json").read_text())
    assert set(hooks["hooks"]) == {"SessionStart", "UserPromptSubmit"}
    for event, handlers in hooks["hooks"].items():
        command = handlers[0]["hooks"][0]
        assert command["timeout"] == 10
        assert command["additionalContextLimit"] == (
            8000 if event == "SessionStart" else 2000
        )
        argv = shlex.split(command["command"])
        assert argv[0] == response["data"]["entrypoint"]
        result = subprocess.run(
            argv,
            input=json.dumps({"hook_event_name": event, "cwd": str(task.root)}),
            env={**os.environ, "RCTL_TASK_PATH": "tasks/retained-comparison"},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert (
            "active"
            in json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
        )
    args = inline_arguments(hooks)
    for i in range(1, len(args), 2):
        assert tomllib.loads(args[i])["hooks"]
    skill = (bundle / "research-task/SKILL.md").read_text()
    assert yaml.safe_load(skill.split("---")[1])["name"] == "research-task"
    ui = yaml.safe_load((bundle / "research-task/agents/openai.yaml").read_text())
    assert "$research-task" in ui["interface"]["default_prompt"]
    before = {p: p.read_bytes() for p in bundle.rglob("*") if p.is_file()}
    cli("integration", "codex", "export", "bundle with spaces", expected=4)
    assert before == {p: p.read_bytes() for p in bundle.rglob("*") if p.is_file()}
    assert config.read_text() == "# Existing host configuration\n"
    assert not (task.root / ".agents").exists()
