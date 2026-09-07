# Host and Skill Integration

## Ownership and reuse

Build the first adapter for Codex. Core commands remain host-neutral. The [new M3 probes](M3-VERIFICATION.md) and [two-session release task](RELEASE-VERIFICATION.md) establish invocation-local delivery on Codex CLI 0.153.4. A [follow-up](PROJECT-HOOKS-VERIFICATION.md) also establishes project-file delivery with normal configuration loading and invocation-only hook-trust bypass; copying files alone does not grant trust. See [SOURCES](SOURCES.md) and [limitations](READINESS.md#limitations).

The release packages one `research-task` skill with these responsibilities: read contract/result/handoff, establish scope within existing authorization, preserve amendments, execute using appropriate domain skills, inspect evidence, invoke verification, and close only after the recorded guard succeeds. It must explicitly separate a chat pause from task closure.

Scientific methods and evidence requirements remain in the domain skills. As of v0.2,
research-experiment uses native rctl contract/result files; model-training-workflow and
experiment-adapter-builder retain runner authority, while research-review-case labels
represent evidence coverage. None owns a competing task lifecycle. The shared setup skill
is retired; its orientation/vault assets and workspace guidance now ship in rctl.
The user-authorized M5 migration changes shared source skills; ordinary init/export commands
never edit that repository or migrate live tasks.

`init --codex` creates missing `.codex/hooks.json`, `.codex/config.toml`, and
`.rctl/codex/README.md` plus the project-local skill. Existing host files are preserved for
manual reconciliation. It does not grant project/hook trust, launch Codex, or claim delivery
from file creation. The tested project-file loading route and its trust boundary remain as
recorded in PROJECT-HOOKS-VERIFICATION.

## Bundle contract

`integration codex export DIRECTORY` creates a new directory containing:

- `hooks.json`: only rctl's hook definitions, using the actual installed rctl entrypoint and explicit project root.
- `research-task/SKILL.md` and `research-task/agents/openai.yaml`: host-neutral instructions plus native invocation metadata; `research-task/references/` includes workspace and optional graph guidance.
- `README.md`: the tested host version, loading procedure, task-selection environment, removal steps, and the exact scope of the delivery test.

The exporter does not launch a host, alter global configuration, merge a live project config, grant trust, or install a shared skill. During the integration milestone, validate a disposable launch using the exported definitions. Normal persisted project loading requires separate delivery evidence. If project loading fails, retain the invocation-local path as the documented supported route; do not label export alone as installation success.

## Adapter interface

The internal command `rctl hook codex` reads one event JSON object from stdin. It requires `RCTL_PROJECT_ROOT` or an explicit global `--root`; it must not infer a different project from the host payload. `RCTL_TASK_PATH` selects the task relative to that root. The payload's `cwd` must resolve inside that root.

Use one initial `SessionStart` handler. Add `UserPromptSubmit` for updated handoffs, contract changes, and selection reminders. Both must render fresh state; prompt events use a compact summary plus source paths rather than reinjecting the entire contract. No daemon or continuous polling is involved.

The pilot's retained event and response shape is:

```json
{"hook_event_name":"SessionStart","source":"startup","session_id":"example-session","cwd":"/example/project"}
```

```json
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Task comparison: active; contract revision 1; verification not checked. Read tasks/comparison/contract.md and the saved handoff."}}
```

The same response shape uses `UserPromptSubmit` for that event. Unsupported events return `{}`. Supported events with absent selection or unreadable state return a short unavailable/selection reminder and exit 0. Malformed JSON also returns `{}` with a concise diagnostic on stderr and exits 0. A broken reminder must not invent a successful task state or prevent ordinary conversation.

Cap rendered `SessionStart` context at 8,000 Unicode characters and `UserPromptSubmit` at 2,000, preserving warnings and source paths before excerpts. Configure a 10-second host timeout as the initial setting, not a promised latency. Adapter code delegates to the pure context renderer; no checks or state mutations occur.

The [pilot launch record](SOURCES.md#local-evidence) is the concrete starting reference for invocation-local host configuration. Recheck official protocol documentation through smart-search before host-specific implementation, then record the actual version and working launch syntax in the generated bundle. Online retrieval failed during preparation and succeeded during M3. The [M3 record](M3-VERIFICATION.md#official-source-recheck) retains the official source and actual tested loading procedures.

## Events deliberately outside v0.1

Do not install Stop, PreToolUse, PreCompact, or SubagentStart handlers. Task completion is the CLI close boundary, not an inferred host stop event. Subprocess fixtures may describe future resume/compact payloads, but only actual host delivery can establish support.

## Delivery evidence

For disposable host tests, `RCTL_HOOK_LOG` may select a local receipt file. No receipts are written when it is unset. Each JSONL receipt records event, source, session ID, task path, timestamp, and delivered context. Keep it in local test output because context can include private material; do not send telemetry.

Release evidence must include two distinct fresh host sessions, their launch arguments and host version, receipt records, the first session's saved handoff, and proof that the second received it. Also launch without hooks and show the core terminal loop still works. The no-hook run establishes core independence; it is not a comparative model-performance experiment.

## v0.3 maintenance and handoff delivery

`doctor --codex` inspects only project-local JSON/TOML configuration. It can identify
missing/duplicate rctl handlers, stale executable/root addressing, customized options,
and explicit disabling. An absent feature setting is inherited; the current official
host documentation describes hooks as enabled by default. Effective global/managed
settings, trust, and model-visible delivery remain outside static inspection.

`update export DIRECTORY --codex` provides reviewed-update material, with host fragments
and scoped diffs. It does not merge configuration or grant trust. Update the packaged
skill and intended rctl handlers after reviewing local differences; retain other content.
Changed definitions may need renewed host trust. The official protocol/trust source is
https://developers.openai.com/codex/hooks (rechecked through smart-search 2026-09-07).

Both reminder events now prioritize explicit next-action/blocker fields before long
handoff prose. Ended tasks label those fields historical; they remain reported progress,
not permission or acceptance. A-30 requires actual two-session delivery evidence.
