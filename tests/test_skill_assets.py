"""The workflow suite ships intact without broadening project installation."""

import ast
import re
import runpy
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
import yaml
from test_research_skill_contracts import ACTIVE_RESEARCH_SKILLS

from rctl.documents import resource_directory

PACKAGED_SKILLS = ACTIVE_RESEARCH_SKILLS | {"paper-discovery", "research-task"}


def test_exact_packaged_workflow_set():
    root = resource_directory("skills")
    assert {path.name for path in root.iterdir() if path.is_dir()} == PACKAGED_SKILLS
    # Bundled templates/fixtures must not register extra workflows during discovery.
    assert set(root.rglob("SKILL.md")) == {
        root / name / "SKILL.md" for name in PACKAGED_SKILLS
    }


@pytest.mark.parametrize("name", sorted(PACKAGED_SKILLS))
def test_skill_metadata_resources_and_script_syntax(name):
    root = resource_directory("skills").joinpath(name)
    text = root.joinpath("SKILL.md").read_text(encoding="utf-8")
    metadata = yaml.safe_load(text.split("---", 2)[1])
    assert metadata["name"] == name
    assert metadata["description"].strip()
    projection = yaml.safe_load(root.joinpath("agents/openai.yaml").read_text())
    assert f"${name}" in projection["interface"]["default_prompt"]
    allow = projection.get("policy", {}).get("allow_implicit_invocation", True)
    disable = metadata.get("disable-model-invocation", False)
    assert isinstance(allow, bool) and isinstance(disable, bool)
    assert allow is not disable

    documents = [root / "SKILL.md", *root.joinpath("references").rglob("*.md")]
    for document in documents:
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text()):
            parts = urlsplit(target.strip("<>"))
            if not parts.scheme and parts.path:
                assert (document.parent / unquote(parts.path)).is_file(), (
                    document,
                    target,
                )
    for script in root.rglob("*.py"):
        ast.parse(script.read_text(encoding="utf-8"), filename=str(script))


def test_project_init_and_exports_remain_task_only(project, cli):
    cli("init")
    installed = project / ".agents/skills"
    assert {path.name for path in installed.iterdir()} == {"research-task"}
    cli("integration", "codex", "export", "bundle")
    assert {path.name for path in (project / "bundle").iterdir() if path.is_dir()} == {
        "research-task"
    }
    cli("update", "export", "update-candidates")
    candidates = project / "update-candidates/candidates/.agents/skills"
    assert {path.name for path in candidates.iterdir()} == {"research-task"}


def test_experiment_templates_complete_native_smoke(project, cli):
    repo = Path(__file__).resolve().parents[1]
    walkthrough = runpy.run_path(str(repo / "scripts/smoke_shared_skills.py"))[
        "walkthrough"
    ]
    cli("init")
    record = walkthrough(cli, project, repo, repo, sys.executable)
    assert record["phase"] == "closed"
    assert record["closures"][-1]["assessment"] == "not_supported"
