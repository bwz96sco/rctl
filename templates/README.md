# Task templates

Copy [contract.md](contract.md) into a new task and replace its angle-bracket placeholders before begin. Set `task_id` to the task directory basename. Keep only criteria that detect a named failure and decide an in-scope action. The default review criterion works for either exploration or analysis; add command criteria using the schema and synthetic example when there is a meaningful executable check.

Use [state.md](state.md) only when work pauses or a handoff helps. Its explicit next-action and blocker sections are extracted for bounded reminders; keep one concrete step and replace placeholder text. Write [result.md](result.md) when a bounded result exists; `contract_revision` must match the governing record. Replace each `<...>` authoring placeholder in these templates; `contract check` and `begin` reject unreplaced template tokens, but do not attempt to judge all possible placeholder prose.

A task needs contract and result records; the machine acceptance record is produced by rctl. Review-input JSON is needed only for review criteria. It records the judgment used by verification and does not own a second result. Hook receipts and host launch fixtures belong to integration testing, not every task.

Scientific requirements come from the project and relevant research skills. For a comparison, add baseline, intervention, data/split, metric direction, aggregation/selection, budget, and stopping rules to the contract body before dependent work. Do not copy historical compute budgets as new execution authorization.

When a task tests only one part of an existing project question, add this optional
section after `## Question` and replace every value:

```markdown
## Question alignment

- Governing question source: research/questions/example.md#mechanism
- Governing mechanism: The broader mechanism whose evidence is being accumulated.
- This task tests: The specific increment or relationship isolated by this task.
- This task does not decide: The broader conclusion that this result cannot support or refute alone.
```

The source must be a readable project-relative Markdown path; a fragment may name
the relevant section. All four fields are required when the section is present.
Add a review criterion when closure depends on whether the declared relationship
and non-claim boundary are scientifically adequate. `rctl` validates structure and
source availability, not that scientific judgment. Criterion `evidence_refs` remain
task-relative, so cite the same source file without its fragment using a path from
the task directory, plus `result.md`.

## Project and vault scaffolding

`rctl init` reads `project/research/`; optional `--vault PATH` reads `vault/` only when
creating a new vault. Existing files are preserved. The five research files describe
durable intent, resources, baselines, and routes; vault templates hold linked scientific
notes. The packaged research-task skill explains workspace and migration boundaries.
