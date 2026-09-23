# Research Problems and Method Opportunities

This file owns the current project-level problem/method overview. PROGRAM owns
the objective, BASELINES the comparison identities, and ROUTES scoped investment
decisions. Tasks own execution and lifecycle; linked notes hold detailed analysis.

## Governing Question

<State the outcome the project aims to improve and how it will be measured.>

## Problems

| Problem ID | Failure or scientific question | Evidence and population | What remains unresolved |
|---|---|---|---|
| `<problem-id>` | `<concrete problem>` | `<observed, constructed, hypothesized or unresolved; source and scope>` | `<question that new evidence would answer>` |

Distinguish demonstrated failures from hypotheses, evaluator defects and public
ambiguity. A stopped implementation does not erase the problem it targeted.

## Method Opportunities

| Method ID | Target problem | Additional operation | Evidence and feedback required | Actual coverage | Next decision |
|---|---|---|---|---|---|
| `<method-id>` | `<problem-id>` | `<concrete mechanism>` | `<available evidence, assumptions and any supervision>` | `<unrun, partial operation, conditional comparison or complete method; source>` | `<what observation would justify further work or stopping>` |

Use stable IDs where useful; link detailed literature/source notes. A related
operation is not a full reproduction. Methods learned from development labels
need an explicit held-out evaluation boundary.

## Current Decision

<Name the unresolved choice and the specific comparison or evidence that would
change it. Keep candidates under consideration separate from authorized runs.>

Before selecting a comparison, read [comparison-design.md](guidelines/comparison-design.md)
and the actual control versions in [BASELINES.md](BASELINES.md). Reconcile retained
evidence before repeating experiments merely to harmonize historical names.

## Update Policy

Update problem existence, method coverage and unresolved questions when evidence
changes. Preserve links to bounded positive/negative findings. Keep live progress
in task/runner records and route decisions in [ROUTES.md](ROUTES.md).
