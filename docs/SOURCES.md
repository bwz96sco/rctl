# Source Register

Prepared 2026-09-05. Local files were inspected during this preparation. Statements about the prior pilot are historical evidence, not new rctl runtime tests.

## Local evidence

| ID | Source | What it supports | Design use |
|---|---|---|---|
| S-01 | [Original proposal](../research-control-layer-development-plan.md) | Earlier detailed SQLite/CLI/verification architecture and explicit separation of task, execution, and scientific judgment. | Retain useful semantics; narrow initial implementation in DEVELOPMENT. |
| S-02 | Mempal drawer `drawer_pinyin_vsr_research_default_1dcd8e50c1ba`; its [source result](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/result.md) | Two fresh sessions, handoff recovery, correct negative closeout, and one corrected host configuration. | Evidence for feasibility of the small task arrangement. |
| S-03 | [Pilot execution summary](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/evidence/session-summary.json) and [review](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/evidence/review.md) | Distinct session IDs, actual receipt events, arithmetic/review checks, and tested CLI 0.153.4. | Separate actual delivery from manual hook tests. |
| S-04 | [Working launch arguments](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/evidence/attempt-002-first-launch.json) and [harness](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/harness/README.md) | Invocation-local configuration worked; project-only loading failed in the first isolated launch. | Start the Codex adapter from the observed protocol, then verify the installation route. Do not copy invocation trust bypass into a default installer. |
| S-05 | [Pilot task skill](/Users/zhangbowen/Projects/pinyin-vsr-research/tasks/2026-09-05-research-workflow-pilot/harness/templates/.agents/skills/research-task/SKILL.md) | Contract/result/handoff ownership and bounded closeout without Trellis. | Seed the future host-neutral local skill. |
| S-06 | [research-experiment skill](/Users/zhangbowen/Projects/agent-skills-private/skills/research-experiment/SKILL.md) | Scientific open/close gates, amendments, negative results, and current Trellis coupling. | Reuse scientific requirements; keep rctl lifecycle plumbing separate. |
| S-07 | [Result validator](/Users/zhangbowen/Projects/agent-skills-private/skills/research-experiment/scripts/validate-result.py) | Structural field checks and candidate-lineage checks; no general evidence-content verification. | Separate structural validation from command execution and review. |
| S-08 | [research-project-setup skill](/Users/zhangbowen/Projects/agent-skills-private/skills/research-project-setup/SKILL.md) and [research control entry template](/Users/zhangbowen/Projects/agent-skills-private/skills/research-project-setup/assets/research-control/README.md) | Static scientific controls and task-local live state have distinct owners. | Preserve research knowledge ownership and local project paths. |
| S-09 | [research-computation skill](/Users/zhangbowen/Projects/agent-skills-private/skills/research-computation/SKILL.md) | Real execution, separate validation, and bounded computation-backed claims. | Define honest verification source labels. |

The Mempal search also returned earlier Quest-retirement and Trellis-pilot decisions. These describe past changes, not authorization to migrate the current live project. The user identified contract, verification, and state reminders as the main priorities, then requested this development-ready document package and corrected the project spelling to `rctl`.

Local source links deliberately point to the inspected originals. They may be unavailable on another machine; the decision-relevant observations above are self-contained. No private metrics, session transcripts, or global configuration have been copied into this project.

## Online documentation retrieval

The following commands were actually attempted through smart-search during preparation:

```sh
smart-search doctor --format json
smart-search exa-search 'Codex hooks SessionStart UserPromptSubmit' --include-domains developers.openai.com --num-results 3 --format json --output /tmp/rctl-codex-hooks-search.json
smart-search fetch https://developers.openai.com/codex/hooks.md --format json --output /tmp/rctl-codex-hooks.json
smart-search fetch https://docs.astral.sh/uv/concepts/projects/init/ --format json --output /tmp/rctl-uv-projects.json
```

Doctor reported configured capabilities but a network timeout. Official-domain search timed out. Both fetches exhausted their configured Tavily/Jina/Firecrawl attempts and returned no content. Their compact outcomes are retained in [source-retrieval.json](evidence/source-retrieval.json); the temporary raw outputs are not required to use this document pack.

The official [Codex hooks](https://developers.openai.com/codex/hooks.md) and [uv project initialization](https://docs.astral.sh/uv/concepts/projects/init/) URLs are recheck targets, not successfully fetched citations from this preparation. The pilot had previously retrieved Codex documentation through smart-search and retained actual host behavior. M3 must inspect version-appropriate official documentation or actual installed host source before asserting compatibility beyond that concrete target.

## New design choices

The rctl YAML/JSON shapes, command names, phase/cycle model, local evidence observations, acceptance IDs, and narrower v0.1 scope are design decisions made for this baseline. They are not attributed to external documentation or presented as features already supplied by the existing skills. Source evidence motivates them; [SPEC](SPEC.md) defines them.
