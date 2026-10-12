# Project experiment adapters

Use this reference when creating or updating reusable project runner guidance.
Actual project adapters retain command authority; this reference supplies a
packaging example, not permission to launch experiments.

## Input and output contract

Inspect the requested project and existing adapter, normally
`.agents/skills/<project>-experiment-workflow/`. Capture stable facts whose source
future agents need: command authority, working directory/environment, canonical
outputs and applicable resource, monitoring or evidence constraints. Preserve
working customizations. Unknown facts identify the needed source inspection.

Deliver a short `SKILL.md` with name/description frontmatter, invocation scope and
verified facts or links to existing project documentation. Each consequential rule
has source provenance. Live run IDs, metrics, queue status and temporary blockers
remain in runner records. The accepted task agreement governs scientific changes.

Use an available skill-creation workflow when useful. The
[entrypoint example](../assets/project-adapter/project-experiment-workflow-SKILL.md)
and other files in `assets/project-adapter/` are optional. Create only relevant
references; reuse project-owned manifests and result formats. Queues, profiling
and training sections apply only when the project uses them. For an unresolved
operations question, consult [runner operations](runner-operations.md).

## Verification

From the installed experiment skill directory, run
`uv run --no-project --script scripts/validate-adapter.py ADAPTER` for metadata,
guidance presence and declared local reference availability. It accepts inline
facts and project-owned documents without a fixed file tree. The helper also
detects accidental mutable-state field declarations in operational guidance.

Inspect commands and constraints against their sources. Structural success does
not establish that commands were executed or are usable. A bounded runner check
belongs here only when the requested work includes it and its outcome changes
the adapter. Report the path, material changes, sources, actual checks and unknowns.

An rctl contract/result own managed completion; creating an adapter supplies no
new execution budget. Preserve existing project adapters when retiring a generic
builder entrypoint.
