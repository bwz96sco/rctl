---
name: research-computation
description: Run or check scientific computations when numerical validity or local software usability is the question. Use for solver checks, simulations, numerical counterexamples, and inspecting retained computation outputs. Optional support for experiments and theory, not a required research stage.
---

# Research Computation

Resolve a bounded computation question with traceable execution and numerical checks. Work inside the calling task or trial and reuse its evidence; a separate computation phase or report is not required. Project runners own job submission and monitoring, while research-task owns any managed lifecycle.

## Workflow

1. **Bound the question.** Identify whether the request needs a new run, a local usability check, or inspection of existing outputs. Keep the supplied inputs, execution route, budget, and success criteria.
2. **Check what can change the action.** Reuse adequate current environment and run evidence. Before new execution, check only relevant unresolved imports/executables, backend access, schemas, or a smoke path. Documentation alone never establishes local usability; a known working CPU calculation needs no unrelated GPU preflight.
3. **Execute or inspect.** Run the required command only when new execution is in scope; otherwise inspect the retained inputs, logs, outputs, and return status. Report the actual observed job state (queued, running, completed, failed, or unknown) separately from whether outputs were inspected or validated. Submission is not completion, and an uninspected completed job is not still running. Preserve the command and evidence behind any execution claim.
4. **Validate separately.** Successful execution is not correctness. Check convergence, tolerances, units, schemas, leakage, seeds, invariants, and output persistence as applicable. Never weaken checks to force success.
5. **Type the claims.** Distinguish `computed` (traceable real execution), `parsed`, `digitized`, and `hypothesis`. Identify reused or remote execution as such; reading an existing result is not a fresh run. Link material claims to evidence and state what remains unvalidated.

Complete when the requested check or computation is answered or explicitly blocked, relevant execution evidence is identifiable, and validation remains separate from execution. Put the finding in the existing task/trial artifact or a concise standalone response, according to the request.

## Rules

- When a standalone durable note is needed, read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Use `<vault>/computation/<topic-slug>/`, or `artifacts/research-computation/<topic-slug>/` without a note root. Raw solver outputs, checkpoints, and large datasets stay in runner-owned storage.
- `smart-search-cli` for solver/library docs; `research-literature` when package behavior or validation criteria depend on papers; project scripts own exact commands.
- HPC jobs are submitted only with log paths and an output-persistence plan.
- Comparative scientific claims belong to research-experiment; early promote-or-drop pilots belong to research-rapid-test. Neither workflow must detour through this skill.
