# Development Plan

## Latest deployment

v0.5.1 source `84c4779` is pushed, passed all four CI jobs, and is installed in the
global tool environment. The authorized OR task-skill and guidance merge is also
complete; see the [deployment record](V0.5.1-DEPLOYMENT.md). Version-only historical
currentness and additional reminder coverage remain separate runtime work.

## Completed release preparation

Prepared v0.5.1 from the training migration (`1c098df`) and
comparison-template follow-up (`0140b19`). Restore route-entry granularity,
separate open-question ownership, explain evidence for living guidance, and
shorten shared comparison instructions using generic terminology. Read short
project guidance first and related history on demand. Preserve native scaffold
markers and existing invocation policies.

Use A-01/A-02 for draft compatibility and A-21/A-22/A-23/A-24/A-29 for resource
delivery and preservation, plus the full release checks. The version bump leaves
currentness behavior unchanged: closed tasks may show a version-only stale report
without losing historical closure. Runtime display changes and reminder coverage
are separate follow-ups. The
[review record](COMPARISON-REVIEW-FOLLOWUP.md) records decisions and validation.

## Included source increments

The September23 comparison-template follow-up adds project problem/method and
comparison-guidance scaffolds, scopes route decisions and control versions, and
updates native task authoring plus research-task references. Use A-21/A-22/A-24
for affected initialization/preservation/template checks. CLI, schemas, task
phases and host integration are unchanged. Source validation is distinct from
installed-wheel delivery and release; see
[COMPARISON-TEMPLATE-FOLLOWUP.md](COMPARISON-TEMPLATE-FOLLOWUP.md).

The 2026-09-21 source-management follow-up adds experiment-adapter-builder and
model-training-workflow, including their validators, fixtures and pinned source
audit. Use M5/A-23/A-24 for packaged resources and A-21/A-29 for task-only
init/export preservation. Preserve scientific instructions and native invocation
policies; redirect existing discovery links after package verification. The
[migration record](RESEARCH-SKILLS-MIGRATION.md#training-and-adapter-follow-up)
records the source cutover. Other auxiliary tools and live tasks stay outside scope.

The current task repairs the two research-skill review rounds after source migration:
pilot/formal handoffs, human selection sizes, vault and installed-resource paths,
operation-specific completion, and computation/theory/writing evidence boundaries.
Keep research-computation as an optional lightweight helper and preserve invocation
policies, human selection, and native rctl acceptance. Use M5/A-23/A-24 as the main
integration checks, plus A-22/A-29 for binding and packaged-asset regressions. The
[follow-up record](RESEARCH-SKILLS-FOLLOWUP.md) records changes and their checks.

The preceding migration consolidated 13 research workflows from agent-skills-private
and the independently installed research-rapid-test, preserving their source content
and existing installation identities. The
[catalog](RESEARCH-SKILLS.md) defines ownership and the
[migration record](RESEARCH-SKILLS-MIGRATION.md) records preservation and cutover.
Auxiliary tools, live tasks, shared installation configuration, and CLI deployment stay
outside this follow-up. The simplification increment below is committed at `87157e9`.

The governing-question alignment baseline is v0.5.0 at `82a5ec8`. The user
requested implementation of the [simplification plan](SIMPLIFICATION-REVIEW.md)
on 2026-09-14. This unreleased follow-up keeps lifecycle, schemas, and public CLI
syntax stable while shortening the packaged skill, sharing immutable task snapshots,
and using one reminder layout with both existing hook events.

Use M8/A-37–A-40 as the regression anchor, plus the affected discovery, context,
packaging, history-reuse, and real-host cases identified in the plan. The
[verification record](SIMPLIFICATION-VERIFICATION.md) separates automated behavior,
installed-package execution, and observed GPT-6-Astra use. Remaining installation,
review-input, and verification-protocol decisions stay outside this increment.

## Work by affected behavior

README defines document authority. Use PRD for scope, SPEC for behavior, CLI for
syntax/output, schemas for structural inputs, and INTEGRATION for skills and hooks.
Select the affected ACCEPTANCE cases before implementation. Update an owning
document and its examples/tests before changing its contract; resolve routine
internal choices within the authorized task.

Use uv and the locked project dependencies. Keep source and installed-package
behavior consistent: schemas, templates, and skills ship in the wheel. Parsing,
record publication, execution, currentness, and host delivery retain distinct owners.
Tests cross the supported read/lifecycle interfaces, use real local files and
subprocesses where those affect behavior, and preserve distinct regression coverage.

Run affected tests during development, then the full suite once before release,
plus lint, documentation checks, build, and installed-wheel smoke. The commands
are in [README](../README.md#run-the-local-cli). Record actual versions, commands,
results, and untested behavior. A hook fixture proves the payload contract; actual
host/model delivery and scientific adequacy need their respective evidence.

Shared installations, live research tasks, and host configuration are changed only
when the current task includes those targets. The simplification acceptance probes
use disposable local projects and invocation-local reviewed hook definitions.

## Release and deployment order

For authorized upgrades of actively used projects: complete local validation,
commit and push the release, then wait for the CI run on that exact commit to
succeed before installing or updating project assets. Build deployment artifacts
from that clean committed source and verify the installed code/assets against it.
After deployment, run scoped installation and reminder checks. If CI fails, fix
and validate a new commit before deployment. Local tests alone do not satisfy this
release gate; an explicit user request may authorize an experimental deployment.

## Changes from the original proposal

| Original proposal | v0.1 development baseline | Reason |
|---|---|---|
| SQLite state and events, row/material versions, migrations | One machine record per task; accepted contract revisions and actual check records | Target the demonstrated task boundary before database operations. |
| Content-addressed objects and general snapshots | Exact retained contract/result text; lightweight metadata observations of declared evidence | Detect ordinary drift without copying a scientific artifact store. |
| `context / record / verify / advance / report` plus broad supporting commands | The explicit command set in CLI, including begin/amend/verify/close | Give each operation one narrow meaning; no generic advance or status setter. |
| Separate in-review phase and default local approval for analysis | Review criteria inside verification; active/closed/cancelled phases | Scientific review is required when the contract calls for it; avoid automatic approval ceremonies. |
| Claude Code first | Codex first, anchored to the existing pilot | There is already host execution evidence to start from. |
| Full backup/restore subsystem | Whole-task copying when quiescent, followed by fresh verification | No database or immutable-object service to back up in v0.1. |
| Same-host concurrent writes, idempotency protocol | One writer per task and a detected-change recheck | Keep coordination proportional; stronger coordination needs its own observed use case. |
| New `.claude/skills/research-state` and installation merge machinery | Exported local `research-task` package and reviewed host bundle | Preserve shared skills and unrelated live configuration. |

Keep the original's useful semantics: closure needs evidence, successful execution is not scientific validity, negative findings may finish, historical acceptance has a scope, and a session can stop before the task closes.

## Historical milestones

The [release-evidence index](RELEASE-EVIDENCE.md) maps completed increments and
review follow-ups to their original verification records. M1–M7 and the v0.1 release
remain completed historical work; M8 implementation is recorded with release pending.
The older development proposal remains historical and does not override this plan.
