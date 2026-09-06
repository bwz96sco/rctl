# Project-file hook delivery follow-up

Date: 2026-09-06. Host: Codex CLI 0.153.4. Scope: follow-up to M3/A-16–A-18, authorized by the user's request to test project auto-loading and use YOLO-style hook trust. This does not change the completed release task or its frozen findings.

**Project-file delivery works with normal configuration loading and `--dangerously-bypass-hook-trust` in the tested environment.** SessionStart and UserPromptSubmit both delivered the selected task, and a fresh session received the updated handoff. Adding `--ignore-user-config` to the successful launch eliminated delivery. A normal launch without trusted project hooks, and a launch with hooks disabled, also produced no reminder.

## Procedure and evidence

[probe_project_hooks.py](../scripts/probe_project_hooks.py) creates a disposable project under `.work/project-auto-probe`, copies the synthetic task, begins it, and exports the installed rctl hooks. Definitions live only in `.codex/hooks.json`; no `-c hooks.SessionStart=...` or `-c hooks.UserPromptSubmit=...` definitions are supplied. The successful cases also have `.codex/config.toml` containing `[features]` and `hooks = true`.

The fixture is nested inside the already-trusted rctl Git repository. Task selection and separate receipt paths are supplied through `RCTL_PROJECT_ROOT`, `RCTL_TASK_PATH`, and `RCTL_HOOK_LOG`. Each probe starts a fresh ephemeral host with read-only tool sandboxing, apps/plugins/delegation disabled, and a prompt prohibiting tools. The prompt asks for the marker but does not disclose it. Hooks are host commands; the tool sandbox setting is not a sandbox guarantee for hooks.

The script was invoked as `uv run scripts/probe_project_hooks.py STAGE` in this order. Existing evidence destinations are refused so prior attempts remain available.

| Stage | Launch difference or purpose | Receipts | Model result |
|---|---|---:|---|
| `leaf-trust` | Ignore user config; trust nested directory; attempt exact hook state overrides | 0 | `NO_RCTL_REMINDER` |
| `repo-trust` | Trust actual Git root instead | 0 | `NO_RCTL_REMINDER` |
| `trusted` | Load user config; attempt hook trust/enabled state overrides | 0 | `NO_RCTL_REMINDER` |
| `repo-bypass` | Ignore user config; actual Git-root override; explicit hook-trust bypass | 0 | `NO_RCTL_REMINDER` |
| `config-layer` | Add project config.toml to the preceding setup | 0 | `NO_RCTL_REMINDER` |
| `normal-bypass` | Normal config loading; explicit hook-trust bypass; no state overrides | 2 | Correct `COPPER-ORCHID-73`, task/phase, and next action |
| `normal-ignore` | Add only `--ignore-user-config` to the successful setup | 0 | `NO_RCTL_REMINDER` |
| `updated` | Normal config and bypass; update handoff before fresh launch | 2 | Correct new `SILVER-MAPLE-29` and new next action |
| `untrusted` | Normal config, no hook-trust bypass, project hooks remain untrusted | 0 | `NO_RCTL_REMINDER` |
| `disabled` | Disable hooks | 0 | `NO_RCTL_REMINDER` |

All ten processes exited 0 and their event streams contain no model tool calls. These are delivery observations, not ten successful loading configurations. The [audit](evidence/project-auto/audit.json) binds each launch to a distinct actual session, checks both successful event receipts against that session, confirms marker presence in context and output but not the prompt, and confirms the controlled argv comparison after excluding output artifact paths. Receipt destinations differ by stage.

The successful [launch](evidence/project-auto/normal-bypass/launch.json), [project hook file](evidence/project-auto/normal-bypass/hooks.json), [receipts](evidence/project-auto/normal-bypass/receipts.jsonl), and [model event stream](evidence/project-auto/normal-bypass/events.jsonl) establish discovery, execution, and model-visible delivery separately. The [updated handoff](evidence/project-auto/updated/handoff.md) and [updated receipts](evidence/project-auto/updated/receipts.jsonl) establish fresh-state recovery. The [ignore-user-config comparison](evidence/project-auto/normal-ignore/launch.json) retains the failed counterpart.

## Discovery and corrected assumptions

The host's native `hooks/list` RPC identifies both definitions as `source: project`, with their `.codex/hooks.json` source path. Normal discovery reported no errors and both definitions as untrusted. This read-only query starts no task or model turn. The generated local protocol schemas came from `codex app-server generate-json-schema --experimental --out .work/codex-protocol`; the client uses `initialize`, `initialized`, and `hooks/list`.

An early assumption was incorrect: supplying `hooks.state.<key>.trusted_hash` and `.enabled` through command-line config did not change native trust/enabled state on this host. The [query with those overrides](evidence/project-auto/discovery-with-state-overrides.json) still shows project hooks untrusted and existing user hooks enabled. Early launch metadata's `trust_scope` describes intended overrides, not established trust or isolation. The later successful tests use the explicit native trust-bypass flag. Normal configuration can run the preexisting user hooks; they were not disabled by those ineffective overrides.

The controlled `normal-bypass` / `normal-ignore` pair establishes sensitivity to `--ignore-user-config` in this environment. It does not establish which internal configuration or trust-loading code caused the difference. Merely changing the trusted directory or adding config.toml did not make the isolated launch work. The original M3 failure remains a correct observation for its recorded flags.

## Practical use

For an already-reviewed test bundle in a trusted project, select the task and start Codex with `--enable hooks --dangerously-bypass-hook-trust`, preserving ordinary configuration loading. Project hook definitions must be in the project file, not copied into launch arguments. The dedicated hook-trust bypass is separate from `--dangerously-bypass-approvals-and-sandbox`; disabling tool approvals or sandboxing alone does not establish hook trust.

For normal persisted use, Codex `/hooks` reviews and trusts the exact definitions. Exporting a bundle does not grant that trust. This follow-up establishes an automated test route; it did not install persistent trust into the user's configuration.

## Documentation and validation

Official sources were searched and fetched through smart-search:

```sh
smart-search exa-search 'Codex project hooks config trust' --include-domains developers.openai.com --include-text --num-results 2 --format json --output .work/project-auto-search.json
smart-search fetch https://developers.openai.com/codex/hooks --format markdown --output .work/project-auto-hooks.md
smart-search fetch https://developers.openai.com/codex/app-server --format markdown --output .work/project-auto-appserver.md
```

The [official hook documentation](https://developers.openai.com/codex/hooks) describes project discovery, project/hook trust, `/hooks`, and invocation-only bypass. The [official app-server documentation](https://developers.openai.com/codex/app-server) defines initialization and JSON-RPC transport; the installed host's generated schema supplies the exact `hooks/list` fields. CLI help confirms separate hook-trust and approval/sandbox flags. These sources support configuration expectations; actual receipts bound the compatibility claim.

The retained audit passed. `uv run ruff check scripts/probe_project_hooks.py`, `uv run ruff format --check scripts/probe_project_hooks.py`, and `uv run --offline scripts/check_docs.py` passed, detecting script/static defects or broken evidence links that would require repair. Product code did not change, so the release's 112-test suites were not rerun.

## Limitations

Persistent trust, ordinary interactive startup without bypass, same-session second-prompt refresh, native resume/compact, other versions, and other platforms were not tested here. The handoff refresh used a new session. The existing user config and hooks participate in normal startup; the unique task marker and project receipts distinguish rctl delivery. No shared configuration file was intentionally edited, and neither YOLO nor a bypass proves persistent trust. General product boundaries remain in [READINESS](READINESS.md#limitations).
