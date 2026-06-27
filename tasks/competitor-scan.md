# Task: competitor-scan

**Persona:** Mara (Discovery Analyst)
**Phase:** discover
**Command:** `competitor-scan`
**Output:** Competitor/approach comparison in the brief; Worker Result Contract

## Purpose

Survey comparable products or approaches and capture an evidence-backed comparison in the discovery brief. A scan informs design with what already exists and where the gap is — it cites every claim and never substitutes opinion for evidence.

## Inputs

- The comparison question and the dimensions to compare on
- Allowed sources (product docs, sites, repos, prior `.sdlcfa/discovery/` notes)
- Known constraints, the citation standard, and stop conditions

## Preconditions

- The set of competitors/approaches to survey is bounded, or a rule for bounding it is given
- Local evidence has been searched before any external research

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. State the comparison question and fix the dimensions (e.g. capability, pricing model, maturity, constraints fit) before gathering data, so each entry is comparable.
2. Identify the competitors/approaches in scope. Search local evidence first, then allowed external sources within scope.
3. For each entry, record the value on each dimension with a citation — URL, doc, or artifact. Mark any cell you cannot source as `unknown`; do not estimate.
4. Separate **evidence-backed observations** from **assumptions and inferences**. Label inferred positioning as assumption.
5. Summarize the gap: where comparables are strong, where they are weak, and the differentiated opening relevant to this project's constraints.
6. Tag any decision the scan surfaces (build vs adopt, positioning, scope) by owner. **(elicit: true for any decision only a human can make)**
7. Append the comparison (matrix, gap summary, decisions) to `.sdlcfa/discovery/brief.md`. Do not fill a cell with a guess to make the matrix look complete.

## HALT / Blocking conditions

- The comparison set is unbounded or the sources are out of allowed scope → return `blocked`; ask the orchestrator to bound it.
- Required evidence is unavailable for a key competitor → record the cells as `unknown`; do not infer them as fact.
- A positioning or build-vs-adopt decision is required → record it in `open_decisions` with an owner.

## Output contract

- **Writes/updates:** the competitor/approach comparison section of `.sdlcfa/discovery/brief.md` (matrix + gap summary).
- **Returns:** Worker Result Contract with the comparison and gap in `findings`, citations in `artifacts`, unknowns flagged, and decisions in `open_decisions` with owners.

## Done when

- The brief holds a cited comparison matrix across fixed dimensions, unknowns marked rather than guessed, observations separated from assumptions, a gap summary, and any surfaced decision named with an owner.
