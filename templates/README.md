# Task templates

Copy [contract.md](contract.md) into a new task and replace its angle-bracket placeholders before begin. Set `task_id` to the task directory basename. Keep only criteria that detect a named failure and decide an in-scope action. The default review criterion works for either exploration or analysis; add command criteria using the schema and synthetic example when there is a meaningful executable check.

Use [state.md](state.md) only when work pauses or a handoff helps. Write [result.md](result.md) when a bounded result exists; `contract_revision` must match the governing record. Replace each `<...>` authoring placeholder in these templates; `contract check` and `begin` reject unreplaced template tokens, but do not attempt to judge all possible placeholder prose.

A task needs contract and result records; the machine acceptance record is produced by rctl. Review-input JSON is needed only for review criteria. It records the judgment used by verification and does not own a second result. Hook receipts and host launch fixtures belong to integration testing, not every task.

Scientific requirements come from the project and relevant research skills. For a comparison, add baseline, intervention, data/split, metric direction, aggregation/selection, budget, and stopping rules to the contract body before dependent work. Do not copy historical compute budgets as new execution authorization.
