# Computation checks

Use these checks when numerical validity or scientific-software usability affects the current question. Reuse the task's inputs, execution route, evidence, and budget. A small standalone calculation can be answered directly; these checks do not require a formal experiment, proof workflow, separate phase, or report.

## Establish execution evidence

Decide whether the question needs a new run, a local usability check, or inspection of existing outputs. Reuse adequate current evidence. Before new execution, check only unresolved imports, executables, backend access, or a smoke path that could change the action. Documentation alone does not establish local usability.

Project runners own submission and monitoring. Retain the actual command, inputs, logs, outputs, and return status; remote jobs need log paths and an output-persistence plan. Report queued, running, completed, failed, or unknown separately from whether outputs have been inspected or validated. A submitted job has not necessarily completed, and a completed job with unread outputs is still completed.

## Check numerical validity

Successful execution does not establish correctness. Select checks relevant to the result and the conclusion:

- **Convergence and tolerances:** inspect termination status, convergence criteria, and the residual, feasibility tolerance, or optimality gap relevant to the claimed result.
- **Inputs and outputs:** check units, dimensions, schemas, applicable invariants, and whether the expected outputs were saved.
- **Randomness and data use:** retain seeds and account for variability or leakage where they affect the interpretation.

Choose checks whose failure would change the answer or next action. Preserve failed checks; do not loosen acceptance conditions to obtain a pass.

## Report what the evidence establishes

Distinguish a fresh computation from reused or remote execution, parsed outputs, values digitized from a figure, and an untested hypothesis. Link material results to their evidence and state what remains unvalidated.

Keep numerical validity separate from the scientific conclusion. Comparative claims stay with the experiment or trial; numerical searches supporting a mathematical argument retain their checked scope and do not establish a general proof. Put the finding in the existing artifact or the requested concise response.
