# Adapter Sources

## fact_sources

- command_authority: fixture-specified `uv run python train.py --config configs/tiny.yaml`.
- canonical_output_root: fixture-specified `runs/demo-fixture/`.
- validator source: `skills/research-experiment/scripts/validate-adapter.py`; stage this fixture's `entrypoint.md` as `SKILL.md` in a disposable directory before checking it.

## update_history

- 2026-07-03: created fixture adapter; added all required files and validator labels; validator command above should return OK.

## open_questions

None for fixture.
