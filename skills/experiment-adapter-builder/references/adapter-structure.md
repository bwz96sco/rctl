# Adapter Structure

Generated adapter path:

```text
<project>/.agents/skills/<project>-experiment-workflow/
```

## Required Files

```text
SKILL.md
references/runners.md
references/preflight-health.md
references/queue-and-concurrency.md
references/monitoring.md
references/profiling.md
references/result-validation.md
references/adapter-sources.md
templates/run-manifest.md
templates/experiment-campaign.md
templates/experiment-code-review.md
templates/result-ledger.csv
```

## `SKILL.md` Shape

Keep it under 100 lines. Include:

- project-specific trigger description
- when to use the adapter
- command authority and reference load order
- safety rules: no invented commands, no silent metric/split/baseline changes, no claim from unchecked runs
- output handoff: run manifest, execution log, result ledger, claim boundary

## Reference File Roles

- `runners.md`: command authority, environment, working directory, runner selection, output roots
- `preflight-health.md`: data, checkpoints, baseline files, GPU/memory, environment, dry-run or smoke gates
- `queue-and-concurrency.md`: max parallelism, job state machine, retry policy, stale-job cleanup, shared-state hazards
- `monitoring.md`: logs, tracker sources, structured outputs, progress checks, raw-number summary rules
- `profiling.md`: when to profile, available tools, instrumentation policy, artifact location, cleanup
- `result-validation.md`: expected outputs, metric parsing, baseline comparison, failure classes, paper-valid evidence gate
- `adapter-sources.md`: fact provenance, update history, validator evidence, and open questions

## Template Use

Copy `templates/project-experiment-workflow-SKILL.md` to generated `SKILL.md`. Copy each `templates/reference-*.md` file to the matching generated reference file. Copy `templates/reference-adapter-sources.md` to `references/adapter-sources.md`. Copy run/campaign/result templates only if the project does not already own better ones.

## Update Policy

When updating an existing adapter, preserve project-specific facts unless a newer source proves them stale. Append unknowns to an open-questions section; do not overwrite working commands with guesses.

Every update must record:

- added facts
- modified facts
- deprecated facts
- evidence path, command, user instruction, mempal drawer ID, remote path evidence, or validator output for each changed fact
- validator command and result
