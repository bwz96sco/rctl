# M3 reminder integration verification

Date: 2026-09-06. Starting point: M2 commit `3655f2d`.

## Delivered behavior

`rctl hook codex` consumes host event JSON and returns the host's raw output shape. SessionStart uses the shared renderer with an 8,000-character budget; UserPromptSubmit provides status, warnings, paths, and a bounded handoff within 2,000 characters. It performs no verification or lifecycle mutations. Supported events with unavailable selection/state give a visible reminder; malformed input and unsupported events return `{}`. Adapter failures exit 0.

`integration codex export DIRECTORY` creates reviewed hook definitions, a packaged `research-task` skill with native invocation metadata, and loading/removal instructions. It uses the installed console entrypoint and explicit root, refuses an existing destination, and changes no shared skills or live host configuration. Optional project-local JSONL receipts record the event, source, session ID, selection, timestamp, and context; unset logging creates no receipts.

The local skill preserves rctl's record ownership when consulting domain skills that assume another framework. It carries the scientific contract, amendment, evidence review, negative-result, pause-versus-close, and durable-knowledge boundaries from the documented source skills without importing Trellis commands.

## Structure and subprocess evidence

`uv run pytest tests/test_m3.py --basetemp=.work/pytest-m3 -q` passed 15 cases covering A-12 adapter, A-16, and A-17: both events and budgets, fresh handoff delivery, malformed payloads, unsupported events, absent/wrong selection and cwd, malformed records, optional receipts and receipt failures, export preservation, real execution of exported commands, and TOML-compatible inline settings.

`uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-task` returned `Skill is valid!`. This establishes skill structure, not behavior. Real-session behavior belongs to M4.

## Actual host delivery

Three fresh, ephemeral Codex CLI 0.153.4 processes were launched using [probe_codex.py](../scripts/probe_codex.py). Each received the same no-tool-use prompt and a separate disposable root with the same task materials. User configuration, apps, and plugins were disabled. Auth used the existing host account. Reviewed generated hooks received invocation-only hook trust; no persisted trust or global configuration was changed.

| Procedure | Host exit | Receipts and model output | Result |
|---|---|---|---|
| `uv run scripts/probe_codex.py inline` | 0 | SessionStart and UserPromptSubmit receipts; model reported the selected task, active phase, and the B0/C1 handoff before any tool use | Supported invocation-local route |
| `uv run scripts/probe_codex.py project` | 0 | No receipts; model reported `NO_RCTL_REMINDER` despite project-file hooks and a project trust override | Project-file loading failed under this isolated launch; root cause unestablished |
| `uv run scripts/probe_codex.py none` | 0 | No receipts; model reported `NO_RCTL_REMINDER` | Hooks-disabled control |

Full launch arguments, prompts, JSONL host events, model final responses, and summaries are in [inline](evidence/host-probes/inline/launch.json), [project](evidence/host-probes/project/launch.json), and [none](evidence/host-probes/none/launch.json). [Inline receipts](evidence/host-probes/inline/receipts.jsonl) establish both actual events. Model-visible delivery is separately established by [the inline final response](evidence/host-probes/inline/final.txt) and its no-tool-use [event stream](evidence/host-probes/inline/events.jsonl).

The failed project-file attempt remains evidence. The supported initial route is invocation-local inline configuration. These observations do not establish ordinary persisted project installation, other host versions, resume/compact, or model-performance benefit. General operating boundaries are recorded in [READINESS: Limitations](READINESS.md#limitations).

## Official source recheck

Both commands succeeded:

```sh
smart-search exa-search 'Codex hooks SessionStart UserPromptSubmit hooks.json' --include-domains developers.openai.com --include-text --num-results 3 --format json --output docs/evidence/m3-hook-search.json
smart-search fetch https://developers.openai.com/codex/hooks --format markdown --output docs/evidence/m3-hooks-official.md
```

The [fetched official page](evidence/m3-hooks-official.md) documents both event payloads, `hookSpecificOutput.additionalContext`, timeouts, active config layers, project trust, and invocation-only bypass for previously vetted automation. The live host evidence above bounds compatibility more narrowly than the current [official documentation](https://developers.openai.com/codex/hooks).
