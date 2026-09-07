# M6 verification — discovery, handoff summaries, and maintenance

Observed 2026-09-07 for rctl 0.3.0 on macOS arm64, CPython 3.13.2.
M6 implements the first three recommendations in the
[upstream research](UPSTREAM-FEATURE-RESEARCH.md), within the user-approved plan.

## Outcome

Task listing, explicit handoff summaries, read-only installation inspection, and
candidate-only update export are implemented. Existing task/project schema versions
remain 1. Supported lifecycle commands and closure guards retain their meanings.
The packaged task skill and workspace guidance describe the new commands and handoff
format. No global install, shared skill, live research project, or host trust was changed.

| Acceptance | Evidence | Result |
|---|---|---|
| A-25 | Mixed active/draft/cancelled/damaged task fixtures; frozen title and phase filtering; installed-wheel closed-task listing | Pass |
| A-26 | New headings, legacy lines/bullets, multiline Unicode, ignored fenced examples, placeholders and ambiguous fields; checkpoint preservation | Pass |
| A-27 | Long late handoff, both context budgets, bounded added JSON, unreadable handoff and ended-task historical labeling; existing read-only adapter regressions | Pass |
| A-28 | Matching/customized/missing skills; invalid JSON/TOML; stale root/missing executable; missing/duplicate handlers; inline configuration and unrelated settings | Pass |
| A-29 | Candidate fragments/diffs, refused destinations, before/after live-file comparisons, package resource and command checks in isolated wheel environment | Pass |
| A-30 | Two distinct real Codex sessions; first checkpointed a long handoff, second identified its late next action from delivered context without tools | Pass |

## Commands and results

```sh
uv sync
uv run pytest tests/test_m1.py tests/test_m3.py -q
uv run pytest tests/test_m6.py -q
uv run ruff check src tests scripts
uv run pytest -q
uv run scripts/check_docs.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.3.0-py3-none-any.whl
uv run python /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-task
git diff --check
```

- Existing M1/M3 regression selection: 60 passed.
- New M6 regression selection: 25 passed.
- Full suite: 165 passed, including the unchanged verification/currentness tests.
- Ruff and skill structural validation passed; document checks cover 17 requirements
  mapped to 30 acceptance cases. These establish code/document structure, not scientific judgment.
- Built source distribution and wheel. The isolated wheel smoke completed 26 CLI
  operations including doctor, candidate export, active/closed discovery, verification,
  negative closeout, and reopen. See [wheel summary](evidence/m6/wheel-summary.json).

The first M6 run found that candidate export mistakenly rejected a valid project whose
vault binding was null. The branch now distinguishes a valid null binding from a failed
manifest read; both candidate-export tests passed after correction. This was an
implementation defect, not a need to initialize a vault for maintenance.

## Actual host delivery

The disposable fixture was `.work/m6/host-project`, with an active retained-comparison
task and a long supplied progress file. No scientific computation was requested or run.
The first host session read the supplied progress and continuation sources, created a
checkpoint input with the next action after more than 26,000 characters, and invoked
`rctl checkpoint`. The acceptance-record bytes stayed unchanged.

The second session was fresh and read-only. Its prompt contained no target next-action
text and prohibited file/tool access. Both SessionStart and UserPromptSubmit receipts
contained the actual late next action. The model replied:

> Selected task: retained-comparison. Phase: active.
> Reported next action: Inspect row 7 of the retained delivery table and record whether
> its receipt is missing. Blocker: None.

Both host processes exited 0. The second event stream contained no command execution,
file changes, or MCP calls. Its session ID differed from the first session. The
[delivery evidence](evidence/m6/host-delivery.json) retains session IDs, launch arguments,
receipt context, completed first-session commands, model responses, and handoff offsets.
Large repetitive process output remains in the ignored local fixture instead of being
copied into the documentation tree.

The tested host was Codex CLI 0.153.4, using reviewed generated inline definitions,
`--ignore-user-config`, disabled apps/plugins/multi-agent capability, and invocation-only
hook-trust bypass. First-session sandbox was workspace-write; second was read-only.
The host's expected bypass notice was retained as a diagnostic, not mistaken for failure.
No project/global trust setting was written.

Official hook documentation was rechecked through smart-search on 2026-09-07:

```sh
smart-search exa-search 'Codex hooks project config trust' --include-domains developers.openai.com --num-results 2 --format json
smart-search fetch https://developers.openai.com/codex/hooks --format markdown
smart-search fetch https://developers.openai.com/codex/hooks.md --format markdown
```

The [official source](https://developers.openai.com/codex/hooks) supports separate
project-layer trust, exact-definition hook review, JSON/inline sources, and invocation-only
bypass. Its current default-enabled setting is why doctor labels an absent local feature
setting inherited rather than automatically broken.

## Publication follow-up

Published on 2026-09-07 as commit `ffed00b1390d5e38e65316a6e747e480f8b107ea`.
[GitHub CI](https://github.com/bwz96sco/rctl/actions/runs/34073127344) passed all four
macOS/Linux × Python 3.11/3.13 jobs, including the full tests, Ruff, documentation
check, build, and installed-wheel smoke. Results were inspected with
`gh run view 34073127344 --repo bwz96sco/rctl --json status,conclusion,headSha,jobs,url`.

## Limitations

See [READINESS](READINESS.md#limitations) for the maintained guarantee boundary. Local
host checks used macOS/Python 3.13.2; the published CLI/package matrix passed as recorded
above. Static
doctor findings do not prove effective global host configuration, trust, or model-visible
delivery. The host experiment establishes this concrete long-handoff delivery case,
not persistent trust, other host versions, or quantified research-performance gains.
Candidate export does not apply updates, infer the history of customized files, or
provide transactional recovery after a filesystem failure. Review a partial export and
choose a fresh destination if a write is interrupted. Schema-1 records remain readable;
a version change still requires fresh verification before a new closure under the
existing currentness rule.
