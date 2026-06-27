# Task: handoff

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `handoff`
**Output:** `.sdlcfa/handoffs/<name>.md`; Worker Result Contract

## Purpose

Write a resumable handoff when stopping, so the next agent resumes from disk rather than reconstructing context from chat. The handoff is a pointer to durable state, not a replacement for it.

## Inputs

- The current ledger snapshot and the active story/run
- Worker results, gate records, and validation/review evidence produced this session
- Open decisions and their owners

## Preconditions

- The ledger is current and structurally valid (`status` has recorded this session's changes)
- Any open worker results are filed under `.sdlcfa/assignments/`

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Summarize what was completed this session and the current phase, citing the artifacts that prove it (do not restate their contents).
2. Record the active story, its ledger status, and the lowest unmet gate — the exact resume point.
3. List open decisions with owners, and any blockers returned by workers. **(elicit: true for human-decision items)**
4. State the single recommended next action and the role that owns it.
5. Write the handoff to `.sdlcfa/handoffs/<name>.md` using the `handoff` template. Reference state by path; never copy live status into it.
6. Mark any prior handoff that this one supersedes as historical.
7. Return the Worker Result Contract pointing at the new handoff. **HALT** — stopping is the point of this task.

## HALT / Blocking conditions

- The ledger is stale or invalid → `blocked`; run `status` (and `resume` if needed) before writing a handoff that would mislead the next agent.
- A blocker has no named owner → record it in `open_decisions` with an owner rather than leaving it implicit.

## Output contract

- **Writes/updates:** `.sdlcfa/handoffs/<name>.md`; marks superseded handoffs historical.
- **Returns:** Worker Result Contract with the handoff path, the resume point (lowest unmet gate), `open_decisions` with owners, and `handoff.next_action`.

## Done when

- A handoff exists naming completed work, the active story, the resume point, open decisions with owners, and the next action; superseded handoffs are marked historical; the ledger remains authoritative.
