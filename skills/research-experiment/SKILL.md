---
name: research-experiment
description: Gate one bounded research experiment from an rctl contract through runner evidence to a validated claim, including reproduction, baseline validation, method comparison, ablation, robustness, or problem validation.
---

# Research Experiment

Own the scientific gates for one experiment. The project-local `$research-task` skill owns
rctl lifecycle commands and machine acceptance. `contract.md` owns the bounded agreement,
`result.md` its findings, runner artifacts the execution evidence, and vault notes the
long-form interpretation. `research/` receives durable facts promoted at closeout.

For an early feasibility or promote-or-drop request, use `research-rapid-test` before
this formal workflow. A pilot is not a prerequisite for a supplied formal experiment.

## Comparison scope

Fix a named main control and distinguish published baselines from local controls.
Compare declared starting inputs, tools and total effort. Keep method-generated
records in the producing arm: sharing them tests a conditional ablation. Controls
may independently discover the same strategy within their allowance. Give assisted
or otherwise enhanced controls separate versions and retain the original results.

Separate development feedback from final evaluation. Report the primary endpoint,
regressions and costs, keeping diagnostic gains distinct. Bound conclusions by the
actual comparison; a single-control screen or conditional tie cannot settle an
untested complete-method claim. When choosing controls or interpreting results,
read applicable project guidance such as `research/guidelines/comparison-design.md`
where present for evaluation boundaries, baseline corrections and interpretation.

## Scale and claim adequacy

Before freezing counts, complete the contract's scale assessment. State the
decision/population, independent case or cluster unit, repeats, worthwhile effect
or required precision, supporting assumptions and executable budget. Use compatible
pilot evidence or a sensitivity range for unknown error rates and variance.

For statistical superiority, noninferiority or equivalence claims, justify scale
with the relevant paired/clustered uncertainty or power calculation and planned
interim rules. Separate sample-size planning data from untouched confirmation
when outcomes informed the design. For a prescribed reproduction, retain its
protocol and bound the inference; for a deterministic mechanism test, justify
coverage instead of imposing a statistical power gate.

If the budget cannot support the intended claim, narrow the claim or propose a
revised allowance before execution. Predeclare what would remain inconclusive;
no significant gain is not evidence of equivalence. A failure-selected control
draw is admission evidence, not the failed comparator for estimating benefit.
Report achieved scale, missing outcomes and uncertainty at closeout. A budget
stop can complete the task with an inconclusive result; it does not refute the
method. Count repeats and parameter variants separately from independent problems.

## Workflow

1. **Establish authority.** Use `supplied` for a user-specified experiment, protocol, reproduction, or existing method. Use `problem` for an independently supplied failure or mechanism test; no ideation artifact is required. Use `candidate` only when the experiment actually follows idea evaluation; require the selected `C#` brief in `decision.md` without changing it. If a rapid test intervened, retain that original selection and link its preliminary result; it does not replace the formal contract or verification.
2. **Open or resume the rctl task.** Read the project's `.agents/skills/research-task/SKILL.md`; initialize a missing project scaffold with `rctl init` within the authorized project root. Inspect `rctl status TASK` and the existing contract before dependent work. For a new experiment use `rctl task new tasks/SLUG --kind analysis --title TITLE`, then adapt `assets/experiment-contract.md` while preserving the generated task ID. Advice, inspection, and fixed-wording mechanical transformations may stay inline.
3. **Freeze the comparison before execution.** Fill one bounded claim contract: question, null or anti-win condition, origin, baseline and source, intervention, dataset and split, metric and evaluator, seed and aggregation policy, scale assessment, total budget, stop conditions, expected evidence, and one compact run matrix. Preserve a supplied total budget; unresolved allocation stays unresolved. Use no more than six stop/kill/relaunch/fallback rules and separate smoke checks from claim-carrying runs. Fill native frontmatter criteria with actual command inputs and evidence-based reviews, run `rctl contract check TASK` for structure, then `rctl begin TASK` before claim-carrying execution.
4. **Execute through the project runner.** Preserve actual run IDs, commands, configs, code state, environment, inputs, outputs, health evidence, retries, failures, and null results in runner-owned artifacts. Keep run-by-run history out of the frozen contract. A launch is healthy only when evidence shows real workload progress. Consult research-computation only for a concrete numerical or scientific-software validity question, reusing checks already performed; it adds no mandatory phase or separate report. Use research-task for handoff and phase.
5. **Amend explicitly.** Before dependent execution, apply research-task's `rctl amend TASK --reason TEXT` workflow for material baseline, intervention, data/split, evaluator, seed/aggregation, budget, or claim changes. Preserve prior values and the reason; mark affected run-matrix rows with their governing revision. If the scientific question changes, end the current task honestly and create a new one; do not claim successful closure merely to move on.
6. **Build the result.** Use `assets/result-template.md` for the task-local `result.md`, retaining native schema fields and the current contract revision. Record every actual run, governing revisions, evidence references, aggregation, baseline relation, comparability, deviations, supported claim, claims not made, and next action. Multiple seeds without a frozen aggregation or claim rule support seed-level observations only; the aggregate claim remains inconclusive. Use `not_supported` for a bounded negative result; unresolved work remains inconclusive or open according to the criteria.
7. **Validate and close through research-task.** Use this skill's actual installed directory as `<experiment-skill>` and run `uv run --no-project --script "<experiment-skill>/scripts/validate-result.py" TASK`; add `--decision PATH/decision.md` only for candidate provenance. Candidate validation requires the `research-idea-evaluation` package beside this package under the same skills root; supplied/problem origins need no such dependency. This checks domain structure and candidate lineage only. Inspect actual evidence, run the contract's execution checks and attributed reviews with `rctl verify`, and use `rctl close` only after current machine acceptance passes. A domain validator passing is insufficient for closure. Return minimum trust-bearing evidence with the result.
8. **Promote durable truth.** Update the project's named owners for intent, open problems/methods, resources, baseline identities and route decisions (for example `research/PROGRAM.md`, `PROBLEM_METHODS.md` where present, `INVENTORY.md`, `BASELINES.md`, or `ROUTES.md`). Keep unresolved opportunities distinct from stopped implementations. Never copy live task status, partial metrics, or execution history into these files. Vault interpretation notes link to the task and runner artifacts.

Complete when the current rctl contract governed execution, actual evidence supports the bounded result, current verification passes, and rctl close succeeds. Unresolved criteria keep the task open.

## Native files and scientific provenance

Keep rctl frontmatter unchanged: contract metadata uses schema version, task ID, title, kind,
and criteria; result metadata uses schema version, task ID, contract revision, and assessment.
Put origin type (`supplied`, `problem`, or `candidate`), origin ID, and experiment role in the
contract body. Put mechanism tested (`yes`, `no`, or `not_applicable`) and evidence details
in the result body. The templates define these fields; do not add a second contract-status
field, result summary file, or task acceptance registry.

For `problem_validation`, retain the proposed failure mechanism and a finite construction
budget. A null result refutes only the frozen operationalization. Candidate provenance
proves selection, not experimental validity. Reject unconfirmed object, domain, or contribution
pivots. A fixed-wording mechanical transformation preserves supplied wording and decisions
and adds no experimental judgment.

Existing Trellis tasks and old result summaries are historical inputs, not native acceptance.
Use research-task's workspace migration reference before explicitly migrating live work;
never synthesize an accepted rctl record from legacy status.
