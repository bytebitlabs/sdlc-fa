# Task: research-spike

**Persona:** Mara (Discovery Analyst)
**Phase:** discover
**Command:** `research-spike`
**Output:** Evidence notes with citations; Worker Result Contract

## Purpose

Answer exactly one bounded discovery question from allowed sources, producing evidence notes that separate fact from assumption. A spike reduces a specific ambiguity that blocks design — it does not write the brief or make a decision.

## Inputs

- One discovery question stated in a single sentence
- Known assumptions and constraints
- Allowed source artifacts or research paths, and the evidence/citation standard
- Stop conditions (depth limit, source scope, time box)

## Preconditions

- The question is bounded and independent of other open questions
- Local evidence has been searched before any external research is requested

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Restate the question in one sentence and confirm it is answerable from the allowed sources. If it is two questions, split and answer only the one assigned.
2. Search local evidence first: repository docs, prior `.sdlcfa/discovery/` notes, code, and source artifacts the question cites.
3. Consult external/allowed sources only when local evidence is insufficient and the scope permits it. Stay inside the allowed research paths.
4. For each finding, capture a citation — file path, URL, or artifact — so a later agent can verify it without re-running the spike. Drop any claim you cannot cite.
5. Separate **evidence-backed observations** from **assumptions** and **unknowns**. Do not promote an assumption to a fact to fill a gap.
6. Tag any decision the evidence surfaces by owner (product, technical, data, operational, or human). **(elicit: true for any decision only a human can make)**
7. Write the evidence notes (question, observations with citations, assumptions, unknowns, decisions). Recommend whether the question is answered or needs a follow-up spike.

## HALT / Blocking conditions

- The question is unanswerable from the allowed sources → return `blocked`; name the source or access that would unblock it rather than guessing.
- The evidence is contradictory and resolving it needs a human decision → record it in `open_decisions` with an owner.
- Answering would require sources outside the allowed scope → stop and escalate to the orchestrator.

## Output contract

- **Writes/updates:** evidence notes for this question (handed to `write-brief`; not the brief itself).
- **Returns:** Worker Result Contract with observations vs assumptions in `findings`, citations in `artifacts`, decisions in `open_decisions` with owners, and `handoff.next_action` (answered → `write-brief`, or another spike).

## Done when

- The one question is answered (or recorded as blocked) with every observation cited, assumptions and unknowns separated, decisions tagged by owner, and a clear next action.
