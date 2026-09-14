# Simplification acceptance evidence

Recorded on 2026-09-14 with Codex CLI 0.154.0 and GPT-6-Astra at medium reasoning
effort. The [verification record](../../SIMPLIFICATION-VERIFICATION.md) owns the
interpretation, commands, instruction repair, and limitations.

Each stage JSON retains exact launch argv and prompt, hook receipts with delivered
text, CLI responses, completed host events including source reads, and the final
response. Started-event duplicates are omitted. In compact stages only, repetitive
delivery-only helper stdout is replaced by its character count and first/last rows.
No scientific evidence output or failed command is omitted by that projection.
Original raw logs remain in the disposable project paths recorded in each launch.

| Stage | Baseline 82a5ec8 | Candidate |
|---|---|---|
| First session / long handoff | [first.json](baseline/first.json) | [first.json](candidate/first.json) |
| Fresh-session continuation | [resume.json](baseline/resume.json) | [resume.json](candidate/resume.json) |
| History and automatic compaction | [compact.json](baseline/compact.json) | [compact.json](candidate/compact.json) |
| Stale result and corrective closure | [stale.json](baseline/stale.json) | [stale.json](candidate/stale.json) |
| Final contract, record, result, review, handoff and execution logs | [task-final.json](baseline/task-final.json) | [task-final.json](candidate/task-final.json) |

The first three candidate stages used the initial wheel. The stale stage used the
final wheel with active-only checkpoint guidance; no runtime code changed between
these wheels. [doctor-final.json](candidate/doctor-final.json) records that all
project-local skill files matched the final installed package before that stage.

Package checks retain the [full initial wheel-smoke trace](wheel-smoke-before-guidance-fix.json)
and [final captured wheel-smoke output](wheel-smoke-final-captured.txt). The final
command exited 0; the capture explicitly marks the tool's stdout truncation.
All tasks and evidence are synthetic fixtures, not live research results.
