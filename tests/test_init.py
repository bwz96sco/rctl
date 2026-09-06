import json
import re

import pytest


def snapshot(root):
    return {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_init_repeat_preserves_customized_files_and_links(project, cli):
    first = cli("init", "--vault", "note/main", "--codex")
    assert first["data"]["vault"] == "note/main"
    assert (project / "tasks").is_dir()
    research = project / "research"
    assert {p.name for p in research.iterdir()} == {
        "README.md",
        "PROGRAM.md",
        "INVENTORY.md",
        "BASELINES.md",
        "ROUTES.md",
    }
    links = re.findall(
        r"\[[^]]+\]\(([^)]+\.md)\)", (research / "README.md").read_text()
    )
    assert links == ["PROGRAM.md", "INVENTORY.md", "BASELINES.md", "ROUTES.md"]
    assert all((research / path).is_file() for path in links)
    for name in (
        "research/PROGRAM.md",
        ".agents/skills/research-task/SKILL.md",
        "note/main/AGENTS.md",
        ".codex/hooks.json",
    ):
        (project / name).write_text("User customization\n")
    before = snapshot(project)
    repeat = cli("init", "--codex")
    assert repeat["data"]["created"] == []
    assert snapshot(project) == before
    assert not (project / ".git").exists()
    assert not (project / ".rctl/record.json").exists()


def test_existing_vault_is_only_associated(project, cli):
    vault = project / "notes"
    vault.mkdir()
    (vault / "existing.md").write_text("existing note")
    before = snapshot(vault)
    cli("init", "--vault", "notes")
    assert snapshot(vault) == before
    assert not (project / ".codex").exists()
    assert json.loads((project / ".rctl/project.json").read_text())["vault"] == "notes"


@pytest.mark.parametrize(
    "collision",
    [
        "research",
        "research/PROGRAM.md",
        ".agents/skills",
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
    cli("init", "--vault", "notes")
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


def test_existing_vault_cannot_overlap_a_control_directory_alias(project, cli):
    vault = project / "notes"
    vault.mkdir()
    (vault / "existing.md").write_text("Keep this vault untouched.")
    (project / "research").symlink_to(vault, target_is_directory=True)
    before = snapshot(vault)
    cli("init", "--vault", "notes", expected=2)
    assert snapshot(vault) == before
    assert not (project / "tasks").exists()
