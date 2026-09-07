# rctl v0.1 Acceptance Plan

All cases below are required for release. None is claimed to have passed merely because these documents exist. Use temporary projects and synthetic evidence for automated tests; keep a real-task acceptance record separate.

| Case | Requirements | Scenario and observable result | Failure detected; response |
|---|---|---|---|
| A-01 | R-01, R-02 | A valid draft passes structural checks; missing method, duplicate criterion ID/YAML key, unknown field, or empty required section rejects begin without a record. | An ambiguous agreement reaches execution; fix parser/schema enforcement. |
| A-02 | R-03 | Begin retains exact revision 1; changed contract refuses verify/close; amendment preserves old text and adds a reasoned revision. | Silent agreement drift; fix governing-contract comparison. |
| A-03 | R-03, R-06 | Editing result or a declared local input after pass makes closure stale; handoff-only edits preserve applicability. | A check covers the wrong material or is needlessly invalidated; fix subject selection/currentness. |
| A-04 | R-05 | Declared local check records exact argv/cwd/logs and exit 0/nonzero as pass/fail. Fake prose saying passed does not create a command result. | Execution claims substituted for execution; fix executor/report provenance. |
| A-05 | R-05, R-06 | Missing executable/input, timeout, or absent review produces unknown and no closure; malformed review input executes nothing. | Missing evidence accepted as success; fix error/unknown handling. |
| A-06 | R-05 | Review IDs/revision match; source, rationale, and references are recorded; an agent review cannot satisfy an operator-only criterion. | Review applied to the wrong agreement or source; fix review binding. |
| A-07 | R-06, R-07 | Synthetic no-improvement result passes its completion criteria and closes with `not_supported`; a missing required review remains active. | Positive scientific result confused with task completion; fix aggregation and closure. |
| A-08 | R-06 | Close without result/report fails; a later failed report cannot be bypassed by an older pass; repeated close adds no entry. | Unverified/duplicate closure; fix transition guards. |
| A-09 | R-03, R-06 | Reopen requires a reason and new verification; historical closure remains visible after current files change. | Old acceptance reused across cycles or history erased; fix lifecycle. |
| A-10 | R-08 | Checkpoint saves only handoff; fresh process context finds it; an unfinished task can pause without close. | Session continuity tied to completion; fix handoff and read path. |
| A-11 | R-09, R-10 | Session task selection is explicit; unset, out-of-root, and wrong-root paths give an unavailable reminder; no other task is picked. | Wrong-task context; fix path/selection logic. |
| A-12 | R-09 | Context respects character budgets, prioritizes warnings, labels truncation, and does not run a checker or write a record. | Reminder performs work, hides critical state, or grows without bound; fix renderer/adapter boundary. |
| A-13 | R-11 | CLI operates in a non-Git temporary directory with no host, framework, network, or LLM; JSON stdout and exit codes match CLI. | Hidden runtime dependency or unusable machine interface; fix packaging/output. |
| A-14 | R-06 | Interrupted publication leaves previous record parseable; orphan logs do not become a pass; detected record change refuses overwrite. | Partial record or obvious overlapping write loses facts; fix publication/recheck. |
| A-15 | R-05, R-06 | Changing contract/result/input during a check produces unknown or record-conflict rejection, never closure. | Long check is applied to changed input; fix before/after observations. |
| A-16 | R-09, R-12 | Adapter subprocess fixtures cover both events, invalid JSON, absent state, output shape, optional logging, and disabled logging. | Payload/receipt mismatch; fix adapter mapping. |
| A-17 | R-12 | Export to a new directory produces reviewable files; existing destination and unrelated host configuration stay unchanged. | Integration setup overwrites existing work; fix exporter. |
| A-18 | R-08, R-09, R-12 | Two real fresh Codex sessions on a new bounded task: first writes handoff, second receives it and verifies a justified result; actual events have receipts. | Config copied but not invoked, or handoff not delivered; fix supported loading route before release. |
| A-19 | R-06, R-11 | Copy a quiescent entire task and required project-relative evidence to a second local project; inspect and rerun verification there. | Records cannot be recovered portably; fix root-relative paths and relocation behavior. |
| A-20 | R-04, R-07 | Real-task review confirms scope/criteria were fixed before dependent work, amendments were explicit, and no unfavorable finding triggered unauthorized extra execution. | The software loop exists but research behavior violates its agreement; fix instructions or task wording using observed evidence. |

## v0.2 initialization and skill migration

The following cases extend the original 20-case v0.1 release matrix.

| Case | Requirements | Scenario and observable result | Failure detected; response |
|---|---|---|---|
| A-21 | R-13, R-11 | Initialize a non-Git root, customize files, and rerun; only missing files are created, with unchanged task/config contents. Invalid manifest/path collisions reject before writes. | Overwritten work or inconsistent setup; fix initialization and preflight. |
| A-22 | R-13, R-08 | New vault receives note scaffolding; existing vault is associated without edits; omitted binding is reused, conflicting/out-of-root binding rejects. | Duplicated or misplaced knowledge; fix binding and scaffold behavior. |
| A-23 | R-13, R-12 | Installed wheel initialization includes workspace guidance, local skill, and optional working hook definitions; existing host files stay intact. | Checkout-only resources or destructive integration; fix packaging/preservation. |
| A-24 | R-14, R-05, R-06 | Migrated experiment templates and validator work with native rctl contract/result; real verification executes declared domain checks, evidence review remains separate, and negative/unknown outcomes retain their meaning. | Renamed files lose scientific evidence or bypass closure; fix skill/template/check integration. |

## v0.3 discovery and maintenance

| Case | Requirements | Scenario and observable result | Failure detected; response |
|---|---|---|---|
| A-25 | R-15, R-10, R-11 | List mixed phases and filter them; empty roots succeed, damaged candidates remain visible, titles use governing contracts, JSON/text agree. | Hidden or wrongly selected tasks; fix discovery and projection. |
| A-26 | R-16, R-08 | Extract explicit new/legacy handoffs including multiline Unicode; ignore fenced examples and diagnose ambiguous fields without rewriting files. | Invented or lost continuation; fix extraction. |
| A-27 | R-16, R-09 | Both reminder budgets preserve late next steps, warnings and sources; ended-task handoffs are historical; context is read-only and JSON fields bounded. | Truncated next step or accidental continuation; fix prioritization. |
| A-28 | R-17, R-12, R-13 | Inspect matching/customized/missing skill assets, invalid config, relocated commands, both hook sources, disabled and duplicate handlers; unrelated settings stay outside diffs. | Misleading installation diagnosis; fix scoped inspection. |
| A-29 | R-17, R-11, R-13 | Export candidates from an installed wheel into a new directory; live assets and records remain identical; existing/out-of-root/owned-asset destinations reject. | Destructive or checkout-dependent update; fix exporter and packaging. |
| A-30 | R-16, R-08, R-12 | One real Codex session checkpoints a long handoff; a distinct fresh session receives and identifies its concrete next step. | Scripted fixture mistaken for real delivery; fix supported host path and record evidence. |

## Test organization

Pure tests cover parsing, lifecycle, verdict aggregation, and rendering. Integration tests use actual subprocess checks and real temporary files. Do not use only mocked execution for A-04/A-05/A-14/A-15. A-18/A-20 require a real host/task; they cannot be satisfied by scripted payload injection or the old pilot alone.

The implementation should run `uv run pytest` with only suites relevant to each milestone, followed by the full suite once for release. Use installed, declared development dependencies rather than untracked ad hoc environments. Exact commands and resolved versions belong in the implementation's test record.

## Evidence record

For each milestone, record the case IDs, command/launch procedure, environment and version, actual outcome, evidence paths, and unresolved cases. A failed attempt remains in the record if its failure changes the supported setup. Distinguish pass, fail, and not run. An expected failure fixture passes only when the expected rejection is observed.

The synthetic example supplies test inputs and expected scientific interpretation, not an implementation test result. Preparation checks are separately recorded in [READINESS](READINESS.md).
