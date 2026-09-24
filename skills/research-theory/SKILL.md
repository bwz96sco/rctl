---
name: research-theory
description: Derive, formulate, prove, repair, and audit research-level mathematical claims, theorem statements, proof obligations, assumptions, counterexamples, and asymptotics. Use when mathematical validity affects a research contribution or manuscript proof. Exclude textbook exercises and routine symbolic algebra.
---

# Research Theory

Turn formula ideas, theorem drafts, and proof sketches into explicit derivations, proofs, counterexamples, or precise unresolved reports. Try to break a claim before proving it. For an audit, report findings without editing the source claim; formulation or repair must be part of the request.

## Workflow

1. **Freeze the claim.** Exact mathematical object, notation, domains, assumptions, quantifiers, limit order, and non-claims. Missing load-bearing information blocks an unconditional conclusion. For formulation work, proposed assumptions may be explicit design choices, not facts silently attributed to an existing claim.
2. **Derive stepwise.** When the formula or invariant is not fixed, derive it, distinguishing identities, theorem applications, approximations, heuristics, and conjectures. Record approximation boundaries and constant dependence.
3. **Try to break it.** Before proving or repairing: boundary and degenerate cases, toy examples, dimensional consistency, numerical or symbolic checks when feasible. Read [computation-checks.md](references/computation-checks.md) when a numerical check's validity or local software usability is unresolved. Record any counterexample found or the scope actually checked.
4. **Discharge obligations.** For every nontrivial theorem or lemma applied, expose its hypotheses and where each is discharged. Separate proven facts, stated assumptions, heuristics, conjectures, and blockers.
5. **Resolve the stated claim.** Supply a proof, a valid counterexample, or the precise open obligation. When repair is requested, state and justify a minimal explicit revision separately from the original. In an audit, a possible repair is a proposal, not an edit or a proof of the original. Never silently strengthen assumptions, narrow scope, change quantifiers, or hide conditionality.
6. **Classify each claim.** Use `proved`, `refuted` (with a counterexample), `not_proved` (an unresolved argument), or `blocked` (missing required inputs). An incomplete proof is not a refutation. Report original and revised claims separately; only discharged obligations justify `proved`. These are note-level judgments, not rctl phases or machine acceptance.

Complete when the claim, assumptions, and quantifiers are explicit, the break attempt is recorded, every obligation is discharged or listed open, and the proof status is assigned.

## Rules

- Durable artifacts: read the project-relative `vault` binding in `.rctl/project.json`, otherwise retain the existing note convention. Reuse the current note; for new durable work use `<vault>/theory/<topic-slug>/`, or `artifacts/research-theory/<topic-slug>/` without a note root. Manuscript LaTeX stays in the paper repo.
- Route prior-theorem and citation work to `research-literature` and manuscript integration to `research-writing`. Small numerical or symbolic checks may stay inline; formal comparative experiments belong to `research-experiment`.
