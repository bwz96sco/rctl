# Comparison-template follow-up — 2026-09-23

## Purpose and scope

The OR discussion exposed two authoring gaps: the project route template listed
only negative/parked/unrun directions, and comparison templates did not make
changing control versions or shared diagnostic information visible enough.
Earlier research-experiment and research-rapid-test source edits supplied domain
guidance; this follow-up connects native project/task scaffolding and research-task.

## Changes

- Add project PROBLEM_METHODS and comparison-design templates, with README/PROGRAM
  navigation. The existing recursive resource copier needs no runtime change.
- Expand ROUTES to include candidates and bounded positive findings; distinguish
  an implementation stop from refutation of a broader problem/mechanism.
- Identify baseline versions, roles and information conditions; keep a fixed main
  comparison while adding enhanced controls and conditional ablations separately.
- Native contract/result guidance prompts purpose, information boundaries and
  primary endpoints conditionally for comparison tasks. No required schema field,
  command, task phase or automatic scientific judgment is added.
- Planning, rapid-trial and workspace references carry the same ownership and
  interpretation rules. Reviewed copies are synchronized into the OR project's
  local research-task skill; unrelated local and source edits remain intact.

## Validation scope

Affected checks cover A-21/A-22 initialization/resource preservation and A-24 native
template compatibility. The existing init test includes new resources, reading
links and preservation of customized new files. Documentation checks cover local
links and schema examples. The source-level validation record is retained by the
OR task `tasks/2026-09-23-rctl-comparison-template-followup`.

Observed local checks: 106 tests pass across test_init, test_m1,
test_research_skill_contracts and test_research_handoffs (11.58 seconds). The
documentation checker passes 305 local links, 100 JSON files, four schemas/example
inputs and requirement/acceptance mappings. The edited initialization test passes
ruff; scoped diff checks pass. The OR task-skill entrypoint passes skill structural
validation, and its three updated references are byte-identical to source.

## Release-readiness recheck — 2026-09-23

The working tree based on `2416b47` was checked together with the pending
training/adapter migration. Two failures were reproduced and repaired:

- Installed-wheel smoke still filled the previous experiment-template placeholders.
  It now supplies the updated comparison, information and endpoint fields and lists
  any remaining placeholders in its assertion message.
- Changing native Scope/Constraints placeholder strings made unfinished v0.5.0
  drafts pass `begin` and `amend`. The installed CLI rejected the same drafts.
  Keep those existing marker strings and append the new comparison guidance outside
  them. Four CLI regressions failed before this repair and pass afterward, including
  preservation of the existing record after a rejected amendment. Runtime code and
  schemas remain unchanged.

The additional guard checks cover A-01; initialization, installed resources, native
experiment execution and update preservation retain A-21/A-22/A-23/A-24/A-29.
Environment: macOS 26.6.2 arm64, Python 3.13.2, uv 0.12.3, pytest 9.1.1,
ruff 0.16.6, PyYAML 6.0.3 and jsonschema 4.26.0.

| Command or check | Observed result and authority |
|---|---|
| `uv run --locked pytest tests/test_m1.py -k v050_scaffold -q` | Four failures before repair; four passes afterward. Checks rejection of unfinished old drafts/amendments, not scientific adequacy. |
| `uv run --locked pytest -q` | 303 passed, 39 passing subtests in 41.10 seconds. |
| `uv run --locked ruff check src tests scripts` and `git diff --check` | Passed. |
| `uv run scripts/check_docs.py` | Passed local links, JSON/schema examples and requirement/acceptance mappings. |
| `uv build --out-dir .work/readiness-20260923-smdbqU/dist-final` | Built source distribution and wheel. |
| `uv run --locked scripts/smoke_package.py .work/readiness-20260923-smdbqU/dist-final/rctl-0.5.0-py3-none-any.whl` | Passed 37 expected CLI outcomes, the three migrated validator fixtures and generated hook payload checks in an isolated installed environment. |
| Wheel/source byte comparison and installed init output | All 5 schema-directory files, 31 template files and 109 skill files match; the two new research resources and rapid-trials reference are created. |

Local logs, the initial failures, final smoke output and official-source fetches are
retained under `.work/readiness-20260923-smdbqU/`. The initial attempt to run the
documentation script with `--locked` was an invocation error: its inline script
metadata has no script lockfile. The documented `uv run scripts/check_docs.py`
command passed without adding a lockfile.

The global CLI still uses the wheel built on September 15; all 17 runtime Python
files and schemas match current source, but its packaged templates and skills are
older. The affected shared domain-skill links already resolve into this repository.
The fetched official Codex skill documentation confirms symlink discovery; uv's
tool documentation confirms installed tools use their own environment:
https://developers.openai.com/codex/skills and
https://docs.astral.sh/uv/concepts/tools/ . Both were rechecked through smart-search.

Commit the intended changes, including untracked packages/templates and these
repairs, then follow `docs/DEVELOPMENT.md` release order: push, wait for CI on that
exact commit, build from clean committed source, and replace the installed wheel.
Existing project copies require scoped merging; init preserves existing files,
and update export supplies research-task candidates without merging research
orientation documents. No hook-definition change is needed for these asset edits.

## Limitations

This follow-up is source/template work. It does not upgrade the global CLI, change
host integration, migrate existing task contracts or prove future agent compliance.
Native structural validation cannot determine whether a scientific comparison is
fair; that remains an evidence-based review responsibility. The local wheel smoke
establishes installed-package execution, not live-host delivery or real training
quality. This recheck did not commit, push, replace the global CLI, edit shared
links or revalidate the OR project's local copies. CI currently passes only for
the previous committed `2416b47`, not this working tree; Linux and Python 3.11
checks remain part of the next commit's CI gate.
