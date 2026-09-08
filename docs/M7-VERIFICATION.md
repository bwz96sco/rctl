# M7 verification — project reminders and history reuse

Date: 2026-09-08. Version: 0.4.0. Scope: A-31–A-36 and existing lifecycle
regressions. Project sections are reported guidance, task records own acceptance,
and the planning case evaluates one evidence-based recommendation.

## Implementation and automated checks

Project guidance now loads independently of task selection. Missing selection is
project-only success; selected-task errors retain project context and their CLI
error. Short reminders share value space across fields, use relative source aliases,
and omit duplicate handoff prose. Goal, optional Current guidance and Reuse Rule
come from current research files, with no summary store or machine schema migration.

The task skill routes experimental proposals, contracts and material direction
changes through related evidence, the unanswered question, the reopen condition or
mechanism difference, and the decision a new result would change. Templates and
native examples preserve structural versus scientific judgment boundaries.

Actual commands:

```sh
uv run pytest -q
uv run ruff check src tests scripts
uv run scripts/check_docs.py
uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-task
uv build --out-dir .work/m7/dist
uv run scripts/smoke_package.py .work/m7/dist/rctl-0.4.0-py3-none-any.whl
```

The suite passed 191 tests, including 15 new M7 cases. Ruff, the skill validator,
and documentation checks passed. The installed-wheel lifecycle smoke returned
`ok: true`. After final exporter/initialization wording changes, the focused command
`uv run pytest tests/test_m3.py tests/test_init.py tests/test_m7.py -q` passed 49 tests.
The final wheel's Python source, templates and skill files matched the checkout
byte-for-byte. Cases exercise absent/bad task selection, record corruption, missing
research files, fresh corrections, fenced headings, duplicate sections, unfinished
placeholders, unreadable/escaping sources, long paths/handoffs, Unicode budgets,
nullable tiny-budget fields, and unchanged task/source bytes. Existing tests were
updated for the intentional no-selection success and relative-source/compact-output
contracts. Validation records are under `.work/m7/`.

## Official documentation

Fetched with smart-search on 2026-09-08:

- https://developers.openai.com/codex/hooks : SessionStart sources and compact
  continuation delivery; invocation-only hook trust bypass; approximate-token host
  spill threshold, separate from rctl's Unicode-character budgets.
- https://developers.openai.com/codex/skills : progressive disclosure, repository
  `.agents/skills` discovery and automatic skill refresh.
- https://developers.openai.com/codex/app-server : initialization, thread/turn start
  and manual-compaction protocol, inspected for the unsuccessful route below.

Local fetched pages and command logs are retained under `.work/m7/`; the hooks
page was fetched during diagnosis to `/tmp/rctl-hooks-20260908.md`.

## Actual host and planning evidence

Host: Codex CLI 0.153.4. Successful probes used `codex -a never exec`,
`--ignore-user-config`, disabled plugins/apps/multi_agent, explicit inline hooks,
`--ephemeral`, and invocation-only hook trust bypass for reviewed definitions.
No shared host configuration or persistent trust was changed. Launch arrays,
prompts, JSONL events, receipts and final messages are in the named local directories.

- `host-project/startup`: no task selected; SessionStart and UserPromptSubmit
  receipts carried the project goal and correction. Without tool calls, the model
  identified comparable error reduction, coverage as a separate axis, and no task.
- `host-project/planning`: a distinct fresh session read the packaged research-task
  skill, project files and synthetic route evidence. Given a proposed source-first
  curriculum, it matched R07 staged exposure, cited 0.5335 versus baseline 0.5285
  and the equal-compute control, and explained a distinct retention intervention,
  its reopen condition, matched comparison and advance/park decision. It explicitly
  qualified the evidence as synthetic. No experiment or project mutation occurred.
- `auto-compact-project-v2`: only SessionStart was enabled, excluding prompt-hook
  refresh as an alternative explanation. One authorized fixture command changed
  current guidance from AMBER to COBALT and emitted synthetic retained rows.
  `model_auto_compact_token_limit=3000` exercised actual automatic compaction.
  A SessionStart receipt with `source: compact` carried COBALT, and the continuation
  named COBALT and its replacement of AMBER. The helper ran with uv `--no-cache`
  and an explicit local Python interpreter inside the disposable workspace.

The initial app-server route did not apply the attempted process-level isolation
configuration: it ran existing user hook handlers and delivered no rctl reminder.
That process was stopped and this route is not claimed supported. The first CLI
compact attempt delivered a real compact reminder, but uv could not access its
normal cache from the sandbox, so the fixture update did not happen. Its AMBER
answer was correct for the unchanged file. Retain both failed attempts; the working
route used isolated exec and cache-independent Python execution.

## Project rollout

Process deviation: the rollout below happened after local validation but before
commit, push and remote CI. The user identified this ordering error. Local checks
did not justify skipping the release gate. Before publication, the CI wheel-smoke
command was corrected from the obsolete hard-coded 0.3.1 filename to the wheel
built in the clean CI checkout. The development plan now requires successful CI
on the release commit before deployment. Remote validation and installed-content
reconciliation are the corrective follow-up, not evidence that the original
deployment happened in the required order.

Installed the final wheel with:

```sh
uv tool install --offline --force .work/m7/dist/rctl-0.4.0-py3-none-any.whl
```

For each project, compared all five installed skill files to the prior committed
bundle before copying reviewed `update export .work/rctl-v040-2026-09-08`
candidates. Added Current guidance to PROGRAM.md from its existing decisions and
clarified project-only reminders in research/README.md. OR's existing introductory
reuse rule moved under Reuse Rule; its route entries and scientific outcomes were
preserved. Resuming its parked routes is distinguished from planning an independent
new mechanism. Shared skills, host settings and archives were not edited.

Installed `doctor --codex` reported rctl 0.4.0 and `review_needed: false` for both
projects. No-selection context returned current guidance; direct installed adapter
calls for all five Pinyin VSR and seven OR tasks included current guidance and
history reuse within 2000 characters. Pinyin VSR's long integrity handoff now exposes
actual blocker and next-step text rather than only a label and truncation path.

Byte comparisons preserved 22 Pinyin VSR and 28 OR task/configuration files,
including available contracts, results, handoffs, records, project bindings, root
instructions and host JSON/TOML. Scoped backups, exported candidates and per-task
outputs remain local under `.work/m7/before-projects/`, each project's update
export, and `.work/m7/*-upgrade.json`. No scientific checks or experiments ran.

Seven previously closed tasks now report stale applicability with retained historical
closures; a different rctl version requires new verification for any future closure
under the existing version rule. This upgrade neither reopens them nor invalidates
their historical scientific observations. Research projects also contained unrelated
preexisting changes; no research repository commits were made.

## v0.4.1 review fixes

On 2026-09-08, the review reproductions became 11 regression cases in
`tests/test_m7_review.py`: the original implementation failed 10 and passed the
packaged-placeholder control. After the fix, all 11 passed, including inequalities,
inline and standalone autolinks, individual warning markers at both budgets,
conditional orientation, and relative missing/UTF-8/directory diagnostics.
The broad angle-span search was the content-loss cause; whole-section placeholder
matching now excludes URI/email autolinks. Warning separators retain their markers,
and project errors retain their diagnosis without repeating the absolute root.

Local release checks:

- `uv run --locked pytest tests/test_m7_review.py tests/test_m7.py -q`: 26 passed.
- `uv run --locked pytest -q`: 202 passed.
- `uv run --locked ruff check src tests scripts`: passed.
- `uv run scripts/check_docs.py`: passed, 215 links and 36 acceptance cases.
  An initial invocation with `--locked` was rejected because this standalone script
  has no script lockfile; the documented invocation above succeeded.
- `uv build --out-dir .work/m7-review/dist`: built the 0.4.1 wheel and sdist.
- `uv run --locked scripts/smoke_package.py .work/m7-review/dist/rctl-0.4.1-py3-none-any.whl`:
  passed in an isolated installed environment; output is retained locally in
  `.work/m7-review/wheel-smoke.json`.
- `git diff --check`: passed.

These are parser/renderer and execution checks, not scientific evidence judgments.
Publication must precede deployment: the exact pushed commit requires successful CI,
then a wheel rebuilt from clean committed source may replace the local installation.
The scoped deployment checks inspect both research projects' installed reminders,
doctor findings and unchanged task/configuration/skill/guidance bytes. This patch
changes neither host event integration nor skills; actual startup/compaction host
sessions are not rerun, and prior M7 host evidence retains its original scope.

## Limitations

- The planning probe is one synthetic case, not a measured reduction in repeated
  suggestions across research sessions. Delivery does not establish scientific judgment.
- Long values remain excerpts; a single short reminder cannot carry every route or
  blocker. Current guidance must be maintained in its existing authoritative file.
- Actual compact evidence covers automatic compaction on the tested CLI version,
  not manual compaction, resume, other hosts or persisted trust. Root task errors
  still require explicit correction; no fallback task is chosen.
- The unsuccessful app-server invocation also exercised preexisting global hooks;
  their side effects were not certified by this test. Supported probes isolate user
  configuration. Existing [readiness limitations](READINESS.md#limitations) still apply.
