"""Read explicit handoff fields without interpreting scientific prose."""

import re

from .documents import RctlError, read_text

FIELDS = {"Next action": "next_action", "Blockers": "blockers"}


def extract(text):
    entries = {key: [] for key in FIELDS.values()}
    current = None
    legacy = False
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        field = re.match(r"^(?:-\s+)?(Next action|Blockers):\s*(.*)$", line)
        if heading:
            current = FIELDS.get(heading[1]) if line.startswith("## ") else None
            legacy = False
            if current:
                entries[current].append([])
        elif field:
            current = FIELDS[field[1]]
            legacy = True
            entries[current].append([field[2]])
        elif legacy and (
            not line.strip() or re.match(r"^(?:-\s+)?[A-Za-z][A-Za-z /-]+:", line)
        ):
            current = None
        elif current:
            entries[current][-1].append(line)
    result = {}
    warnings = []
    for key, values in entries.items():
        value = "\n".join(values[0]).strip() if len(values) == 1 else ""
        if re.fullmatch(r"<[^>]+>", value):
            value = ""
        result[key] = value or None
        if len(values) > 1:
            warnings.append(f"Ambiguous handoff {key}: repeated fields; read state.md.")
        elif key == "next_action" and not value:
            warnings.append("No explicit handoff next action; read state.md.")
    return result, warnings


def read_handoff(task):
    empty = dict.fromkeys(FIELDS.values())
    try:
        path = task.file("state.md")
        if not path.exists() and not path.is_symlink():
            return empty, [
                "No handoff recorded; save a concrete next action to resume."
            ]
        return extract(read_text(path))
    except RctlError:
        return empty, ["Handoff unavailable; inspect state.md."]
