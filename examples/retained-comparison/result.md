---
schema_version: 1
task_id: retained-comparison
contract_revision: 1
assessment: not_supported
---

# Synthetic comparison result

## Outcome

C1 does not meet the promotion rule. Its error is higher than B0, and the gain is −0.03 absolute error units, below the required +0.01.

## Evidence

The supplied [metrics](evidence/metrics.json) are B0 = 0.20 and C1 = 0.23. [Derived evidence](evidence/derived.json) records 0.20 − 0.23 = −0.03 and no promotion. The example [arithmetic check](check_arithmetic.py) can reproduce this relation. This fixture does not claim a completed rctl verification run.

## Deviations

None in the specified synthetic assessment; the threshold and inputs are unchanged.

## Next action

Retain B0 within this fictional comparison and close the assessment after both required checks pass. There is no authorized extra experiment.

## Limitations

All observations are synthetic aggregates. They establish no real model performance, prediction quality, uncertainty, or general scientific conclusion.
