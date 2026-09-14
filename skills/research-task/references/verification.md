# Verification and closeout

Use the current agreement's criteria and [Task files](task-files.md) when preparing
the result and reviews. Generate analysis artifacts before verification; declared
local checks validate existing evidence. Include check scripts, helpers, and
preexisting data in command inputs. New remote jobs need their own authority.

Write the current revision's result with outcome, evidence, deviations, next action,
and limitations. Distinguish computed observations, parsed evidence, and hypotheses.
For an aligned task, assess only the declared test and honor its non-claim scope.
Inspect cited content before supplying a review verdict, reviewer source, rationale,
and all required references. An operator-only criterion needs an operator judgment;
reviewer labels are declared sources, not authenticated identities.

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
