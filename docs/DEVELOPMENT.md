# Development Plan

## Entry condition and first assignment

Start from this documentation baseline. The first coding task is **M1: contract and readable state**, with the acceptance cases listed below. Implement a runnable increment with real temporary-file tests, not a scaffold for every later feature. No further product-choice meeting is required to start M1.

M1 was implemented on 2026-09-05; its [verification record](M1-VERIFICATION.md) separates completed M1 checks from the portions completed by [M2 on 2026-09-06](M2-VERIFICATION.md). [M3](M3-VERIFICATION.md) and [M4 release acceptance](RELEASE-VERIFICATION.md) completed on 2026-09-06. All four milestones are complete; further integrations or live task migration need their own scope. The user separately authorized repository creation; this checkout has a local Git repository on `main`.

At implementation, set up the Python package with uv, an `rctl` console entrypoint, runtime dependencies PyYAML and jsonschema, and test dependencies pytest and Ruff. Commit a resolved `uv.lock` only when Git work is separately in scope. No Git repository was initialized during preparation. The initial implementation target is Python 3.11+ on macOS/Linux; record actual tested combinations before claiming support.

Suggested initial files: `src/rctl/cli.py`, `records.py`, `policy.py`, `verification.py`, `context.py`, and `hooks/codex.py`. Start with fewer files when cohesive. Keep schemas inside the installed package at build time, sourced from this repository's `schemas/`; command behavior must not depend on the checkout being present.

## Milestones

| Milestone | Bounded deliverable | Exit evidence |
|---|---|---|
| M1 — Contract and state | Packaging; new/check/begin/amend/checkpoint/status/context; parsing and record preservation. | A-01, A-02, A-10, A-11, A-12 core portion, A-13 core portion. A new process can recover a begun task. |
| M2 — Verification and closure | Command/review checks, currentness, close/reopen/cancel, JSON/error protocol. | A-03 through A-09, A-14, A-15, A-19, completed A-13. Synthetic negative task closes; missing evidence does not. |
| M3 — Reminder integration | Packaged local task skill, Codex adapter, bundle export, tested loading instructions. | A-12 adapter portion, A-16, A-17; official protocol/source recheck; actual host smoke with receipts. |
| M4 — Real-task release | A new bounded task through two fresh sessions; release documentation and example walkthrough. | A-18, A-20 and all remaining cases; full automated suite; installed-package walkthrough. |

M3 depends on the context interface from M1 and verification summaries from M2. A documentation fetch failure does not block M1/M2; it must be resolved or replaced by adequately inspected version-specific source evidence before publishing a host compatibility claim in M3.

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

## Release contents

Deliver an installable package and lockfile, schemas, templates, synthetic example, CLI help/usage, one local skill, the Codex exporter/adapter, tests, and a release verification record. Update README's status only after actual implementation milestones pass. Package installation and source checkout execution both need a smoke test.

Shared-skill updates, moving a live project to rctl, renaming this checkout directory, or retiring Trellis are subsequent tasks with their own concrete scope. They are not hidden steps in these milestones.

## Changes during implementation

Routine internal choices may be resolved locally. If a discovery changes scope, acceptance semantics, file ownership, or the CLI contract, update the owning document and affected examples/tests before dependent implementation. Preserve a failed host setup as evidence and document the supported replacement. Do not add a new framework, validation score loop, or service merely to satisfy an imagined future use.

## M5 — Project initialization and shared-skill migration (v0.2)

Authorized on 2026-09-06. Implement `rctl init`, move setup/vault assets and workspace guidance into the rctl distribution, retire the shared setup entrypoint, and migrate experiment/training/adapter/review references. Preserve the user's existing synthesis edits and all live research tasks. Exit evidence: A-21–A-24, relevant packaging/regression checks, shared-skill validators, and a migrated-task execution walkthrough. Commit rctl and the shared skills repository separately.

## v0.2.1 — Review follow-up

Authorized on 2026-09-06. Extend M2 diagnostics and publication handling using A-13
(JSON/error protocol), A-14 (failed publication preservation), and A-15 (material
changes during checks). Keep verdict and closure rules unchanged. Add explicit
platform metadata/runtime errors, full-script lint, and macOS/Linux CI. Exercise
actual subprocess evidence regeneration and fault-injected record/publication errors;
run the full suite and installed wheel smoke before the local patch release.
