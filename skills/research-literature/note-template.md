# Paper record template

You are reading one or more papers for a target question. For each paper, return one record file in the format below. Later agents cite these records by ID; nobody reads them as prose. Write atomic, self-contained records, one line each where possible, and nothing else: no overview, field map, method walkthrough, section-by-section summary, or reflection. Record only what bears on the target question or the paper's main claims; length follows the evidence, not the paper.

Rules:
- Every record has an anchor (section, page, figure, table, or equation), an evidence basis (`text`, `figure`, `table`, `equation`, or `code`), and a confidence (`high`, `medium`, `low`) with a short caveat when needed.
- `result` and `null` records give the exact value, the comparator, the sample size, and the uncertainty (interval, seeds, or `not reported`).
- `limitation` records quote the authors verbatim. If none exist after a full-text check, write one `limitation` record: `not found after full-text check: <sections checked>`.
- `defect` records are your inferences or observed failures, never author statements. Type each as `assumption`, `evaluation`, `mechanism`, or `scope`, and mark it `observed` or `inferred`. Look for asserted but undemonstrated problems, assumptions that fail in the intended setting, missing or unequally resourced baselines, uncontrolled confounds, leakage, metrics that hide failure, narrow data, and claims that exceed the results. Distinguish failure to establish a claim from evidence against it. Report only defects the evidence supports, or one record `no material defect established`.
- A `test` record names the observation that would show a defect matters, which defect it tests, and what it would need (existing data, replay, or new runs).
- With partial text or an abstract, write only the records the source supports and mark the rest `not assessable from available access`.

```markdown
# <paper-id>: <short title>

Version read: <arXiv id+version/date, DOI, or supplied PDF identity>
Publication: <venue/year/track or preprint>; <source and check date, or "unverified">
Metadata status: verified | conflicting | unverified
Access: full_pdf | partial_text | abstract_only
Read: <F (sections read) | P (sections read) | A>
Code / data: <stated release; checked link and what was inspected, or "not checked">

R1 [setting] <decision or object handled; required inputs; what must hold> — <anchor> — <basis>, <confidence>
R2 [result] <claim: value vs comparator; n; uncertainty; conditions> — <anchor> — <basis>, <confidence>
R3 [null] <reported null or negative result with numbers> — <anchor> — <basis>, <confidence>
R4 [limitation] "<verbatim author statement>" — <anchor> — text
R5 [defect: <assumption|evaluation|mechanism|scope>, <observed|inferred>] <defect and why it matters; author-acknowledged yes|no> — <anchor> — <basis>, <confidence>
R6 [test] for R5: <observation that would show it matters; data or runs needed>
R7 [relation] <supports | limits | contradicts | direct overlap | closest_candidate | mechanism neighbor | irrelevant>: <why; affected part of the question; strongest support and main limitation> — <anchors> — <confidence>
R8 [lead] <unresolved concept, technique, or cited work; why it matters> — <anchor>
```

`closest_candidate` marks a plausible neighbor; final closest-prior selection belongs to `$research-synthesis`.

Return only the record files, one per paper, with no commentary around them.
