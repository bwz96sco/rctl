# Lightweight rapid trials

Use this route when `research-rapid-test` or project rules call for task tracking.
It preserves a small experiment's question, limits and continuation without
requiring the formal `research-experiment` workflow. Existing governed studies
retain their accepted requirements. Discussion and bounded mechanical edits may
stay inline.

## Register the existing bet

Use one task per bounded empirical question, not one per model call or an
open-ended task for the entire research direction. Derive its scope from the
user's request and inspected related evidence. Same-question recovery stays in
the existing task. Changed comparison, metric, budget or stop rules require an
amendment; a different scientific question belongs in a linked new task.
Neither operation renews consumed allowances or supplies missing authorization.

Create the task with `task new` and use the native format in
[Task files](task-files.md). Reuse the trial note's six-line bet:

- **Question:** mechanism, related result, remaining uncertainty and the decision
  this comparison changes. For a derived question, use Question alignment to
  identify its governing source, actual test and non-claim boundary.
- **Scope:** control version/intervention, information conditions, cases, primary
  endpoint and decision rule from the bet; link `rapid-test.md` and the fresh
  output root for implementation detail. Use the project's comparison guidance
  where present when deciding the scientific scope.
- **Constraints / Stop conditions:** feedback boundaries, actual authorized
  time/call limits, retry allowance and stopping rule, including previous spend.
- **Criteria:** a small evidence-based review of the actual control and information
  conditions, consumed budget, gains/regressions, failures and scoped decision.
  Use agent review where sufficient; add a command check only for a concrete
  failure that would change the next action.

Criteria should establish an honestly reported result, not require the method to
win. Do not add an operator approval, independent review campaign, clean commit,
sealed pack or comprehensive baseline reproduction merely to register a pilot.
Keep registration within the pilot's preparation allowance, usually a few minutes.
Run `contract check`, then `begin`, and read `context TASK`. Retain enough comparison
and limit detail in the contract that later note edits cannot silently change it.

When connecting an already running trial, record that registration occurred after
launch, cite the original plan and output paths, and carry forward actual spend
and deadlines. Do not rerun it or claim its earlier work was rctl-governed.

## Handoff and result

Link the task from the trial note and project orientation. An originating
discovery/selection task should link its experiment handoff without absorbing the
experiment's different question or allowance. Preserve incomplete discovery work
as incomplete rather than inventing its closure.

At a handoff, background launch, recovery or material result, save `state.md`
through `checkpoint`: actual completed/failed/pending work, cumulative time/calls,
runner/output paths, blockers and one concrete next action. Read the runner for
live counts at the user's monitoring cadence; rctl is not a second scheduler.

At the decision, write a short native result linking the inspected note and raw
evidence. Apply the existing [verification and closeout](verification.md) process
to the small declared criteria. Negative or bounded inconclusive findings may
close; an unresolved verification must not be presented as managed completion.
Keep the pilot decision distinct from authorization for a further experiment.

Update established corrections and route decisions in the project's guidance
files when learned, with evidence and scope, so reminders remain current. Live
progress stays in the handoff and runner. Task creation does not select a host
session: use explicit `context TASK` when selected reminders are absent.
