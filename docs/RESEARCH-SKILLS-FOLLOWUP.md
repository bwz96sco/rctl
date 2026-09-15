# Research skill review follow-up

Date: 2026-09-14. Status: implemented and locally validated; uncommitted.

This user-authorized follow-up implements the two review rounds after the
[source migration](RESEARCH-SKILLS-MIGRATION.md). It keeps all 15 packages and their
invocation identities. The [catalog](RESEARCH-SKILLS.md) owns the current workflow
and installation map. Native rctl lifecycle, schemas, and CLI syntax are unchanged.

## Changes and acceptance boundary

Use M5/A-23/A-24 as the integration anchor, with A-22/A-29 for bound-vault and
packaged-resource preservation. The added handoff cases exercise domain structure
and provenance, not the scientific validity of any candidate.

| Reviewed issue | Implemented boundary |
|---|---|
| Evaluation cannot hand off to rapid-test | Selected decisions allow a preliminary pilot or formal experiment; the original selected C# survives a pilot-to-formal follow-up. |
| A human's one-candidate shortlist is rejected | Any nonempty explicit known-ID selection is accepted; human rationale, screening coverage, exact attack/disposition scope, and the final two-survivor cap remain required. |
| Note paths ignore the configured vault | The eight affected skills read the project-relative vault binding, preserve existing topic artifacts, and fall back only when unbound. |
| Ideation sends new paper search to literature | New discovery routes to paper-discovery; full-paper evidence work stays with literature. |
| Plan/audit requests inherit production completion | Slides, figures, and writing now complete against the requested operation; production render/build checks remain real when applicable. |
| Theory cannot distinguish refutation from an incomplete proof | Each stated claim receives proved/refuted/not_proved/blocked; audit and repair remain separate, and revised claims do not overwrite the original judgment. |
| Uninspected computation is described as running | Actual observed job state and result validation are reported separately; computation is optional support that reuses the calling task's evidence and budget. |
| Writing strength follows study counts or missing evidence implies no prior work | Wording follows design, observation, uncertainty, and scope; literature-absence claims require actual search coverage. |
| Helpers assume one user-level installation path | Commands use the discovered skill directory; candidate validation has an explicit sibling-package dependency and a useful missing-dependency error. |
| Broad defaults expand narrow requests | Ideation counts/diversity and opportunity lenses remain defaults; explicit smaller requests override them, and unknown prior work need not be invented. |

Evidence anchors, actual execution/render checks, pilot controls, cumulative pilot
budgets, untested-versus-refuted distinctions, and the literature reader's existing
model policy are retained. Research-computation remains a thin optional skill, not
a required stage or a competing task lifecycle. Existing research-task, synthesis,
and referee-review core workflows did not need rewriting.

## Mechanical regression checks

New subprocess fixtures cover one/two/six-ID human selections, empty/duplicate/
unconfirmed selections, pilot and formal owners, invalid owner/status combinations,
required attacks and briefs, unchanged selection provenance after a pilot, and a
relocated installation with spaces in its path. Supplied/problem experiments work
without the peer validator; candidate-origin work reports its missing dependency.

Before changing the validator implementations, the updated handoff suite reported
9 failures, 31 passes, and 8 passing subtests. These failures exposed the old count
gate, formal-only owner, and missing-peer diagnostic. After repair, the affected
three-suite run passed 59 tests and 39 subtests. A few fixed-prose assertions were
removed; structural metadata, artifact fields, and invocation checks remain.

| Command actually run | Result |
|---|---|
| `uv run pytest tests/test_research_handoffs.py tests/test_research_skill_contracts.py tests/test_skill_assets.py -q` | 59 passed, 39 passing subtests in 2.66 seconds after repair |
| `uv run pytest -q` | 294 passed, 39 passing subtests in 36.62 seconds |
| `uv run ruff check src tests scripts skills` | Passed, including both domain validators |
| `uv run ruff format --check tests/test_research_handoffs.py skills/research-idea-evaluation/scripts/validate-handoff.py skills/research-experiment/scripts/validate-result.py` | All three modified Python files formatted |
| `uv run scripts/check_docs.py` | Passed: 292 local links, 100 JSON files, 4 schemas, 20 requirements mapped to 40 acceptance cases |
| `uv build --out-dir .work/research-skill-fixes-2pTbwE/dist` | Built source distribution and wheel |
| `uv run scripts/smoke_package.py .work/research-skill-fixes-2pTbwE/dist/rctl-0.5.0-py3-none-any.whl` | Passed from the isolated installed wheel; packaged skill bytes matched the checkout, task-only init/export remained intact, and the native negative experiment closed only after its checks/review passed |
| `uv run /Users/zhangbowen/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/<changed-skill>` for all 12 modified skills | 10 passed; the two existing explicit-only packages hit the known unsupported-key limitation below |
| `git diff --check` | Passed for tracked changes |

The installed-wheel smoke used Python 3.13.2, PyYAML 6.0.3, and jsonschema 4.26.0 on
macOS arm64. It retained expected unknown/fail outcomes for missing review and bad
arithmetic; a domain-structure pass alone did not allow closure.

## Independent request trials

Following skill-creator's forward-testing guidance, two clean-context agents received
only realistic requests, named skill paths, and synthetic fixture files. Neither
received the review, intended answer, patch, or test assertions. They performed five
local requests with no network, remote jobs, installation changes, or writes outside
their fixture directories. The implementation author then read their actual outputs.

| Request and raw input | Observed result |
|---|---|
| Plan an eight-minute lab talk from one synthetic comparison (baseline error 0.20, candidate 0.23, required reduction 0.01); the bound vault is `notes`, with a separate legacy `note/` directory present. | Created `notes/slides/error-threshold/outline.md`: six evidence-grounded slides totaling 480 seconds. Produced no deck and claimed no visual QA. The configured vault won over the legacy directory convention. |
| Audit SVG numerical labels and a caption claiming a 15% accuracy improvement on all tasks; only the same one-comparison error values are supplied, without a plotting script. | Preserved the SVG, confirmed the values, identified error increasing by 0.03/15% and the unsupported generalization, and delivered an audit. Missing plotting provenance did not trigger a rebuild; visual properties remained unassessed. |
| Revise a standalone LaTeX fragment reporting A error 0.20 versus B error 0.23 in one paired run and claiming no prior studies; no literature search or build project exists. | Preserved the measured values, used "show" for the bounded 0.03 arithmetic difference, removed the unsupported literature-absence claim, and delivered `revised.tex` as unbuilt. |
| Audit a proposed lemma that every extreme-point linear minimizer over a bounded `P` inside `[0,1]^n` containing a binary point must be binary. | Classified the original as `refuted`, using `P = [1/2, 1]` and `c = 1`. Checked every hypothesis and left the manuscript source unchanged; no formal experiment was opened. |
| Report status and result validity from retained job 4812 with `COMPLETED`, exit `0:0`, objective 17.4, and a log saying constraint/gap validation was not performed. | Reported recorded completion separately from validation, classified the objective as a parsed report, and made no feasibility/optimality or fresh-execution claim. Created only the requested response. |

Scratch evidence is under `.work/research-skill-fixes-2pTbwE/`: `output-cases/` contains
the talk/figure/writing inputs, outputs, and `response.md` command logs; `science-cases/`
contains the theory/computation trials. The mathematics, arithmetic, and claim checks
are evidence-based judgments; file-presence and timing checks do not substitute for them.

## Official integration evidence

Executed through the required Smart Search route:

```sh
smart-search search 'site:developers.openai.com/codex skills paths invocation' --format markdown
smart-search fetch 'https://developers.openai.com/codex/skills.md' --format markdown
```

The fetched [official skill documentation](https://developers.openai.com/codex/skills)
describes repository/user/admin discovery, symlinked folders, progressive disclosure,
and explicit/implicit invocation policy. It supports resolving a skill's actual path
and preserving existing invocation policy; it does not establish the scientific
quality of these workflows. No hook protocol or trust change is needed.

## Limitations

- No live OR/Pinyin task, auxiliary private skill, shared install configuration,
  global rctl CLI, hook, or trust setting is modified. Existing links continue to
  read their rctl-owned source packages.
- Independent request trials use synthetic local inputs and the available agent
  runtime. They are not a fresh-host installation check, an exhaustive workflow
  benchmark, or evidence of general scientific/model performance.
- Candidate-origin experiments still require the evaluation package at the
  documented sibling location; arbitrary split-root installations are not inferred.
- The generic skill-creator validator rejects the preserved `disable-model-invocation`
  field on research-idea-evaluation and research-opportunity-mining. Repository-native
  metadata/invocation-parity checks pass; their explicit-only controls were not removed
  to satisfy a validator that does not support that existing host field.
- No commit, push, CI run, or deployment is included in this follow-up.
