---
name: paper-discovery
description: Project-scoped paper discovery and Zotero collection curation. Use when building or refreshing a research paper pool, expanding from venues, seeds, citation graphs, authors, or benchmark ecosystems, deduplicating candidates, or saving verified papers to a project's Zotero collection. Full-paper reading belongs to research-literature.
---

# Paper Discovery

Build the smallest sufficient, reusable paper pool for a research question. Zotero owns item identity and bibliographic metadata; the question register owns coverage, triage, and project-specific relevance. Hand retained papers to `$research-literature` for full-paper evidence extraction.

## Project collection

For durable work, map each research repository to exactly one Zotero collection. Read the project-relative `vault` binding in `.rctl/project.json`; when unbound, retain the project's existing note convention. Reuse the existing collection binding; for a new one use `<vault>/literature/zotero-collection.md`, or `artifacts/research-literature/zotero-collection.md` without a note root:

```text
repository: <Git remote or repository name>
zotero_library: <user or group:id>
collection_name: <name>
collection_key: <key>
```

Keep one collection across all questions in that repository; keep one `register.md` per question under `literature/<topic-slug>/`.

An ad hoc paper-list request may remain read-only and in chat. A request to build or refresh a project's paper pool includes adding retained, metadata-verified items to its bound collection.

## Workflow

1. **Bound the search.** Fix the research question, relevant date or venue window, supplied seeds, and whether the user wants an ad hoc list or a durable project-pool update.
2. **Reuse project state.** Read the collection binding, existing question register, and current collection contents before searching. Look up relevant papers in other project registers and reading notes by identifier; link reusable evidence so a new question does not silently lose previously read work. Use `$zotero-cli` to verify the bound collection key. When a durable project has no binding, inspect existing collections before creating one named for the repository, then record the returned key. Resolve an ambiguous existing match with the user instead of creating a second collection.
3. **Choose search neighborhoods.** For field or closest-prior coverage, identify venue families from both the method community and application domain, then choose routes that can fill a meaningful gap:
   - Direct keyword and semantic search for the question, closest competitors, baselines, evaluation work, adjacent mechanisms, and negative evidence.
   - Relevant venue proceedings and OpenReview cycles. For AI, starting points include ICML/NeurIPS/ICLR, ACL/EMNLP/COLM, CVPR/ICCV/ECCV, AAAI/IJCAI, KDD, and field-relevant journals such as TPAMI, JMLR, TMLR, TKDE, or Nature Machine Intelligence. Adapt the list to the field, advisor guidance, and local citation practice; venue is a discovery route, not a quality verdict.
   - Seed expansion backward through references and forward through citations, including work that extends, disputes, or evaluates the seed.
   - Repeatedly relevant authors, labs, and their recent publication or project pages.
   - Dataset, benchmark, leaderboard, code, project-page, and model-hub ecosystems, including compared methods in recent experiments.
   - For recurring refreshes, arXiv categories, venue announcements, Hugging Face Daily Papers, Scholar alerts, and other recommendation feeds. Treat social or recommendation posts as leads whose paper identity still requires verification.

   Use `$paper-search-cli` for scholarly search, identifiers, and citation graphs. Use `$smart-search-cli` for current official venue lists, author or lab pages, benchmark sites, leaderboards, repositories, and project pages.
4. **Triage and verify.** Retain papers that may change the answer, closest-prior set, or evaluation boundary. Verify persistent identifiers, title, authors, and year. For each retained paper, record the discovery route, publication status and venue/track, and author affiliations using the source rules in [register-template.md](register-template.md). Keep unresolved fields explicit with their source or lookup limitation. Abstracts support candidate relevance, not method or result claims; scientific evidence quality remains unassessed until reading.
5. **Deduplicate before every write.** Search the entire Zotero library, not only the project collection. Match persistent identifiers first, then normalized title plus authors and year. Reuse an exact existing item and add it to the project collection; never create a second item merely because the first belongs to another collection. Hold ambiguous matches as conflicts. When a formal publication matches an existing preprint, record the verified publication metadata while preserving the preprint identifier/link and the version used by reading notes. Surface uncertain version matches instead of overwriting them. Follow `$zotero-cli`'s write workflow and re-read the item and collection membership after mutation, using current server state if local sync has not caught up.
6. **Update the register.** For durable work, use [register-template.md](register-template.md) for the table, per-paper provenance, and `Search coverage`. Keep `zotero_key` separate from collection membership and `metadata_status` separate from publication verification. Typical roles are `core`, `closest_candidate`, `baseline_evaluation`, `adjacent`, `negative`, and `watchlist`; `read` remains reserved for full-paper work by `$research-literature`. Keep plausible exclusions as `dropped` with a reason. When refreshing an older register, fill provenance for retained papers in the current scope and preserve historical search events. Reconcile bibliographic and Zotero fields in existing notes for papers touched by this update, preserving the version actually read and its scientific content. Do not repeat an unchanged query window unless this is an explicit refresh.
7. **Hand off the corpus.** Report added or reused items, bibliographic updates, collection membership changes, conflicts, and retained-but-unavailable papers. Summarize the verified venue/publication-status mix, recurring author teams, and material coverage gaps from the recorded provenance. Point `$research-literature` to the binding, register rows, and corresponding provenance entries when reading is requested.

A read-only list completes when every retained candidate has verified or explicitly unresolved identity and provenance, relevance, and stated search coverage; this can stay compact in chat. A durable project-pool update additionally requires a resolved project collection, a whole-library duplicate check before writes, one Zotero key and verified membership or an explicit blocker per retained paper, a completed register, and a `Search coverage` stop reason. Unknown publication or group information stays visible and does not by itself block reading a relevant paper.

## Boundaries

- Within a durable pool update, add bibliographic items, update verified bibliographic metadata for the same work, and add collection membership. PDF upload or attachment, deletion, merging, bulk reorganization, alert subscription, and sharing changes require an explicit request.
- Do not deep-read papers, write evidence notes, compare findings across papers, or make novelty claims. Route those to `$research-literature` and `$research-synthesis`.
- Keep raw provider output outside the literature artifact.
