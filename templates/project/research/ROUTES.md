# Research Route Ledger

This file owns mechanism-level directions that are refuted, parked, or not
executed: what was tried or planned, what closed or stopped it, and what would
justify trying it again. Read it before proposing any new direction. Keep run
detail, metrics tables, and task status out of this file and link to them
instead.

## Status Vocabulary

- `refuted`: the route ran and failed a predeclared gate. The killing evidence is named.
- `parked`: the route ran or partly ran and stopped for a stated external or unresolved condition that could change.
- `not_executed`: the route was planned with a gate but never ran. Absence of evidence, not evidence of failure.

Never record a `not_executed` route as `refuted`. They call for opposite responses.

## Reuse Rule

A new candidate whose mechanism matches a listed route must cite the entry and argue its `Reopen if` condition explicitly. A candidate that cannot meet the condition is dropped before it consumes budget. Match on mechanism, not on name: read `Also called` and `Mechanism` before concluding a candidate is new.

## Routes

### R01 · <route name>

- **Also called**: <every other name this mechanism has appeared under — plan names, campaign IDs, method names from the literature>
- **Mechanism**: <one or two sentences describing what was actually done, in mechanism terms a differently named proposal could still match>
- **Status**: `<refuted|parked|not_executed>` · <YYYY-MM-DD>
- **Closed, parked, or stopped by**: <the result or condition, named against the gate or unresolved blocker>
- **Reopen if**: <the specific, testable condition that would justify revisiting>
- **Evidence**: <path to a durable tracked artifact, relative to the project root>

## Update Policy

Add one entry when a mechanism-level direction becomes refuted, parked, or not executed. Use one entry per direction — never per run, per seed, or per campaign stage; that is what turns a ledger into an unread registry.

Do not rewrite an entry's closing evidence. If later evidence overturns it, add
a new entry and link back from both.

New entries must point at tracked evidence. A pointer into ignored run storage is not durable and will outlive the file it names.
