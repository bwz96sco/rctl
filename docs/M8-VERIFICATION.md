# M8 verification — governing-question alignment

Date: 2026-09-14. Version: 0.5.0. Scope: A-37–A-40 plus existing lifecycle,
context, packaging, and documentation regressions. This is a local implementation
record, not a release, installation, live-project migration, commit, or publication.

## Outcome

M8 passes locally. A contract may declare an optional strict `Question alignment`
section that points to a readable project-relative Markdown source and records the
governing mechanism, the relationship isolated by the task, and the broader claim
the task does not decide. Existing contracts remain valid without this section.

Selected-task status and both context modes now project the accepted task question,
declared alignment, and latest verified assessment with its verification ID,
contract revision, and currentness. Compact reminders put this retained task context
ahead of mutable project guidance. A drifted working contract cannot replace it.

## Acceptance evidence

| Case | Result | What the check establishes |
| --- | --- | --- |
| A-37 | Pass | Complete alignment accepts; unknown, missing, duplicate, extra-prose, external, absolute, escaping, non-Markdown, missing, and unreadable sources reject before begin. Legacy contracts return null alignment. |
| A-38 | Pass | Compact 2,000-character and extended 8,000-character reminders retain the accepted question, full declared relationship, warnings, blocker, and next action ahead of long mutable guidance; JSON stays bounded. |
| A-39 | Pass | A verified `not_supported` result is exposed as a task-scoped assessment bound to V0001/revision 1/currentness. A declared source review becomes stale when that source changes; removing an accepted source otherwise warns without changing closed phase or historical closure. |
| A-40 | Pass | Packaged template and research-task guidance explain alignment and evidence review. Installed-wheel SessionStart and UserPromptSubmit responses use the unchanged hook envelope and contain the declared non-claim boundary. |

The focused regression was first run before implementation and produced 17 expected
failures and 15 passes, demonstrating the missing parser, compact reminder, and
assessment projection. The completed commands were:

```text
uv run --locked pytest -q tests/test_m8.py tests/test_m3.py
35 passed in 3.84s

uv run --locked pytest -q
222 passed in 32.81s

uv run --locked ruff format src/rctl/__init__.py src/rctl/cli.py src/rctl/context.py src/rctl/documents.py src/rctl/records.py tests/test_m3.py tests/test_m8.py scripts/smoke_package.py
8 files left unchanged

uv run --locked ruff check src tests scripts
All checks passed!

uv run --locked python scripts/check_docs.py
PASS: 216 local links; 88 JSON files; 20 requirements mapped to 40 cases

uv build --out-dir .work/m8/dist
Built sdist and wheel

uv run --locked scripts/smoke_package.py .work/m8/dist/rctl-0.5.0-py3-none-any.whl
Passed in an isolated Python 3.13.2 environment on macOS 26.6.2 arm64
```

The wheel smoke initializes a disposable non-Git project, confirms the packaged
template and local skill contain alignment guidance, accepts an aligned contract,
runs lifecycle verification and closure, and observes aligned context through both
generated Codex handlers.

## Integration source recheck

The official [Codex hooks documentation](https://developers.openai.com/codex/hooks)
was fetched through smart-search on 2026-09-14. It continues to define
`additionalContext` for SessionStart and UserPromptSubmit; M8 changes the shared
rendered content only. No hook definition, event selection, response envelope, trust,
or host configuration behavior changed.

## Limitations

- Scientific adequacy of the declared relationship is not inferred by rctl. A review
  criterion must judge it when it affects closure.
- A Markdown fragment is retained as an anchor hint; rctl checks the file, not whether
  the named heading exists.
- Existing accepted tasks whose declared source later disappears receive a warning;
  their retained contract, phase, and historical meaning are not rewritten.
- Real-host launch was not repeated because the authorized M8 plan requires
  content-only fixtures when the verified hook shape remains unchanged. Release,
  installation, OR task migration, shared-skill changes, commit, push, and CI remain
  separate actions.
