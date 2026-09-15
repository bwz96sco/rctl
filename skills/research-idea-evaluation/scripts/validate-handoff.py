#!/usr/bin/env python3
"""Validate idea-workflow IDs and stage ownership without judging idea quality."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CANDIDATE_ID = re.compile(r"C[1-9][0-9]*")
CANDIDATE_HEADING = re.compile(r"(?m)^##\s+(C[1-9][0-9]*)\s*:")
SCREENING_SIGNALS = {"advance", "hold", "reject"}
BRIEF_HEADING = re.compile(r"(?m)^##\s+Experiment Brief:\s*(C[1-9][0-9]*)\s*$")


def frontmatter(path: Path) -> dict[str, str | list[str]]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name}: missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path.name}: unterminated YAML frontmatter")
    result: dict[str, str | list[str]] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("\"'") for item in value[1:-1].split(",")]
            result[key] = [item for item in items if item]
        else:
            result[key] = value
    return result


def scalar(fields: dict[str, str | list[str]], key: str, path: Path) -> str:
    value = fields.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path.name}: {key} must be a nonempty scalar")
    return value


def id_list(fields: dict[str, str | list[str]], key: str, path: Path) -> list[str]:
    value = fields.get(key)
    if not isinstance(value, list):
        raise TypeError(f"{path.name}: {key} must be an inline list")
    invalid = [item for item in value if not CANDIDATE_ID.fullmatch(item)]
    if invalid:
        raise ValueError(f"{path.name}: malformed candidate IDs {invalid}")
    if len(value) != len(set(value)):
        raise ValueError(f"{path.name}: duplicate IDs in {key}")
    return value


def portfolio_ids(root: Path) -> list[str]:
    path = root / "ideas.md"
    if not path.is_file():
        raise ValueError("missing ideas.md")
    fields = frontmatter(path)
    if scalar(fields, "stage", path) != "expand_complete":
        raise ValueError("ideas.md: stage must be expand_complete")
    if scalar(fields, "next_owner", path) != "research-idea-evaluation":
        raise ValueError("ideas.md: next_owner must be research-idea-evaluation")
    ids = CANDIDATE_HEADING.findall(path.read_text(encoding="utf-8"))
    if not ids:
        raise ValueError("ideas.md: no candidate headings found")
    if len(ids) != len(set(ids)):
        raise ValueError("ideas.md: duplicate candidate IDs")
    return ids


def screening_ids(root: Path, portfolio: set[str]) -> list[str]:
    path = root / "screening.md"
    if not path.is_file():
        raise ValueError("missing screening.md")
    fields = frontmatter(path)
    if scalar(fields, "stage", path) != "screening_complete":
        raise ValueError("screening.md: stage must be screening_complete")
    if scalar(fields, "portfolio", path) != "ideas.md":
        raise ValueError("screening.md: portfolio must be ideas.md")
    if scalar(fields, "next_owner", path) != "human_shortlist":
        raise ValueError("screening.md: next_owner must be human_shortlist")

    text = path.read_text(encoding="utf-8")
    matches = list(CANDIDATE_HEADING.finditer(text))
    ids = [match.group(1) for match in matches]
    if len(ids) != len(set(ids)):
        raise ValueError("screening.md: duplicate candidate IDs")
    missing = sorted(portfolio - set(ids))
    extra = sorted(set(ids) - portfolio)
    if missing or extra:
        raise ValueError(
            "screening.md: candidate coverage mismatch; "
            f"missing={missing} extra={extra}"
        )

    required_fields = (
        "Closest-prior status",
        "Surviving delta",
        "Asset feasibility",
        "Strongest concern",
        "Evidence",
        "Screening signal",
    )
    for index, match in enumerate(matches):
        candidate_id = match.group(1)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end]
        values: dict[str, str] = {}
        for label in required_fields:
            field = re.search(rf"(?im)^-\s+{re.escape(label)}:\s*(.+?)\s*$", section)
            if field is None or not field.group(1).strip():
                raise ValueError(f"screening.md: {candidate_id} missing {label}")
            value = field.group(1).strip()
            if value.startswith("<") and value.endswith(">"):
                raise ValueError(
                    f"screening.md: {candidate_id} has placeholder {label}"
                )
            values[label] = value
        signal = values["Screening signal"].lower()
        if signal not in SCREENING_SIGNALS:
            raise ValueError(
                f"screening.md: {candidate_id} signal must be advance, hold, or reject"
            )
    return ids


def shortlist_ids(root: Path, portfolio: set[str]) -> list[str]:
    path = root / "shortlist.md"
    if not path.is_file():
        raise ValueError("missing shortlist.md")
    fields = frontmatter(path)
    if scalar(fields, "stage", path) != "shortlist_complete":
        raise ValueError("shortlist.md: stage must be shortlist_complete")
    if scalar(fields, "decision_recorded_by", path) != "human_confirmed":
        raise ValueError("shortlist.md: decision_recorded_by must be human_confirmed")
    if scalar(fields, "portfolio", path) != "ideas.md":
        raise ValueError("shortlist.md: portfolio must be ideas.md")
    if scalar(fields, "screening", path) != "screening.md":
        raise ValueError("shortlist.md: screening must be screening.md")
    if scalar(fields, "next_owner", path) != "research-idea-evaluation":
        raise ValueError("shortlist.md: next_owner must be research-idea-evaluation")
    selected = id_list(fields, "selected_candidate_ids", path)
    if not selected:
        raise ValueError(
            "shortlist.md: selected_candidate_ids must contain at least one ID"
        )
    unknown = sorted(set(selected) - portfolio)
    if unknown:
        raise ValueError(f"shortlist.md: unknown candidate IDs {unknown}")
    text = path.read_text(encoding="utf-8")
    rationale = re.search(r"(?ms)^## Human rationale\s*$\n(.*?)(?=^##\s|\Z)", text)
    rationale_text = rationale.group(1).strip() if rationale is not None else ""
    if not rationale_text or rationale_text == "<verbatim human wording>":
        raise ValueError(
            "shortlist.md: Human rationale must preserve nonempty human wording"
        )
    return selected


def table_dispositions(text: str) -> list[tuple[str, str]]:
    match = re.search(r"(?ms)^## Candidate Dispositions\s*$\n(.*?)(?=^##\s|\Z)", text)
    if not match:
        return []
    dispositions: list[tuple[str, str]] = []
    for line in match.group(1).splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and CANDIDATE_ID.fullmatch(cells[0]):
            dispositions.append((cells[0], cells[1].lower()))
    return dispositions


def validate_portfolio(root: Path) -> None:
    portfolio_ids(root)


def validate_screening(root: Path) -> None:
    portfolio = set(portfolio_ids(root))
    screening_ids(root, portfolio)


def validate_shortlist(root: Path) -> None:
    portfolio = set(portfolio_ids(root))
    screening_ids(root, portfolio)
    shortlist_ids(root, portfolio)


def validate_decision(root: Path) -> None:
    portfolio = set(portfolio_ids(root))
    screening_ids(root, portfolio)
    shortlisted = shortlist_ids(root, portfolio)
    shortlist = set(shortlisted)
    path = root / "decision.md"
    if not path.is_file():
        raise ValueError("missing decision.md")
    fields = frontmatter(path)
    if scalar(fields, "stage", path) != "converge_complete":
        raise ValueError("decision.md: stage must be converge_complete")
    status = scalar(fields, "decision_status", path)
    if status not in {"selected", "blocked"}:
        raise ValueError("decision.md: decision_status must be selected or blocked")
    selected = id_list(fields, "selected_candidate_ids", path)
    if len(selected) > 2:
        raise ValueError("decision.md: at most two candidates may be selected")
    outside = sorted(set(selected) - shortlist)
    if outside:
        raise ValueError(f"decision.md: selected IDs outside shortlist {outside}")
    if status == "selected" and not selected:
        raise ValueError("decision.md: selected status requires one or two IDs")
    if status == "blocked" and selected:
        raise ValueError("decision.md: blocked status requires no selected IDs")
    if scalar(fields, "portfolio", path) != "ideas.md":
        raise ValueError("decision.md: portfolio must be ideas.md")
    if scalar(fields, "shortlist", path) != "shortlist.md":
        raise ValueError("decision.md: shortlist must be shortlist.md")
    owners = (
        {"research-rapid-test", "research-experiment"}
        if status == "selected"
        else {"none"}
    )
    if scalar(fields, "next_owner", path) not in owners:
        raise ValueError(f"decision.md: next_owner must be one of {sorted(owners)}")

    text = path.read_text(encoding="utf-8")
    disposition_rows = table_dispositions(text)
    disposition_ids = [candidate_id for candidate_id, _ in disposition_rows]
    if len(disposition_ids) != len(set(disposition_ids)):
        raise ValueError("decision.md: duplicate candidate dispositions")
    missing = sorted(shortlist - set(disposition_ids))
    extra = sorted(set(disposition_ids) - shortlist)
    if missing or extra:
        raise ValueError(
            f"decision.md: dispositions mismatch shortlist; missing={missing} extra={extra}"
        )
    disposition_by_id = dict(disposition_rows)
    invalid_dispositions = sorted(
        candidate_id
        for candidate_id, disposition in disposition_rows
        if disposition not in {"selected", "rejected", "blocked"}
    )
    if invalid_dispositions:
        raise ValueError(
            "decision.md: invalid dispositions for "
            f"{invalid_dispositions}; expected selected, rejected, or blocked"
        )
    mismatched_selected = sorted(
        candidate_id
        for candidate_id in shortlist
        if (candidate_id in selected) != (disposition_by_id[candidate_id] == "selected")
    )
    if mismatched_selected:
        raise ValueError(
            "decision.md: selected_candidate_ids disagree with Candidate Dispositions "
            f"for {mismatched_selected}"
        )

    attack_root = root / "attacks"
    attacks = (
        {item.stem for item in attack_root.glob("*.md")}
        if attack_root.is_dir()
        else set()
    )
    if attacks != shortlist:
        raise ValueError(
            "attacks/: files must cover exactly the shortlist; "
            f"missing={sorted(shortlist - attacks)} extra={sorted(attacks - shortlist)}"
        )

    briefs = BRIEF_HEADING.findall(text)
    if len(briefs) != len(set(briefs)):
        raise ValueError("decision.md: duplicate experiment brief IDs")
    if set(briefs) != set(selected):
        raise ValueError(
            "decision.md: experiment briefs must cover exactly selected IDs; "
            f"expected={selected} actual={briefs}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stage", choices=("portfolio", "screening", "shortlist", "decision")
    )
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    try:
        if args.stage == "portfolio":
            validate_portfolio(args.root)
        elif args.stage == "screening":
            validate_screening(args.root)
        elif args.stage == "shortlist":
            validate_shortlist(args.root)
        elif args.stage == "decision":
            validate_decision(args.root)
    except (OSError, TypeError, ValueError) as exc:
        print(f"FAIL {exc}")
        return 1
    print(f"OK research handoff: {args.stage}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
