"""Structural checks only; no scientific or execution verdicts."""

import json
import re
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator


class RctlError(Exception):
    def __init__(self, code, message, next_action, exit_code=2, data=None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.next_action = next_action
        self.exit_code = exit_code
        self.data = data or {}


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


def resource_directory(directory):
    resource = files("rctl").joinpath(directory)
    # Editable installs import src/rctl; wheels carry the same resources.
    source_root = Path(__file__).resolve().parents[2]
    if not resource.is_dir() and (source_root / "pyproject.toml").is_file():
        resource = source_root / directory
    return resource


def resource_text(directory, name):
    return resource_directory(directory).joinpath(name).read_text(encoding="utf-8")


def resource_tree(directory):
    """Return packaged UTF-8 scaffold files, including dotfiles."""
    def walk(parent, prefix=""):
        for item in sorted(parent.iterdir(), key=lambda item: item.name):
            name = prefix + item.name
            if item.is_dir():
                yield from walk(item, name + "/")
            else:
                yield name, item.read_text(encoding="utf-8")

    return dict(walk(resource_directory(directory)))


def markdown_lines(body):
    """Yield each original line and whether it may define document structure."""
    fence = None
    for line in body.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if (
                marker
                and marker[1][0] == fence[0]
                and len(marker[1]) >= len(fence)
                and not marker[2].strip()
            ):
                fence = None
            yield line, False
        elif marker and (marker[1][0] == "~" or "`" not in marker[2]):
            fence = marker[1]
            yield line, False
        else:
            yield line, True


def sections(body):
    """Ignore fenced examples when identifying document headings."""
    found = {}
    current = None
    for line, structural in markdown_lines(body):
        if not structural:
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


def parse_document(text, source, task_id, kind):
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
    validate_schema(data, source, kind)
    if data["task_id"] != task_id:
        raise invalid(f"{source}: task_id must match directory basename {task_id}.")
    headings = sections("".join(lines[end + 1 :]))
    required = (
        ("Question", "Scope", "Constraints", "Stop conditions")
        if kind == "contract"
        else ("Outcome", "Evidence", "Deviations", "Next action", "Limitations")
    )
    for name in required:
        if not headings.get(name):
            raise invalid(f"{source}: require nonempty ## {name} section.")
    return data


def validate_schema(data, source, kind):
    schema = json.loads(resource_text("schemas", f"{kind}.schema.json"))
    error = next(Draft202012Validator(schema).iter_errors(data), None)
    if error:
        field = ".".join(str(part) for part in error.absolute_path) or "frontmatter"
        location = list(error.absolute_path)
        if len(location) >= 2 and location[0] == "criteria":
            criterion = data["criteria"][location[1]]
            if isinstance(criterion, dict):
                field += f" (criterion {criterion.get('id', location[1])}; methods: command or review)"
        raise invalid(
            f"{source}: invalid {field} ({error.validator}); follow {kind}.schema.json."
        )


def parse_contract(text, source, task_id, root=None, task=None):
    data = parse_document(text, source, task_id, "contract")
    ids = [criterion["id"] for criterion in data["criteria"]]
    if len(ids) != len(set(ids)):
        raise invalid(f"{source}: criterion IDs must be unique.")
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


def parse_result(text, source, task_id, revision):
    data = parse_document(text, source, task_id, "result")
    if data["contract_revision"] != revision:
        raise RctlError(
            "INVALID_INPUT",
            f"{source}: result revision {data['contract_revision']} does not match governing revision {revision}.",
            "Update the result for the governing revision and verify again.",
        )
    return data


def parse_reviews(text, source, task_id, revision, contract, root=None, task=None):
    try:
        data = json.loads(text)
    except ValueError:
        raise invalid(f"{source}: invalid review JSON.") from None
    validate_schema(data, source, "reviews")
    if data["task_id"] != task_id or data["contract_revision"] != revision:
        raise invalid(
            f"{source}: review task/revision must match {task_id}, revision {revision}."
        )
    criteria = {item["id"]: item for item in contract["criteria"]}
    checks = {}
    for check in data["checks"]:
        key = check["criterion_id"]
        if (
            key in checks
            or key not in criteria
            or criteria[key]["method"]["type"] != "review"
        ):
            raise invalid(f"{source}: {key} must uniquely identify a review criterion.")
        if not set(criteria[key]["evidence_refs"]) <= set(check["evidence_refs"]):
            raise invalid(
                f"{source}: {key} must include the contract's required evidence references."
            )
        if root is not None:
            for ref in check["evidence_refs"]:
                if not urlsplit(ref).scheme:
                    local_path(root, ref, task)
        checks[key] = check
    return checks


def require_completed(text, source):
    # The bundled draft uses <...> authoring markers, not a semantic score.
    markers = re.findall(r"<[^<>\n]+>", resource_text("templates", "contract.md"))
    if any(marker in text for marker in markers):
        raise invalid(
            f"{source}: replace the draft's <...> authoring placeholders before begin/amend."
        )
