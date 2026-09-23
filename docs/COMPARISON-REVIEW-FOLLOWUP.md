# Comparison-guidance review and v0.5.1 preparation

Date: 2026-09-23. Baseline: `0140b19`, following the training/adapter migration
`1c098df`. This increment implements the agreed source changes from the comparison
guidance review; the earlier [template record](COMPARISON-TEMPLATE-FOLLOWUP.md)
retains its original validation evidence.

## Decisions and changes

- Bump the package to 0.5.1 so the new packaged assets can be distinguished from
  the installed September 15 wheel. Update current usage examples; preserve
  historical version references and v0.5.0 draft regression fixtures.
- Keep currentness behavior unchanged. Exact version mismatch still marks a
  report stale, including on closed tasks, without revoking historical closure.
  Active tasks need verification by the current version before closing.
- Let PROBLEM_METHODS own open questions and candidate methods, and ROUTES own
  scoped investment decisions. Restore the rule against entries for each run,
  seed or campaign stage; preserve the distinction between an implementation stop
  and refutation of a broader claim.
- Start planning with the problem/method overview and PROGRAM's Goal and Current
  guidance, then inspect related route evidence and other sections as needed.
- For tasks updating living guidance, retain task-local evidence of the update
  and link the research files in the body. Continue declaring live files when
  their current content is a real acceptance dependency, including in reviews.
- Keep essential control identity, information boundaries and endpoint rules in
  shared skills. Route detailed comparison design to the project guide where
  present, remove OR-specific terminology, and shorten duplicated rapid-trial
  bookkeeping. Standalone pilots still work without rctl or the project guide.
- Reduce whitespace-delimited entrypoint words from 1,083 to 1,005 for
  research-experiment and from 1,657 to 1,455 for research-rapid-test. These counts
  describe reading cost, not behavioral effectiveness.
- Preserve native task-template markers, command and schema contracts, skill
  invocation policies, and project-file preservation on initialization/export.

The official [Codex skill documentation](https://developers.openai.com/codex/skills)
was searched and fetched with smart-search. It documents progressive disclosure,
optional references and symlink discovery; the edits change guidance rather than
host configuration. Retrieval commands:

```sh
smart-search exa-search "Codex skills progressive disclosure" --include-domains developers.openai.com --num-results 2 --format json --output .work/review-followup-20260923/codex-skills-search.json
smart-search fetch https://developers.openai.com/codex/skills --format markdown --output .work/review-followup-20260923/codex-skills.md
```

Fetched evidence and local test/smoke logs remain under
`.work/review-followup-20260923/`.

## Verification

Affected acceptance cases: A-01/A-02 for old-draft rejection and amendment
preservation; A-21/A-22/A-23/A-24/A-29 for initialization, packaged skill execution,
native experiment compatibility and update preservation.

Environment: macOS 26.6.2 arm64, Python 3.13.2, uv 0.12.3, pytest 9.1.1,
ruff 0.16.6, PyYAML 6.0.3 and jsonschema 4.26.0.

| Command or check | Observed result |
|---|---|
| `uv lock --offline` and `uv sync --locked` | Only rctl's locked version changed, from 0.5.0 to 0.5.1; project environment synchronized. |
| `uv run --locked rctl --version` | `rctl 0.5.1`. |
| `uv run --locked pytest -q` | Final run: 303 passed and 39 passing subtests in 41.53 seconds. Includes old native-draft rejection and preservation of customized initialized assets. |
| `uv run --locked ruff check src tests scripts` and `git diff --check` | Passed. |
| `uv run scripts/check_docs.py` | Passed local links, JSON/schema examples and requirement/acceptance mappings. |
| skill-creator `scripts/quick_validate.py`, called through `uv run --locked python` | research-experiment, research-rapid-test and research-task pass structural validation. Invocation metadata remains unchanged. |
| `uv build --out-dir .work/review-followup-20260923/dist-final` | Built the 0.5.1 source distribution and wheel. |
| `uv run --locked scripts/smoke_package.py .work/review-followup-20260923/dist-final/rctl-0.5.1-py3-none-any.whl` | Passed 37 expected CLI outcomes, all three migrated validator fixtures, generated hook payloads, packaged skill byte comparisons and task-only init/export preservation in an isolated installed environment. Installed distribution reports 0.5.1. |

The first full run found one stale test expectation: initialization still expected
the old PROGRAM-first reading order. Updated that expected navigation sequence;
all link-resolution and customized-file preservation assertions remain intact.
The final suite and rebuilt-wheel smoke pass. No runtime implementation changed
apart from the version constant, and native contract/result markers are unchanged.

These are locally validated candidate artifacts. For deployment, push the release
commit, wait for its exact CI run, rebuild from the clean committed source and
perform the scoped installation checks in [DEVELOPMENT](DEVELOPMENT.md).

## Deferred work

Version-only currentness on historical closures and PROBLEM_METHODS reminder
coverage need a separate runtime increment. OR's project-local skill merge,
review-timing note and updated adapter-validator audit entry remain a separate
live-project follow-up. No historical task needs reopening just to annotate a
later source review or validator run.

## Limitations

Structural validation and software execution do not establish scientific adequacy
or prove that an agent will follow the instructions. This source increment does
not revalidate OR's local copies, migrate live tasks, change shared links or host
configuration, or install a global wheel. CI on the eventual release commit and
installation checks remain release gates under the development plan.
