# Preflight Health

## data_checks

Verify `data/demo_train.jsonl` and `data/demo_valid.jsonl` exist.

## checkpoint_checks

Checkpoint is optional for fixture; if provided, verify path exists.

## baseline_checks

Baseline metrics live at `runs/demo-baseline/metrics.json`.

## environment_checks

Run `uv run python --version` and import the demo package.

## gpu_memory_checks

Fixture is CPU-only; GPU memory checks are marked not applicable.

## dependency_checks

Check `pyproject.toml` and `uv.lock` when present.

## smoke_or_dry_run_gate

Run `uv run python train.py --config configs/tiny.yaml --dry-run`.

## launch_blockers

Missing data, missing config, failed import, or unwritable output root.

## unknowns

None for fixture.
