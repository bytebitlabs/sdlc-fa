# Task: draft-story

**Persona:** Sol (Planning Lead)
**Phase:** plan
**Command:** `draft-story`
**Output:** `.sdlcfa/stories/STORY-<id>.md`; Worker Result Contract

## Purpose

Write one worker-ready, self-contained story contract so a build agent can implement it within its write scope without re-reading the design docs. Everything the builder needs — source-cited context, acceptance criteria, disjoint write scope, invariants, validation — lives in the story. A story that is not ready is returned `blocked` with the exact missing decision or artifact.

## Inputs

- One sliced story from `slice-stories` (id, scope, dependencies, acceptance themes)
- The design sources it draws on: PRD, UX, architecture, ADRs, readiness findings
- The `story` template and the `story-draft-checklist`
- Validation commands, invariants, and human-gate owners

## Preconditions

- The story exists in the backlog with a known write scope and dependencies
- Its acceptance criteria trace to a real, settled design source

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Open the `story` template and fill **Source** with exact citations (PRD/UX/architecture/discovery sections) so the builder need not re-read those docs.
2. Write **User Value** in one sentence and **Acceptance Criteria** as checkable, observable behaviors.
3. Inline the context the builder needs from each source — quote the relevant requirement, invariant, or interface rather than linking out.
4. Set the **Write Scope** by path prefix and confirm it is disjoint from concurrently buildable stories (or serialized via **Dependencies**).
5. Record **Nonfunctional Requirements**, **Invariants**, **Human Gates** (gate, question, owner, evidence, outcomes), and the **Validation** commands.
6. Leave **Implementation Notes** empty for the builder. Run the `story-draft-checklist` via `execute-checklist`; resolve every item or record it as a blocker.
7. Write `.sdlcfa/stories/STORY-<id>.md`. Keep it a specification — do not put live status here; that belongs in the ledger. **(elicit: true for any unresolved human gate owner)**

## HALT / Blocking conditions

Return `status: blocked` with the **exact** missing decision or artifact when:

- A required design source for an acceptance criterion does not exist or is unsettled.
- The write scope cannot be made disjoint without a sequencing/product decision.
- A human gate (product, UX, architecture, data, safety, spend) has no owner or evidence path.
- The `story-draft-checklist` has an unresolvable failed item.

## Output contract

- **Writes/updates:** `.sdlcfa/stories/STORY-<id>.md` (self-contained, source-cited; no live status).
- **Returns:** Worker Result Contract with the story path, the checklist result in `findings`, any missing decision/artifact in `open_decisions` with owners, and `handoff` → `init-ledger` (or `build` once eligible).

## Done when

- A self-contained STORY-<id>.md exists with cited sources, acceptance criteria, disjoint write scope, NFRs, invariants, human gates, and validation; the draft checklist passes; live status is excluded; and the result contract is returned — or the story is returned `blocked` naming the exact gap.
