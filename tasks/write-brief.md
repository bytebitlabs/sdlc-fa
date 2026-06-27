# Task: write-brief

**Persona:** Mara (Discovery Analyst)
**Phase:** discover
**Command:** `write-brief`
**Output:** `.sdlcfa/discovery/brief.md`; Worker Result Contract

## Purpose

Synthesize discovery evidence into one durable brief so design and planning resume from disk, not chat. The brief reduces ambiguity and names the decisions that block design.

## Inputs

- Discovery question(s) and any `research-spike` evidence notes
- Known assumptions, constraints, and source artifacts
- The evidence/citation standard and stop conditions

## Preconditions

- At least one discovery question is defined in a single sentence
- Local evidence has been searched before requesting new research

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. State the problem or opportunity in one sentence.
2. Identify target users/stakeholders and the value at stake.
3. Record evidence and source artifacts; cite each source. Separate **evidence-backed observations** from **assumptions**.
4. List constraints (system, repo, product, UX, data, safety, spend) and explicit out-of-scope items.
5. List risks, unknowns, and decision points. Tag each decision as product, technical, data, operational, or human. **(elicit: true for any decision only a human can make)**
6. Recommend the next phase and what it needs to start.
7. Write the brief to `.sdlcfa/discovery/brief.md` using the `discovery-brief` template. Do not invent facts to fill a section — mark unknowns as unknown.

## HALT / Blocking conditions

- The core problem, users, or evidence are unclear → return `blocked`; route back to `research-spike` rather than guessing.
- A decision required to frame the problem can only be made by a human → record it in `open_decisions` with an owner.

## Output contract

- **Writes/updates:** `.sdlcfa/discovery/brief.md`.
- **Returns:** Worker Result Contract with the brief path, observations vs assumptions in `findings`, decision points in `open_decisions` with owners, and `handoff.next_phase`.

## Done when

- The brief exists with problem, users, evidence+citations, constraints, risks/unknowns, decision points with owners, out-of-scope items, and a recommended next phase.
