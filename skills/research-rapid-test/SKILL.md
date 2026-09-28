---
name: research-rapid-test
description: Resolve a research investment uncertainty with a bounded first observation. Use for fast method pilots, measurement checks, or empirical contrasts with minimal preparation. Formal reproduction, comprehensive ablation, and publication validation belong to later work.
---

# Research Rapid Test

Optimize for decision-relevant evidence per hour. Obtain an observation that
distinguishes the important possibilities, inspect it, and decide whether further
investment is justified. Preparation is a cost, never the deliverable.

## Keep the trial connected to its task

In an rctl-managed project (an existing `.rctl/project.json`), read `research-task`'s
`references/rapid-trials.md` before launch unless the user chooses note-only
tracking. Register the six-line bet below with links to the trial note and outputs;
use explicit task context when selected reminders are absent. Registration stays
within the pilot's preparation allowance and adds no formal reproduction gate.

Outside a managed project, keep the one-note workflow; do not install rctl merely
to run a pilot. Discussion and read-only inspection do not require a new task.

## Enter from the question and proposed observation

Read the supplied question, idea/evaluation and directly relevant prior result. Identify the
question, possible contribution, intended reader, strongest prior or rival, and
the uncertainty most likely to change investment. Reuse an existing affirmative
investment case. At direct entry, explain why resolving this uncertainty matters,
what evidence makes the investigation credible, and what observation distinguishes
the possibilities. Put this in the existing bet; evaluation files are not a
prerequisite for a user-supplied question or idea. A clear user request to test a weak bet can
still be honored: state the concern and scope rather than inventing an endorsement.

Carry the active user goal and selected research object into that bet. A smaller
test must preserve the relevant distinction and explain how its result informs
the parent claim. For example, testing a measure's validity can be a small version
of a measurement study; replacing it with a repair-accuracy comparison changes
the question. If the proposed reduction loses the scientific point, return to
selection instead of launching on the strength of available cases or low cost.

For a question-origin trial, retain its statement or existing question reference
and specify the actual observation and allowance here; no solution portfolio or
invented `C#` is needed. Question formation belongs to `$research-question` if that
is still the requested work, rather than forcing an experiment to complete it.
For an evaluated investigation candidate, retain the original `C#`, `decision.md`
path and selected brief. A later formal experiment keeps that lineage even when
the decision's first next owner was `research-rapid-test`.

Respect a specified candidate. If selection is delegated, choose a worthwhile
question with a discriminating observation and available evidence. Explain the
choice briefly; do not treat absence of a fatal objection as sufficient upside.
If no bet has a defensible next observation, report that rather than launch a
comparison merely because it is cheap. Test one bet at a time.

For an already tested idea, identify what this trial changes. Do not reset a
failed attempt's budget by renaming it or starting another preparation task.

## Default pace

Use the user's limits when supplied. Otherwise adopt these adjustable defaults
and announce them before executing:

| Item | Default |
| --- | --- |
| Preparation before launching the first meaningful test | At most 20 minutes |
| First interpretable observation resolving the declared uncertainty | Aim for 2 hours or less |
| Total time on one idea | 4 hours, including setup, retries, debugging and analysis |
| Initial material | Size for the decision; a few favorable cases can test a property, while population claims need broader evidence |
| Method revisions after the first result | One concrete rescue attempt |

Carry consumed time and calls across resumptions. Choose a small call/compute
allowance within existing authorization before batch work. If the investigation
cannot fit the default window, isolate a pivotal uncertainty or drop it for now.
Any smaller version must preserve the premise it claims to test.
A longer window needs an actual user-supplied budget; announcing an extension
or resuming tomorrow does not grant one.
At the limit, stop new work and make a decision from what exists. Do not turn
an unavailable measurement into a scientific refutation.

## State the bet, then run it

Before execution, use the [scale rationale](#size-the-test-for-its-decision) to choose
counts, then put these six short lines in the conversation and the trial note:

1. **Question and bet:** The contribution, reader value, and key uncertainty; for a method, the added operation and why it could help.
2. **Evidence opportunity:** The case/property that can discriminate the possibilities, with units/coverage and repeat counts.
3. **Main comparison:** The relevant fixed control, existing measure, or rival explanation; information and evaluation boundaries.
4. **Decision-changing observation:** The concrete result that would justify more work, and the result that would weaken the bet.
5. **Minimal investigation:** Reused assets and the smallest implementation, audit, or analytic contrast that preserves the tested premise.
6. **Stop:** Time/call allowance, planned batches, what would justify the single rescue attempt, and when evidence would remain inconclusive.

Match the evidence to the declared contribution. A measurement test examines
independently judged sensitivity, invariance, and useful decisions against simpler
measures. An explanatory study contrasts rival predictions within a defined
population or domain; a causal claim needs identification. Synthetic examples can
establish a property or mechanism, not natural prevalence. Require a downstream
performance gain when that is the claim, not as a universal pilot endpoint.

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

Use cases chosen for a real opportunity: known control failures, contrasts between
competing explanations, meaningful measurement changes/invariances, or a small
constructed example exposing the tested property. Favorable selection is appropriate
for a mechanism demonstration; record it and keep its population limits explicit.
Start with a plausible version of the idea, not an arbitrary weak implementation.
Simplify the setting when that preserves the mechanism. If a manual component
stands in for an unbuilt step, state exactly which part was tested.

For an intervention claim, run the method and a credible inexpensive control.
Prefer an existing runnable control; a simple implementation or labeled approximation
is enough to start. For another claim, execute its specified discriminating contrast.
Full reproduction of several published baselines can wait. Give compared arms
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

- Name the decision: find an opportunity, demonstrate a mechanism, validate a
  measurement property, distinguish explanations, or screen a performance gain.
  A few favorable cases can establish a property; population claims need broader evidence.
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

Show a complete input → operation or contrast → observation → inference chain.
Inspect the claimed finding itself: did it resolve the uncertainty, improve the
requested quantity, or merely change a proxy? Check an apparent win for an obvious
broken control, changed problem, or extra answer information. Save all tried outcomes,
including failures and any manual assistance. A model's success claim is not
an observation.

Report the declared primary endpoint, relevant paired gains/regressions and costs;
keep diagnostic metrics and secondary gains distinct. A single-control screen
cannot establish method benefit. Bound a tie by its control version and assistance:
a shared-information ablation does not test the production of that information.

Record the evidence conclusion separately from the spending decision. No observed
opportunity leaves the intervention untested; inadequate precision is inconclusive.
Both can justify stopping expenditure without rejecting the method scientifically.
Make one of these spending decisions and act on it:

- **PROMOTE:** An independently supported useful finding or capability is visible
  and justifies a specific next investigation. For a method, connect the effect
  to its mechanism. If a cheap repeat or nearby case could expose a lucky result,
  use it within the same allowance. Retain the strongest evidence, any working
  implementation, and the next uncertainty worth testing. This supports focused follow-up
  within authorization, not a general performance claim or a new spending allowance.
- **ITERATE ONCE:** A specific observed failure has a specific inexpensive fix.
  State “I will change X; then Y should happen on this case,” apply it and rerun
  the affected comparison within the same total allowance. “Try a bigger model,”
  “more prompts/data,” or “maybe the implementation is weak” alone is not a plan.
- **DROP:** No useful finding or capability and no concrete affordable fix, an unsuccessful
  rescue, or setup cost outweighs plausible upside. Record the result and stop
  spending. Infrastructure-only failure means untested/dropped for now, not
  “the hypothesis is false.” Preserve a specific reopening hook only if one exists.

Finish a rescue with PROMOTE or DROP; do not leave the direction indefinitely
“pending more preparation.” When authorized to screen several ideas, move to the
next existing candidate within the shared budget instead of defending sunk costs.

## Minimal output and later handoff

Keep one `rapid-test.md` beside the idea, plus any scripts/commands and raw evidence
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
