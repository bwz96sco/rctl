# Profiling

## profiling_triggers

Profile only if fixture runtime unexpectedly exceeds one minute.

## target_types

script: `train.py`

process: local Python process

gpu: not used in fixture

memory: local process RSS

interconnect: not used in fixture

framework: Python runtime

cpu: per-function runtime if needed

## tools

Use `python -m cProfile` for fixture profiling.

## instrumentation_policy

Prefer wrapper commands over inline edits.

## profile_output_root

`runs/demo-fixture/profile/`

## report_structure

Summarize top functions, total runtime, and suggested cleanup.

## instrumentation_changelog_required

Required if any inline instrumentation is added.

## cleanup_policy

Remove temporary profiling wrappers after validation.

## unknowns

None for fixture.
