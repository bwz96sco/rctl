# M5 verification — initialization and shared skills

Date: 2026-09-06. Version: rctl 0.2.0. Scope: A-21–A-24, on macOS arm64.
The user authorized implementation and separate commits in rctl and agent-skills-private.
Shared migration commit: `380e02a` in agent-skills-private.
The existing synthesis changes in the shared repository were preserved and excluded.

## Delivered behavior

`rctl init [--vault PATH] [--codex]` creates missing project orientation, a local task
skill, and a static project binding. It preflights collisions and root boundaries before
writing; existing files are preserved and listed. A new vault receives note scaffolding;
an existing vault is associated without edits. Optional project hook/config files are
created without merging or granting trust. CLI task use remains independent of init.

The shared research-project-setup skill is retired. Its durable orientation and vault
assets now ship with rctl; research-task includes workspace, Git/data, vault, and explicit
migration guidance. research-experiment now uses native contract/result files and rctl
lifecycle commands. Training, adapter, and referee skills retain their scientific/runner
roles while delegating task phase and acceptance to research-task. Historical evaluation
records retain their original owner; the still-open routing campaign excludes setup.

## Acceptance evidence

| Case | Observation | Authority established |
| --- | --- | --- |
| A-21 | New non-Git project; repeat init preserves customized research, skill, vault, and hook files. Missing project files are restored; invalid manifest version, path collisions, and escaping symlinks reject before writes. | Filesystem behavior and structure |
| A-22 | New-vault scaffold, existing-vault preservation, retained binding, conflicting binding rejection, reserved/escaping vault rejection, and a control-directory symlink overlapping a vault. | Storage boundaries and preservation |
| A-23 | An isolated installed wheel provides project/vault resources, skill references, and project hooks; repeat init preserves bytes. Both generated hook commands execute and return selected-task context. | Package/resource execution and adapter protocol, not fresh host delivery |
| A-24 | Original shared templates validate against wheel schemas. Adapted synthetic experiment executes arithmetic and domain checks; missing/unknown review blocks closure, a deliberately incorrect promotion fails verification, and corrected negative evidence closes. | Structure, actual check execution, and explicitly attributed fixture review kept distinct |

[Wheel smoke evidence](evidence/m5/wheel-smoke.json) retains 33 CLI calls, two generated
hook-adapter responses, four native experiment verification reports, and 22 stdout/stderr
logs. Native experiment verdicts are unknown, unknown, fail, pass; its final assessment
is not_supported. No training or external scientific inference is claimed by this fixture.

## Commands and results

From the rctl repository:

```sh
uv run pytest -q
UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --python 3.11 pytest -q
uv run pytest tests/test_init.py -q
UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --python 3.11 pytest tests/test_init.py -q
uv run ruff check src tests scripts/smoke_package.py scripts/smoke_shared_skills.py
uv build
uv run scripts/smoke_package.py dist/rctl-0.2.0-py3-none-any.whl --skills-root /Users/zhangbowen/Projects/agent-skills-private
uv run scripts/check_docs.py
```

Both full runs passed 130 tests on CPython 3.13.2 and 3.11.11. After the final vault/control
alias protection was added, the complete initializer suite passed all 19 tests on both
runtimes, including the new regression. Ruff passed. The final wheel smoke passed with
rctl 0.2.0, PyYAML 6.0.3, and jsonschema 4.26.0. The documentation checker validates four
schemas and maps 14 requirements to 24 acceptance cases. Logs: [3.13](evidence/m5/py313.log),
[3.11](evidence/m5/py311.log), [final init 3.13](evidence/m5/init-final.log),
[final init 3.11](evidence/m5/init311-final.log), [Ruff](evidence/m5/ruff.log).

From agent-skills-private, with `PYTHONDONTWRITEBYTECODE=1`:

```sh
uv run --no-project python -m unittest discover -s evals/research-skills -p 'test_research_handoffs.py'
uv run --no-project python -m unittest discover -s evals/research-skills -p 'test_run.py'
uv run --no-project python -m unittest discover -s evals/research-skills -p 'test_research_skill_contracts.py'
uv run --no-project python scripts/validate-research-skills.py
bash scripts/validate-skills.sh
bash scripts/install-links.sh --dry-run
```

The [handoff suite](evidence/m5/handoff-tests.log) passed 28 tests, including selected and
unselected candidate lineage, invalid decisions, independent supplied/problem origins,
missing comparability, placeholders, task identity, YAML comments, and ordinary less-than
comparisons. The [evaluation harness](evidence/m5/shared-run-tests.log) passed 33 tests.
The skill-creator quick validator passed for research-task and all four modified shared
skills. The shared blanket checks are not all green; the exact inherited failures are
recorded below and in [READINESS limitations](READINESS.md#limitations).

## Shared baseline comparison

A clean `git archive HEAD` of the pre-change shared repository, extracted under rctl's
ignored `.work/`, reproduces the [baseline blanket failures](evidence/m5/shared-baseline-validation.log):
oversized autocli, missing autocli/playwright metadata, native invocation projection
mismatches in eight other skills, and the smart-search snapshot digest mismatch.
The [current blanket log](evidence/m5/shared-full-validation.log) also reports an existing
ignored model-training `__pycache__`; the tracked source migration does not add it.

The current [contract suite](evidence/m5/shared-contract-tests.log) passes 9/10 tests;
its sole failure is an older exact-wording assertion against the user's existing synthesis
edit. The [research validator](evidence/m5/shared-research-validation.log) reports only
two such synthesis wording mismatches. These files and unrelated native invocation
policies were not changed to make the blanket checks green. No paid evaluation campaign ran.

## Source and installation checks

Smart-search Context7 retrieval rechecked [Python filesystem APIs](evidence/m5/pathlib-docs.json)
and [uv tool installation](evidence/m5/uv-tool-docs.json). The official Codex hook guide
was reread from the retained smart-search source used by the [project loading follow-up](PROJECT-HOOKS-VERIFICATION.md).
Initialization reuses the same hook definition builder as export. No new real-host delivery
or persisted interactive-trust claim is inferred from direct adapter execution.

The final wheel was installed with `uv tool install --offline dist/rctl-0.2.0-py3-none-any.whl`;
`rctl --version` returned `rctl 0.2.0`. The link installer preview identified two stale
setup links. Only those owned links under `~/.agents/skills/` and `~/.gemini/config/skills/`
were removed; other shared skills already resolve to their edited source. No live research
project, task history, or global host configuration was migrated.

## Limitations

Use [READINESS limitations](READINESS.md#limitations) for preservation/upgrade behavior,
partial filesystem writes, inherited shared validation failures, platform coverage, hook
trust, and version-dependent verification currentness. This increment establishes local
initialization and native skill compatibility; the original real-host evidence remains
at its recorded v0.1/CLI-0.153.4 scope.
