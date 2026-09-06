# Initial retained-evidence analysis handoff

Task: hook-loading-compatibility. Governing contract revision: 2. First-session analysis is complete; pause with the task active. No acceptance verification or closure has been performed.

## Observed progress

Read the task skill, governing contract, research/README.md, and installed CLI status. Initial status was active, revision 2, contract_drift False, verification None, currentness not_checked, historical_closure None. No prior state.md or result.md existed.

Inspected all three routes' launch.json, summary.json, events.jsonl, receipts.jsonl, final.txt, prompt.txt, and stderr.txt. The prompts are identical no-tool-use reminder-delivery prompts; stderr files are empty. Host agent-message events agree with final.txt and summary final fields. Event streams contain no tool executions. Inline and project streams each include two hook-trust warning items; these warnings alone do not establish delivery.

All launches record codex-cli 0.153.4 with approval never, --ignore-user-config, plugins/apps disabled, --skip-git-repo-check, --ephemeral, workspace-write sandbox, and separate --cd roots. Environment overrides select tasks/retained-comparison and hook-receipts.jsonl in each root. Inline supplies SessionStart and UserPromptSubmit command hooks via invocation-local -c arguments, with context limits 8000/2000 and timeout 10. Inline and project enable hooks and use --dangerously-bypass-hook-trust. Project supplies the explicit project trust_level="trusted" override but no inline hook definitions. The none control disables hooks. Paths in retained launch arguments were inspected as evidence only; no commands from those arguments were executed.

Implemented task-local analyze.py independently using only the Python standard library, without reading, importing, executing, or modifying check_analysis.py. The script derives receipt event counts and session binding from receipts and thread.started host events, task reporting from final.txt, and exit codes from summary.json. It writes evidence/analysis.json under the frozen rule.

Executed once, from tasks/hook-loading-compatibility:

```sh
UV_CACHE_DIR=/Users/zhangbowen/Projects/rctl/.work/release-task/.uv-cache uv run --offline --no-project python analyze.py
```

Exit code: 0. Derived output:

| Route | Exit | Receipts | Receipt events | Task reported | Complete delivery |
| --- | --- | --- | --- | --- | --- |
| inline | 0 | 2 | SessionStart: 1; UserPromptSubmit: 1 | true | true |
| project | 0 | 0 | none | false | false |
| none | 0 | 0 | none | false | false |

Host session IDs:

- inline: 01a07578-3f7e-7550-9472-8a0db586b725; both receipts match.
- project: 01a07578-4304-78f0-9367-e60133d2f5d7.
- none: 01a07578-4054-70d0-81d3-68d323aa9054.

Inline final reports retained-comparison, active, B0, and C1. Project and none finals report NO_RCTL_REMINDER. Derived assessment: not_supported. The inline baseline and disabled control satisfy the fixed conditions, while project exits 0 without complete delivery. Empty project/none receipts files are the contract's normalized absence inputs, not emitted receipts.

Raw evidence, the contract, and the supplied independent checker were preserved. No result.md, reviews.json, verification report, or closeout was created. No network, new host-route probes, agents, or global configuration changes were used. The one local analysis run consumes the first-session analysis portion of the frozen budget.

## Unresolved work and next action

Next action: in a fresh rctl-enabled host session, read contract.md, this saved state.md, analyze.py, evidence/analysis.json, and raw cited evidence, and run status with the exact installed executable before preparing result.md and the AC-02 evidence review for revision 2.

The second session must inspect the independent checker and applicable review format, write the bounded result and reviews.json, then run the declared verification through rctl. AC-01 command verification and AC-02 evidence judgment are both pending. Analysis execution is not independent verification; no acceptance criterion is claimed passed. Close only after verification passes and is applicable; otherwise retain the unresolved failure with the task active.

Use /Users/zhangbowen/Projects/rctl/.work/release-venv/bin/rctl for every rctl operation, with --root /Users/zhangbowen/Projects/rctl/.work/release-task and task tasks/hook-loading-compatibility. Keep the second session within the remaining review/verification/guarded-closeout budget; no new route probes or network research.

## Limitations

The observations support inline reminder delivery and absent observed project-file delivery only for these three launches and recorded isolated settings. Missing receipts plus NO_RCTL_REMINDER do not identify the root cause. One launch per route cannot establish reliability, other host versions, ordinary persisted installation, resume/compaction behavior, or comparative model performance. The synthetic B0/C1 task content is a delivery marker, not research-performance evidence. Launch metadata records the intended project-file route; this analysis does not independently inspect the original project configuration outside the working root.

README.md, docs/PRD.md, docs/SPEC.md, docs/DEVELOPMENT.md, docs/ACCEPTANCE.md, docs/CLI.md, and schemas/ referenced by project instructions are absent in this disposable root. The task contract and research/README.md supply the bounded analysis authority; no rctl implementation milestone or source change was attempted.
