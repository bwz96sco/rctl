"""Structural checks only; no scientific or execution verdicts."""

import json
import re
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator


class RctlError(Exception):
    def __init__(self, code, message, next_action, exit_code=2):
        super().__init__(message)
        self.code = code
        self.message = message
        self.next_action = next_action
        self.exit_code = exit_code


def invalid(message):
    return RctlError("INVALID_INPUT", message, "Correct the input and try again.")


def read_text(path: Path) -> str:
    try:
        with path.open(encoding="utf-8", newline="") as stream:
            return stream.read()
    except FileNotFoundError:
        raise RctlError(
            "NOT_FOUND",
            f"Missing file: {path}",
            "Restore the file or correct its path.",
            3,
        ) from None
    except UnicodeError:
        raise invalid(f"Expected UTF-8 text: {path}") from None
    except OSError:
        raise RctlError(
            "NOT_FOUND",
            f"Cannot read file: {path}",
            "Check the file path and permissions.",
            3,
        ) from None


def local_path(root: Path, value: str | Path, base: Path | None = None) -> Path:
    path = ((base or root) / value).resolve()
    if not path.is_relative_to(root):
        raise invalid("Selected path must remain inside the project root.")
    return path


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise invalid("YAML mapping keys must be strings.")
        if key in mapping:
            raise invalid(
                f"Duplicate YAML mapping key at line {key_node.start_mark.line + 1}."
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


def resource_text(directory, name):
    resource = files("rctl").joinpath(directory, name)
    # Editable installs import src/rctl; wheel installs carry these resources.
    source_root = Path(__file__).resolve().parents[2]
    if not resource.is_file() and (source_root / "pyproject.toml").is_file():
        resource = source_root / directory / name
    return resource.read_text(encoding="utf-8")


def sections(body):
    """Ignore fenced examples when identifying document headings."""
    found = {}
    current = None
    fence = None
    for line in body.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            if current:
                found[current].append(line)
            continue
        if fence:
            if current:
                found[current].append(line)
            continue
        heading = re.match(r"^## (.+?)\s*$", line)
        if heading:
            current = heading[1]
            if current in found:
                raise invalid(f"Duplicate section: {current}.")
            found[current] = []
        elif re.match(r"^# ", line):
            current = None
        elif current:
            found[current].append(line)
    return {key: "\n".join(value).strip() for key, value in found.items()}


def parse_contract(text, source, task_id, root=None, task=None):
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise invalid(f"{source}: require leading YAML frontmatter delimited by ---.")
    end = next(
        (i for i in range(1, len(lines)) if lines[i].rstrip("\r\n") == "---"), None
    )
    if end is None:
        raise invalid(f"{source}: missing closing frontmatter delimiter.")
    try:
        data = yaml.load("".join(lines[1:end]), Loader=UniqueLoader)
    except yaml.YAMLError:
        raise invalid(f"{source}: invalid safe YAML frontmatter.") from None
    except RctlError as exc:
        raise invalid(f"{source}: {exc.message}") from None
    schema = json.loads(resource_text("schemas", "contract.schema.json"))
    error = next(Draft202012Validator(schema).iter_errors(data), None)
    if error:
        field = ".".join(str(part) for part in error.absolute_path) or "frontmatter"
        location = list(error.absolute_path)
        if len(location) >= 2 and location[0] == "criteria":
            criterion = data["criteria"][location[1]]
            if isinstance(criterion, dict):
                field += f" (criterion {criterion.get('id', location[1])}; methods: command or review)"
        raise invalid(
            f"{source}: invalid {field} ({error.validator}); follow contract.schema.json."
        )
    if data["task_id"] != task_id:
        raise invalid(f"{source}: task_id must match directory basename {task_id}.")
    ids = [criterion["id"] for criterion in data["criteria"]]
    if len(ids) != len(set(ids)):
        raise invalid(f"{source}: criterion IDs must be unique.")
    headings = sections("".join(lines[end + 1 :]))
    for name in ("Question", "Scope", "Constraints", "Stop conditions"):
        if not headings.get(name):
            raise invalid(f"{source}: require nonempty ## {name} section.")
    if root is not None:
        for criterion in data["criteria"]:
            for ref in criterion["evidence_refs"]:
                if not urlsplit(ref).scheme:
                    local_path(root, ref, task)
            for ref in criterion["method"].get("inputs", []):
                if urlsplit(ref).scheme:
                    raise invalid(f"{source}: command inputs must be local paths.")
                local_path(root, ref, task)
    return data


def require_completed(text, source):
    # The bundled draft uses <...> authoring markers, not a semantic score.
    markers = re.findall(r"<[^<>\n]+>", resource_text("templates", "contract.md"))
    if any(marker in text for marker in markers):
        raise invalid(
            f"{source}: replace the draft's <...> authoring placeholders before begin/amend."
        )
