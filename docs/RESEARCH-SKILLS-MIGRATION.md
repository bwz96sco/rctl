# Research workflow source migration

Date: 2026-09-14. Status: source migration and local link cutover complete; uncommitted.
rctl baseline: `87157e9`; private source
baseline: `3320099` plus its working-tree changes. The user explicitly selected
the 12 active research-* workflows plus paper-discovery, excluding auxiliary tools.
The user subsequently added the independent research-rapid-test skill. The
2026-09-21 follow-up below adds two training/adapter workflows, bringing that
migration to 17 managed workflows. The [catalog](RESEARCH-SKILLS.md) records the
current set, including subsequent retirements. The first-stage
evidence below covers the original 13-package move; its counts remain historical.

The later user-authorized [review follow-up](RESEARCH-SKILLS-FOLLOWUP.md) changes
workflow content after these preservation checks. Byte-identity claims below describe
the migration snapshots and cutover, not the subsequently edited current sources.

## Scope and preservation

Move the 13 packages, their 40 source files, and workflow-specific regression tests
into rctl. Preserve native invocation policy and scientific instructions; change
only source-addressing details needed by the move. Keep general tools, historical
campaigns, live research projects, rctl's installed CLI and hook configuration outside
the cutover. Project init/export continues to install only research-task.

The source had uncommitted paper-discovery and research-literature instructions,
the literature note template, and a new discovery register template. Their current
bytes were copied, not replaced from HEAD. Pending research-contract tests and
source-I/O changes are retained in the corresponding new ownership locations.
An unrelated oracle-cli edit stays untouched in the private repository.

Before editing, all 40 package files were compared byte-for-byte with their copies.
A recoverable source snapshot, including the affected private management files,
is retained at `.work/research-skill-migration-xwpGd4/source/`. Private Git history
continues to retain committed versions; that local snapshot additionally retains
the original uncommitted content.

## Implementation sequence and acceptance

Use M5/A-23 and A-24 as the packaging and native-experiment regression anchor, with
A-21/A-29 for init/update preservation. This is source management, not a new scientific
workflow or a change to task records or verification semantics.

1. Copy and verify the selected sources; retain uncommitted changes and notices.
2. Make the slides dependency location-independent. Move active workflow tests and
   current artifact contracts; leave auxiliary-tool tests with their source owner.
   Preserve the private I/O table as an explicitly historical snapshot with a link
   to the current rctl-owned contract table.
3. Make ordinary wheel smoke inspect all packaged skill files and execute the native
   experiment walkthrough without a private-repository dependency. Preserve the
   existing task-only init/export boundary.
4. After local checks, redirect only the 13 existing shared links, remove their old
   source copies and registry entries, and update private historical-reader paths.
   Verify that shared and projected discovery paths resolve to the new sources and
   that unrelated private changes remain intact.

Failures that change the migration: a lost byte or local change blocks old-source
removal; a missing resource or broken script-relative dependency requires a path or
packaging repair; policy drift requires restoration; an unrelated installation change
requires a narrower cutover. No model-quality campaign is needed for a source move.

## Observed checks

Before migration, the private workflow suites produced 37 passes, 25 passing subtests,
and one failure: a synthesis text assertion still expected the singular wording
`paper ID and note anchor`, while the current skill requires `paper IDs and note
anchors`. The migrated assertion is updated; the scientific instruction is preserved.

The private structural validator also had an outdated synthesis boundary assertion;
it now matches the existing instruction to leave retain/hold/reject and selection
gates to explicit evaluation. Neither assertion repair changes skill behavior.

| Check actually run | Result and authority |
|---|---|
| `uv run pytest tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py -q` | 51 passed, 24 passing subtests: metadata, invocation policy, resources, handoffs and task-only exports |
| `uv run pytest -q` | 286 passed, 24 passing subtests in 38.75 seconds: full local regression suite |
| `uv run ruff check src tests scripts` | Passed |
| `uv run scripts/check_docs.py` | Passed: 286 local links, 100 JSON files, 4 schemas, 20 requirements mapped to 40 acceptance cases |
| `uv build --out-dir .work/research-skill-migration-xwpGd4/dist` | Built source distribution and wheel |
| `uv run scripts/smoke_package.py .work/research-skill-migration-xwpGd4/dist/rctl-0.5.0-py3-none-any.whl` | Passed, 37 expected CLI outcomes; all 47 files across 14 skill packages match the installed wheel byte-for-byte |
| `uv run ../agent-skills-private/scripts/validate-research-skills.py` | Passed against migrated packages and historical manifests; no paid calls |
| `uv run pytest ../agent-skills-private/evals/research-skills/test_research_skill_contracts.py -q` | 3 passed, 1 passing subtest: retained auxiliary composition and Smart Search contracts |
| Private registry/directory comparison | Exactly 19 remaining packages; no migrated names or empty source directories |
| Installed-path file-identity checks | All 39 paths (13 shared, 13 Antigravity CLI, 13 Antigravity IDE) resolve to the rctl sources |

Installed-wheel execution used Python 3.13.2 on macOS arm64, with PyYAML 6.0.3 and
jsonschema 4.26.0. The native experiment rejected missing reviews, a missing runner
receipt and contradictory arithmetic before closing with `not_supported` only after
the declared checks and synthetic evidence review passed. This verifies the software
boundary, not a real scientific conclusion.

All 40 package files were rechecked against the original snapshot before old-source
removal. After cutover, 39 remain byte-identical; the sole skill edit is the installed
personal-slides contract lookup. Removed 40 old package files and the relocated
handoff test; the new sources, private Git history and local snapshot retain them.
The private registry no longer owns those packages, so its installer does not prune
their rctl-targeting links. No auxiliary skill file was edited by this migration.

## Research-rapid-test follow-up

On 2026-09-14 the user explicitly added research-rapid-test to the scope. Its
`SKILL.md` and `agents/openai.yaml` were copied from
`~/.codex/skills/research-rapid-test/` without content changes. The existing omitted
policy retains normal automatic invocation; no explicit-only control was added.
This skill owns a preliminary `rapid-test.md` and actual pilot evidence, before
formal research-experiment work. It does not bypass a frozen rctl agreement.

Use the same M5/A-23 packaging and A-21/A-29 preservation checks for this additive
source move. The preserved snapshot is under
`.work/rapid-test-migration-VNHdPn/source/`. After validation, the original Codex
package directory was moved intact to `installed-original/` beside that snapshot,
and its former path was replaced by a link to the rctl source. Both files remain
byte-identical to the saved originals. No second shared discovery entry or other
host installation was added. The private historical
validator keeps its original 12-workflow profile and excludes this additional
rctl-owned package alongside research-task; active rctl tests include all 15.

Follow-up checks completed:

- `uv run pytest tests/test_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py -q`: 52 passed, 26 passing subtests. Invocation checks honor the native default when policy is omitted; all 15 packages and task-only init/export are covered.
- `uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/research-rapid-test`: passed.
- `uv run ruff check src tests scripts`: passed. `uv run scripts/check_docs.py`: passed, now 287 local links with the same 100 JSON files, 4 schemas and acceptance mapping.
- `uv run ../agent-skills-private/scripts/validate-research-skills.py`: passed for its unchanged historical workflow profile.
- `uv build --out-dir .work/rapid-test-migration-VNHdPn/dist`, then `uv run scripts/smoke_package.py .work/rapid-test-migration-VNHdPn/dist/rctl-0.5.0-py3-none-any.whl`: passed, 37 expected CLI outcomes and all 49 files across 15 packages matched the installed wheel.
- File-identity checks confirmed both package files at the existing Codex discovery path resolve to the rctl sources; byte comparisons confirmed preservation; no duplicate shared entry exists.

## Training and adapter follow-up

Date: 2026-09-21. The user identified experiment-adapter-builder and
model-training-workflow as missing research workflows. The earlier catalog had
explicitly excluded them as auxiliary tools; this follow-up corrects that ownership
boundary. Other auxiliary packages remain outside scope.

Source baselines: rctl `2416b47`, agent-skills-private `8d65985`. The private
working tree also contained unrelated autocli deletions, which are preserved.
All 44 source package files (18 adapter, 26 training) were copied and compared
byte-for-byte before edits. The snapshot and original discovery-link targets are
retained under `.work/training-skill-migration-11s899tb/`.

The adapter fixture moves inside its package so installed helpers can use it.
Training's three pinned Orchestra audit/review files are packaged under
`references/source-audits/`; source routing now reaches those files and identifies
them as historical evidence. Changes to the original package files are limited to
these resource locations and historical-source clarification. Scientific gates,
runner authority, rctl acceptance ownership, and native invocation policies remain
unchanged. Both added packages retain Codex explicit-only invocation and their
existing frontmatter default for other hosts.

Use M5/A-23/A-24 and A-21/A-29 as the regression anchors. Validator fixtures check
structure and executable packaging, not real training quality or scientific
acceptance. Installed-wheel smoke runs both validators on the adapter fixture,
the tiny-overfit fixture and the strict collapse-diagnostic fixture, and verifies
all packaged files against source. Init/export still installs only research-task.

Observed checks:

- `uv run pytest tests/test_skill_assets.py tests/test_training_skill_assets.py tests/test_research_skill_contracts.py tests/test_research_handoffs.py -q`: 64 passed, 39 passing subtests. Includes three real validator subprocesses and rejection after removing a required evidence file from each fixture.
- `uv run ruff check src tests scripts`: passed.
- `uv run scripts/check_docs.py`: passed, 295 local links, 100 JSON files, 4 schemas, 20 requirements mapped to 40 acceptance cases.
- `uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<name>` for each added package: both passed.
- `uv build --out-dir .work/training-skill-migration-11s899tb/dist` and `uv run scripts/smoke_package.py .work/training-skill-migration-11s899tb/dist/rctl-0.5.0-py3-none-any.whl`: passed on Python 3.13.2 / macOS arm64; installed adapter, tiny-overfit and strict diagnostic validators all passed, every packaged skill file matched source, and task-only init/export was preserved.
- `uv run pytest ../agent-skills-private/evals/research-skills/test_research_skill_contracts.py ../agent-skills-private/evals/research-skills/test_source_io_mapping.py -q`: 4 passed, 1 passing subtest, and the previously recorded source-I/O failure described under Limitations. The checker and its input were unchanged.

After verification, the two shared discovery links and their existing Antigravity
CLI targets were redirected to rctl; the IDE projections through the shared paths
needed no edit. All six discovery paths resolve to the new sources. The original
package directories and external adapter fixture are retained under the snapshot's
`retired-source/`; the private registry no longer owns the two skills. The private
README now points to rctl. The remaining private registry/directory difference is
the pre-existing autocli deletion. Pinned audit copies in the private registry stay
as historical records; the rctl package owns the active source-routing resources.

The official [Codex skill documentation](https://developers.openai.com/codex/skills)
was re-fetched with `smart-search fetch https://developers.openai.com/codex/skills
--format markdown --output /tmp/rctl-skill-docs-20260921.md` on 2026-09-21. It
confirms symlink discovery and Codex's explicit-only policy. A copy is retained in
`.work/training-skill-migration-11s899tb/codex-skills.md`.

## Limitations

- Both repositories contain uncommitted migration changes. No commit/push, CLI
  deployment, live OR/Pinyin task edit, hook/trust change or new model campaign was
  performed. The archived private paid-run harness still binds candidate revisions
  to that repository; it is historical machinery, not a current rctl-suite runner.
  The rapid-test follow-up checked source, packaging and installed-path identity;
  it did not run an empirical pilot or a fresh-host model invocation. The training/adapter
  follow-up likewise checks packaging, structure and installed-path identity; it does
  not establish live training behavior or fresh-host invocation.
- The first-stage run of `uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py
  skills/<name>` on all 14 packages passed 12 and rejected the two explicit-only
  packages solely because it does not accept Claude's native `disable-model-invocation`
  key. Native policy-parity tests pass for all 14; those existing controls were retained.
- The first-stage private `scripts/validate-skills.sh` run was red on then-untouched auxiliary assets:
  generated caches in personal-slides/model-training-workflow; autocli length and
  missing OpenAI metadata; missing playwright-cli OpenAI metadata; invocation-policy
  mismatches in autofigure-edit, experiment-adapter-builder, model-training-workflow,
  nlm-skill, obsidian-dev, oracle-cli, personal-slides and slurm-hpc-runner; and the
  Smart Search upstream snapshot mismatch. Its manifest and JavaScript syntax checks
  passed. These findings did not justify changing auxiliary packages in a 13-workflow
  relocation.
- The combined private contracts/source-I/O test run had 4 passes and one failure:
  the old source-I/O checker calls the already-present `research-task` table row an
  extra research workflow. Applying the same unchanged checker to the preserved
  pre-migration I/O text reproduces that failure. The historical checker was not
  expanded into a second authority for rctl's current artifact contracts.
