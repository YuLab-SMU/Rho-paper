# Working on Rho-paper

Rho-paper owns the research proposal and the paper for Rho: the candidate
contribution, the single-cell walkthrough that makes it concrete, and the judgments
about what existing work already covers. Read [README](README.md), the
[manuscript](docs/MANUSCRIPT.md) and the [positioning record](docs/PAPER.md) before
changing any of them.

## Ownership

- This project owns claims, the scenario and related-work judgments. Implementation
  facts — what Rho, Rho-core and Rho-plugins actually do, at which version, with what
  evidence — stay with those owners. Cite them; do not restate them as this project's
  results.
- The proposal sets no requirements on unbuilt screens, plugins or acceptance
  criteria. Observed layouts, design values, limits and measurements belong in the
  implementation owner's records and are reached through them.
- A citation covers only the version recorded with it. Benchmarks, preference scores
  and reported successes of another system are not evidence that people understand
  their own analysis.

## Two documents, two jobs

- `docs/MANUSCRIPT.md` is the paper: abstract, related work by research thread, method,
  walkthrough, the criteria under which its claim fails, limitations and references.
  It carries no work notes.
- `docs/PAPER.md` is the positioning record: each source keeps its reading position and
  an explicit note of what it does not establish. It is the source of the manuscript's
  qualifiers; a sentence may only be as strong as its entry there.
- Changing a claim means changing the record first, then the manuscript. Do not let the
  two drift: a manuscript claim with no basis in the record is a defect.

## Claims

- Every claim traces to one of two sources: the cited work at the recorded version, or
  an observed record in an implementation repository. A claim that outgrows its basis
  is withdrawn or narrowed, not kept and softened.
- Novelty is argued against the closest work, including the parts that already do what
  the proposal might otherwise claim: purpose-driven composition, shared analysis
  context, plugin-capable compute backends, human revisions feeding later Agent work.
- Do not invent bibliographic detail. Author initials, venues and versions come from the
  cited source; where only a surname and "et al." are established, write that.
- Unverified parts stay labelled. No experiment has been run and no user study exists;
  data, runs and version identities in the scenario are illustrative.

## Language and links

- The documents are written in Chinese; agent-facing documents are English. Quoted
  terminology keeps the source's wording.
- References to another owner's records use absolute published URLs
  (`https://github.com/YuLab-SMU/<repo>/blob/main/...`) so they stay valid outside a
  local checkout. Local links and anchors must pass `scripts/check_docs.py`.
- When a cited page no longer contains the heading or anchor referred to, fix the
  reference. Leave no reference that only works in someone's working tree.

## Work and delivery

- Advance one argument at a time: state it, check its basis, render the document and
  read the rendered pages.
- `python3 scripts/check_docs.py` must pass before a commit; a nonzero exit is a
  failure, not a warning.
- Commit coherent changes on `main` and push with fast-forward. The push is the
  publication; a local commit is not a published claim.
