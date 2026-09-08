"""Review regressions for project reminder content and diagnostics."""

import pytest
from test_m7 import guidance

from rctl.context import load_context
from rctl.documents import resource_text, sections
from rctl.project_context import read_project


@pytest.mark.parametrize(
    "value",
    [
        "Reach WER < 8% while keeping decode latency > 2x realtime.",
        "See the decision:\n<https://example.com/decision>.",
        "<https://example.com/decision>",
        "<research@example.com>",
    ],
)
def test_valid_angle_brackets_survive_project_context(project, value):
    guidance(project, value)
    path = project / "research/PROGRAM.md"
    path.write_text(path.read_text().replace("Reduce comparable error.", value))
    data, warnings = load_context(project, budget=2000, compact=True)
    assert data["project"]["goal"] == value
    assert data["project"]["current_guidance"] == value
    assert value in data["context"]
    assert not warnings


def test_packaged_project_placeholders_are_omitted(project):
    guidance(project)
    template = resource_text("templates", "project/research/PROGRAM.md")
    assert sections(template)["Goal"].strip().startswith("<")
    (project / "research/PROGRAM.md").write_text(template)
    data, warnings = read_project(project)
    assert data["goal"] is None and data["current_guidance"] is None
    assert len(warnings) == 2


@pytest.mark.parametrize("budget,compact", [(2000, True), (8000, False)])
def test_each_task_warning_has_a_marker(task, budget, compact):
    guidance(task.root)
    task.begin()
    contract = task.file("contract.md")
    contract.write_text(contract.read_text() + "\nChanged scope.\n")
    data, warnings = load_context(task.root, task=task, budget=budget, compact=compact)
    assert any("AMENDMENT_REQUIRED" in warning for warning in warnings)
    assert any("No verification" in warning for warning in warnings)
    for warning in warnings:
        assert f"Warning: {warning}" in data["context"]
    assert len(data["context"]) <= budget


def test_orientation_is_only_listed_when_it_exists(project):
    data, _ = load_context(project, compact=True)
    assert "Orientation:" not in data["context"]
    guidance(project)
    (project / "research/README.md").write_text("# Research\n")
    data, _ = load_context(project, compact=True)
    assert "Orientation: research/README.md" in data["context"]


@pytest.mark.parametrize("bad", ["missing", "invalid-utf8", "directory"])
def test_project_diagnostics_keep_reason_without_repeating_root(project, bad):
    root = project / ("deep-research-root-" + "x" * 90)
    (root / "research").mkdir(parents=True)
    path = root / "research/PROGRAM.md"
    reason = "Missing file"
    if bad == "invalid-utf8":
        path.write_bytes(b"\xff")
        reason = "Expected UTF-8 text"
    elif bad == "directory":
        path.mkdir()
        reason = "Cannot read file"
    data, warnings = load_context(root, budget=2000, compact=True)
    assert any(
        reason in warning and "research/PROGRAM.md" in warning for warning in warnings
    )
    assert all(str(root) not in warning for warning in warnings)
    assert data["context"].count(str(root)) == 1
    assert len(data["context"]) <= 2000
