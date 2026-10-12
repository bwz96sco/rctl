---
name: paper-discovery
description: Build or refresh a deduplicated project Zotero paper pool and question-scoped register.
---

# Paper Discovery

Build a sufficient paper pool for the question. Zotero owns item identity and
bibliographic metadata; the question register owns coverage and relevance.
Paper reading and cross-paper answers use research-literature. Ad hoc scholarly
lookups can use paper-search-cli directly.

## Search and write contract

Establish the question, scope/date window, supplied seeds and requested output:
a read-only list or durable project-pool update. Reuse relevant registers, notes
and verified identities. Choose keywords, venues, citation directions, author
pages or benchmark ecosystems according to the coverage gap; no route quota applies.
Use `$paper-search-cli` for scholarly search/identifiers/citation graphs and
`$smart-search-cli` for official venue, author, benchmark and repository pages.

For durable work, keep exactly one Zotero collection per repository across questions.
Read the bound vault in `.rctl/project.json` or retain the existing note convention.
Reuse `zotero-collection.md`; a new binding records repository, library, collection
name and key under `<vault>/literature/` or `artifacts/research-literature/`.
Verify the binding through `$zotero-cli`; resolve an ambiguous existing match before
creating another collection. Keep one `register.md` per question.

## Before returning or writing

Each retained paper has a verified or visibly unresolved identifier, title,
authors, year/version, relevance and discovery source. Verify publication/venue
claims before relying on them. Collect affiliation/team provenance when it bears
on the requested search or coverage; otherwise leave it uncollected rather than
require unrelated lookups. Abstracts establish candidate relevance, not validated
methods/results.

Before every Zotero write, deduplicate against the entire Zotero library using
persistent identifiers first, then title/authors/year. Reuse the existing key,
preserve the version actually read and hold ambiguous matches as conflicts. Follow
zotero-cli's mutation workflow and verify item state and collection membership
after writing. Keep `zotero_key` distinct from membership and `metadata_status`
distinct from publication verification.

A durable pool update includes adding retained verified items to the bound
collection and maintaining [register-template.md](register-template.md) with
applicable provenance, Search coverage and a stop reason. Preserve prior search
events and reading evidence. Ad hoc lists may stay compact in chat.

## Completion

Report the retained candidates, identity/access gaps, coverage and stopping basis.
For a pool update, additionally report added/reused items, verified membership or
explicit blockers, metadata changes and conflicts. Hand supplied papers and
existing records to research-literature when reading is requested.

Pool updates authorize bibliographic items, verified metadata and membership.
Attachment uploads, deletion/merging, reorganization, subscriptions and sharing
need an explicit request. Keep raw provider output outside the literature artifact.
