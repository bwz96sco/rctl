# References

Make every cited work identifiable through accurate metadata and a consistently formatted reference list. Review imported entries individually: an export from DBLP, Google Scholar, or another service is a starting record, not a finished bibliography. Bibliographic correctness and support for the sentence carrying the citation are separate checks.

## Establish the style and citation keys

Read the venue's bibliography requirements and the manuscript's existing style before normalizing entries. Reuse its bibliography database and citation convention. For a new convention, use first-author surname, year, and a short identifying keyword, such as `zhou2024symagent`. Keep keys unique and readable.

Preserve working keys in an existing manuscript unless renaming is part of the requested cleanup. When renaming, update every affected citation together. Merge duplicate records for the same work and reconcile their citations; check the actual publication version before treating a preprint and published article as interchangeable.

Start from DBLP when it covers the work, or from the official publication record or another verified source. Check uncertain titles, authors, venue information, dates, and identifiers against the relevant publication record using the main skill's lookup tools. Mark unresolved metadata in the working notes rather than filling it by guesswork.

## Match entry types and fields to the work

For BibTeX, use `@inproceedings` for a paper in conference proceedings and `@article` for a journal article. Use the appropriate type for other sources. Keep the source type and the manuscript's bibliography system consistent.

For ordinary paper entries, check `author`, `title`, `booktitle` or `journal`, and `year`, together with the applicable `volume`, `number`, and `pages`. These are common core fields, not a universal whitelist. Retain DOI, URL, publisher, or other fields when the source type or venue requires them, or when they are needed to locate the work. Remove redundant export metadata according to the chosen style.

- **Authors:** preserve verified names, order, spelling, accents, and name structure. A correct DBLP name format need not be rewritten for appearance. Keep the full known author list in the database and let the bibliography style handle displayed truncation to “et al.”
- **Volume and issue:** verify the journal's volume and issue number where assigned; preserve relevant proceedings volume information as well. Do not infer a missing value from a neighboring article or year.
- **Pages:** use the published page range, with BibTeX's `--` range notation. Some publications use article identifiers or assign no pages; retain the applicable locator instead of inventing pagination.
- **Year and version:** make the date, venue, and identifiers refer to the version actually cited. Resolve conflicting imported records before presenting the entry as verified.

## Preserve title capitalization

Keep the verified title wording and let the chosen style control ordinary title capitalization. Protect proper names, model names, and acronyms that must retain their case with braces, for example:

```bibtex
title = {{GPT}-4o mini}
title = {{Qwen3}-8B}
title = {{LLM-SR}: Scientific Equation Discovery}
```

These illustrate separate title fields. Protect the necessary terms instead of automatically bracing the entire title, which can prevent the style from applying its capitalization rules. Inspect the rendered list for inconsistent title case and lost capitals; the appearance of the raw `.bib` file does not establish the rendered result.

## Normalize venue names accurately

Use a consistent full name or accepted abbreviation for the same conference or journal, following the venue style. Keep spelling and capitalization consistent without erasing genuine differences between proceedings editions or publication titles.

Conference titles are not all built from the same pattern. Copy the verified title: it may contain an edition number, a year, or neither. If an ordinal is present, preserve the correct `1st`, `2nd`, `3rd`, `4th`, and subsequent forms. Do not add an edition number or “Proceedings of” when it is not part of the appropriate title.

For example, NeurIPS uses *Advances in Neural Information Processing Systems*. Treat its proceedings volume as volume metadata rather than inconsistently appending it to the venue name; preserve it where the style requires it. Apply the same principle to other venues: normalize presentation while retaining bibliographic identity.

## Draft and check

After bibliography edits in a buildable manuscript, follow the main skill's build rules and inspect the rendered reference list as well as the source entries. Fix unresolved citations, duplicate keys or works, parsing warnings, and visible formatting defects relevant to the change.

- **Identity:** each cited work has the correct type, authors, title, publication version, and available locator.
- **Completeness:** required volume, issue, pages or article identifiers, and other venue-required fields are present where applicable.
- **Consistency:** title protection, author rendering, venue names, and field presentation follow one style.
- **Integrity:** renamed or merged keys resolve, duplicate records are reconciled, and citations still support their attached claims.
