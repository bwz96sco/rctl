# Simplification verification

Date: 2026-09-14. Baseline: `82a5ec8`, package version 0.5.0. Status: first increment
implemented and locally validated; release pending. This record covers the first increment of
the [implementation plan](SIMPLIFICATION-REVIEW.md), using M8/A-37–A-40 and its named
context, discovery, packaging, history-reuse, and real-host regression cases.

## Implemented behavior

The root research-task skill routes planning and verification to packaged references
while retaining lifecycle syntax, addressing conventions, and completion invariants.
Its root text decreased from 1,306 to 577 whitespace-separated words. That is an
instruction-size observation, not a measured model-quality improvement.

An immutable TaskSnapshot supplies status, discovery, and reminder projections.
Nested report data cannot be changed through a snapshot or a returned JSON projection.
Renderers perform no additional file reads. Each new snapshot refreshes handoff and
verification applicability, using the existing lifecycle and currentness logic.

Both hooks retain their response shape, selection rules, and 8,000/2,000-character
caps. One layout replaces compact/extended branches and omits appended contract and
handoff excerpts. Alias C points to retained accepted text for managed tasks and the
working contract for drafts. Required scope, warnings, next steps and source paths
retain bounded visibility. Record and review schemas are unchanged.

## Automated checks

The first focused run passed 167 cases and failed four assertions requiring the old
full-document injection or alignment details directly in the root skill. Those
assertions were replaced with the new source/routing behavior, preserving their
read-only, truncation, and packaged-guidance checks.

The updated focused run passed 174 cases, including three snapshot regressions:
deep immutability and detached JSON, fresh evidence/handoff state, and I/O-free
projections using the same layout at both budgets.

```sh
uv run pytest tests/test_snapshot.py tests/test_m1.py tests/test_m3.py tests/test_m6.py tests/test_m6_review.py tests/test_m7.py tests/test_m7_review.py tests/test_m8.py tests/test_init.py -q
uv run ruff check src tests scripts
uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-task
```

All three commands passed. The full suite then passed **235 tests in 36.95 seconds**.
After the real-host checkpoint finding below, the exported-guidance test and wheel
smoke were updated to retain the active-only rule. The affected init tests passed
**19 tests**; lint and skill validation passed again. Runtime code did not change
after the full-suite run. The skill validator establishes frontmatter/scaffold
validity, not research behavior.

```sh
uv run pytest -q
uv run pytest tests/test_init.py -q
uv run ruff check src tests scripts
uv run scripts/check_docs.py
uv build --out-dir .work/simplification-zsjIFu/dist
uv run scripts/smoke_package.py .work/simplification-zsjIFu/dist/rctl-0.5.0-py3-none-any.whl
uv build --out-dir .work/simplification-zsjIFu/dist-final
uv run scripts/smoke_package.py .work/simplification-zsjIFu/dist-final/rctl-0.5.0-py3-none-any.whl
```

Both source distributions and wheels built successfully. Both installed-wheel
smokes exited 0 with `ok: true`, including lifecycle execution, exported references,
and both hook response envelopes. The final wheel includes the active-only guidance
repair. See the [initial full trace](evidence/simplification/wheel-smoke-before-guidance-fix.json),
[final captured output](evidence/simplification/wheel-smoke-final-captured.txt), and
[final package/skill comparison](evidence/simplification/candidate/doctor-final.json).
The latter reports every project-local skill file current with the final package.
The final document check passed: **265 local links, 100 JSON files, four schemas
and example inputs, and 20 requirements mapped to 40 acceptance cases**.
`git diff --check` passed; new files were also checked individually for whitespace.

## Official source check

Fetched through smart-search on 2026-09-14:

- [Astra skill and prompt guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra.md): progressive disclosure and clear completion conditions.
- [Codex hooks](https://developers.openai.com/codex/hooks.md): SessionStart/compact, UserPromptSubmit, and invocation-only trust for previously reviewed hooks.
- [Codex configuration](https://developers.openai.com/codex/config-reference.md): automatic-compaction threshold and body-after-prefix scope used only in the disposable probe.

## Real-host acceptance

Host: Codex CLI 0.154.0. Model: `gpt-6-astra`, reasoning effort `medium`.
An isolated availability invocation returned READY without tools. The acceptance
driver is [probe_simplification.py](../scripts/probe_simplification.py); it uses
fixed synthetic fixtures, a selected baseline/candidate executable, reviewed inline
hooks, workspace-write sandboxing, and no persisted host configuration or trust edits.

The [evidence index](evidence/simplification/README.md) retains exact launch argv,
prompts, delivered context, source-reading commands and outputs, continuations,
CLI responses, final records, and arithmetic execution logs. Original raw session
files remain under `.work/simplification-zsjIFu/`. Each variant used a separate
disposable project and four fresh, ephemeral sessions in stage order: `first`,
`resume`, `compact`, `stale`. Here `resume` means fresh-session handoff recovery,
not the host's `codex resume` command.

The baseline executable came from an isolated checkout of `82a5ec8`. The candidate
used an isolated installed wheel. The first three candidate stages used the initial
wheel; before the already-planned stale stage, it was replaced with the final wheel
and its two clarified skill files were applied only to the disposable project.
No case was repeated to obtain a favorable result.

Actual driver invocations used the stage names above with these arguments; each
stage's evidence retains the fully expanded host command and prompt:

```sh
uv run scripts/probe_simplification.py first --root /Users/zhangbowen/Projects/rctl/.work/simplification-zsjIFu/baseline-project --rctl /Users/zhangbowen/Projects/rctl/.work/simplification-zsjIFu/baseline/.venv/bin/rctl
uv run scripts/probe_simplification.py first --root /Users/zhangbowen/Projects/rctl/.work/simplification-zsjIFu/candidate-project --rctl /Users/zhangbowen/Projects/rctl/.work/simplification-zsjIFu/candidate-venv/bin/rctl
```

For a new reproduction, choose new project destinations and run all four stages in
order for each executable. The driver refuses to overwrite existing stage evidence.
It sets a 3,000-token body-after-prefix automatic-compaction threshold only for the
compact stage. A helper changes project guidance and emits delivery-only rows; the
model is instructed to use no tools afterward. This separates later hook delivery
from an explicit source reread.

| Case | Baseline observation | Candidate observation |
|---|---|---|
| Recover concrete work | Saved a 13,660-character handoff, then a fresh session identified its next step before tools, inspected sources, verified and closed with V0001. [First](evidence/simplification/baseline/first.json), [recovery](evidence/simplification/baseline/resume.json). | Saved a 15,248-character handoff; a fresh session recovered the named assessment step before tools and closed with current V0001. An unnecessary post-close checkpoint was rejected; see the repair below. [First](evidence/simplification/candidate/first.json), [recovery](evidence/simplification/candidate/resume.json). |
| Narrow negative, history and automatic compaction | Closed `not_supported`; cited related question/route history for a matched component-removal follow-up. After actual compaction, reported refreshed guidance and the accepted non-claim, with no tools after the helper. [Evidence](evidence/simplification/baseline/compact.json). | The routed planning reference led to the same bounded distinction and a distinct component-removal question/decision, without executing research. A post-helper `SessionStart`/`compact` receipt contained the changed guidance, which the final response quoted while preserving scope. [Evidence](evidence/simplification/candidate/compact.json). |
| Verification applicability | Handoff-only edit preserved current V0002; a result annotation made it stale and `close` exited 4 / VERIFICATION_STALE. Astra reviewed, verified V0003, checkpointed, then closed. [Evidence](evidence/simplification/baseline/stale.json). | The same guard sequence held. With final guidance, Astra inspected the annotation, refreshed its evidence review, verified V0003, checkpointed while active, then closed in cycle 2. [Evidence](evidence/simplification/candidate/stale.json). |

Both variants retained the fixed synthetic calculation: error 0.20 versus 0.23,
gain -0.03 below the +0.01 threshold, so C1 is not promoted. Their results did not
decide whether complementary components improve generated programs. These are
observed bounded continuations, not a claim that negative language alone proves
scientific judgment. Hook receipts establish delivery; reports and execution logs
establish actual checks/closure; source reads and continuations support the scoped
interpretation.

### Observed instruction repair

The initial candidate recovery successfully closed, then unnecessarily attempted
`checkpoint` and received STATE_REJECTED. The root command table had lost its
active-task qualification. The final skill restores that qualification and adds
one sentence to the closeout reference: checkpoint any final handoff before closing.
No lifecycle exception or automatic reopening was added. The final candidate stale
session read that reference and executed `verify -> checkpoint -> close` successfully.
The rejected original command remains in the recovery evidence.

Neither variant needed a routine `rctl --help` lookup. Both still inspected source
files; candidate planning and verification loaded their routed references. Some
inspection batches encountered an absent optional file or an empty `rg` result,
and the baseline recovery corrected a patch attempt; these did not prevent completion
and do not warrant new rctl machinery.

### Reminder size observations

| Delivered context | Baseline characters | Candidate characters |
|---|---:|---:|
| First-session startup | 4,206 | 1,565 |
| Long-handoff recovery startup | 8,000 | 2,267 |
| Post-helper automatic-compaction reminder | 8,000 | 2,299 |

All recorded prompt reminders stayed within 2,000 characters, and SessionStart
reminders stayed within 8,000. Both variants completed the required observations.
The first fixture was fixed, but later handoffs and project notes were independently
authored; these lengths are delivery observations, not a controlled token-cost or
model-quality benchmark.

## Limitations

This is one synthetic bounded comparison per variant, not evidence of a general
Astra quality, latency, or read-count improvement. Final checkpoint wording was
exercised in the stale stage, not a rerun of the earlier recovery or compaction
stages. Host evidence covers Codex CLI 0.154.0 with inline hooks and invocation-only
trust; host resume, manual compaction, and persisted trust without bypass were not
tested here. The final wheel-smoke stdout capture was truncated by the tool output
budget; its exit 0, captured output, prior full smoke, and final packaged-skill
comparison are retained separately.

At validation closeout, no commit/push, release, shared installation upgrade, live
OR/Pinyin VSR migration, hook retirement, or verification-protocol migration had occurred.
Existing [readiness limitations](READINESS.md#limitations) retain their scope.
