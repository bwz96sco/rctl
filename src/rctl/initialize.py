"""Create missing project scaffolding while preserving operator-owned content."""

import json

from .documents import invalid, local_path, read_text, resource_tree, validate_schema
from .integration import codex_hooks


def vault_path(root, value):
    path = local_path(root, value)
    reserved = {"tasks", "research", ".rctl", ".agents", ".codex", ".git"}
    control_paths = [(root / name).resolve() for name in reserved]
    if path == root or any(
        path.is_relative_to(control) or control.is_relative_to(path)
        for control in control_paths
    ):
        raise invalid("Vault must be a separate directory inside the project root.")
    return path


def initialize(root, vault=None, codex=False):
    manifest = local_path(root, ".rctl/project.json")
    binding = {"schema_version": 1, "vault": None}
    if manifest.is_file():
        try:
            binding = json.loads(read_text(manifest))
        except ValueError:
            raise invalid("Invalid JSON in .rctl/project.json.") from None
        validate_schema(binding, manifest, "project")
    if binding["vault"] is not None:
        bound = vault_path(root, binding["vault"])
        if bound.relative_to(root).as_posix() != binding["vault"]:
            raise invalid(
                "Stored vault binding must be a normalized project-relative path."
            )
    selected = vault_path(root, vault) if vault is not None else None
    if selected is not None:
        value = selected.relative_to(root).as_posix()
        if manifest.is_file() and binding["vault"] != value:
            raise invalid(
                "Vault binding differs; review and edit .rctl/project.json explicitly."
            )
        binding["vault"] = value
    if binding["vault"] is not None:
        selected = vault_path(root, binding["vault"])

    files = resource_tree("templates/project")
    files["research/README.md"] = files["research/README.md"].replace(
        "__VAULT_LOCATION__",
        binding["vault"] or "Existing project note location (no vault bound)",
    )
    files.update(
        {
            f".agents/skills/research-task/{name}": content
            for name, content in resource_tree("skills/research-task").items()
        }
    )
    files[".rctl/project.json"] = json.dumps(binding, indent=2) + "\n"
    directories = {root / "tasks"}
    warnings = []
    if selected is not None:
        directories.add(selected)
        if selected.exists():
            warnings.append("Existing vault associated without modifying its contents.")
        else:
            files.update(
                {
                    f"{binding['vault']}/{name}": content
                    for name, content in resource_tree("templates/vault").items()
                }
            )
    if codex:
        hooks, entrypoint = codex_hooks(root)
        files[".codex/hooks.json"] = json.dumps(hooks, indent=2) + "\n"
        files[".codex/config.toml"] = "[features]\nhooks = true\n"
        files[".rctl/codex/README.md"] = f"""# Project Codex reminders

Inspect `.codex/hooks.json`, then launch Codex from this project with the selected task:

```sh
export RCTL_TASK_PATH=tasks/your-task
codex --enable hooks
```

Codex owns project and hook trust. Review and trust the exact definitions through `/hooks`.
`rctl init` does not grant trust or start Codex. Existing configuration is preserved;
merge the two rctl hook handlers manually if `.codex/hooks.json` already existed.
Do not use `--ignore-user-config` for project-file loading: it suppressed delivery in
Codex CLI 0.153.4 testing. Tested delivery used invocation-only hook trust bypass;
persisted interactive trust has not been verified by rctl's release checks.

The hook uses `{entrypoint}` and fixes project root `{root}`. After moving the project
or Python environment, review and update the hook command; rerunning init preserves it.
Hook reminders never execute checks or confer scientific acceptance.
See https://developers.openai.com/codex/hooks for host configuration and trust behavior.

To remove this integration, remove its two handlers and the project-local research-task
skill if no longer wanted. Preserve unrelated host settings and task records.
"""
        warnings.append(
            "Codex files do not grant project or hook trust; read .rctl/codex/README.md."
        )

    # Inspect every destination and ancestor before the first write.
    targets = {}
    for name, content in files.items():
        target = local_path(root, name)
        targets[target] = content
        directories.update(
            parent
            for parent in target.parents
            if parent != root and parent.is_relative_to(root)
        )
    for path in directories:
        local_path(root, path)
        if path.exists() and not path.is_dir():
            raise invalid(f"Expected directory: {path.relative_to(root)}")
    for path in targets:
        if path in directories or (path.exists() and not path.is_file()):
            raise invalid(f"Expected file: {path.relative_to(root)}")
    created, preserved = [], []
    for path in sorted(directories, key=lambda path: (len(path.parts), str(path))):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created.append(path.relative_to(root).as_posix() + "/")
    for path, content in targets.items():
        name = path.relative_to(root).as_posix()
        if path.exists():
            preserved.append(name)
            if name in {".codex/hooks.json", ".codex/config.toml"}:
                warnings.append(
                    f"Preserved {name}; review existing configuration before use."
                )
        else:
            with path.open("x", encoding="utf-8") as stream:
                stream.write(content)
            created.append(name)
    return {
        "root": str(root),
        "vault": binding["vault"],
        "created": created,
        "preserved": preserved,
    }, warnings
