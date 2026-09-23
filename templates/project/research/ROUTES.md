# Research Route Ledger

This file owns scoped research opportunities and investment decisions. Use
[PROBLEM_METHODS.md](PROBLEM_METHODS.md) for the full problem/method inventory.
Keep the status of a problem, a mechanism and a particular implementation distinct.
Task records own authorized execution and lifecycle; link run details rather than
copy them here.

## Status Vocabulary

- `candidate`: an unresolved opportunity under consideration; no run is implied.
- `promising`: a bounded useful effect warrants a stated next question, not a general superiority claim.
- `stopped`: a particular implementation or setting does not justify more investment under its declared endpoint.
- `parked`: the route ran or partly ran and stopped for a stated external or unresolved condition that could change.
- `not_executed`: the route was planned with a gate but never ran. Absence of evidence, not evidence of failure.
- `refuted`: evidence contradicts the explicitly scoped claim; state that claim and the decisive evidence.

An unrun mechanism is not a failed mechanism. Failing a small promotion gate can
justify stopping an implementation without refuting the broader research idea.

## Reuse Rule

Read related mechanisms, their tested scope, actual control versions and information
conditions before proposing new work. A renamed implementation does not reset its
evidence or budget. Explain the unanswered question, substantive difference or
applicable reopen condition and the decision new evidence would change. Shared-
information ablations and guided-control ties do not decide every complete method.
Use [comparison-design.md](guidelines/comparison-design.md); a different unanswered
comparison may be a candidate without overturning an earlier scoped stop. Listing
that candidate does not authorize execution.

## Routes

### R01 · <route name>

- **Also called**: <every other name this mechanism has appeared under — plan names, campaign IDs, method names from the literature>
- **Mechanism**: <one or two sentences describing what was actually done, in mechanism terms a differently named proposal could still match>
- **Target problem**: <problem ID or governing question>
- **Tested scope**: <implementation, population, baseline version, information condition and primary endpoint; or explicitly unrun>
- **Status**: `<candidate|promising|stopped|parked|not_executed|refuted>` · <YYYY-MM-DD>
- **Decision and reason**: <bounded finding or unresolved opportunity; preserve observed positives and negatives>
- **Does not decide**: <broader mechanism or problem claim outside this evidence>
- **Next evidence / Reopen if**: <specific observation that would change the decision; listing it grants no execution budget>
- **Evidence**: <path to a durable tracked artifact, relative to the project root>

## Update Policy

Update an opportunity or scoped implementation decision when evidence changes.
Keep per-run and per-seed accounting in tasks/runner records. State the scope of
each decision rather than applying one implementation's stop to every method for
the same problem.

Do not rewrite an entry's closing evidence. If later evidence overturns it, add
a new entry and link back from both.

New entries must point at tracked evidence. A pointer into ignored run storage is not durable and will outlive the file it names.
