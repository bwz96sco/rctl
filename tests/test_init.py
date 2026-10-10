import json
import re

import pytest


def snapshot(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_default_init_prepares_codex_but_reports_pending_delivery(project, cli):
    response = cli("init")
    assert response["data"]["codex_requested"]
    hooks = json.loads((project / ".codex/hooks.json").read_text())["hooks"]
    assert set(hooks) == {"SessionStart", "UserPromptSubmit"}
    assert all(len(groups[0]["hooks"]) == 1 for groups in hooks.values())
    assert (project / ".codex/config.toml").read_text() == "[features]\nhooks = true\n"
    assert "/hooks" in response["data"]["next_action"]
    assert any("pending host confirmation" in text for text in response["warnings"])
    instructions = (project / ".rctl/codex/README.md").read_text()
    assert "SessionStart and UserPromptSubmit" in instructions
    assert "direct hook invocation is not delivery evidence" in instructions
    data = cli("doctor")["data"]
    assert data["codex_inspected"] and not data["review_needed"]
    assert data["codex_trust"] == data["codex_delivery"] == "not_inspected"


def test_default_init_prepares_claude_code_hooks_and_skill(project, cli):
    response = cli("init")
    assert response["data"]["claude_requested"]
    assert "workspace trust" in response["data"]["next_action"]
    assert any("Claude Code setup is pending" in text for text in response["warnings"])
    hooks = json.loads((project / ".claude/settings.json").read_text())["hooks"]
    assert set(hooks) == {"SessionStart", "UserPromptSubmit"}
    for groups in hooks.values():
        (handler,) = groups[0]["hooks"]
        assert set(handler) == {"type", "command", "timeout"}
        assert handler["command"].endswith(f"--root {project} hook claude")
    # Claude Code does not load .agents/skills/.
    for path in (project / ".agents/skills/research-task").rglob("*"):
        copy = project / ".claude/skills/research-task" / path.relative_to(
            project / ".agents/skills/research-task"
        )
        assert path.is_dir() or copy.read_bytes() == path.read_bytes()
    instructions = (project / ".rctl/claude/README.md").read_text()
    assert "workspace\ntrust dialog" in instructions
    assert "direct hook invocation is not delivery evidence" in instructions
    data = cli("doctor")["data"]
    assert data["claude_inspected"] and not data["review_needed"]
    assert data["claude_trust"] == data["claude_delivery"] == "not_inspected"


def test_terminal_only_setup_is_explicit(project, cli):
    response = cli("init", "--no-codex", "--no-claude")
    assert not response["data"]["codex_requested"]
    assert not response["data"]["claude_requested"]
    assert "skipped" in response["data"]["next_action"]
    for path in (".codex", ".rctl/codex", ".claude", ".rctl/claude"):
        assert not (project / path).exists()
    inspection = cli("doctor", "--no-codex", "--no-claude")["data"]
    assert not inspection["codex_inspected"] and not inspection["claude_inspected"]
    assert not inspection["review_needed"]


@pytest.mark.parametrize("command", ["init", "doctor"])
@pytest.mark.parametrize("host", ["codex", "claude"])
def test_conflicting_host_options_do_not_write(project, cli, command, host):
    cli(command, f"--{host}", f"--no-{host}", expected=2)
    assert list(project.iterdir()) == []


def test_init_repeat_preserves_customized_files_and_links(project, cli):
    first = cli("init", "--vault", "note/main", "--codex")
    assert first["data"]["vault"] == "note/main"
    assert (project / "tasks").is_dir()
    research = project / "research"
    assert {p.name for p in research.iterdir()} == {
        "README.md",
        "PROGRAM.md",
        "PROBLEM_METHODS.md",
        "INVENTORY.md",
        "BASELINES.md",
        "ROUTES.md",
        "guidelines",
    }
    links = re.findall(
        r"\[[^]]+\]\(([^)]+\.md)\)", (research / "README.md").read_text()
    )
    assert links == [
        "PROBLEM_METHODS.md",
        "PROGRAM.md",
        "ROUTES.md",
        "guidelines/comparison-design.md",
        "BASELINES.md",
        "INVENTORY.md",
    ]
    assert all((research / path).is_file() for path in links)
    for name in (
        "research/PROGRAM.md",
        "research/PROBLEM_METHODS.md",
        "research/guidelines/comparison-design.md",
        ".agents/skills/research-task/SKILL.md",
        "note/main/AGENTS.md",
        ".codex/hooks.json",
        ".claude/settings.json",
        ".claude/skills/research-task/SKILL.md",
    ):
        (project / name).write_text("User customization\n")
    before = snapshot(project)
    repeat = cli("init")
    assert repeat["data"]["created"] == []
    assert any(".claude/settings.json" in text for text in repeat["warnings"])
    assert snapshot(project) == before
    assert not (project / ".git").exists()
    assert not (project / ".rctl/record.json").exists()


def test_existing_vault_is_only_associated(project, cli):
    vault = project / "notes"
    vault.mkdir()
    (vault / "existing.md").write_text("existing note")
    before = snapshot(vault)
    cli("init", "--vault", "notes", "--no-codex")
    assert snapshot(vault) == before
    assert not (project / ".codex").exists()
    assert json.loads((project / ".rctl/project.json").read_text())["vault"] == "notes"


@pytest.mark.parametrize(
    "collision",
    [
        "research",
        "research/PROGRAM.md",
        ".agents/skills",
        ".claude/skills",
        ".rctl/project.json",
        "notes",
    ],
)
def test_collisions_fail_before_writes(project, cli, collision):
    path = project / collision
    path.parent.mkdir(parents=True, exist_ok=True)
    if collision.endswith(".md") or collision.endswith(".json"):
        path.mkdir()
    else:
        path.write_text("not a directory")
    before = snapshot(project)
    cli("init", "--vault", "notes", expected=2)
    assert snapshot(project) == before
    assert not (project / "tasks").exists()


@pytest.mark.parametrize(
    "vault",
    [
        "../outside",
        ".",
        "tasks/notes",
        "research",
        ".rctl/vault",
        ".agents/vault",
        ".claude/vault",
        ".git",
    ],
)
def test_invalid_vault_is_rejected_before_writes(project, cli, vault):
    cli("init", "--vault", vault, expected=2)
    assert list(project.iterdir()) == []


def test_symlink_escape_is_rejected(project, cli, tmp_path_factory):
    outside = tmp_path_factory.mktemp("external")
    (project / "research").symlink_to(outside, target_is_directory=True)
    cli("init", expected=2)
    assert list(outside.iterdir()) == []
    assert not (project / "tasks").exists()


def test_binding_change_and_unknown_schema_fail_before_new_files(project, cli):
    cli("init", "--vault", "notes", "--no-codex")
    before = snapshot(project)
    cli("init", "--vault", "another-vault", "--codex", expected=2)
    assert snapshot(project) == before
    assert not (project / ".codex").exists()
    manifest = project / ".rctl/project.json"
    manifest.write_text('{"schema_version": 2, "vault": "notes"}')
    cli("init", "--codex", expected=2)
    assert not (project / ".codex").exists()


def test_missing_project_file_is_restored_without_touching_vault(project, cli):
    cli("init", "--vault", "notes")
    (project / "research/ROUTES.md").unlink()
    (project / "notes/AGENTS.md").unlink()
    cli("init")
    assert (project / "research/ROUTES.md").is_file()
    assert not (project / "notes/AGENTS.md").exists()


def test_workspace_reference_links_are_exported(project, cli):
    cli("integration", "codex", "export", "bundle")
    refs = project / "bundle/research-task/references"
    assert (refs / "workspace.md").is_file()
    assert (refs / "graphify.md").is_file()
    assert (refs / "planning.md").is_file()
    assert "only accepts active tasks" in (refs / "verification.md").read_text()
    for source in (project / "bundle/research-task").rglob("*.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text()):
            if "://" not in target:
                assert (source.parent / target.split("#")[0]).is_file(), (
                    source,
                    target,
                )


def test_existing_vault_cannot_overlap_a_control_directory_alias(project, cli):
    vault = project / "notes"
    vault.mkdir()
    (vault / "existing.md").write_text("Keep this vault untouched.")
    (project / "research").symlink_to(vault, target_is_directory=True)
    before = snapshot(vault)
    cli("init", "--vault", "notes", expected=2)
    assert snapshot(vault) == before
    assert not (project / "tasks").exists()
