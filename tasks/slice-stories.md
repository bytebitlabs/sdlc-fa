# Task: slice-stories

**Persona:** Sol (Planning Lead)
**Phase:** plan
**Command:** `slice-stories`
**Output:** Story list with dependencies and write scopes; Worker Result Contract

## Purpose

Convert ready design into an executable backlog: small, bounded, independently verifiable stories with acceptance criteria, disjoint write scopes, dependencies, gates, and validation. Decompose ruthlessly so each story can be built and verified on its own. Keep live status out of this — this produces specs, not the ledger.

## Inputs

- Ready design: PRD, UX spec, architecture, ADRs, and `readiness-check` findings
- Story sizing constraints, risk level, and existing backlog or epics
- Validation commands and invariants from architecture/NFRs

## Preconditions

- `readiness-check` reports design ready, or its blockers are explicitly accepted
- Requirements, invariants, and validation commands are available to attach to stories

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Group requirements into epics, then slice each epic into the smallest stories that each deliver observable user value and can be verified alone.
2. For each story, draft acceptance criteria as observable behavior, traced to a PRD/UX/architecture source.
3. Assign each story a **write scope** by path prefix. Check pairwise that scopes are **disjoint**; where they must overlap, serialize the stories via a dependency instead.
4. Record dependencies and sequencing so no story is blocked by work scheduled after it. Flag cycles and break them.
5. Attach gates (`G0`–`G6`, plus human gates), validation commands, invariants, and stop conditions to each story.
6. Mark deferred work outside the first build path and identify the recommended first build batch.
7. Emit the story list with all of the above. Do **not** write story contracts or the ledger here — that is `draft-story` and `init-ledger`. Flag any story that cannot be made ready.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- Two stories need the same write paths concurrently and cannot be serialized without a product decision.
- A story's acceptance criteria require a requirement or decision the design never settled → route back to design.
- A story cannot be made small, bounded, and independently verifiable → record it and the exact missing decision.

## Output contract

- **Writes/updates:** the story list / backlog with per-story acceptance criteria, write scopes, dependencies, gates, and validation (proposed; not the live ledger).
- **Returns:** Worker Result Contract with the backlog and sequencing in `findings`, the recommended first batch in `summary`, unresolved scope/decisions in `open_decisions`, and `handoff` → `draft-story`.

## Done when

- Every story is small, bounded, independently verifiable, source-traced, with disjoint (or serialized) write scopes, acceptance criteria, dependencies, gates, and validation; the first batch is identified; and the result contract is returned.
