# rctl Specification

This document defines core behavior and the v0.2–v0.4 extensions for [R-01–R-19](PRD.md). See [CLI](CLI.md) for syntax and [schemas](../schemas/README.md) for structural validation. All times are UTC ISO 8601 strings.

## 1. Architecture and ownership

Target macOS and Linux; ordinary CLI commands reject other platforms before project access. Use Python 3.11+, `argparse`, `pathlib`, `json`, and `subprocess`. Use PyYAML for safe frontmatter loading and `jsonschema` for Draft 2020-12 validation; pin resolved versions with `uv.lock` at implementation. Reject duplicate YAML mapping keys rather than silently choosing the last one. Ordinary Markdown bodies are preserved, not reserialized by a YAML writer.

Separate pure parsing/policy, local record storage, check execution, context generation, and the host adapter. CLI and host code call the same context function. Only CLI application services mutate the acceptance record. No LLM or network call is part of the core.

| Location | Authority | Writer |
|---|---|---|
| `contract.md` | Proposed/current human agreement | User or agent |
| `.rctl/record.json` → `contracts` | Exact contract text accepted at each revision | `begin` / `amend` |
| `state.md` | Optional progress/handoff, including next action | User, agent, or `checkpoint` |
| `result.md` | Scientific interpretation and next decision | User or agent |
| `.rctl/record.json` → `verifications`, `closures`, `phase` | Observed checks and managed lifecycle | `verify` / `close` / `reopen` / `cancel` |
| `.rctl/checks/` | Check stdout/stderr | Verification executor |
| Local evidence and external run storage | Underlying observations | Analysis tools or project runners |
| Hook receipts | Delivery diagnostics | Adapter, only when logging is selected |

The retained contract text records an agreement, not proof that all earlier execution followed it. The record stores no transcript. Copying a pilot `result.md` does not create a managed closed task.

## 2. Project and task addressing

Resolve the project root from global `--root`, else `RCTL_PROJECT_ROOT`, else the current working directory. Resolve a supplied task argument relative to that root; an absolute task path is allowed only inside it. Only `context` and the host adapter may omit the task argument: they then use `RCTL_TASK_PATH`, interpreted relative to the root, or return project-only context when it is unset. No parent-directory discovery, global current-task pointer, most-recent-task fallback, or automatic selection is performed.

The task's `task_id` equals its directory basename, is immutable after begin, and is unique by the pair `(resolved project root, task path)`. Different projects can use the same short task ID. Paths to task inputs and review attachments resolve relative to the task directory and must remain within the project root; `../../runs/...` is valid when it stays inside that root. External evidence uses URI references and is never fetched by rctl.

## 3. Contract and result format

Both are UTF-8 Markdown with one leading YAML frontmatter block delimited by `---` lines. Frontmatter follows the corresponding JSON schema. Require nonempty bodies under the following exact level-two headings:

| File | Required headings |
|---|---|
| Contract | `Question`, `Scope`, `Constraints`, `Stop conditions` |
| Result | `Outcome`, `Evidence`, `Deviations`, `Next action`, `Limitations` |

Contract frontmatter contains `schema_version`, `task_id`, `title`, `kind`, and `criteria`. Criterion IDs are unique within a contract and stable when the underlying requirement is unchanged. Every criterion is required. Each has a requirement, evidence references, a named failure action, and either a command or review method. Local command inputs must be explicit. The body carries the scientific question and boundaries, not a second copy of the criteria.

A comparison contract must state baseline, intervention, data/split, metric direction and evaluator, aggregation/selection rule, budget, and stop conditions in its body. A review must assess their adequacy; heading presence cannot establish scientific completeness. Existing user instructions can supply authority; `begin` is not a new permission request.

Result frontmatter contains `schema_version`, `task_id`, `contract_revision`, and `assessment` (`supported`, `not_supported`, `inconclusive`, or `not_applicable`). These are interpretations, not task phases or check verdicts. A result may contain a scientific failure while its verification passes.

## 4. Machine record

Use `.rctl/record.json`, created at `begin`. Absence means an unmanaged draft; there is no separate draft record. Required top-level fields are:

| Field | Type and meaning |
|---|---|
| `schema_version` | Integer `1`; unknown versions reject mutations. |
| `task_id` | Immutable string matching the contract and task directory. |
| `phase` | `active`, `closed`, or `cancelled`. |
| `cycle` | Positive integer, initially 1; increment only on reopen. |
| `contracts` | Nonempty ordered array of `{revision, text, reason, recorded_at}`; revisions are consecutive from 1. |
| `verifications` | Ordered array of verification objects from section 6; initially empty. |
| `closures` | Array of `{verification_id, contract_revision, cycle, assessment, closed_at}`; initially empty. |
| `lifecycle` | Ordered entries `{action, reason, recorded_at}` for begin, amendment, close, reopen, and cancellation. |

`text` is the exact decoded contract source, read without newline normalization. The last contract is governing. IDs for new reports are `V0001`, `V0002`, and so on, local to the task. Never rewrite old entries through a supported command. The latest verification is the only candidate for a new closure; an older pass cannot bypass a later failure.

Write the entire record to a temporary sibling, flush Python buffers, call `os.fsync` on that file, and publish with `os.replace`. A pre-publication sync failure leaves the previous record in place; temporary files are cleaned up. Logs are written first; an interrupted check may leave unreferenced logs, which do not imply a saved verification. A malformed record rejects mutations and yields an unavailable context, without silently resetting it. Repeating a mutation after an uncertain response begins by reading the record; no automatic retry protocol is promised.

One writer per task is the v0.1 operating model. A verification process must reread the record and contract before publishing and reject a detected intervening change; this check detects ordinary accidental overlap, not atomic multi-writer coordination. See [limitations](READINESS.md#limitations).

## 5. Lifecycle

| Operation | Preconditions | Effect |
|---|---|---|
| `begin` | Draft; contract structural validation passes; scaffold placeholders replaced. | Save contract revision 1; phase `active`. |
| `amend` | Active; changed contract validates; task ID unchanged; nonempty reason. | Append next contract revision; previous verification is stale. |
| `verify` | Active; current contract exactly equals governing text; result parses and names current revision. | Run/record checks and append a report; phase remains active. |
| `close` | Active; latest report passes and is current. | Append closure referencing that report; phase `closed`. |
| `reopen` | Closed or cancelled; nonempty reason. | Phase active; increment cycle; append event; pre-reopen reports cannot close this cycle. |
| `cancel` | Active; nonempty reason. | Phase cancelled; retain all materials; no successful closure claim. |

`begin` on an already managed task, unchanged `amend`, or repeated `close` returns a clear state error without duplicating entries. Amendment and reopen each require a new verification before close. A different scientific comparison should become a new task; the operator/reviewer judges this boundary.

Editing a governing contract makes it `amendment_required`; `verify` and `close` refuse until `amend`. Editing a result after verification makes that report stale. Editing the handoff does not invalidate verification. A closed task retains its historical closure if files change, but context must separately flag changed current materials. Revising the accepted result requires reopen and verification.

Paused work stays active, with an optional handoff. Finishing a chat response never changes lifecycle.

## 6. Verification procedure

1. Parse the governing contract, result, and optional review input. Invalid structural input returns before executing commands or appending a report.
2. Capture the starting record and contract text, exact result text, and observations of all declared local inputs and local evidence references. Automatically include task-local check scripts when named in `inputs`; the author is responsible for declaring scripts, helper files, and data actually needed by a check.
3. Execute criteria in contract order. A criterion's command must be an independently runnable check, not a prerequisite-generating pipeline. Continue collecting criteria after a normal failure; do not launch repair/retry loops.
4. Reobserve inputs and compare contract, result, and record. A material change during checks prevents a passing report: it is `unknown` unless a criterion failed, in which case the aggregation rule below retains `fail`. An intervening record mutation rejects publication to avoid overwriting it.
5. Append the completed report atomically. A fail or unknown report is still a saved result and returns its ID. Verification never changes phase.

### Command checks

Use the exact nonempty `argv` from the frozen contract, `shell=False`, task directory as cwd, and the declared positive `timeout_seconds`. Preserve the normal local environment without recording it. Record argv, start/end time, exit code, timeout/execution error, and stdout/stderr file references.

Exit 0 means this declared command passed; nonzero means fail. Missing executable, timeout, unreadable required input, or inability to establish a check result means unknown. Capture output directly to files rather than holding it in memory. On timeout, terminate the launched local process group and record unknown. Check commands must remain bounded local validation and must not submit or detach jobs. `verify` explicitly runs these commands; hooks never do so.

Command inputs must already exist. Command output logs are evidence of this execution and are not contract inputs. A checker that must inspect an analysis artifact declares that preexisting artifact as an input; analysis generation happens before verify. When an observed path changes and is declared evidence for an executed command criterion, the diagnostic names the criterion and explains this ordering. This association does not prove which process changed the file. Subject issues remain visible even when another criterion fails.

### Review checks

Review input follows `reviews.schema.json`: task ID, contract revision, and entries with criterion ID, verdict, reviewer label, rationale, and evidence references. A supplied entry must correspond to a review criterion and IDs must be unique. Missing review entries produce unknown, not success. Review evidence must include the contract's required references; additional references are allowed and retained.

`reviewer` is `agent` or `operator`, a declared source of judgment with no authenticated identity guarantee. A review criterion can require `either` or `operator`; an agent entry for the latter is unknown with an explanation. Require nonempty rationale and references even for pass. A review author must inspect the cited source content; rctl verifies reference availability and records the judgment, not the truth of arbitrary prose. The review input itself is captured as exact text in the report when supplied.

### Report content and verdict

Every report contains `id`, `contract_revision`, `cycle`, `created_at`, `rctl_version`, `result_text`, optional `review_input_text`, `observed_files`, `external_refs`, `subject_issues`, `checks`, and `verdict`. `subject_issues` is an array of explanations for missing, unreadable, or changed subject observations, empty when none occur. `external_refs` is a deduplicated array of URI strings; the review rationale carries any version and observation qualification.

A check contains `criterion_id`, `method` (`command` or `review`), `verdict`, `rationale`, and `evidence_refs`. Command checks additionally contain `execution` with `argv`, project-relative `cwd`, `started_at`, `finished_at`, nullable integer `exit_code`, boolean `timed_out`, nullable string `error`, `stdout_ref`, and `stderr_ref`. If execution never started, `execution` is null and the rationale explains why. Review checks additionally contain nullable `reviewer`; it is null when the required entry is missing. Enumerate all criteria exactly once.

An `observed_files` entry has project-relative `path`, `observation` (`present`, `missing`, or `unreadable`), nullable `size_bytes`, and nullable `mtime_ns`. Store the final observation; either a missing/unreadable observation or a difference from the starting observation adds a `subject_issues` entry. Observe newly written stdout/stderr logs after execution and include them in `observed_files`, so missing execution evidence also prevents later closure. Their absence from the starting input list is expected and does not itself create an issue.

Report verdict is `fail` if any criterion fails, otherwise `unknown` if any criterion is unknown or subject observation is incomplete/changed, otherwise `pass`. Structural parsing success is not a check verdict. `close` requires pass plus currentness; it does not reinterpret scientific assessment.

## 7. Currentness and scope of observations

Compare current contract and result text exactly against the governing contract and report's `result_text`. For each declared local evidence/input file, record project-relative path, byte size, and nanosecond mtime before and after verification. At close, observe these again. Missing or changed metadata makes a report stale; an observation error makes applicability unknown. No background scanning or full data hashing is required.

This is an ordinary-change detector in a cooperating workspace, not content-integrity certification. Store `external_refs` as the URI and reviewer-supplied version/observation description; rctl makes no current remote availability claim. Evidence freshness and reproducibility beyond these observations must be covered by the criterion's check. A report from a different `rctl_version` cannot close a task until verification is rerun.

Currentness values are `not_checked`, `current`, `stale`, or `unknown`; they are derived views, not writable phase fields. Even a current report may have a fail verdict. A report's cycle must equal the task's current cycle. All referenced local files in review entries join `observed_files`, including references added by the reviewer.

## 8. Context and handoff

`context` is read-only and loads project guidance before attempting an optional task.
Read only explicit level-two `Goal` and optional `Current guidance` sections from
`research/PROGRAM.md`, and `Reuse Rule` from `research/ROUTES.md`. Fenced headings
are content, not structure. Duplicate sections make that source unavailable; empty
or sections consisting solely of an authoring placeholder supply no guidance.
Inequalities and Markdown URI/email autolinks remain content, including standalone
autolinks. Missing/unreadable sources
produce warnings, never task read failures. Resolve sources within the explicit
root, without scanning the vault, reading transcripts, fetching URLs, or ranking
routes. Read current bytes on every call. No separate summary store is created.

A selected task adds identity, phase, governing revision, verification/applicability,
historical closure, warnings, reported blockers/next step and lifecycle action.
Without selection, identify project-only context and select no task. A task error
preserves project context while retaining its CLI error code; hooks still exit 0.
Project content is reported guidance, not task authorization or machine acceptance.

Default to 8000 Unicode characters; compact reminders use 2000. Show project goal,
current guidance and reuse rule first, reserving content space for task warnings,
blockers and next action. Prefix each warning with `Warning:`. Use one root and a
short relative source map, including in project-source diagnostics while retaining
the failure reason. List the research README only when it exists. Allocate
unused field space to remaining fields; bound values separately from labels and
use short truncation references. Compact output does not append the whole handoff.
Long output adds bounded contract/handoff excerpts after core fields. Bound added
JSON summaries too; an insufficient budget yields null text fields rather than
fragments of truncation markers. Extremely long fields still require source reads.

Keep current corrections in `PROGRAM.md` with evidence links and explicit scope.
When a route conclusion is superseded, link its replacement and retained evidence
in the existing ledger. rctl neither chooses replacements by timestamp nor decides
scientific truth. The task skill requires history reuse before experimental proposals,
new contracts and material direction changes: cite related mechanisms/evidence,
what is already answered, the new question/reopen condition, and the decision new
evidence would change. Record this in Question/Scope, using existing review criteria
where appropriate. Heading presence is not scientific adequacy.

`checkpoint` replaces `state.md` with a user-supplied Markdown handoff. It does not edit the machine record or certify statements in the handoff. A result saying closed while the record is active must not be presented as managed closure.

## 9. Error and preservation behavior

`task new` creates only a new task directory and its contract draft; an existing destination is an error. Commands preserve unrelated files. Read and syntax failures name the file and corrective action without dumping its contents. Unknown schema versions reject writes. Root/path selection errors never fall back to another project.

Task lifecycle commands do not change global configuration, scientific knowledge files, the shared skill repository, or live Trellis tasks. Project init creates missing orientation and integration files as specified below. See [INTEGRATION](INTEGRATION.md) for separately invoked host setup and [READINESS](READINESS.md#limitations) for the guarantee boundary.

## 10. Project initialization (v0.2)

`init` operates on the existing explicitly selected project root. It creates `tasks/`, the five `research/` orientation templates, `.agents/skills/research-task/`, and `.rctl/project.json` with schema version 1 and a nullable project-relative `vault` path. This is static configuration, not a task record or implicit current-task selection. The CLI remains usable without initialization.

`--vault PATH` selects an in-root directory outside control directories. A new vault receives packaged note templates and ownership instructions; an existing directory is associated without modifying its contents. Omitting the option preserves an existing binding; an explicitly different binding is rejected before writes, with manual reviewed migration required. Unknown manifest fields/versions reject initialization.

All intended paths are checked before writing. Existing regular files are preserved and listed, including customized orientation or host files; file/directory collisions and paths outside the selected root reject the operation. Missing files use exclusive creation. A failed filesystem operation may leave an incomplete scaffold; rerunning fills missing project files without replacing earlier content. A partially created vault needs explicit repair because existing vault contents are never populated automatically. Existing files are not certified compatible merely because they are preserved.

`--codex` creates missing `.codex/hooks.json`, `.codex/config.toml`, and project-local loading instructions using the installed entrypoint. Existing host files are preserved and named as needing review; initialization does not merge definitions, grant trust, change global config, start a host, or run a task. Repeated initialization must not change task records or file contents. The local task skill points to packaged workspace guidance for Git/data boundaries, legacy migration, and optional vault use.

## 11. Discovery, handoff summaries, and installation inspection (v0.3)

`task list` inspects immediate directories under `tasks/` containing `contract.md` or
`.rctl/record.json`. Missing `tasks/` yields an empty list. It never recursively discovers
run artifacts, selects a task, executes checks, or writes an index. Entries are sorted
by project-relative path. Unavailable entries retain their error and null phase even
when filtering a phase; they cannot silently disappear. Managed titles come from the
retained governing contract, draft titles from the proposed contract.
An existing non-directory `tasks/` is an invalid input. In-root task aliases are
deduplicated by resolved task path and use the canonical path and task ID. Reading a
managed title validates the retained contract structure without requiring its evidence
paths to remain usable; existing verification applicability still reports unavailable
evidence. Verification retains its project-root path constraints. Text list titles are
collapsed to one line and limited to 160 characters; JSON retains the complete title.

`status.handoff` contains nullable `next_action` and `blockers`, extracted from explicit
`## Next action` / `## Blockers` sections or legacy optional-bullet `Next action:` /
`Blockers:` fields. Fenced content cannot define headings or fields, but code blocks
inside an identified field are retained verbatim. Inline backtick spans do not open
fences. Repeated, empty, or unrecognized
fields are not inferred; missing/ambiguous next action is a read warning, not a mutation
error. Checkpoint still preserves the supplied text. Lifecycle `next_action` remains
separate. Closed/cancelled handoffs are historical. Context reserves bounded space for
reported next action and blockers before long prose, retains warnings and source paths,
and bounds its added handoff JSON fields too. Neither record nor project schema changes.

`doctor` completes a read-only inspection of project binding, bound vault existence,
and packaged task-skill differences. `--codex` additionally inspects project JSON and
inline TOML hooks, executable/root addressing, duplicates, and explicit disabling.
Absent feature settings are inherited, not proven broken. Differences mean review
needed, not proof of local modification or an outdated version. Unknown custom commands
are never executed. No global layers, hook trust, or actual delivery are inferred.
Inspection findings return success with `review_needed`; failures preventing inspection
use existing errors. Each finding names its source, observed status, and next action.
Symlinked in-root skill directories use their logical installed paths in findings.
Finder `.DS_Store` files are ignored and preserved; other local assets remain visible.
A missing local console entrypoint adds an unavailable finding without discarding
skill or host configuration diagnostics. Export with `--codex` still requires that
entrypoint and rejects before writing when it is unavailable.

`update export DIRECTORY [--codex]` writes current packaged skill candidates, scoped
diffs, inspection findings, and merge instructions to a new project-local directory.
Codex candidates are fragments, not replacements for unrelated configuration. Destinations
inside live control/knowledge directories are rejected. No snapshot, installation-history
schema, automatic application, or configuration merge is introduced. Init and existing
integration export semantics are unchanged.
