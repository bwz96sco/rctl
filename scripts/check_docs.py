# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7", "jsonschema>=4.18,<5"]
# ///
"""Check preparation artifacts; this is not the rctl acceptance suite."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> object:
    def reject_constant(value: str) -> None:
        raise ValueError(f"{path}: non-JSON constant {value}")

    return json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_constant)


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader: UniqueLoader, node: yaml.MappingNode) -> dict:
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in mapping:
            raise ValueError(f"Duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"Missing frontmatter: {path}"
    metadata, body = text[4:].split("\n---\n", 1)
    parsed = yaml.load(metadata, Loader=UniqueLoader)
    assert isinstance(parsed, dict), f"Expected metadata object: {path}"
    return parsed, body


def anchor_ids(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        heading = re.sub(r"[`*_]", "", heading).lower()
        result.add(re.sub(r"[^\w\- ]", "", heading).replace(" ", "-"))
    return result


def check_links() -> int:
    count = 0
    sources = list(ROOT.glob("*.md"))
    for directory in ("docs", "schemas", "templates", "examples"):
        sources.extend((ROOT / directory).rglob("*.md"))
    for source in sources:
        if source.is_relative_to(ROOT / "docs/evidence"):
            continue  # Retrieved source pages retain their original relative links.
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
            target = target.strip("<>")
            parts = urlsplit(target)
            if parts.scheme or parts.netloc:
                continue
            path = (source.parent / unquote(parts.path)).resolve() if parts.path else source
            assert path.exists(), f"Broken link: {source.relative_to(ROOT)} -> {target}"
            if parts.fragment and path.suffix == ".md":
                assert unquote(parts.fragment) in anchor_ids(path), f"Broken anchor: {source} -> {target}"
            count += 1
    return count


def require_sections(body: str, names: list[str]) -> None:
    chunks = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    sections = dict(zip(chunks[1::2], chunks[2::2]))
    for name in names:
        assert sections.get(name, "").strip(), f"Missing or empty section: {name}"


def main() -> None:
    json_files = [
        path
        for directory in ("schemas", "examples", "docs/evidence")
        for path in (ROOT / directory).rglob("*.json")
    ]
    for path in json_files:
        read_json(path)
    schemas = {name: read_json(ROOT / "schemas" / f"{name}.schema.json") for name in ("contract", "result", "reviews")}
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    example = ROOT / "examples/retained-comparison"
    contract, contract_body = frontmatter(example / "contract.md")
    result, result_body = frontmatter(example / "result.md")
    reviews = read_json(example / "reviews.json")
    for name, instance in (("contract", contract), ("result", result), ("reviews", reviews)):
        Draft202012Validator(schemas[name]).validate(instance)
    require_sections(contract_body, ["Question", "Scope", "Constraints", "Stop conditions"])
    require_sections(result_body, ["Outcome", "Evidence", "Deviations", "Next action", "Limitations"])
    assert contract["task_id"] == result["task_id"] == reviews["task_id"] == example.name
    assert result["contract_revision"] == reviews["contract_revision"] == 1
    criteria = {item["id"]: item for item in contract["criteria"]}
    assert len(criteria) == len(contract["criteria"]), "Duplicate criterion IDs"
    review_ids = [item["criterion_id"] for item in reviews["checks"]]
    assert len(review_ids) == len(set(review_ids)), "Duplicate reviews"
    assert set(review_ids) == {key for key, item in criteria.items() if item["method"]["type"] == "review"}
    for criterion in criteria.values():
        refs = criterion["evidence_refs"] + criterion["method"].get("inputs", [])
        for ref in refs:
            assert (example / ref).is_file(), f"Missing fixture evidence: {ref}"
    for review in reviews["checks"]:
        assert set(criteria[review["criterion_id"]]["evidence_refs"]) <= set(review["evidence_refs"])
        for ref in review["evidence_refs"]:
            assert (example / ref).is_file(), f"Missing review evidence: {ref}"

    requirements = re.findall(r"^\| (R-\d+) \|", (ROOT / "docs/PRD.md").read_text(), re.MULTILINE)
    acceptance = (ROOT / "docs/ACCEPTANCE.md").read_text()
    cases = re.findall(r"^\| (A-\d+) \| ([^|]+) \|", acceptance, re.MULTILINE)
    assert len(requirements) == len(set(requirements)) == 12
    assert len(cases) == len({case[0] for case in cases}) == 20
    mapped = set(re.findall(r"R-\d+", " ".join(case[1] for case in cases)))
    assert mapped == set(requirements), f"Requirement coverage mismatch: {mapped ^ set(requirements)}"
    links = check_links()
    print(f"PASS preparation documents: {links} local links; {len(json_files)} JSON files; 3 schemas and example inputs; 12 requirements mapped to 20 acceptance cases.")


if __name__ == "__main__":
    main()
