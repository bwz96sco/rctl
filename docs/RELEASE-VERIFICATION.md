# rctl v0.1.0 release verification

Date: 2026-09-06. All four milestones and A-01–A-20 are complete within the tested scope below. This is a local release; no remote repository, package index, shared skill, or global host configuration was changed.

## Delivered release

The installable package includes contract/state commands, command and attributed-review verification, currentness and closure guards, handoffs, Codex adapter/export, schemas, templates, and the local `research-task` skill. The source repository also includes the synthetic walkthrough, tests, retained real-host evidence, and a new completed real analysis task. `uv.lock` fixes the development environment; package and command are named `rctl`.

## Full release checks

Environment: macOS 26.3 arm64, uv 0.12.3, CPython 3.13.2 and 3.11.11, Codex CLI 0.153.4. Resolved dependencies: PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.1.1, Ruff 0.16.6; build metadata records Hatchling 1.32.0.

| Actual command | Observed result | Failure detected; response |
|---|---|---|
| `uv run pytest --basetemp=.work/release-pytest -q > docs/evidence/release-pytest-py313.txt` | [112 passed on Python 3.13](evidence/release-pytest-py313.txt) | Product behavior regression; repair affected implementation. |
| `UV_PROJECT_ENVIRONMENT=.work/venv311 uv run --python 3.11 pytest --basetemp=.work/release-pytest311 -q > docs/evidence/release-pytest-py311.txt` | [112 passed on Python 3.11](evidence/release-pytest-py311.txt) | Minimum-runtime incompatibility; fix before support claim. |
| `uv build` | Source archive and wheel built, including wheel from source archive | Missing build inputs/resources; fix packaging. |
| `uv run scripts/smoke_package.py dist/rctl-0.1.0-py3-none-any.whl > docs/evidence/release-package-smoke.json` | [20 installed CLI calls passed](evidence/release-package-smoke.json); six execution logs retained | Installed entrypoint/resource/lifecycle failure; fix package. |
| `uv run ruff check src tests scripts/smoke_package.py scripts/probe_codex.py scripts/run_release_session.py` | Passed | Import/name/static errors; fix source. |
| `uv run ruff format --check src tests scripts/smoke_package.py scripts/probe_codex.py scripts/run_release_session.py` | Passed | Formatting divergence; normalize source. |
| `uv run --offline scripts/check_docs.py` | Passed | Broken local links, malformed JSON/schema/example, unmapped requirements; repair documentation. This checks structure. |

The smoke installs the wheel and dependencies offline into a fresh environment, uses a non-Git temporary project, executes the negative-result lifecycle, and exports packaged hook/skill files. It preserves responses and command logs before removing its temporary project. `mkdir -p .work` is needed before custom pytest base paths in a fresh checkout; ordinary `uv run pytest` needs no custom directory.

## Acceptance matrix

The full release suite re-executes M1/M2 coverage along with M3. Earlier records explain the detailed fixtures; their earlier remaining-work statements are historical.

| Case | Result | Concrete evidence |
|---|---|---|
| A-01 | Pass | [M1 tests](../tests/test_m1.py): invalid or ambiguous contracts reject begin without a record. |
| A-02 | Pass | M1 exact-text tests and [M2 tests](../tests/test_m2.py) reject drift and preserve reasoned amendments. |
| A-03 | Pass | M2 edits result/declared inputs, observes stale close, and preserves applicability after handoff-only changes. |
| A-04 | Pass | M2 real command executions retain argv/cwd/exit/logs; prose cannot substitute. |
| A-05 | Pass | M2 missing input/executable/review and timeout cases save unknown; malformed reviews execute nothing. |
| A-06 | Pass | M2 review identity/revision/source/rationale/reference tests, including operator-only rejection. |
| A-07 | Pass | M2 synthetic `not_supported` closure and missing-review rejection; real negative closeout below. |
| A-08 | Pass | M2 no-result/no-report guards, latest-failure precedence, and repeated-close behavior. |
| A-09 | Pass | M2 reasoned reopen, new cycle verification, preserved closure history. |
| A-10 | Pass | M1 fresh-process checkpoint recovery; first real session remains active after checkpoint. |
| A-11 | Pass | M1 path selection and [M3 tests](../tests/test_m3.py) for absent/wrong/out-of-root selection. |
| A-12 | Pass | M1 read-only bounded renderer plus M3 real adapter subprocess budgets and no checker execution. |
| A-13 | Pass | M1/M2 non-Git CLI/error protocol tests and independent offline installed-package smoke without a host. |
| A-14 | Pass | M2 real checks with interrupted publication, SIGINT, orphan logs, and detected record changes. |
| A-15 | Pass | M2 real checkers change contract/result/input during execution; no passing closure follows. |
| A-16 | Pass | M3 subprocess fixtures cover both events, malformed JSON/state, receipts on/off, and fail-open behavior. |
| A-17 | Pass | M3 exporter preserves existing destination/config and executes exported commands from the installed environment. |
| A-18 | Pass | Two distinct actual sessions below, bound event receipts, checkpoint, pre-tool handoff report, verification, closure. |
| A-19 | Pass | M2 copies a whole task with project-relative inputs, inspects/reopens/reverifies/closes it in another root. |
| A-20 | Pass | Contract/revision snapshots, actual event streams, retained raw inputs, and evidence judgment below. |

The [PRD](PRD.md) requirements R-01–R-12 map to these cases through [ACCEPTANCE](ACCEPTANCE.md). Structure, actual execution, and evidence-based judgment remain separate: pytest asserts behavior, command logs establish execution, and A-20 includes an attributed interpretation of the actual host actions.

## New real task across two sessions

The task asks whether actual retained project-file hook loading achieved delivery parity with inline loading under the recorded isolated Codex settings. Its data are the three new [M3 probes](M3-VERIFICATION.md), not invented research metrics. Synthetic B0/C1 content is only a delivery marker. One launch per route was fixed before analysis, without retries or selection; the observations were already available and this was not a blinded prospective experiment.

The [contract and machine record](evidence/release-task/tasks/hook-loading-compatibility/.rctl/record.json) retain revision 1 and the explicit revision-2 amendment. At 06:52:58 UTC, before either analysis session, revision 2 declared normalized empty receipt inputs for routes that emitted no receipt file. Original zero-count summaries and `NO_RCTL_REMINDER` outputs remain intact. The comparison rule, command checker, budget, and review criterion were fixed before dependent analysis.

| Session | ID | Actual behavior |
|---|---|---|
| First | `01a0757d-e5c1-7bb0-8d89-c98576255c79` | Both events received. Inspected raw launches/outputs, independently implemented and ran one standard-library analysis, then checkpointed with task active at revision 2 and no verification. |
| Second | `01a07580-c440-76a3-909f-93f6e97b5e19` | Both events received. Before any tool call, accurately reported the delivered finding and pending review/verification. Inspected sources, wrote result/review, verified once, inspected logs/status, and closed successfully. |

Actual launches used [run_release_session.py](../scripts/run_release_session.py), invoked with `first` and then `second`, the independently installed `rctl 0.1.0` wheel, and the reviewed inline bundle. The [first launch](evidence/release-sessions/first/launch.json) and [second launch](evidence/release-sessions/second/launch.json) retain exact arguments and selected environment overrides. Each host exited 0. Both used ephemeral execution, workspace-write sandboxing, disabled user configuration/apps/plugins, and invocation-only trust for reviewed hooks. No shared installation was performed.

The [first handoff](evidence/release-sessions/first/handoff.md) and [active record snapshot](evidence/release-sessions/first/record.json) establish the pause. The [second receipts](evidence/release-sessions/second/receipts.jsonl) contain the bounded handoff, and the [second event stream](evidence/release-sessions/second/events.jsonl) independently records its correct interpretation before tools. The second prompt requested a report of delivered progress but did not disclose the finding or counts. SessionStart/UserPromptSubmit contexts stayed within 8,000/2,000 characters; long handoff excerpts were explicitly truncated with source paths.

The [result](evidence/release-task/tasks/hook-loading-compatibility/result.md) correctly reports `not_supported`: inline delivered two bound receipts and task information; project and disabled control delivered none. Verification V0001 at 06:58:31 UTC passed AC-01 by actual independent checker execution and AC-02 by [agent evidence review](evidence/release-task/tasks/hook-loading-compatibility/reviews.json). Managed closure followed at 06:58:44 UTC. Command stdout records the derived counts; the machine record, rather than the pre-verification next-action prose, owns final closure.

Source inspection of both event streams found one analysis run and one declared verification, no changed criteria after dependent work, no new probes or network execution, and no extra work triggered by the negative finding. The final raw inputs are byte-equal to all 19 original probe files. The second session independently inspected the derived analysis and its raw evidence. This is the A-20 evidence judgment; it does not authenticate an independent operator.

The completed task, required evidence, machine record, logs, and project orientation were copied while quiescent to [the retained task root](evidence/release-task/research/README.md). Metadata-preserving copying allowed the installed CLI to report [closed/current at archival inspection](evidence/release-task/status-at-archive.json). A later Git checkout may change mtimes; copy to a disposable root and freshly verify when resuming. The [release audit](evidence/release-audit.json) retains binding/order/input-preservation checks and the bounded judgment.

## Observed corrections and limitations

The actual project-file probe delivered no reminder, so only the tested inline route is claimed. The failure and control remain in the evidence; root cause was not diagnosed. Official smart-search retrieval succeeded for M3 and is retained in its verification record.

The first analysis session encountered absent optional result/project-development files in the disposable root. The second initially placed the global root option after the subcommand, received exit 2, then corrected it. These read-only errors are preserved in host events and did not change scope or task state. Archival audit assertions were corrected to allow host trust warnings before the first agent message and to match the actual handoff text; product behavior was correct.

Runtime/platform, host-installation, single-writer, metadata-currentness, judgment, and untested interruption boundaries are centralized in [READINESS: Limitations](READINESS.md#limitations). No ordinary persisted installation, resume/compact support, other host version, fresh training, or model-performance benefit is claimed by this release.
