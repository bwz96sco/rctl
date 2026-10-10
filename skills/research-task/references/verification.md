# Verification and closeout

Use the current agreement's criteria and [Task files](task-files.md) when preparing
the result and reviews. Generate analysis artifacts before verification; declared
local checks validate existing evidence. Include check scripts, helpers, and
preexisting data in command inputs. New remote jobs need their own authority.

Write the current revision's result with outcome, evidence, deviations, next action,
and limitations. Distinguish computed observations, parsed evidence, and hypotheses.
For an aligned task, assess only the declared test and honor its non-claim scope.
For a declared target-relevance criterion, compare the actual workload, platform
and operating conditions with the scenario brief; explain what the result
establishes for that target. A runnable artifact alone does not establish this
mapping. If the link is unresolved, narrow the conclusion or leave the criterion
unresolved according to its requirement. A bounded component or feasibility task
may close with that finding; apply the agreed criteria without adding a new gate.
Inspect cited content before supplying a review verdict, reviewer source, rationale,
and all required references. An operator-only criterion needs an operator judgment;
reviewer labels are declared sources, not authenticated identities.

For paper-directed tasks, the required publication-purpose review judges local
delivery and publication consequence separately. Inspect the cited brief and
primary evidence: which claim/evidence obligation is supported, narrowed or still
unresolved, and does this justify the proposed next investment? Put that reasoning
in Outcome and Next action and in the review rationale. A goal link, successful
command or completed headings do not satisfy this judgment. A negative result may
pass an honest-assessment requirement and close locally while the paper obligation
remains unsupported. Missing reasoning leaves the required review unresolved;
positive expansion requires a defensible claim or bounded repair. Review the
existing criteria rather than retroactively requiring a positive scientific win.

For contracts declaring `goal_contribution`, supply `goal_impact` on the named
review criterion: claim effect and evidence-based reason, remaining gap, next
investment decision and reason (see Task files). In the goal-review source
increment these fields are mechanically required, and missing review entries
still produce unknown. Verify field completeness separately from adequacy of the
judgment. Check status for this reviewed decision and currentness before planning
continuation; a local pass with `stop` completes the task without authorizing more
of the stopped investment. Old accepted contracts retain their original criteria.

Run `rctl verify TASK --reviews FILE`, omitting reviews for command-only criteria.
Inspect every criterion and its logs as needed. Nonzero verification can still save
a report; use status after an interruption or uncertain write. Correct the named
failure within the agreement or leave work unresolved, then explicitly verify again.
Changed results/evidence, amendments, and reopened cycles require fresh verification.
An unfavorable finding does not justify expanding the budget or weakening criteria.

Checkpoint any final handoff before closing; `checkpoint` only accepts active tasks.
Close only when the latest report passes and remains applicable. Scientific
`not_supported` and bounded `inconclusive` results can close. A missing judgment or
unknown check remains unresolved; an older pass cannot replace a later failed report.
`reopen --reason TEXT` starts a new cycle; `cancel --reason TEXT` stops active work
without verified completion.

Promote established findings to existing project research files at closeout, keeping
their scope and evidence links. Task progress and execution history remain with the
task. To pause instead, checkpoint a concrete next action, blockers, last verified
progress, evidence locations, and unresolved work. The source handoff preserves the
detail that a bounded reminder may omit.
