# Task: create-prd

**Persona:** Paul (Product Manager)
**Phase:** design
**Command:** `create-prd`
**Output:** `.sdlcfa/design/prd.md`; Worker Result Contract

## Purpose

Turn discovery evidence into a product requirements document engineers can build against — every functional requirement tracing to a planned capability, every nonfunctional requirement owning a test strategy, and every product decision only a human can make recorded as an open decision, never inferred.

## Inputs

- The discovery brief (`.sdlcfa/discovery/brief.md`) and any cited research evidence
- An existing `.sdlcfa/design/prd.md`, constraints, and out-of-scope items
- Human product decisions supplied in the assignment packet (`inputs.human_decisions`)

## Preconditions

- Discovery is sufficient: problem, users, and evidence are clear. If not, route back to discover — do not start writing requirements.
- The brief names the value at stake and the decisions that block design

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** discovery brief. Restate the problem, target users, and value in one sentence each, citing the brief.
2. Derive **functional requirements**. For each, cite the source observation in the brief and state the capability it implies. Do not invent requirements with no evidence — mark gaps as assumptions or open decisions.
3. Derive **nonfunctional requirements** (performance, security, reliability, accessibility, compliance). Give each an owner and a test strategy; an NFR with neither is not done.
4. Define success metrics and explicit out-of-scope / deferred items, labeling deferred work outside the first build path.
5. Surface every product decision only a human can make (scope cuts, pricing, target segment, data/compliance posture) as an `open_decision` with an owner. **(elicit: true)** Never resolve these by inference.
6. Write `.sdlcfa/design/prd.md` using the `prd` template: problem, users, functional requirements (with source citations), NFRs (with owner/test), metrics, out-of-scope, open decisions. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

- Discovery is missing or contradictory on problem, users, or evidence → return `blocked`; route to discover.
- A requirement depends on a product decision only a human can make → record it in `open_decisions`; do not pick an answer.
- A required capability conflicts with a stated constraint or invariant → `blocked`.

## Output contract

- **Writes/updates:** `.sdlcfa/design/prd.md`.
- **Returns:** Worker Result Contract with the PRD path, requirements-to-source citations in `findings`, product decisions in `open_decisions` with owners, and `handoff.next_phase` (epics, architecture, UX, or planning).

## Done when

- The PRD exists with problem, users, functional requirements each citing a source and mapping to a capability, NFRs each with an owner and test strategy, success metrics, out-of-scope items, and open product decisions with owners.
