---
schema_version: 1
task_id: hook-loading-compatibility
contract_revision: 2
assessment: not_supported
---

# Retained hook-loading comparison

## Outcome

The retained launches do not establish project-file delivery parity with invocation-local inline hooks. Inline delivered the selected-task reminder; the project route, with its recorded project-trust override, had no observed delivery. The disabled control behaved as required. Under revision 2's fixed rule, the assessment is `not_supported`.

## Evidence

The second session inspected `analyze.py`, `evidence/analysis.json`, the supplied independent `check_analysis.py`, and every route's `launch.json`, `summary.json`, `events.jsonl`, `receipts.jsonl`, `final.txt`, `prompt.txt`, and `stderr.txt`. The derived analysis agrees with the raw observations:

| Route | Exit code | Receipts | Receipt event counts | Model reports task | Complete delivery |
| --- | --- | --- | --- | --- | --- |
| inline | 0 | 2 | SessionStart: 1; UserPromptSubmit: 1 | true | true |
| project | 0 | 0 | empty | false | false |
| none | 0 | 0 | empty | false | false |

`evidence/inline/events.jsonl` identifies session `01a07578-3f7e-7550-9472-8a0db586b725`; both receipts in `evidence/inline/receipts.jsonl` bind to it and identify `tasks/retained-comparison`. `evidence/inline/final.txt` reports `retained-comparison`, `active`, `B0`, and `C1`. Thus all complete-delivery conditions hold for the baseline.

`evidence/project/events.jsonl` identifies session `01a07578-4304-78f0-9367-e60133d2f5d7`; `evidence/none/events.jsonl` identifies session `01a07578-4054-70d0-81d3-68d323aa9054`. Both routes have empty normalized `receipts.jsonl` inputs, zero receipt counts in their `summary.json`, and `NO_RCTL_REMINDER` in their `final.txt`. The normalized inputs represent absence, not emitted receipts. Host agent-message events agree with all three final texts and summary final fields. All stderr files are empty; the event streams show no tool execution. Inline and project both emit hook-trust warnings, which do not establish delivery.

The three `launch.json` files record Codex CLI 0.153.4, approval `never`, `--ignore-user-config`, disabled plugins/apps, `--skip-git-repo-check`, `--ephemeral`, and `workspace-write`, with separate roots and the same task-path and receipt-log selections. The prompts are identical and prohibit tools. Inline enables hooks with invocation-local SessionStart and UserPromptSubmit definitions (timeout 10; context limits 8000 and 2000). Project enables hooks and supplies an explicit project `trust_level="trusted"` override without inline hook definitions. Both use `--dangerously-bypass-hook-trust`; none disables hooks.

Computed observations in `evidence/analysis.json` come from the first session's single standard-library run: `UV_CACHE_DIR=/Users/zhangbowen/Projects/rctl/.work/release-task/.uv-cache uv run --offline --no-project python analyze.py` (exit 0, recorded in `state.md`). This session inspected that derivation without rerunning it. With a complete inline baseline, a valid disabled control, and successful project exit without complete delivery, the frozen comparison yields `not_supported`.

AC-01's declared command, `uv run --offline --no-project python check_analysis.py`, independently recomputes the retained counts and assessment and checks result agreement. AC-02 in `reviews.json` is an agent evidence judgment about interpretation and scope. Document parsing establishes structure; neither parsing nor a review label substitutes for command execution. Verification outcomes and closure belong to the rctl machine record.

## Deviations

No changes to revision 2, raw observations, the analysis, or the independent checker. No additional analysis run, host probe, network work, delegation, or global configuration changes. The initial status invocation placed `--root` after the subcommand and was rejected; the corrected invocation succeeded without changing task state. This second session completes the existing handoff's review and verification scope.

## Next action

Run the declared verification with `reviews.json`, inspect both criteria and command logs, and close only if the current report passes and the rctl guard succeeds. Stop at this bounded finding; investigation of root cause or other host settings requires separate authorized work.

## Limitations

Missing receipts together with `NO_RCTL_REMINDER` establish absent observed delivery under these recorded flags, not its root cause. Launch metadata records the intended project-file route; the original project configuration outside this working root was not independently inspected. One retained launch per route cannot establish reliability, other versions, ordinary persisted installation, resume/compaction behavior, or comparative model performance. The observations were already available, not a blinded prospective experiment. Synthetic B0/C1 content serves as a delivery marker and provides no research-performance evidence. Project development documents and schemas are absent from this disposable root; the frozen contract governs this analysis, with the installed CLI's packaged schemas consulted for result/review format only.
