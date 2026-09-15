---
name: research-review-case
description: Run evidence-bound referee-side audits of scholarly manuscripts, submissions, claims, citations, proofs, evaluation designs, or novelty without issuing paper verdicts. Use for bounded scholarly audits or durable referee cases. Exclude software and pull-request review.
---

# Research Review Case

Inspect one manuscript without repairing it and without accept/reject decisions. Findings are anchored observations; verdicts belong to humans.

## Workflow

1. **Load the submission once** with stable line or exact-span anchors; copy claims verbatim.
2. **Select dimensions by the claims** — arithmetic, scope, methods, baselines, seeds, protocol, citations, proofs, figures — only where evidence can support findings.
3. **Compare claims against evidence.** Each substantive finding gets an exact anchor, the discrepancy, observed evidence, false-positive risk, and its unresolved questions kept separate. Findings above `info` require evidence; conclusions never exceed available observability.
4. **Grade citation support** as `supporting`, `partial`, `limiting`, `contradicting`, or `unverified`. Missing or not-evaluated scope is `limiting`; use `contradicting` only when observed evidence supports the opposite result.
5. **Close each dimension** or mark it explicitly blocked. Durable case status describes evidence coverage only: `incomplete`, `blocked`, `findings_present`, or `ready_for_human_review`.

Complete when every requested dimension is closed or blocked, each substantive finding has an exact anchor with bounded evidence and false-positive risk, and unresolved questions remain visible.

When governed by an rctl task, use the project-local research-task skill for its contract, result, handoff, phase, and acceptance. Case coverage and dimension closure do not close that task. Read `.rctl/project.json` for the bound vault; keep the existing note convention when unbound.

## Multi-paper work

A plain `cases.md` index records cross-paper review coverage: one case root per manuscript, one row per case (paper id, root, status, blocker). Reviewer independence stays explicit; sibling findings stay unread until a case closes. No registries or rankings — synthesis across papers is human-authorized.

## Rules

- Never edit the audited paper, repository, or results.
- No paper verdicts, accept/reject recommendations, misconduct claims, authorship probabilities, or cross-paper rankings; style impressions carry zero verdict weight.
- Source-check external facts (SOTA, "first", DOI, retraction, venue status) before relying on them.
- Distinguish incomplete proof from false claim; PDF-only absence does not prove missing experiment artifacts.
- Durable cases: `<bound-vault>/_review/<case-slug>/` when a vault is bound, else the existing note convention or `artifacts/research-review/<case-slug>/`.
