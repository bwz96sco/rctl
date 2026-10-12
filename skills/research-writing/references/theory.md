# Mathematical claims and proof checks

Use this reference when a research argument depends on a derivation, proof or
counterexample. It supplies checks and reporting conventions, not a fixed proof
strategy. Routine calculations can stay inline.

## Claim contract

Identify the exact mathematical object, notation, domains, assumptions, quantifiers,
limit order and intended conclusion. For formulation work, proposed assumptions
are design choices; they are not facts attributed to an existing claim. A proof
audit inspects the stated claim; changing or repairing it follows the request.

## Before assigning a conclusion

Separate identities, theorem applications, approximations, heuristics and
conjectures. Expose the hypotheses of each load-bearing result and where they are
discharged; retain approximation boundaries and constant dependence.

Choose discriminating checks for actual uncertainty: boundary/degenerate cases,
dimensional consistency, a counterexample construction or a numerical/symbolic
check. Consult [computation checks](../../research-experiment/references/computation-checks.md)
when that check's validity or execution remains unresolved, reusing current evidence.
The scope of a break attempt bounds what it establishes.

Report a proof, a valid counterexample or the precise open obligation. A requested
repair states its revised assumptions/conclusion separately from the original.
An incomplete proof does not refute a claim. Preserve quantifiers and scope;
unresolved load-bearing information prevents an unconditional conclusion.

When a status is useful, use `proved`, `refuted`, `not_proved` or `blocked` per claim.
Only discharged obligations justify `proved`; `refuted` needs a counterexample.
These describe the argument, not rctl phase or machine acceptance. Complete with
the explicit claim, evidence, discharged/open obligations and bounded conclusion.

Reuse the current proof/note and project convention. Manuscript LaTeX remains in
the paper repository; new durable theory notes can use the bound vault's
`theory/<topic-slug>/` or `artifacts/research-theory/<topic-slug>/` when unbound.
