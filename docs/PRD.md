# rctl Product Requirements

Baseline: 2026-09-05. The v0.1 release is complete; the user-authorized v0.2 increment adds project initialization and research-skill migration. v0.3 adds task discovery, prioritized handoff summaries, and candidate-only installation maintenance. v0.4 adds independent project reminders and history reuse before experimental planning.

## Problem and evidence

A research agent can start without settling what would count as done, lose the current agreement across sessions, or report completion after checking document structure rather than the underlying evidence. The operator then has to reconstruct scope and repeat the verification request.

The retained Pinyin-VSR pilot demonstrated a smaller useful loop: a contract, optional handoff, result, local task skill, and context hook supported two fresh sessions and a correct negative closeout. The pre-migration `research-experiment` skill contained open and close gates with Trellis-specific task plumbing; v0.2 moves that integration to native rctl tasks. Its result validator checks structure and lineage; substantive evidence review remains a separate responsibility. See [sources](SOURCES.md).

## Intended user and outcome

The initial user is a cooperating researcher using an agent on one local workstation. A task may span sessions and refer to remote experiment artifacts, while rctl itself handles local contracts, verification records, and reminders.

The desired outcome is that the researcher can inspect what was agreed, what was checked, and why a task is complete without reconstructing the conversation. The agent retains freedom to choose the execution method within the agreement.

## First release scope

Support two task kinds: `exploration` and `analysis`. Exploration closes with bounded findings and a next question or stopping reason. Analysis evaluates supplied evidence against a defined question; retained-evidence comparison is the first complete example. Neither kind grants permission for new remote jobs.

Ship a local Python CLI, readable task templates, small machine records, command and review checks, a host-neutral task skill package, and a tested Codex reminder adapter. Use one new, bounded real task to validate the arrangement after synthetic acceptance tests. Portability claims require actual host evidence.

## Requirements

| ID | Requirement | Observable user benefit |
|---|---|---|
| R-01 | A new task has a question, scope, constraints, stopping conditions, and named acceptance criteria before `begin`. | The agent and user can identify the same finish line. |
| R-02 | Each criterion specifies a check method, evidence locations, and the failure that changes the next action. | Verification is designed before results are examined. |
| R-03 | `begin` retains the governing contract; material changes require an explicit amendment reason. | The operator can distinguish the original comparison from later work. |
| R-04 | Execution tools and sequence remain agent-selected unless constrained by the contract. | The process does not require a fixed research workflow or phase ontology. |
| R-05 | Verification reports show every required criterion, method, actual result, evidence references, and source of judgment. | Structural validity, execution success, and scientific review remain distinguishable. |
| R-06 | `close` succeeds only with a current passing verification and a complete result. | A prose completion claim cannot itself become verified closure through the CLI. |
| R-07 | Negative and bounded inconclusive findings can close; missing required verification cannot. | The system does not encourage threshold changes or repeated experiments until a win. |
| R-08 | An optional handoff records last verified progress and next action; a new session can recover it. | The task survives conversation loss without a transcript dependency. |
| R-09 | Reminders load the selected contract, handoff, and verification status without executing checks or changing task state. | Context delivery does not become another research controller. |
| R-10 | Task selection is session-local and explicit; ambiguous or missing selection is visible. | A reminder does not silently route to another task. |
| R-11 | Core commands work without a host, skill, framework, network, or LLM. | Research records remain useful from a normal terminal. |
| R-12 | Host installation is reviewable, preserves unrelated configuration, and has real delivery evidence. | Copied configuration is not mistaken for working integration. |
| R-13 | Repeatable project initialization creates missing orientation, task-skill, and optional vault/host files while preserving existing content and explicit vault selection. | A new project has one discoverable entry point without manual template copying. |
| R-14 | Domain skills use native task contracts/results and retain domain-specific evidence checks without maintaining a competing task lifecycle. | Existing research workflows can use rctl without conflicting state files. |
| R-15 | Read-only task discovery lists conventional task paths, phases, and verification applicability, keeping damaged entries visible. | Find work without maintaining a second status index or selecting a task implicitly. |
| R-16 | Explicit handoff next steps and blockers survive bounded reminders independently of lifecycle advice. | Resume concrete work even when a handoff is long. |
| R-17 | Read-only installation diagnostics and candidate exports compare packaged project assets without replacing live content. | Review skill and hook updates without losing local changes. |
| R-18 | Project reminders survive missing task selection and task read failures, using explicit current research sections. | Planning retains project goals and corrections. |
| R-19 | Experiment planning cites related history, the unanswered question, and the decision new evidence changes. | Repeated mechanisms require a substantive reason. |

## Typical use

The researcher requests a retained-evidence comparison. The agent creates a draft contract from that request, specifies arithmetic checks and an evidence review, then begins within existing authorization. It inspects inputs and saves a handoff when the session pauses. A fresh session reads the same contract and handoff, performs the analysis, writes the result, and runs the declared checks. If the evidence shows no improvement, the result can still satisfy the contract. The agent closes the task with that bounded conclusion.

Only ask for missing input when it changes scope, authority, or the acceptance decision. Writing or freezing a contract does not introduce a mandatory approval ritual. Human review is one possible verification source, not a default extra approval stage.

## Non-goals

- Experiment submission, remote monitoring/retry, DAG scheduling, or resource allocation.
- Replacement of project research knowledge, long-form notes, run storage, or memory tools.
- SQLite, general artifact snapshots, content-addressed storage, distributed coordination, request-id protocols, or a generic workflow language.
- Authentication, independent approval identities, automatic scientific verdicts, or mandatory multi-agent review.
- Automatic migration of Trellis tasks, installation into shared skills, Git initialization, commits, pushes, or directory renaming.
- Claude Code support, Stop-triggered repair loops, subagent delivery, or Web/MCP interfaces in the first release.

## Release success

Every acceptance case in [ACCEPTANCE](ACCEPTANCE.md) must have observed evidence before v0.1 release. The decisive product test is two fresh sessions completing a new bounded task from records, with the contract preserved, material changes explicit, real reminder delivery, and a justified closeout. At least one synthetic case must close with a negative finding, and one must remain unclosed because evidence is insufficient.

Preparation readiness is tracked separately in [READINESS](READINESS.md). Preparing this PRD does not count as any product acceptance test passing.
