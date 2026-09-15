# Paper register template

Use one register per question. Keep the compact table and put provenance below it, keyed by the same paper ID. Link existing reading notes and reused provenance with their original check dates; refresh facts whose current state matters to this search. Fill unknowns with the missing fact and reason rather than inferring them. `metadata_status` describes paper identity; publication verification is recorded separately.

## Source rules

- Verify acceptance/publication through official proceedings, publisher records, conference programs, or official decisions. A PDF template, copyright line, author claim, or submission listing alone does not verify acceptance. Record main conference, workshop, and other tracks explicitly. An unsuccessful venue lookup establishes an unresolved status, not rejection.
- Preserve the located preprint version and any verified formal version, with their respective identifiers and years. Record established publication status separately from unresolved claims; a verified preprint can coexist with an unverified acceptance claim.
- Record author affiliations as stated in the relevant paper version, with a page anchor or official source. Map institutions to authors or author subsets. Name a lab, group, or PI relationship only when the paper or an official group page establishes it; otherwise use `not established`. Shared affiliation alone does not establish a common research group.
- For every publication or affiliation claim, retain the source URL or file/page, check date, and verification status. Venue and team provenance help assess coverage; claim strength comes from full-paper evidence in `$research-literature`.
- A Zotero item key establishes identity, while collection membership requires a separate check. Keep an existing key for a paper found elsewhere in the library; use `not_registered` only after a library search and `unchecked` when no check was made.

```markdown
# <topic>

Target question: <user's question verbatim>
Scope: <date/venue bounds, supplied seeds, constraints>
Updated: <YYYY-MM-DD>
Project collection: <link to zotero-collection.md>
Reused corpus: <register/note links, or none>

## Papers

| id | zotero_key | title | year | role | metadata_status | access | status | decision | relevance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <persistent ID> | <item-key / not_registered / unchecked> | <title> | <year of listed version> | <role> | <verified / conflicting / unverified> | <access> | <candidate / skimmed / read / blocked> | <retained / dropped + reason> | <relation to question> |

## Paper provenance

### <paper-id>

- Discovery: <query, seed/citation, venue, author/group, or ecosystem route; link to search event or reused record>
- Versions: <located preprint ID/version/year; formal DOI/URL/year when verified>
- Publication: <preprint / submitted / accepted / published / unknown>; <venue, year, track>
- Publication evidence: <source; checked YYYY-MM-DD; verified / conflicting / unverified; unresolved claims or lookup limitation>
- Authors and affiliations: <authors or subsets -> institutions; source/page; check date; verification status>
- Research group: <explicitly sourced group/relationship with source/date, or not established>
- Zotero membership: <in_project / library_only / not_registered / unchecked>; <collection key, check date/source or blocker>
- Evidence note: <existing note link and version read, or not yet read — scientific evidence quality not assessed>

Repeat the provenance entry for each retained paper. Exclusions need only enough identity and a reason to explain the decision.

## Search coverage

| Date | Route and scope | Query / seed / source URL | Result, gap, or reuse |
| --- | --- | --- | --- |
| <YYYY-MM-DD> | <keywords, venue cycle, citation expansion, author/group, or ecosystem> | <reproducible query or source> | <retained IDs, coverage gained, or no useful additions> |

Covered roles: <core, closest candidates, baselines/evaluation, adjacent mechanisms, negative evidence>
Coverage assessment: <verified venue/publication-status mix; recurring author teams; material gaps>
Routes not covered: <relevant venue cycles, author/group sweeps, citation directions, or ecosystems omitted and why>
Stop reason: <why further searching is unlikely to change this answer, or the scope/budget/access limit reached>
```
