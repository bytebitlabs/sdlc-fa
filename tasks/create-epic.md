# Task: create-epic

**Persona:** Paul (Product Manager)
**Phase:** design
**Command:** `create-epic`
**Output:** Epics section of the PRD (`.sdlcfa/design/prd.md`); Worker Result Contract

## Purpose

Slice the PRD's requirements into epics — each a coherent outcome with a goal, acceptance themes, and the requirements it covers — so planning can decompose ready, traceable units of work. Every epic traces back to PRD requirements; no requirement is left uncovered or silently duplicated.

## Inputs

- `.sdlcfa/design/prd.md` with functional and nonfunctional requirements
- Any existing Epics section and architecture/UX constraints that bound sequencing
- Human prioritization decisions supplied in the assignment packet

## Preconditions

- The PRD exists and its functional requirements are stable enough to group
- Open product decisions that would reshape scope are resolved or explicitly recorded

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** PRD. Build the inventory of functional requirements (and NFRs they imply) to be covered.
2. Group requirements into epics by coherent user outcome, not by component. For each epic name the **goal** and cite the PRD requirements it covers.
3. Write **acceptance themes** per epic — the outcome-level conditions that say the epic is satisfied (not yet story-level criteria).
4. Note cross-epic dependencies and sequencing, and flag any requirement that no epic covers (a coverage gap to fix, not ignore).
5. Surface prioritization or scope-ordering choices only a human can make as `open_decisions` with owners. **(elicit: true)** Do not infer priority.
6. Update the **Epics** section of `.sdlcfa/design/prd.md`: each epic with goal, covered requirements, acceptance themes, and dependencies. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

- A PRD requirement cannot be placed in any epic without a human scope/priority decision → record it in `open_decisions`.
- Epics would overlap such that write scopes cannot later be disjoint → `blocked`; route back to refine requirements.
- A requirement is left uncovered and covering it needs new product input → `blocked`.

## Output contract

- **Writes/updates:** the Epics section of `.sdlcfa/design/prd.md`.
- **Returns:** Worker Result Contract with the epic list, requirement-to-epic coverage in `findings`, uncovered requirements and prioritization choices in `open_decisions` with owners, and `handoff.next_phase` (shard-prd or planning).

## Done when

- Every PRD functional requirement maps to exactly one epic, each epic has a goal, covered-requirement citations, and acceptance themes, dependencies are noted, and prioritization decisions are recorded with owners.
