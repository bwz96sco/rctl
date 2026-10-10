---
name: research-literature
description: Question-scoped full-paper reading that produces compact, anchored evidence records for agents to cite, including author-stated limitations, null results, and evidence-backed defects. Use when reading papers, checking claims or methods, or critiquing a paper's assumptions and evaluation. Paper discovery and Zotero curation belong to paper-discovery.
---

# Research Literature

Read the papers that matter to a target question and record what their evidence supports, where they break, and how a defect could be tested. Output is for later agents to cite, not for human reading: no overview, field-map, method-walkthrough, or reflection prose. Paper-pool construction belongs to `$paper-discovery`; cross-paper argument, field maps, and closest-prior selection belong to `$research-synthesis`.

## Workspace

Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse an existing topic directory; for a new one use `<vault>/literature/<topic-slug>/`, or `artifacts/research-literature/<topic-slug>/` without a note root. Read the repository-level `zotero-collection.md` when present. Keep `register.md` and `notes/<paper-id>.md` (one record file per paper) in the topic directory. PDFs stay in an ignored local archive.

## Workflow

1. **Establish the reading purpose and corpus.** Put the user's target question or reading purpose verbatim at the top of `register.md`, followed by supplied scope constraints. Use the existing register and project collection or the exact papers supplied by the user. Route requests for new papers, citation snowballing, or collection updates to `$paper-discovery`, then resume from its register.
2. **Select decisive papers.** Select papers capable of changing the answer, the closest-prior comparison, or the evaluation boundary. For a named paper, stay with that paper. For an existing corpus, prioritize retained `core` and `closest_candidate` rows; do not expand the corpus inside the reading pass.
3. **Establish access.** Resolve each selected row to its Zotero item, supplied file, or stable source, and identify the exact version read. Record access as `full_pdf`, `partial_text`, `abstract_only`, or `unavailable`; preserve the row's `metadata_status` (`verified`, `conflicting`, `unverified`) rather than re-running discovery. Bibliographic, affiliation, and collection provenance stay in the register; the record file carries only the fields in [note-template.md](note-template.md). Send save or refresh requests to `$paper-discovery`.
4. **Reuse before rereading.** Reuse an existing record file when its version, question coverage, and anchors are adequate. For an isolated missing or disputed claim, check the relevant source sections with their definitions and evaluation context, then add or amend the affected records and the checked scope. Reread only when a material version or question change exceeds a local check, contradictions cannot be resolved locally, or the user requests a fresh independent reading. Template changes alone do not justify rereading.
5. **Read with clean readers.** Start each reader without conversation history where the host supports it (`fork_turns: "none"`). One clean reader may take one paper or a small batch (about two to four) that bears on the same question. Give it only the paper texts, the target question, the needed register rows, the minimal project facts the question depends on, and [note-template.md](note-template.md). Report a requested reader configuration the host cannot provide rather than silently substituting it. Reuse a page-preserving text extraction and consult PDF pages for unclear equations, figures, or tables. Save each paper's records as `notes/<paper-id>.md`. Partial or abstract-only reading remains `skimmed`, and its records cannot support method, result, defect, or closest-prior conclusions. Escalate a concrete unresolved proof or experimental interpretation, with its source context, to a more capable model; this is not an automatic second reading.
6. **Close the reading state.** Update access, status, decision, and relevance in `register.md` without changing Zotero identity or search-coverage history. Flag discrepancies between the paper and the supplied provenance for `$paper-discovery` instead of silently replacing verified records. `read` means the full paper was read, including a documented earlier reading; a targeted check alone never promotes `skimmed` to `read`. Otherwise use `skimmed` or `blocked`.
7. **Route the result.** Send `lead` records that name missing papers to `$paper-discovery`. For a decisive paper whose interpretation depends on implementation details, inspect the released code and record what was inspected. Route reproduction of a result that could change the research decision to `$research-experiment`. When the user asks to compare papers, resolve contradictions, map the field, identify closest prior work, or answer across the corpus, invoke `$research-synthesis` after the decisive record files are ready.

For a full-paper assignment, complete when every requested or decisive `core` or `closest_candidate` paper is full-text read or explicitly blocked; adequate existing record files count. For a targeted claim check, complete when the requested claim is supported, corrected, or explicitly unresolved with the checked scope recorded. Every read paper has a record file tied to the version read; every material claim or defect has a record with an anchor, evidence basis, and confidence; and the file contains at least one `relation` record stating what the evidence supports for the question and its main limitation.

## Evidence boundary

- Keep author statements, observed results, and analyst inferences in separate record types; `limitation` records quote the authors verbatim.
- Abstract or partial access establishes candidate relevance only. Keep unresolved identifiers visibly `conflicting` or `unverified`.
- An absence claim names the full-text sections checked; otherwise write `not assessable from available access`.
- Paper-local defects are evidence inputs, not proof that a field-wide problem remains open.
- Ideas raised by reading appear only as `test` records tied to a defect or as `lead` records; develop questions or approaches elsewhere when requested.
- Literature and synthesis are optional evidence providers for ideation, never readiness gates.
