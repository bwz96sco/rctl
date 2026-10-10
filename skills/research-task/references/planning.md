# Planning and history reuse

Before selecting an application setting, proposing an experiment or its contract,
or materially changing direction, start with `research/PROBLEM_METHODS.md` where
present and PROGRAM.md's Goal and Current guidance. Then inspect related ROUTES
entries and their linked evidence;
read other PROGRAM sections when the question touches their criteria or constraints.
Use the project's comparison guidance and baseline registry when choosing controls
or interpreting results. Explain what prior work answered, what remains unanswered,
the substantive difference or satisfied reopen condition, and which decision the
new result would change. Match mechanisms across names. If no related route is
found, name the sources checked. Put the reasoning in the proposal and the
contract's Question/Scope; use domain skills to assess scientific adequacy.

For applied work, carry the target setting from the project's scenario brief into
Question/Scope and Question alignment, and record a setting change with its reason
before dependent work. The project's research guidance says what a good target
mapping, contribution and evidence obligation are; rctl records them.

When PROGRAM has a completed Goal, declare `goal_contribution` as in
[Task files](task-files.md#goal-contribution-and-review). Before authoring the
contract, run `rctl task list` and read related goal decisions. A task resuming a
stopped or adjusted obligation names that task and the new evidence or bounded
reason in Scope.

Write each contract's exclusions for its own question. Do not copy an earlier
task's or plan's boundaries into a contract whose question needs that work; for
example, a selection round's "no simulator or model run" does not bind a later task
that must build or run an evaluator.

A comparison retains named control versions, information boundaries and its
primary outcome in the contract; use the domain skill and, where present,
`research/guidelines/comparison-design.md` for scientific design. A scoped
implementation stop does not close every method for the same problem. Each
acceptance criterion names evidence, a command or review method, and a failure
that changes the next action.
A different scientific question belongs in a new task; material changes to an
active agreement require `amend TASK --reason TEXT` before dependent work.

When a task isolates one part of a broader question, use the four-field Question
alignment section in [Task files](task-files.md). Snapshot the governing mechanism,
the increment tested, and the broader conclusion it does not decide, using one
short sentence per relationship field. When target relevance or alignment adequacy
affects the claim, declare a review criterion citing the governing source and result
through the task-relative evidence convention. It should judge the case's mapping
to the target and the conclusion it supports. The declaration is part of the
agreement; structural validation does not judge its scientific adequacy.

`rctl context` without selection supplies bounded project guidance. Read sources
when relevant details are absent, ambiguous, or truncated. Keep current corrections
and their evidence/scope in PROGRAM.md's `## Current guidance`, and link superseding
route conclusions in ROUTES.md while retaining old evidence. Update established
corrections when learned, independently of task closeout. Project guidance is
reported intent, separate from task acceptance. Edit `## Goal` only for a real goal
change: any non-whitespace edit marks every retained goal decision stale.
