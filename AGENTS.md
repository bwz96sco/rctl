# rctl development

- Before implementation, read `docs/PRD.md`, `docs/SPEC.md`, and `docs/DEVELOPMENT.md`; select one milestone and its checks from `docs/ACCEPTANCE.md`.
- `README.md` defines document authority. The older development proposal is historical. Name the package and command `rctl` even while this directory is named `rtcl`.
- Use `uv` for Python setup and runs. Use smart-search for library/API documentation, setup, configuration, and current source-backed claims.
- Keep generated project documents in English unless the user requests another language.
- For records or verification changes, read `docs/CLI.md` and the relevant `schemas/`. For hooks or skill integration, read `docs/INTEGRATION.md` and recheck the relevant official host documentation.
- Keep contract, result, handoff, and machine acceptance authority distinct. State whether a check verifies structure, execution, or an evidence-based judgment.
- Run a check only when its failure would change an in-scope action. Report actual commands, results, and untested behavior; use `docs/READINESS.md#limitations` for preparation-stage caveats.
- Work stays in this project unless the current task authorizes another path. This documentation task does not authorize migration of live research tasks or modification of shared skills or host configuration.
