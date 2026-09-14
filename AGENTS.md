# rctl development

- `README.md` defines document authority; the older development proposal is historical. The package and command are `rctl`.
- Route reading by the change: `docs/PRD.md` for scope, `docs/SPEC.md` for behavior, `docs/CLI.md` for commands, and `docs/DEVELOPMENT.md` for current work and release order. Select the affected milestone/checks from `docs/ACCEPTANCE.md` before implementation.
- Use `uv` for Python setup and runs. Use smart-search for library/API documentation, setup, configuration, and current source-backed claims.
- Keep generated project documents in English unless the user requests another language.
- For records or verification, read the relevant `schemas/`. For hooks or skill integration, read `docs/INTEGRATION.md` and recheck the relevant official host documentation.
- Keep contract, result, handoff, and machine acceptance authority distinct. State whether a check verifies structure, execution, or an evidence-based judgment.
- Run a check only when its failure would change an in-scope action. Report actual commands, results, and untested behavior; use `docs/READINESS.md#limitations` for preparation-stage caveats.
- Work stays in this project unless the current task includes other paths. Shared skills, live research tasks, and host configuration need explicit task scope; disposable local acceptance fixtures follow the current development plan.
