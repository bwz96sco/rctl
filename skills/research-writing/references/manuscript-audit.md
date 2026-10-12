# Referee-side manuscript audits

Use for a requested scholarly audit. The output is evidence-anchored findings;
author-side drafting/repair is a separate requested operation. Software/PR review
uses the repository's review workflow.

## Audit contract

Identify the manuscript/version, requested dimensions, available evidence and
output. Preserve any required reviewer independence. Inspect claims at stable
line or exact-span anchors and retain the wording relevant to each finding.
Choose dimensions justified by the claims: arithmetic, scope, methods, controls,
protocol, citations, proofs or figures. Use [proof checks](theory.md) when relevant.

## Verification and completion

Each substantive finding names the exact claim, discrepancy and observed evidence.
Separate evidence-backed defects, unresolved questions and judgment calls; inspect
plausible alternative explanations before reporting a defect. External facts such
as novelty, DOI, retraction or venue status need source checks.

Citation support can be `supporting`, `partial`, `limiting`, `contradicting` or
`unverified`. Missing coverage is limiting; contradicting evidence supports an
opposite result. An incomplete proof is not a false claim, and PDF-only absence
does not establish missing execution artifacts.

Complete when every requested dimension is inspected or explicitly blocked and
each material finding has bounded evidence. A bounded audit reports findings
without an unsolicited accept/reject verdict, misconduct claim or authorship
estimate. An audit leaves the source unchanged; repairs need their own scope.

For durable cases, retain existing project conventions or use the bound vault's
`_review/<case-slug>/`, otherwise `artifacts/research-review/<case-slug>/`. Optional
coverage statuses are `incomplete`, `blocked`, `findings_present` and
`ready_for_human_review`. An index can track requested multi-paper work; neither
coverage status nor an index supplies rctl closure or a cross-paper ranking.
