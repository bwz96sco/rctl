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

| Baseline ID/version | Role | Surface ID | Settings contract | Result | Evidence | Status |
|---|---|---|---|---|---|---|
| `<baseline-id/version>` | `<fixed main, published, enhanced or shared-information ablation>` | `<surface-id>` | `<source/configuration and information contract>` | `not recorded` | `<artifact reference or pending audit>` | `pending_audit` |

The settings contract identifies training/development exposure, initialization or
model configuration, prompt/policy, input packet, tools, permitted feedback,
generated/shared evidence, total budget, output selection and evaluator. Use
existing files by link and mark irrelevant fields explicitly rather than inventing
training or initialization work for a method that has none.

Keep the main control fixed across its comparison. Additional lessons, diagnostic
guidance or a changed output-selection policy create a separately named version;
retain the original comparison. A necessary bug fix identifies affected evidence
and corrected pairs. Different versions cannot be pooled under one informal name.
Use [comparison-design.md](guidelines/comparison-design.md) to interpret scope.

## Acceptance Rule

Accept a baseline on a named surface only when its identity, applicable settings,
information conditions, metric contract, result and durable evidence are mutually
consistent. Preserve conflicting or incomplete historical values as non-comparable
evidence. Shared diagnostics support a conditional comparison, not complete-method
benefit; absence of reference answers alone does not establish equal assistance.

## Update Policy

Add or change rows only from durable evidence. Record active experiment execution and task-local outcomes in the project's task system, not here.
