# Research Route Ledger

This file owns scoped investment decisions about research directions and
implementations. [PROBLEM_METHODS.md](PROBLEM_METHODS.md) owns open questions and
candidate methods; link them when recording a decision.
Keep the status of a problem, a mechanism and a particular implementation distinct.
Task records own authorized execution and lifecycle; link run details rather than
copy them here.

## Status Vocabulary

- `promising`: a bounded useful effect warrants a stated next question, not a general superiority claim.
- `stopped`: a particular implementation or setting does not justify more investment under its declared endpoint.
- `parked`: the route ran or partly ran and stopped for a stated external or unresolved condition that could change.
- `not_executed`: the route was planned with a gate but never ran. Absence of evidence, not evidence of failure.
- `refuted`: evidence contradicts the explicitly scoped claim; state that claim and the decisive evidence.

An unrun mechanism is not a failed mechanism. Failing a small promotion gate can
justify stopping an implementation without refuting the broader research idea.

## Reuse Rule

Before proposing work, read related route entries and their linked evidence.
Match mechanisms across names: renaming does not reset evidence or budget.
Explain the unanswered question, substantive difference or applicable reopen
condition and the decision new evidence would change. An earlier stop applies
only to its tested scope. Use [comparison-design.md](guidelines/comparison-design.md)
for control and information boundaries. Listing an opportunity grants no execution
budget.

## Routes

### R01 · <route name>

- **Also called**: <every other name this mechanism has appeared under — plan names, campaign IDs, method names from the literature>
- **Mechanism**: <one or two sentences describing what was actually done, in mechanism terms a differently named proposal could still match>
- **Target problem**: <problem ID or governing question>
- **Tested scope**: <implementation, population, baseline version, information condition and primary endpoint; or explicitly unrun>
- **Status**: `<promising|stopped|parked|not_executed|refuted>` · <YYYY-MM-DD>
- **Decision and reason**: <bounded investment decision and its basis; preserve observed positives and negatives>
- **Does not decide**: <broader mechanism or problem claim outside this evidence>
- **Next evidence / Reopen if**: <specific observation that would change the decision; listing it grants no execution budget>
- **Evidence**: <path to a durable tracked artifact, relative to the project root>

## Update Policy

Use one entry per direction or scoped implementation decision, never per run,
seed or campaign stage. A new stage alone does not warrant another route entry;
keep its progress and metrics in task/runner records and link them here. State
each decision's scope rather than applying one implementation's stop to every
method for the same problem.

Do not rewrite an entry's closing evidence. If later evidence overturns it, add
a new entry and link back from both.

New entries must point at tracked evidence. A pointer into ignored run storage is not durable and will outlive the file it names.
