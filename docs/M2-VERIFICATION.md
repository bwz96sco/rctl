# M2 verification record

Date: 2026-09-06. Package: `rctl 0.1.0a2`. Scope: M2, verification and closure, plus M1 regression coverage. Starting point: local commit `eedbca4`.

## Delivered behavior

`verify` validates the contract, result, and supplied reviews before running declared commands. It saves command argv/cwd/timing/exit status and file-backed stdout/stderr, retains attributed review judgments and exact result/review text, and reports pass/fail/unknown without changing phase. Missing evidence or missing reviews cannot become a passing verification. Failed and unknown reports remain inspectable.

`close` requires the latest passing report, its current contract revision and cycle, matching result text and evidence observations, and the current rctl version. `reopen` requires a reason and a new verification cycle; `cancel` retains materials without claiming completion. Historical closures remain visible when current files change. Status and context expose verification applicability; context remains read-only and bounded.

Machine-record validation now covers nested reports, execution observations, review binding, and lifecycle history, while accepting the existing M1 record shape. Record publication rechecks the starting record text to reject detected overlapping changes. Each verification attempt has a distinct log directory, so retrying after interruption preserves orphan logs without treating them as a report.

Contract/result parsing establishes **structure**. Subprocess checks establish **execution** of the declared criterion. Review entries retain the stated source and rationale for an **evidence-based judgment**; rctl checks binding and reference availability, not the scientific truth of the prose. Scientific assessment remains separate from check verdict and managed phase.

## Acceptance evidence

| Case | Result | Observed behavior |
|---|---|---|
| A-02 | Completed with M1 | Contract drift refuses verify/close; amendment preserves old text and requires a result for the new revision and new verification. |
| A-03 | Pass | Edits to result, input, checker, evidence, or execution logs prevent closure. Deleted logs and re-pointed input symlinks are detected. Handoff-only changes preserve applicability. |
| A-04 | Pass | Real subprocess argv/cwd, exit 0 and exit 7, stdout, stderr, timing, and log observations are asserted. Prose cannot supply a command outcome. |
| A-05 | Pass | Missing executable/input/review/evidence and unreadable input produce unknown; timeout kills the launched process group, including a child that would otherwise write a sentinel. Malformed inputs execute nothing. |
| A-06 | Pass | Review task/revision/criterion, duplicate IDs, required references, rationale, and source are checked. Agent review cannot satisfy operator-only criteria. Extra local attachments are observed; external references are retained without fetching. |
| A-07 | Pass | The documented uv-based synthetic arithmetic checker yields `gain=-0.03; promote=False`; supplied review and command pass permit `not_supported` closure. Missing review leaves the task active. Supported, inconclusive, and not-applicable assessments can also close. |
| A-08 | Pass | Missing report/result prevents close. A later failed verification cannot reuse an older pass. Repeated close changes nothing. |
| A-09 | Pass | Closed/cancelled tasks require reasoned reopen. Prior-cycle reports cannot close the new cycle; prior closures remain visible after changed files and later closure. |
| A-13 | Local CLI portion complete | M1/M2 run in non-Git temporary projects, with actual CLI JSON/text outcomes and exits 0/2/3/4/5/6. Exit 70 is checked using an injected internal exception. Help/version also honor JSON mode. The installed wheel runs independently of source imports. |
| A-14 | Pass within single-writer model | A real check followed by simulated `os.replace` failure retains a parseable prior record. SIGINT during a real check leaves the previous report untouched. Orphan logs are retained and not reused as a report. A real checker-triggered cancellation causes exit 6 instead of overwrite. |
| A-15 | Pass | Real checkers edit contract, result, or declared input while running; verification records unknown and cannot close. A concurrent supported record mutation rejects publication. |
| A-19 | Pass | Entire task and project-relative evidence are copied to a second local root, inspected, reopened, reverified there, and closed while the original task remains unchanged. |

The full suite also retains A-01/A-10/A-11 and A-12 core regression coverage. M3 adapter/export cases and M4 real-host/task cases remain outstanding.

## Executed checks

Environment: macOS 26.3 arm64, uv 0.12.3, CPython 3.13.2 and 3.11.11. Runtime/development dependency versions remain resolved in `uv.lock`: PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.1.1, Ruff 0.16.6. Hatchling 1.32.0 is recorded in wheel metadata.

| Actual command | Outcome | Failure detected; response |
|---|---|---|
| `uv run pytest --basetemp=.work/pytest -q > docs/evidence/m2-pytest-py313.txt` | [97 passed, CPython 3.13.2](evidence/m2-pytest-py313.txt) | Contract, verification, currentness, lifecycle, or output regressions; repair the affected implementation. |
| `UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --python 3.11 pytest --basetemp=.work/pytest311 -q > docs/evidence/m2-pytest-py311.txt` | [97 passed, CPython 3.11.11](evidence/m2-pytest-py311.txt) | Minimum-runtime incompatibility; fix before claiming that runtime. |
| `uv run ruff check src tests scripts/smoke_package.py` | Passed | Import/name and selected static errors; fix source. |
| `uv run ruff format --check src tests scripts/smoke_package.py` | Passed | Formatting divergence; normalize affected files. |
| `uv build` | Source archive and wheel built; wheel built from source archive | Missing packaged resources or build inputs; fix packaging. |
| `uv run scripts/smoke_package.py dist/rctl-0.1.0a2-py3-none-any.whl > docs/evidence/m2-package-smoke.json` | [Passed: 19 installed CLI invocations](evidence/m2-package-smoke.json) | Installation, entrypoint, resource, or installed lifecycle failure; fix before handoff. |
| `uv run --offline scripts/check_docs.py` | Passed | Broken project links, malformed JSON/schema/example, or requirement mapping; repair documentation. This check verifies structure. |

The temporary parent `.work/` already existed from M1. Use `mkdir -p .work` before the custom pytest commands in a fresh checkout, or use ordinary `uv run pytest`. [test_m2.py](../tests/test_m2.py) contains the M2 scenarios; [test_m1.py](../tests/test_m1.py) retains the earlier contract/state suite. The [package smoke](../scripts/smoke_package.py) creates an isolated environment with offline installation and preserves CLI responses and actual check log contents before removing its temporary project.

All executed M2 pytest and installed-package smoke runs passed. Deliberate nonzero verification/error fixtures passed only when the expected rejection and record-preservation assertions were observed.

## Implementation decisions

- SPEC's verification step 4 now states its already-defined aggregation precedence explicitly: changed materials prevent pass, while a failed criterion retains the overall fail verdict. Otherwise changed/incomplete materials produce unknown.
- Result/review parsing shares the M1 safe frontmatter and schema validation machinery. Scientific completeness is not inferred from heading presence.
- Source input paths are recorded relative to the project, retaining input symlink spelling for subsequent observation. Large evidence is observed by size and nanosecond mtime, without hashing or copying it.
- Timeout handling uses a new process session and kills the local process group; interrupted SIGINT checks also clean up that group before unwinding. No repair/retry loop or remote job control was added.

## Documentation evidence and next milestone

API documentation was retrieved using the required smart-search path:

```sh
smart-search context7-docs /python/cpython 'subprocess Popen start_new_session wait timeout os.killpg SIGKILL stat st_mtime_ns' --format json --output docs/evidence/m2-subprocess-docs.json
```

[Retrieved evidence](evidence/m2-subprocess-docs.json) cites the [CPython subprocess documentation](https://github.com/python/cpython/blob/main/Doc/library/subprocess.rst) and [subprocess implementation](https://github.com/python/cpython/blob/main/Lib/subprocess.py). It confirms that `wait(timeout=...)` raises on timeout and waits only for the direct child, so group termination is explicit. M1's retained jsonschema and PyYAML API evidence remains applicable.

The next assignment is M3: the local task skill, Codex adapter/export, official protocol recheck, and real host delivery evidence. The local CLI milestone does not establish host compatibility or real research-task acceptance. Operating and preparation boundaries remain centralized in [READINESS: Limitations](READINESS.md#limitations).

## v0.2.1 review follow-up

Completed on 2026-09-06 against A-13, A-14, and A-15. Record errors now retain the
failed schema field/constraint or lifecycle diagnosis. CLI internal errors advertise
`RCTL_DEBUG=1`; the traceback goes to stderr and JSON stdout remains one envelope.
Changed evidence names executed command criteria that declared it and explains
generation-before-verification, including when another criterion failed. Existing
verdict and closure guards still apply. Temporary record/handoff writes flush and
sync the file before replacement. The CLI now uses the reopen/cancel methods directly.

Package metadata and runtime diagnostics identify the macOS/Linux target. The
[CI workflow](../.github/workflows/ci.yml) specifies both OS targets with Python
3.11/3.13 and includes all scripts in lint, document checks, build, and wheel smoke.

| Command | Observed result |
|---|---|
| `uv run pytest -q` | 140 passed on macOS arm64, CPython 3.13.2. |
| `UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --locked --python 3.11 pytest -q` | 140 passed on CPython 3.11.11, including the final evidence-recovery assertion. |
| `uv run --locked pytest -q tests/test_m2.py -k regenerated` | 2 passed on CPython 3.13.2 after adding the recovery assertion. |
| `uv run ruff check src tests scripts` | Passed after correcting the previously omitted `check_docs.py` import formatting. |
| `uv run scripts/check_docs.py` | Passed local links, retained JSON, four schemas, and the 14-requirement/24-case matrix. |
| `uv build` | Built the v0.2.1 sdist and wheel. |
| `uv run --locked scripts/smoke_package.py dist/rctl-0.2.1-py3-none-any.whl` | Passed the isolated installed-package walkthrough, including generated hook adapter calls. |

The error tests inject malformed local records, an internal exception, an unsupported
platform, and sync/replace failures. They verify diagnostics, JSON output, and
preservation. The evidence test actually executes a checker that modifies a declared
artifact: its command passes but the report cannot close. A check that only reads the
prepared artifact then verifies and closes. This establishes execution and lifecycle
behavior; it is not a scientific evidence judgment.

API/configuration evidence was retrieved through smart-search:

```sh
smart-search context7-docs /python/cpython 'os.fsync flush os.replace atomic rename durability' --format json
smart-search fetch https://docs.astral.sh/uv/guides/integration/github/ --format markdown
```

The retrieved [CPython os documentation](https://github.com/python/cpython/blob/main/Doc/library/os.rst)
specifies flushing Python buffers before file `fsync`, and atomic successful replacement.
The [uv GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/)
provides the setup action and Python matrix configuration. Hosted CI, native Windows,
WSL, and power-loss guarantees remain subject to [Limitations](READINESS.md#limitations).

### First public CI launch

The repository was published at [bwz96sco/rctl](https://github.com/bwz96sco/rctl)
on 2026-09-06. The [first run](https://github.com/bwz96sco/rctl/actions/runs/34024835319)
failed during job setup because `astral-sh/setup-uv@v8` does not exist; no tests ran.
The workflow now names the published `v8.1.0` tag from the earlier documentation
example, confirmed with `gh api repos/astral-sh/setup-uv/git/ref/tags/v8.1.0`.

The [second run](https://github.com/bwz96sco/rctl/actions/runs/34024925168) passed
all 140 tests and lint in each of the four OS/Python jobs. Its documentation check
then found workstation-only links in `SOURCES.md`. Those external local sources are
now recorded as plain provenance paths, while repository links remain checked.
No private source files were imported to satisfy the public documentation check.

The [completed run](https://github.com/bwz96sco/rctl/actions/runs/34024998318) on
commit `ab0d8b5` passed all four macOS/Linux × Python 3.11/3.13 jobs: 140 tests
per job, full-script lint, document checks, build, and installed-wheel smoke. This
establishes hosted Linux and macOS execution for the patch release. The two earlier
failures above explain the setup-tag and source-reference corrections.
