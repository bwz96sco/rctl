# Host and Skill Integration

## Ownership and reuse

Build the first adapter for Codex. Core commands remain host-neutral. The [new M3 probes](M3-VERIFICATION.md) and [two-session release task](RELEASE-VERIFICATION.md) establish invocation-local delivery on Codex CLI 0.153.4. A [follow-up](PROJECT-HOOKS-VERIFICATION.md) also establishes project-file delivery with normal configuration loading and invocation-only hook-trust bypass; copying files alone does not grant trust. See [SOURCES](SOURCES.md) and [limitations](READINESS.md#limitations).

Project initialization and host export install one `research-task` skill with these responsibilities: read contract/result/handoff, establish scope within existing authorization, preserve amendments, execute using appropriate domain skills, inspect evidence, invoke verification, and close only after the recorded guard succeeds. It must explicitly separate a chat pause from task closure.

The repository and distributions also contain the 14 domain workflows in the
[research skill catalog](RESEARCH-SKILLS.md). They are maintained with rctl but are
not automatically installed into projects by init/export or managed by project doctor.
Their user-level source links are a separate, explicitly authorized installation boundary.

Scientific methods and evidence requirements remain in the domain skills. As of v0.2,
research-experiment uses native rctl contract/result files; model-training-workflow and
experiment-adapter-builder retain runner authority, while research-review-case labels
represent evidence coverage. None owns a competing task lifecycle. The shared setup skill
is retired; its orientation/vault assets and workspace guidance now ship in rctl.
The user-authorized M5 migration changes shared source skills; ordinary init/export commands
never edit that repository or migrate live tasks.

`init` creates missing `.codex/hooks.json`, `.codex/config.toml`, and
`.rctl/codex/README.md` plus the project-local skill. Existing host files are preserved for
manual reconciliation. It does not grant project/hook trust, launch Codex, or claim delivery
from file creation. The tested project-file loading route and its trust boundary remain as
recorded in PROJECT-HOOKS-VERIFICATION.

Since the 10 October 2026 first-use repair, Codex preparation and doctor inspection
are defaults. `--codex` remains compatible; `--no-codex` explicitly opts out on
these commands. Candidate export still requires `--codex`. The packaged
[first-use procedure](../skills/research-task/references/workspace.md#host-first-use)
requires configuration inspection, operator trust through `/hooks`, and actual
SessionStart/UserPromptSubmit delivery in a fresh project session. The official
[trust documentation](https://developers.openai.com/codex/hooks/#review-and-trust-hooks)
was fetched through smart-search on 10 October 2026 and still requires review of
the exact definition. Doctor's `codex_trust` and `codex_delivery` remain
`not_inspected` even when no static findings need review.

Claude Code support was added on 10 October 2026, when LEO's Claude Code sessions
were found to receive neither rctl reminders nor the task skill. Claude Code sends
the same `hook_event_name`, `cwd`, `session_id` and `source` fields and accepts the
same `hookSpecificOutput.additionalContext` output, so `rctl hook claude` shares the
Codex adapter and its 8000/2000-character budgets, below Claude Code's 10,000-character
cap. `init` writes the two handlers to `.claude/settings.json`, which has no per-handler
context limit, and copies the task skill to `.claude/skills/research-task/`, the only
project skill location Claude Code loads. Claude Code holds back settings-file hooks
until the folder's workspace trust dialog is accepted; `/hooks` is a read-only list,
and `claude -p` sessions treat the folder as trusted. Hook runs appear in the session
transcript. Doctor inspects both project settings files and `disableAllHooks`; user
settings, trust and delivery are not inspected. Sources:
[hooks](https://code.claude.com/docs/en/hooks),
[skills](https://code.claude.com/docs/en/skills) and
[memory](https://code.claude.com/docs/en/memory), fetched 10 October 2026. One
`claude -p` probe on Claude Code 2.1.296 observed both reminders and the skill
listing; the interactive trust path is unobserved (see
[DEVELOPMENT](DEVELOPMENT.md#claude-code-host-support-10-october-2026)).

## Bundle contract

`integration codex export DIRECTORY` creates a new directory containing:

- `hooks.json`: only rctl's hook definitions, using the actual installed rctl entrypoint and explicit project root.
- `research-task/SKILL.md` and `research-task/agents/openai.yaml`: host-neutral instructions plus native invocation metadata; `research-task/references/` includes task-file, planning, verification, workspace, and optional graph guidance.
- `README.md`: the tested host version, loading procedure, task-selection environment, removal steps, and the exact scope of the delivery test.

The exporter does not launch a host, alter global configuration, merge a live project config, grant trust, or install a shared skill. During the integration milestone, validate a disposable launch using the exported definitions. Normal persisted project loading requires separate delivery evidence. If project loading fails, retain the invocation-local path as the documented supported route; do not label export alone as installation success.

## Adapter interface

The internal command `rctl hook codex` reads one event JSON object from stdin. It requires `RCTL_PROJECT_ROOT` or an explicit global `--root`; it must not infer a different project from the host payload. `RCTL_TASK_PATH` selects the task relative to that root; without it, the project's only active task is used and labeled as selected automatically (SPEC §2). The payload's `cwd` must resolve inside that root.

Use one initial `SessionStart` handler. Add `UserPromptSubmit` for updated handoffs, contract changes, and selection reminders. Both must render fresh state; prompt events use a compact summary plus source paths rather than reinjecting the entire contract. With a selected task, that summary is one capped line per decision-relevant field (see SPEC's reminder section), so it carries whole sentences rather than fragments. No daemon or continuous polling is involved.

The pilot's retained event and response shape is:

```json
{"hook_event_name":"SessionStart","source":"startup","session_id":"example-session","cwd":"/example/project"}
```

```json
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Task comparison: active; contract revision 1; verification not checked. Read tasks/comparison/contract.md and the saved handoff."}}
```

The same response shape uses `UserPromptSubmit` for that event. Unsupported events return `{}`. Supported events with no selection and no single active task return project-only context, listing several active tasks when present; unreadable task state retains project guidance and an unavailable task diagnostic. Both exit 0. Malformed JSON also returns `{}` with a concise diagnostic on stderr and exits 0. A broken reminder must not invent a successful task state or prevent ordinary conversation.

Cap rendered `SessionStart` context at 8,000 Unicode characters and `UserPromptSubmit` at 2,000, preserving warnings and source paths before excerpts. Configure a 10-second host timeout as the initial setting, not a promised latency. Adapter code delegates to the pure context renderer; no checks or state mutations occur.

The simplification follow-up retains both events and caps, using one concise layout
without appended contract/handoff text. Each event loads fresh task/project state;
the renderer consumes a snapshot and performs no further reads. The accepted source
remains explicit when the working contract differs. Detailed skill guidance loads
through operation-specific references, with common lifecycle syntax in the root.
The official hooks and GPT-6-Astra guidance were rechecked through smart-search on
2026-09-14. The response shape and invocation-only hook-trust contract are unchanged;
new real-host evidence must record its actual host version independently of M7.
The [simplification verification](SIMPLIFICATION-VERIFICATION.md#real-host-acceptance)
records actual 0.154.0 inline-hook delivery and Astra continuation across long-handoff
recovery, automatic compaction, and stale-verification correction.

The [pilot launch record](SOURCES.md#local-evidence) is the concrete starting reference for invocation-local host configuration. Recheck official protocol documentation through smart-search before host-specific implementation, then record the actual version and working launch syntax in the generated bundle. Online retrieval failed during preparation and succeeded during M3. The [M3 record](M3-VERIFICATION.md#official-source-recheck) retains the official source and actual tested loading procedures.

## Events deliberately outside v0.1

Do not install Stop, PreToolUse, PreCompact, or SubagentStart handlers. Task completion is the CLI close boundary, not an inferred host stop event. Subprocess fixtures may describe future resume/compact payloads, but only actual host delivery can establish support.

## Delivery evidence

For disposable host tests, `RCTL_HOOK_LOG` may select a local receipt file. No receipts are written when it is unset. Each JSONL receipt records host, event, source, session ID, the `RCTL_TASK_PATH` value, task selection (`explicit`, `automatic` or null), timestamp, and delivered context; an automatically selected task is named in the context. Keep it in local test output because context can include private material; do not send telemetry.

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

## v0.4 project context

Both events use the same independent project/task loader as the CLI. They read current
Goal, Current guidance and Reuse Rule sections, retaining project guidance when task
selection is absent or invalid. Short output reserves content space for task warnings,
blockers and next action and does not repeat full handoff prose. No new events are installed.

The official hooks documentation was fetched through smart-search on 2026-09-08:
https://developers.openai.com/codex/hooks . SessionStart source `compact` runs before
the continuation request after compaction. rctl budgets count Unicode characters;
the host's `additionalContextLimit` is an approximate token spill threshold. These
are separate limits, even though the configured numeric values currently match.
Actual host delivery evidence belongs to the M7 verification record.

## v0.5 governing-question reminders

The existing SessionStart and UserPromptSubmit handlers use the same response shape,
events, limits and pure context renderer. For a selected task, their additional context
now reserves space for the accepted governing question, optional declared alignment,
and task-scoped assessment retained with the latest verification before mutable project
guidance. Core categories retain bounded initial visibility; question/alignment fields
then take priority over remaining mutable guidance space. No hook definition,
trust boundary, timeout, selection rule or machine mutation changes.

The official hooks documentation was rechecked through smart-search on 2026-09-14 at
https://developers.openai.com/codex/hooks . It continues to specify that
`hookSpecificOutput.additionalContext` for SessionStart and UserPromptSubmit is added
to model context, including SessionStart with source `compact`. Fixture coverage is
sufficient for this content-only change; the M7 real-host evidence retains its original
protocol and delivery scope.
