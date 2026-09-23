# Adapter Sources

## fact_sources

- command_authority: fixture-specified `uv run python train.py --config configs/tiny.yaml`.
- canonical_output_root: fixture-specified `runs/demo-fixture/`.
- validator output: `uv run python skills/experiment-adapter-builder/scripts/validate_adapter_skill.py skills/experiment-adapter-builder/fixtures/demo-experiment-workflow`.

## update_history

- 2026-07-03: created fixture adapter; added all required files and validator labels; validator command above should return OK.

## open_questions

None for fixture.
