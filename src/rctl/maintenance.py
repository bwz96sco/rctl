"""Project-local inspection and candidate-only updates."""

import difflib
import json
import os
import shlex
import sys
import tomllib
from pathlib import Path

from . import __version__
from .documents import (
    RctlError,
    invalid,
    local_path,
    read_text,
    resource_tree,
    validate_schema,
)
from .initialize import vault_path
from .integration import claude_hooks, codex_hooks
from .records import state_error


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def inspect_installation(root, codex=False, claude=False):
    findings, diffs = [], {}
    skills = [".agents/skills/research-task"]
    if claude:
        skills.append(".claude/skills/research-task")
    candidates = {
        f"{skill}/{name}": value
        for skill in skills
        for name, value in resource_tree("skills/research-task").items()
    }

    def finding(path, status, message, next_action="None."):
        findings.append(
            dict(path=path, status=status, message=message, next_action=next_action)
        )

    def difference(name, actual, expected):
        if actual == expected:
            return
        diffs[name] = "".join(
            difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=f"installed/{name}",
                tofile=f"candidate/{name}",
            )
        )

    binding = None
    manifest = ".rctl/project.json"
    try:
        binding = json.loads(read_text(local_path(root, manifest)))
        validate_schema(binding, manifest, "project")
        if binding["vault"] is not None:
            vault = vault_path(root, binding["vault"])
            if vault.relative_to(root).as_posix() != binding["vault"]:
                raise invalid(
                    "Vault binding must be a normalized project-relative path."
                )
            if not vault.is_dir():
                finding(
                    binding["vault"],
                    "missing",
                    "Bound vault directory is unavailable.",
                    "Restore the bound vault or review the binding.",
                )
        finding(manifest, "current", "Project binding is structurally valid.")
    except (RctlError, ValueError) as error:
        binding = None
        finding(
            manifest,
            "unavailable",
            str(error),
            "Initialize a missing project binding; review existing invalid content.",
        )

    for name, expected in candidates.items():
        try:
            path = local_path(root, name)
            actual = read_text(path)
        except RctlError as error:
            finding(
                name,
                "unavailable",
                str(error),
                "Review the packaged candidate and restore the file.",
            )
            actual = ""
        else:
            if actual == expected:
                finding(name, "current", "Matches the current package.")
            else:
                finding(
                    name,
                    "different",
                    "Differs from the current package; origin of edits is unknown.",
                    "Compare the candidate and preserve intentional local changes.",
                )
        difference(name, actual, expected)
    for installed in skills:
        try:
            skill = local_path(root, installed)
            if skill.is_dir():
                for path in sorted(skill.rglob("*")):
                    if path.name == ".DS_Store":
                        continue
                    name = f"{installed}/{path.relative_to(skill).as_posix()}"
                    if (path.is_symlink() or path.is_file()) and name not in candidates:
                        finding(
                            name,
                            "extra",
                            "Local-only skill asset; retained.",
                            "Keep or reconcile this local asset explicitly.",
                        )
        except RctlError as error:
            finding(
                installed,
                "unavailable",
                str(error),
                "Inspect the skill directory.",
            )

    def collect(name, hooks, observed, host):
        if not isinstance(hooks, dict):
            raise ValueError("Expected a hooks object/table.")
        for event, groups in hooks.items():
            if not isinstance(groups, list):
                raise ValueError(f"Expected a handler-group array for {event}.")
            for group in groups:
                if not isinstance(group, dict) or not isinstance(
                    group.get("hooks"), list
                ):
                    raise ValueError(f"Invalid handler group for {event}.")
                for handler in group["hooks"]:
                    if not isinstance(handler, dict):
                        raise ValueError(f"Invalid command handler for {event}.")
                    command = handler.get("command")
                    if not isinstance(command, str):
                        if handler.get("type") in {"prompt", "agent", "http", "mcp_tool"}:
                            continue
                        raise ValueError(f"Invalid command handler for {event}.")
                    if "rctl" not in command:
                        continue
                    projection = {"matcher": group.get("matcher"), "handler": handler}
                    if event in observed:
                        observed[event].append(projection)
                    else:
                        finding(
                            f"{name}:{event}",
                            "unexpected",
                            "rctl command configured for an unsupported event.",
                            "Review and remove the unintended rctl handler.",
                        )
                    inspect_command(root, name, event, group, handler, finding, host)

    def count(host, observed, expected_hooks):
        expected_projection = {}
        for event in observed:
            if expected_hooks is not None:
                groups = expected_hooks["hooks"][event]
                expected_projection[event] = [
                    {"matcher": None, "handler": groups[0]["hooks"][0]}
                ]
            total = len(observed[event])
            if total != 1:
                finding(
                    f"{host}:{event}",
                    "missing" if total == 0 else "duplicate",
                    f"Found {total} rctl handlers across project hook sources; expected one.",
                    "Merge exactly one reviewed rctl handler for this event.",
                )
        if expected_hooks is not None:
            difference(
                f"{host}-handlers.json",
                json_text(observed),
                json_text(expected_projection),
            )

    if codex:
        try:
            expected_hooks, _ = codex_hooks(root)
        except RctlError as error:
            expected_hooks = None
            finding(
                "codex:entrypoint",
                "unavailable",
                error.message,
                "Install rctl in this Python environment, then inspect and export again.",
            )
        else:
            candidates[".codex/hooks.json"] = json_text(expected_hooks)
        candidates[".codex/config.toml"] = (
            "# Merge this feature into the existing configuration.\n[features]\nhooks = true\n"
        )
        observed = {event: [] for event in ("SessionStart", "UserPromptSubmit")}
        config = {}
        for name, parse in (
            (".codex/hooks.json", json.loads),
            (".codex/config.toml", tomllib.loads),
        ):
            try:
                path = local_path(root, name)
                if not path.exists():
                    continue
                content = parse(read_text(path))
                if not isinstance(content, dict):
                    raise ValueError("Expected an object/table.")
                if name.endswith("toml"):
                    config = content
                collect(name, content.get("hooks", {}), observed, "codex")
            except (RctlError, ValueError) as error:
                finding(
                    name,
                    "invalid",
                    str(error),
                    "Review the project configuration without replacing unrelated settings.",
                )
        features = config.get("features", {})
        if not isinstance(features, dict):
            finding(
                ".codex/config.toml:features",
                "invalid",
                "Expected a features table.",
                "Correct the local features table.",
            )
            features = {}
        enabled = features.get("hooks", features.get("codex_hooks"))
        if enabled is False:
            finding(
                ".codex/config.toml:features.hooks",
                "disabled",
                "Project configuration explicitly disables hooks.",
                "Enable hooks when reminders are wanted.",
            )
        elif enabled is None:
            finding(
                ".codex/config.toml:features.hooks",
                "inherited",
                "No local setting; effective behavior depends on host defaults and other layers.",
            )
        elif enabled is True:
            finding(
                ".codex/config.toml:features.hooks",
                "current",
                "Project setting enables hooks; delivery and trust are not inspected.",
            )
        else:
            finding(
                ".codex/config.toml:features.hooks",
                "invalid",
                "Expected a boolean setting.",
                "Use a boolean hooks feature setting.",
            )
        count("codex", observed, expected_hooks)
        difference(
            "codex-feature.json",
            json_text({"hooks": enabled}),
            json_text({"hooks": True}),
        )

    if claude:
        try:
            expected_hooks, _ = claude_hooks(root)
        except RctlError as error:
            expected_hooks = None
            finding(
                "claude:entrypoint",
                "unavailable",
                error.message,
                "Install rctl in this Python environment, then inspect and export again.",
            )
        else:
            candidates[".claude/settings.json"] = json_text(expected_hooks)
        observed = {event: [] for event in ("SessionStart", "UserPromptSubmit")}
        # Both project settings files are hook sources; user settings are not read.
        for name in (".claude/settings.json", ".claude/settings.local.json"):
            try:
                path = local_path(root, name)
                if not path.exists():
                    continue
                content = json.loads(read_text(path))
                if not isinstance(content, dict):
                    raise ValueError("Expected an object.")
                switch = content.get("disableAllHooks")
                if switch is True:
                    finding(
                        f"{name}:disableAllHooks",
                        "disabled",
                        "Project settings disable all hooks, including rctl reminders.",
                        "Remove the setting when reminders are wanted.",
                    )
                elif switch not in (None, False):
                    finding(
                        f"{name}:disableAllHooks",
                        "invalid",
                        "Expected a boolean setting.",
                        "Use a boolean disableAllHooks setting.",
                    )
                collect(name, content.get("hooks", {}), observed, "claude")
            except (RctlError, ValueError) as error:
                finding(
                    name,
                    "invalid",
                    str(error),
                    "Review the project settings without replacing unrelated settings.",
                )
        count("claude", observed, expected_hooks)

    return (
        {
            "root": str(root),
            "rctl_version": __version__,
            "codex_inspected": codex,
            "claude_inspected": claude,
            "review_needed": any(
                item["status"] not in {"current", "inherited"} for item in findings
            ),
            "findings": findings,
        },
        candidates,
        diffs,
        binding,
    )


def inspect_command(root, source, event, group, handler, finding, host="codex"):
    name = f"{source}:{event}"
    try:
        argv = shlex.split(handler["command"])
    except ValueError:
        argv = []
    if (
        len(argv) != 5
        or Path(argv[0]).name != "rctl"
        or argv[1] != "--root"
        or argv[3:] != ["hook", host]
    ):
        finding(
            name,
            "unrecognized",
            "Custom rctl command shape; it was not executed.",
            "Review the command against the generated candidate.",
        )
        return
    executable = Path(argv[0])
    problems = []
    if (
        not executable.is_absolute()
        or not executable.is_file()
        or not os.access(executable, os.X_OK)
    ):
        problems.append("executable is missing, not executable, or not absolute")
    elif executable.resolve() != (Path(sys.executable).parent / "rctl").resolve():
        problems.append("command uses a different rctl environment than this package")
    selected = Path(argv[2])
    if not selected.is_absolute() or selected.resolve() != root:
        problems.append("command root differs from the selected project")
    if handler.get("type") != "command":
        problems.append("handler is not a command")
    # Claude Code has no per-handler context limit; the adapter bounds its output.
    limit = {"codex": {"additionalContextLimit"}, "claude": set()}[host]
    if set(handler) - {"type", "command", "timeout"} - limit:
        problems.append("handler includes customized options; compare the candidate")
    if group.get("matcher") not in (None, ""):
        problems.append("custom matcher may limit delivery")
    expected_budget = {"SessionStart": 8000, "UserPromptSubmit": 2000}.get(event)
    if handler.get("timeout") != 10 or (
        limit and handler.get("additionalContextLimit") != expected_budget
    ):
        problems.append("timeout/context budget differs from the packaged handler")
    finding(
        name,
        "different" if problems else "current",
        "; ".join(problems)
        if problems
        else "Command addressing matches this project; delivery and trust are not inspected.",
        "Compare the generated handler and retain intended customization."
        if problems
        else "None.",
    )


def doctor(root, codex=True, claude=True):
    inspection = inspect_installation(root, codex, claude)[0]
    for host in ("codex", "claude"):
        inspection[f"{host}_trust"] = "not_inspected"
        inspection[f"{host}_delivery"] = "not_inspected"
    return inspection, []


def export_update(root, destination, codex=False, claude=False):
    path = local_path(root, destination)
    if path.exists() or (root / destination).is_symlink():
        raise state_error("Update destination already exists; choose a new directory.")
    inspection, candidates, diffs, binding = inspect_installation(root, codex, claude)
    # Diagnostics can finish without an entrypoint; usable host exports cannot.
    if codex and ".codex/hooks.json" not in candidates:
        codex_hooks(root)
    if claude and ".claude/settings.json" not in candidates:
        claude_hooks(root)
    protected = {"tasks", "research", ".rctl", ".agents", ".codex", ".claude", ".git"}
    if binding is not None:
        if binding["vault"]:
            protected.add(binding["vault"])
    elif (root / ".rctl/project.json").exists():
        raise invalid("Repair the project binding before exporting update candidates.")
    for name in protected:
        if path.is_relative_to(local_path(root, name)):
            raise invalid(
                "Update destination must be outside live control and knowledge directories."
            )
    files = {f"candidates/{name}": content for name, content in candidates.items()}
    files.update(
        {f"diffs/{name}.diff": content for name, content in diffs.items() if content}
    )
    files["inspection.json"] = json_text(inspection)
    files["README.md"] = """# Reviewable rctl update candidates

Compare `diffs/` and `inspection.json` with the current project before applying changes.
`candidates/.agents/skills/research-task/` contains current packaged skill files.
Preserve intentional customizations and local-only files; differences do not identify
whether a file is outdated or locally edited. No live file has been replaced.

When included, `candidates/.codex/hooks.json` and `config.toml` are MERGE FRAGMENTS.
Merge the two rctl handlers into ONE project hook representation (JSON or inline TOML),
and merge the hooks feature setting into the existing features table. Do not replace
whole project configurations or add duplicate handlers. The host diffs show only rctl
handlers and the hooks feature; unrelated configuration is deliberately absent.

When included, `candidates/.claude/settings.json` is also a MERGE FRAGMENT: merge the
two rctl handlers into the `hooks` object of `.claude/settings.json`, keeping one per
event across that file and `.claude/settings.local.json`, and compare
`candidates/.claude/skills/research-task/` with the installed Claude Code skill copy.

Candidates name the current project and installed executable. After moving either,
generate candidates again. Review changed hooks through Codex `/hooks` when applying
them; Claude Code runs project hooks after its workspace trust dialog. This export
grants no trust and proves no host delivery. Static inspection does
not read global configuration or launch a host. No apply command is provided.
"""
    path.mkdir(parents=True, exist_ok=False)
    for name, content in files.items():
        target = path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return {
        "directory": str(path),
        "files": sorted(files),
        "review_needed": inspection["review_needed"],
    }, []
