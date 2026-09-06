# Baseline Registry

This file owns comparable baseline contracts. A remembered value or result without its full evaluation contract remains `pending_audit` or `legacy_unverified`, never `accepted`.

## Status Vocabulary

- `accepted`: evidence supports every required field and comparison on the named evaluation surface.
- `pending_audit`: evidence may exist, but one or more contract fields remain unresolved.
- `legacy_unverified`: historical value retained for provenance but not for comparison.
- `rejected`: evidence was inspected and does not satisfy the named contract.

## Evaluation Surfaces

| Surface ID | Dataset or population | Split or protocol | Metric contract | Comparability notes |
|---|---|---|---|---|
| `<surface-id>` | `<dataset/population>` | `<split/protocol>` | `<metric, unit, aggregation, direction>` | `<required preprocessing or exclusions>` |

## Baselines

| Baseline ID | Surface ID | Training data | Initialization | Evaluation contract | Result | Evidence | Status |
|---|---|---|---|---|---|---|---|
| `<baseline-id>` | `<surface-id>` | `<named data or unresolved>` | `<named source or unresolved>` | `<protocol and metric contract>` | `not recorded` | `<artifact reference or pending audit>` | `pending_audit` |

## Acceptance Rule

Accept a baseline only when training data, initialization, evaluation surface, metric contract, result, and durable evidence are all named and mutually consistent. Preserve conflicting or incomplete historical values as non-comparable evidence.

## Update Policy

Add or change rows only from durable evidence. Record active experiment execution and task-local outcomes in the project's task system, not here.
