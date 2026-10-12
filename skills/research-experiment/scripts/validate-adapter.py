#!/usr/bin/env python3
"""Check adapter metadata and declared local references, not runner validity."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

RUNTIME_FIELDS = (
    "current_run_id",
    "current_campaign_status",
    "today_failures",
    "temporary_blockers",
    "live_queue_status",
    "latest_result",
    "raw_log_excerpt",
    "checkpoint_blob",
)


def local_references(text: str, *, legacy: bool = False) -> set[str]:
    links = set(re.findall(r"\[[^\]]+\]\(([^\s)]+)\)", text))
    if legacy:
        # Earlier adapters use code spans for their reference load order.
        links.update(re.findall(r"`((?:references|templates)/[^`\n]+)`", text))
    return links


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill = root / "SKILL.md"
    if not skill.is_file():
        return ["missing required file: SKILL.md"]
    text = skill.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.DOTALL)
    if not frontmatter:
        errors.append("SKILL.md missing YAML frontmatter")
    else:
        for field in ("name", "description"):
            match = re.search(rf"(?m)^{field}:[ \t]*([^\r\n]+)$", frontmatter[1])
            if not match or not match[1].strip().strip("\"'"):
                errors.append(f"SKILL.md missing nonempty {field} frontmatter")
    body = text[frontmatter.end() :] if frontmatter else text
    if not body.strip():
        errors.append("SKILL.md has no operational guidance")

    documents = [skill]
    for directory in ("references", "templates"):
        documents.extend(sorted((root / directory).rglob("*.md")))
    for document in documents:
        source = document.read_text(encoding="utf-8")
        relative = document.relative_to(root)
        for reference in sorted(local_references(source, legacy=document == skill)):
            parts = urlsplit(reference)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = document.parent / unquote(parts.path)
            if not target.is_file():
                errors.append(f"{relative} references missing file: {reference}")
            elif not target.stat().st_size:
                errors.append(f"{relative} references empty file: {reference}")
        if directory_is_runtime_guidance(document, root):
            for field in RUNTIME_FIELDS:
                if re.search(rf"(?im)^\s*(?:[-*]\s*)?{field}\s*:", source):
                    errors.append(f"{relative} contains mutable runtime field: {field}")
    return errors


def directory_is_runtime_guidance(path: Path, root: Path) -> bool:
    return path == root / "SKILL.md" or path.is_relative_to(root / "references")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adapter_dir", type=Path)
    args = parser.parse_args()
    root = args.adapter_dir.resolve()
    if not root.is_dir():
        errors = [f"adapter dir is not a directory: {root}"]
    else:
        try:
            errors = validate(root)
        except (OSError, UnicodeError) as error:
            errors = [f"Cannot inspect adapter: {error}"]
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if errors:
        return 1
    print(
        f"OK adapter structure and local references: {root}; runner evidence unassessed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
