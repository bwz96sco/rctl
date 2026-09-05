---
schema_version: 1
task_id: retained-comparison
title: Inspect a synthetic retained error comparison
kind: analysis
criteria:
  - id: AC-01
    requirement: The recorded gain and promotion label follow the frozen arithmetic rule.
    evidence_refs: [evidence/metrics.json, evidence/derived.json]
    failure_action: Correct the derived arithmetic before closing the assessment.
    method:
      type: command
      argv: [uv, run, --offline, --no-project, python, check_arithmetic.py]
      timeout_seconds: 30
      inputs: [check_arithmetic.py, evidence/metrics.json, evidence/derived.json]
  - id: AC-02
    requirement: The result applies the frozen rule and confines its claims to synthetic aggregate evidence.
    evidence_refs: [result.md, evidence/metrics.json, evidence/derived.json]
    failure_action: Revise the interpretation or leave the assessment unresolved.
    method:
      type: review
      reviewer: either
---

# Synthetic comparison contract

## Question

Does the supplied candidate meet the fixed improvement rule against the supplied baseline?

## Scope

Inspect only the synthetic aggregate observations. Baseline B0 and candidate C1 use the same fictional evaluation set. This task recomputes one error difference; it does not reproduce predictions, training, or uncertainty estimates.

## Constraints

Error is lower-is-better. Gain is B0 error minus C1 error. Promotion requires gain at least 0.01 absolute error units. Use the supplied aggregate directly, with no seed selection or alternative aggregation. Budget: local standard-library arithmetic only; no network, dependency download, or new experiment.

## Stop conditions

Stop with a bounded answer when arithmetic and interpretation are checked. A negative result is a valid completion. Changing the threshold or collecting new observations requires a separate task. Inconsistent input prevents closure until corrected.
