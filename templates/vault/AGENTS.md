# Research vault instructions

This vault stores scientific notes and interpretation. Read the project's `.rctl/project.json`
for its binding, then the selected task's `contract.md`, `result.md`, and `rctl status TASK`
before dependent managed work. Use the project-local research-task skill for lifecycle commands.

## Ownership

- rctl task directories own agreements, results, optional handoffs, and machine acceptance.
  Do not create another task-status registry, current-task pointer, or acceptance ledger here.
- Literature registers, proof obligations, claim-evidence maps, run matrices, and referee
  coverage remain domain evidence. Their labels describe scientific content, not task closure.
- Runner storage owns raw logs, metrics, configs, checkpoints, and large outputs. Notes link
  to that evidence and distinguish computed observations, supplied claims, and hypotheses.
- Code and final manuscript sources keep their established repositories. Do not move them
  into the vault or upload private artifacts without task authority.
- `research/PROGRAM.md`, `INVENTORY.md`, `BASELINES.md`, and `ROUTES.md` outside this vault
  receive only established, slow-changing facts promoted at task closeout.

## Note locations

Use the relevant domain skill's current artifacts rather than imposing a second numbered pack:

- `literature/<topic>/register.md`, `notes/<paper-id>.md`, and `synthesis.md` for a corpus.
  `literature-index.md` links to topic roots. Zotero owns citation metadata; follow the
  project's PDF storage policy. Keep raw search dumps and temporary PDFs in ignored storage.
- `ideas/<topic>/` for ideas, screening, shortlists, and explicit selection decisions.
  Preserve opportunity O# and candidate C# identities and their distinct provenance.
- `experiments/<topic>/` for interpretations and compact evidence notes linked to an rctl
  task and runner artifacts. No vault-owned experiment status or campaign queue is required.
- `computation/`, `theory/`, `figures/`, `slides/`, and `writing/` for their domain evidence
  and working notes; final artifacts keep the project's existing output locations.
- `intake/` for bounded audits of existing assets. Record provenance and comparability
  before reusing results; rerun expensive work only when a concrete trust gap requires it.

Use verified citation keys (`[@citekey]`) and traceable references. State unreadable sources
and unsupported claims. Never invent results or citations. Link existing notes when useful.
Write a dated observation when historical status matters; consult rctl for current phase.
See `_references/workflows.md` for note workflows and `_templates/` for optional templates.

## Optional note graph

Graphify is manual and optional. `.graphifyignore` excludes binary sources and app state.
Inspect source notes behind graph-derived claims. Graph output confers no scientific acceptance.
