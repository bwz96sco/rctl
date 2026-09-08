"""Explicit views of existing research guidance; no second knowledge store."""

import re

from .documents import RctlError, local_path, read_text, sections

SOURCES = {
    "research/PROGRAM.md": {"Goal": "goal", "Current guidance": "current_guidance"},
    "research/ROUTES.md": {"Reuse Rule": "reuse_rule"},
}


def read_project(root):
    data = dict.fromkeys(("goal", "current_guidance", "reuse_rule"))
    warnings = []
    for source, fields in SOURCES.items():
        try:
            content = sections(read_text(local_path(root, source)))
        except (RctlError, OSError, ValueError) as error:
            reason = str(error).replace(f"{root}/", "")
            warnings.append(f"Project guidance unavailable: {source}: {reason}")
            continue
        for heading, key in fields.items():
            value = content.get(heading, "").strip()
            # Authoring placeholders occupy the whole section. Markdown URI and
            # email autolinks are useful guidance even when they stand alone.
            autolink = re.fullmatch(
                r"<(?:[A-Za-z][A-Za-z0-9+.-]*:[^<>\s]*|[^<>\s@]+@[^<>\s@]+)>",
                value,
            )
            placeholder = re.fullmatch(r"<[^<>]+>", value) and not autolink
            if value and not placeholder:
                data[key] = value
            elif heading != "Current guidance" or value:
                warnings.append(
                    f"Project guidance missing or unfinished: {source} / {heading}."
                )
    return {"available": any(data.values()), **data, "sources": list(SOURCES)}, warnings
