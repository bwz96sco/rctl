---
name: research-rapid-test
description: Quickly test the most promising empirical claim from research ideation or idea evaluation. Use for output-driven pilots, fastest-path feasibility tests, and early promote-or-drop decisions with minimal preparation. Formal reproduction, comprehensive ablation, and publication validation belong to later work.
---

# Research Rapid Test

Optimize for useful experimental signal per hour. Give the idea its strongest
plausible inexpensive test, look at the actual result, and decide whether to
invest further. Preparation is a cost, never the deliverable.

## Keep the trial connected to its task

In an rctl-managed project (an existing `.rctl/project.json`), read `research-task`'s
`references/rapid-trials.md` before launch unless the user chooses note-only
tracking. Register the six-line bet below with links to the trial note and outputs;
use explicit task context when selected reminders are absent. Registration stays
within the pilot's preparation allowance and adds no formal reproduction gate.

Outside a managed project, keep the one-note workflow; do not install rctl merely
to run a pilot. Discussion and read-only inspection do not require a new task.

## Enter from the idea, not from an infrastructure plan

Read the supplied candidate/evaluation brief and any directly relevant prior
result. Extract the proposed mechanism, its expected advantage, and the empirical
uncertainty most likely to change the decision. Existing evaluation paperwork is
input, not a prerequisite to testing a clear user-supplied idea.

When entering from an evaluated selection, retain the original `C#`, `decision.md`
path, and selected brief in the trial note. A later formal experiment keeps that
lineage even when the decision's first next owner was `research-rapid-test`.

Respect a specified candidate. If selection is delegated, choose the candidate
with the best combination of plausible upside, observable difference, and cheap
implementation. Explain that choice in two sentences; avoid another scoring
framework or literature-review cycle. Test one bet at a time.

For an already tested idea, identify what this trial changes. Do not reset a
failed attempt's budget by renaming it or starting another preparation task.

## Default pace

Use the user's limits when supplied. Otherwise adopt these adjustable defaults
and announce them before executing:

| Item | Default |
| --- | --- |
| Preparation before launching the first meaningful test | At most 20 minutes |
| First interpretable method-versus-control result | Aim for 2 hours or less |
| Total time on one idea | 4 hours, including setup, retries, debugging and analysis |
| Initial material | 1–3 favorable cases for a mechanism test; size an opportunity/performance screen for its decision |
| Method revisions after the first result | One concrete rescue attempt |

Carry consumed time and calls across resumptions. Choose a small call/compute
allowance within existing authorization before batch work. If the mechanism
cannot fit the default window, use a smaller lower-cost version or drop it for
now. A longer window needs an actual user-supplied budget; announcing an extension
or resuming tomorrow does not grant one.
At the limit, stop new work and make a decision from what exists. Do not turn
an unavailable measurement into a scientific refutation.

## State the bet, then run it

Before coding, use the [scale rationale](#size-the-test-for-its-decision) to choose
counts, then put these six short lines in the conversation and the trial note:

1. **Bet:** The idea's actual additional processing step should cause this result.
2. **Best opportunity:** The case/property where it has the strongest reason to help, with case/structure and repeat counts.
3. **Main comparison:** The fixed control version/source, what each arm does, and which generated information remains private to each arm.
4. **Visible win:** The concrete output difference that would justify more work.
5. **Implementation shortcut:** The smallest runnable version and reused assets.
6. **Stop:** Time/call allowance, planned batches, what would justify the single rescue attempt, and when evidence would remain inconclusive.

A method needs an executable difference, not merely a new name or an action log.
For pipeline benefit, compare complete methods from their raw inputs and keep
generated intermediate records inside each arm. Sharing them tests a conditional
ablation. Give assisted or otherwise enhanced controls separate versions and
retain the original comparison. Baseline bug fixes identify affected pairs and
preserve earlier outcomes.

Separate development feedback from final evaluation; cases used to tune either
arm remain development cases. When choosing controls or interpreting results,
use applicable project guidance such as `research/guidelines/comparison-design.md`
where present. The pilot remains usable without that file or an rctl installation.

Use cases chosen for a real opportunity: known control failures, cases matching
the proposed mechanism, or a small constructed example that exposes it. Favorable
selection is appropriate for this development test; record it. Start with the
strongest plausible version of the idea, not an arbitrary weak implementation.
Simplify the setting when that preserves the mechanism. If a manual component
stands in for an unbuilt step, state exactly which part was tested.

Run the intervention and a credible inexpensive control. Prefer an existing
runnable control; a simple implementation or labeled approximation is enough to
start. Full reproduction of several published baselines can wait. Give the arms
comparable starting inputs, tools and total effort; record material differences.
Controls may independently discover the same strategy. Exact token equalization
and publication-level power analysis must not consume the pilot. If the control saves
an analysis call, let it use the allowance for its own review or improvement.

Reuse available data, scripts, models and evaluators. Write disposable code in a
fresh scratch/output directory. A tiny example or direct inspection can establish
the observable difference; no general framework is needed. Add a preparatory
check only if you can name the imminent failure it detects and the action it
would change. If setup consumes its allowance, simplify, substitute an available
component, or stop that direction for now.

## Size the test for its decision

Before fixing the run count, add a short scale rationale to the existing bet.
Keep it within preparation; about 5–10 minutes is usually enough:

- Name the decision: find an opportunity, demonstrate a mechanism on favorable
  cases, or screen a final-performance gain. A few favorable cases support a
  mechanism story; population claims need broader evidence.
- Count independent cases/structures separately from repeats. Use repeats to
  probe run variability and new cases for coverage. Keep controls and input
  conditions comparable across batches so evidence can accumulate.
- Estimate the opportunity rate and plausible repair/regression or effect size
  from compatible evidence, or state a range of assumptions. Check whether the
  proposed scale is likely to expose the signal: for independent cases, missing
  all failures has probability `(1-f)^n`; expected gains/regressions or a simple
  sensitivity range often suffice. Use direct coverage reasoning for constructed
  or deterministic tests rather than inventing a population failure rate.
- Check that cases × arms × repeats fit the call/time allowance, including
  screening, fresh controls, retries and review. A control draw used to select a
  failure is admission evidence; use fresh draws for the treatment comparison.
- Declare which outcomes support benefit, a tested implementation failure,
  no observed opportunity, or insufficient information. Plan any next batch
  within the allowance before seeing results; a small first batch is an
  observation point unless its stopping rule is justified for the decision.

If the useful scale does not fit, narrow the question, target an evidenced
opportunity or propose a larger allowance. Preserve a supplied budget. A noisy
small tie or a pool without control failures cannot establish method failure.

## Inspect the result and decide

Show at least one complete input → changed step → output comparison. Inspect the
claimed benefit itself: did it fix the intended behavior, improve the requested
quantity, or merely change a proxy? Check an apparent win for an obvious broken
control, changed problem, or extra answer information. Save all tried outcomes,
including failures and any manual assistance. A model's success claim is not
an observation.

Report the declared primary endpoint, paired gains/regressions and material costs;
keep diagnostic metrics and secondary gains distinct. A single-control screen
cannot establish method benefit. Bound a tie by its control version and assistance:
a shared-information ablation does not test the production of that information.

Record the evidence conclusion separately from the spending decision. No observed
opportunity leaves the intervention untested; inadequate precision is inconclusive.
Both can justify stopping expenditure without rejecting the method scientifically.
Make one of these spending decisions and act on it:

- **PROMOTE:** A concrete useful effect is visible and has a plausible connection
  to the mechanism. If a cheap repeat or nearby case could expose a lucky result,
  use it within the same allowance. Retain the strongest case, minimal working
  code, and the next uncertainty worth testing. This supports focused follow-up
  within authorization, not a general performance claim or a new spending allowance.
- **ITERATE ONCE:** A specific observed failure has a specific inexpensive fix.
  State “I will change X; then Y should happen on this case,” apply it and rerun
  the affected comparison within the same total allowance. “Try a bigger model,”
  “more prompts/data,” or “maybe the implementation is weak” alone is not a plan.
- **DROP:** No useful effect and no concrete affordable fix, an unsuccessful
  rescue, or setup cost outweighs plausible upside. Record the result and stop
  spending. Infrastructure-only failure means untested/dropped for now, not
  “the hypothesis is false.” Preserve a specific reopening hook only if one exists.

Finish a rescue with PROMOTE or DROP; do not leave the direction indefinitely
“pending more preparation.” When authorized to screen several ideas, move to the
next existing candidate within the shared budget instead of defending sunk costs.

## Minimal output and later handoff

Keep one `rapid-test.md` beside the idea, plus the script/command and raw outputs
needed to inspect the actual comparison. The note holds the six-line bet, small
result table, time/calls spent, diagnosis, and decision. Update it in place across
the one rescue. Report the effect and decision first; preparation counts are not
research progress. Put qualifications together under Limitations.

This exploratory skill precedes `research-experiment`. Full baseline reproduction,
exhaustive coverage, factorial ablations, multi-engine validation, formal proofs,
hash/replay packs and independent review campaigns are not default prerequisites.
Bring in a specific check only when an observed problem makes the pilot otherwise
misleading. Escalate promising evidence to a scoped formal experiment when that
investment is requested or already authorized; freeze the method and establish
stronger comparability there.

Read the shared [computation checks](../research-theory/references/computation-checks.md)
only when a numerical-validity question is unresolved. Reuse the trial's evidence
and allowance; the checks stay within this trial and need no separate report.

For a managed trial, use `research-task`'s rapid-trial reference for checkpoints,
amendments, late registration and verification/closure. Link the inspected note
and raw evidence from the native result, preserving costs and conclusions across
recovery. Update established project guidance with the scoped result and its
evidence. A negative finding can complete the task; preliminary tracking never
upgrades the scientific claim or authorizes another run.
