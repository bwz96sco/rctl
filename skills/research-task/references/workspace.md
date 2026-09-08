# Project initialization and workspace boundaries

Read this reference when initializing a project, associating a vault, or planning a migration.

## Initialize

Run `rctl init` from an existing selected project root, or use `rctl --root PATH init`.
For a new project with notes and Codex reminders, use `rctl init --vault note/main --codex`.
Choose the vault on first initialization. `.rctl/project.json` records only that static
binding; changing it later requires an explicit reviewed edit and any necessary note moves.
The CLI remains usable without initialization.

Initialization creates missing `tasks/`, five `research/` orientation files, and this
project-local skill. It preserves existing files and reports them. An existing vault is
associated without editing its contents; a new vault receives note templates and guidance.
All generated files and vault paths stay inside the selected root. No Git repositories,
remote services, data moves, task migrations, global configuration, or trust grants occur.
With `--codex`, inspect `.rctl/codex/README.md` and preserved host files before launch.
An interrupted filesystem write can leave partial scaffolding: inspect it and rerun for
missing project files; repair a partially created vault explicitly, since existing vaults
are never populated automatically. Init does not upgrade customized templates or skills.

## Inspect and review updates

Use `rctl doctor` to compare the project-local task skill with the current installed
package and inspect the vault binding. Add `--codex` for project-local hook/configuration
inspection. Findings describe static configuration; host trust and actual delivery
remain separate. Differences require review and do not establish who edited a file.

Use `rctl update export .work/rctl-update --codex` with a new destination to generate
candidate skill files, scoped host fragments, and diffs. Compare each needed change,
preserve intentional local edits and extra files, and apply reviewed changes only within
the authorized project. Host candidates are merge fragments, never entire replacement
configurations. Keep one copy of each rctl handler across project JSON and inline TOML.
The command never applies updates or changes the global installation; rerunning init
continues to preserve existing files.

## Decide boundaries before restructuring

Inspect existing Git roots, remotes, ignore rules, storage paths, note links, manuscript
sources, and task records. Preserve existing layout unless a concrete problem warrants a
change. A single repository works; separate `code/`, `paper/`, and `note/` repositories are
an option when ownership or publication boundaries differ. Do not create nested Git roots
or rewrite remotes merely to match a template.

Keep datasets, models, large run outputs, credentials, local app state, and provider logs
outside tracked source or under appropriate ignore rules. Check actual tracked files before
claiming an ignore rule protects them. Public/private decisions follow existing user intent;
ask only when a necessary decision is missing. A static workspace manifest may describe
repository and storage locations, but must not duplicate task phase or current-task pointers.

## Vault use

Read `.rctl/project.json` to locate the vault, or keep the project's existing note convention
when no vault is bound. Notes hold literature evidence, reasoning, derivations, experiment
interpretation, and drafting material. Scientific checklists and review coverage belong to
the relevant domain artifact. `tasks/TASK/contract.md` owns the bounded agreement;
`result.md` owns its findings; `state.md` is an optional handoff; `.rctl/record.json` inside
that task owns machine acceptance and phase. Link notes to these files instead of copying
live status. `rctl task list [--phase active]` discovers immediate task directories under `tasks/`;
other task locations still require explicit paths. Large raw evidence stays with the runner and is referenced explicitly.

Project `research/` files contain slow-changing scientific intent, verified resources,
audited baselines, and refuted/parked/unexecuted routes. Promote only established findings
at closeout. A vault index is navigation, not an acceptance ledger.

## Existing-project migration

Inventory the files and their owners first. Map each old task agreement, result, handoff,
and evidence source to its destination; preserve historical records and raw artifacts.
Do not copy Trellis status or a legacy validator's success into a new accepted rctl record.
If continuing old work under rctl, create and fill a native contract, cite retained prior
work as supplied evidence, and begin before new dependent execution. Record migration and
comparison changes explicitly. New closure requires the current criteria, execution checks,
and evidence-based reviews. Historical closed records need no synthetic re-verification.

For a requested move, prepare a concrete source-to-destination map, adjust references,
check the affected links and commands, and report any authority or evidence gaps. Review
shared instruction changes separately from live project migration. Automatic initialization
does not perform this migration. Optional note graph guidance: [graphify.md](graphify.md).

## Project reminders

Reminders read PROGRAM.md's `## Goal` and optional `## Current guidance`, plus
ROUTES.md's `## Reuse Rule`. Keep these sections concise and link detailed evidence.
Existing projects may add Current guidance in place; no record or manifest migration
is needed. Repeated sections, unfinished placeholders and unreadable files produce
warnings. Missing research files leave task commands usable. Init preserves existing
files, so reconcile new guidance sections with the actual project content.
