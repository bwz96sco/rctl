# Training Failure Diagnosis

Use observed failure signals to select a discriminating check. Reuse current run
evidence and remaining allowance; diagnostic work does not add a universal gate.

| Layer | Possible signals | Relevant evidence |
|---|---|---|
| Data | missing/corrupt inputs, wrong split, leakage | manifests, samples, split IDs |
| Tokenization/labels | unknown tokens, bad padding or IDs | encoded examples, applicable round trips |
| Model/loading | incompatible weights, unexpected trainable scope | load audit, parameter/config comparison |
| Optimization | NaN/Inf, divergence, plateau or collapse | loss, gradients/logits, schedule, checkpoint lineage |
| Evaluation/decode | implausible scores or disagreement with outputs | metric definition/parser, predictions, decode policy |
| Runner/environment | OOM, failed synchronization or lost outputs | process/backend state, environment, persistence logs |

Tiny overfit or a capped run can answer a particular capacity/generalization
question when needed. It is a launch prerequisite only if the current contract
makes it one. For CTC/sequence tasks, blank/pad/eos mappings, empty-output rate,
hypothesis length and teacher-forced/free-run differences may expose the failure;
select those relevant to the observed signal.

Before another costly attempt, state the observed failure, evidence, proposed
change and what result would distinguish the diagnosis. Keep scientific failure,
implementation failure and unavailable measurement separate. Repeated attempts
without an interpretable delta justify changing the investigation or stopping
within the existing agreement, not resetting its allowance.

Put diagnosis and next action in the current result or run record. Use
`../assets/training/training_diagnostic_report.md` when a separate report is requested;
`scripts/validate-training.py ROOT --strict-diagnostics` checks that report's
structure. Neither the report nor its validator replaces rctl acceptance.
