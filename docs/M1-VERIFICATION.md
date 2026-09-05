# M1 verification record

Date: 2026-09-05. Package: `rctl 0.1.0a1`. Scope: M1, contract and readable state. The local repository was initialized on `main` under the user's repository-creation request.

## Delivered behavior

The installed CLI supports task scaffolding, structural contract checks, begin, reasoned amendment, handoff checkpoint, status, and bounded context. It preserves accepted contract source text including CRLF, publishes records and handoffs through sibling temporary files and `os.replace`, and keeps context read-only. Task selection is explicit and project-bounded. JSON responses carry the specified envelope and M1 error outcomes.

The package includes repository-owned schemas and templates. Editable installs read the authoritative repository directories; wheels carry independent resource copies. `uv.lock` records resolved runtime and development dependencies. The core uses no network or host API.

## Acceptance evidence

| Case | M1 result | Evidence and boundary |
|---|---|---|
| A-01 | Pass | Real-file tests reject missing method/input declarations, duplicate criterion IDs and YAML keys, unknown fields/versions, wrong identity, empty or missing sections, unsafe YAML, and unfinished bundled scaffolds without creating a record. Valid input reports structural validity only. |
| A-02 | M1 portion passed | CRLF source is retained exactly; drift appears in status/context; reasoned amendment preserves revision 1. The verify/close rejection portion requires M2. |
| A-10 | Pass | Checkpoint changes only the handoff; a fresh CLI process recovers it while the record remains active. A prose claim of closure creates no machine closure. |
| A-11 | Pass | Explicit root/task overrides, environment selection, cwd fallback, missing selection, wrong root, and escaped paths are exercised without selecting another task. |
| A-12 | Core portion passed | Unicode reminders stay within 8,000 characters; warnings and file paths precede bounded excerpts; truncation is labeled. File bytes/mtimes remain unchanged, and a declared checker that would write a marker is never executed. Host delivery remains M3. |
| A-13 | M1 portion passed | Each CLI invocation runs as a fresh process in a non-Git temporary project. JSON and exits 0/2/3/4 are observed. Wheel installation uses an isolated environment with offline installation and direct console execution. Verification-related exits require M2. |

Additional tests reject malformed/truncated records without changing them and retain the preceding record after simulated failure of atomic publication. This is storage-level evidence, not full A-14 verification interruption/concurrency acceptance.

## Executed checks

Environment: macOS 26.3 arm64; uv 0.12.3; CPython 3.13.2 and 3.11.11. Resolved direct dependencies: PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.1.1, Ruff 0.16.6. The wheel records Hatchling 1.32.0 as its generator. Runtime dependency versions and complete installed CLI responses are retained in [package smoke evidence](evidence/m1-package-smoke.json).

| Command | Actual outcome | What a failure changes |
|---|---|---|
| `git init -b main` | Local repository initialized | Resolve repository location before Git work. |
| `uv sync` | Dependencies resolved; editable package installed; lockfile created | Correct package/dependency setup. |
| `mkdir -p .work` then `uv run pytest --basetemp=.work/pytest -q > docs/evidence/m1-pytest-py313.txt` | [41 passed on CPython 3.13.2](evidence/m1-pytest-py313.txt) | Fix contract, record, path, reminder, or output behavior. |
| `UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --python 3.11 pytest --basetemp=.work/pytest311 -q > docs/evidence/m1-pytest-py311.txt` | [41 passed on CPython 3.11.11](evidence/m1-pytest-py311.txt) | Fix the declared minimum-runtime incompatibility or narrow the target. |
| `uv run ruff check src tests scripts/smoke_package.py` | Passed | Fix import/name and selected static errors. |
| `uv run ruff format --check src tests scripts/smoke_package.py` | Passed | Normalize formatting before commit. |
| `uv build` | Source archive and wheel built successfully, including wheel construction from the source archive | Fix missing distribution resources. |
| `uv run scripts/smoke_package.py dist/rctl-0.1.0a1-py3-none-any.whl > docs/evidence/m1-package-smoke.json` | Passed: 9 CLI invocations, isolated installed import and packaged-resource assertions | Fix installation, console entrypoint, or checkout dependency. |
| `uv run --offline scripts/check_docs.py` | Passed; local links, JSON, three input schemas/example payloads, and 12-to-20 requirement/case mapping validated | Repair project documentation or fixtures. This is structure, not product verification. |

The test source is [test_m1.py](../tests/test_m1.py), with subprocess fixtures in [conftest.py](../tests/conftest.py). The repeatable installation procedure is [smoke_package.py](../scripts/smoke_package.py). Temporary working files are ignored under `.work/`; the smoke cleans its own environment and project after preserving responses.

## Failed attempts and fixes

- The first test command reported 37 setup errors because `.work/` did not yet exist, one resource test failure, and one pass. Create the temporary parent before using the custom pytest base directory; ordinary `uv run pytest` requires no custom setup.
- Wheel force-inclusion alone did not expose resources in editable source imports. A temporary source-symlink attempt then caused the source archive to omit the canonical template directory and wheel construction failed. The final implementation uses ordinary source resource lookup for editable installs and explicit wheel inclusion, with no source symlinks. Both suites and the source-archive/wheel build passed after this change.
- The first jsonschema documentation lookup used an unavailable Context7 library ID (HTTP 404). Library discovery returned `/python-jsonschema/jsonschema`; the corrected API lookup succeeded. Both responses remain in the evidence directory.

## Documentation sources

Commands were run through smart-search as required; `doctor --format json` reported `ok: true`.

- `smart-search context7-docs /astral-sh/uv 'pyproject build-system uv_build module-root src package data console scripts dev dependencies' --format json --output docs/evidence/m1-uv-docs.json`: [retrieved evidence](evidence/m1-uv-docs.json), including [uv dependency documentation](https://github.com/astral-sh/uv/blob/main/docs/concepts/projects/dependencies.md).
- `smart-search context7-docs /pypa/hatch 'build targets wheel force-include external directory package data' --format json --output docs/evidence/m1-build-docs.json`: [retrieved evidence](evidence/m1-build-docs.json), from [Hatch build configuration](https://github.com/pypa/hatch/blob/master/docs/config/build.md).
- `smart-search context7-library jsonschema 'Python Draft202012Validator iter_errors' --format json --output docs/evidence/m1-jsonschema-library.json`, then `smart-search context7-docs /python-jsonschema/jsonschema 'Draft202012Validator iter_errors validation path' --format json --output docs/evidence/m1-jsonschema-api.json`: [API evidence](evidence/m1-jsonschema-api.json), from [jsonschema error documentation](https://github.com/python-jsonschema/jsonschema/blob/main/docs/errors.rst).
- `smart-search fetch https://pyyaml.org/wiki/PyYAMLDocumentation --format markdown --output docs/evidence/m1-pyyaml-docs.md`: [retrieved source](evidence/m1-pyyaml-docs.md), supporting SafeLoader and custom constructor usage.

## Remaining work

M2 owns verification execution/review, material currentness, closure, reopen/cancel, and full A-02/A-13 coverage. M3 owns actual reminder delivery and export. M4 owns a new real research task across two fresh host sessions and release acceptance. Platform, record-compatibility, and preparation caveats are centralized in [READINESS: Limitations](READINESS.md#limitations).
