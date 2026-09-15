---
name: research-rapid-test
description: Quickly test the most promising empirical claim from research ideation or idea evaluation. Use for output-driven pilots, fastest-path feasibility tests, and early promote-or-drop decisions with minimal preparation. Formal reproduction, comprehensive ablation, and publication validation belong to later work.
---

# Research Rapid Test

Optimize for useful experimental signal per hour. Give the idea its strongest
plausible inexpensive test, look at the actual result, and decide whether to
invest further. Preparation is a cost, never the deliverable.

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
| Initial material | 1–3 favorable, informative cases |
| Method revisions after the first result | One concrete rescue attempt |

Carry consumed time and calls across resumptions. Choose a small call/compute
allowance within existing authorization before batch work. If the mechanism
cannot fit the default window, use a smaller lower-cost version or drop it for
now. A longer window needs an actual user-supplied budget; announcing an extension
or resuming tomorrow does not grant one.
At the limit, stop new work and make a decision from what exists. Do not turn
an unavailable measurement into a scientific refutation.

## State the bet, then run it

Before coding, put these six short lines in the conversation and the trial note:

1. **Bet:** The idea's actual additional processing step should cause this result.
2. **Best opportunity:** The case/property where it has the strongest reason to help.
3. **Main comparison:** What the control does and what the intervention does.
4. **Visible win:** The concrete output difference that would justify more work.
5. **Implementation shortcut:** The smallest runnable version and reused assets.
6. **Stop:** Time/call allowance and what would justify the single rescue attempt.

A method needs an executable difference, not merely a new name or an action log.
For a pipeline-benefit question, compare raw-input ordinary processing with the
pipeline. Keep the pipeline's generated intermediate records inside its arm.
Giving those records to both arms tests a downstream organizational ablation;
run that only when it is the question, usually after a main-effect signal exists.

Use cases chosen for a real opportunity: known control failures, cases matching
the proposed mechanism, or a small constructed example that exposes it. Favorable
selection is appropriate for this development test; record it. Start with the
strongest plausible version of the idea, not an arbitrary weak implementation.
Simplify the setting when that preserves the mechanism. If a manual component
stands in for an unbuilt step, state exactly which part was tested.

Run the intervention and a credible inexpensive control. Prefer an existing
runnable control; a simple implementation or labeled approximation is enough to
start. Full reproduction of several published baselines can wait. Give the arms
comparable effort and record material differences; exact token equalization or
statistical power calculations must not consume the pilot. If the control saves
an analysis call, let it use the allowance for its own review or improvement.

Reuse available data, scripts, models and evaluators. Write disposable code in a
fresh scratch/output directory. A tiny example or direct inspection can establish
the observable difference; no general framework is needed. Add a preparatory
check only if you can name the imminent failure it detects and the action it
would change. If setup consumes its allowance, simplify, substitute an available
component, or stop that direction for now.

## Inspect the result and decide

Show at least one complete input → changed step → output comparison. Inspect the
claimed benefit itself: did it fix the intended behavior, improve the requested
quantity, or merely change a proxy? Check an apparent win for an obvious broken
control, changed problem, or extra answer information. Save all tried outcomes,
including failures and any manual assistance. A model's success claim is not
an observation.

Make one of these decisions and act on it:

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

Consult `research-computation` only when a concrete numerical-validity question
needs it. Reuse the trial's existing evidence and allowance; this is not another
preparation phase or a required separate computation report.

Follow any required workspace bookkeeping in its smallest permitted form. Do not
silently relax an existing frozen task or consume its old allowance: keep rapid
trials separate and retain their preliminary status. A project's explicitly
authorized rapid-screening exception can use this one-note workflow directly.
