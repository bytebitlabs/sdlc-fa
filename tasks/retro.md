# Task: retro

**Persona:** Lena (Learning Scribe)
**Phase:** learn
**Command:** `retro`
**Output:** `.sdlcfa/retros/<scope>.md`; Worker Result Contract

## Purpose

Capture what completed, what changed, what failed, and the lessons for one scope (story, batch, sprint, epic, incident, or review cycle), then convert lessons into routed follow-ups. Prefer hardening a gate, invariant, or guard test over a one-off note so the lesson is enforced on future runs, not just remembered.

## Inputs

- The completed work summary and the status ledger snapshot for the scope
- Review and validation evidence, known failures, blocked items, and human decisions
- For incident scope, the incident record (`.sdlcfa/incidents/INC-<id>.md`)

## Preconditions

- The scope is defined (story/batch/sprint/epic/incident/review cycle)
- The supporting evidence (ledger, reviews, validation) is available on disk

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Determine and name the learning scope.
2. Record what **completed**, what **changed**, and what **failed or blocked** — separating observation from decision.
3. Extract lessons: what worked, what did not, and the root cause where known.
4. For each lesson, draft a concrete follow-up. Prefer a gate/invariant/guard-test change over a reminder; reserve one-off notes for genuinely non-recurring items.
5. Route each follow-up to its owning phase (discover, design, plan, build, review, validate, release) with an owner. **(elicit: true for any follow-up only a human can decide or own)**
6. For **incident** scope, run `gate-escape-analysis` and treat every escaped gate as a required, owned follow-up — not an optional note.
7. Write the retrospective to `.sdlcfa/retros/<scope>.md`. Do not rewrite historical specs here; doc updates go through `doc-sync`.

## HALT / Blocking conditions

- The scope's evidence is missing or contradicts the ledger → return `blocked`; route to `resume`/`audit` before drawing lessons from a stale state.
- A follow-up requires a human product/safety/spend/architecture decision → record it in `open_decisions` with an owner; do not resolve it.

## Output contract

- **Writes/updates:** `.sdlcfa/retros/<scope>.md` (completed/changed/failed, lessons, routed follow-ups).
- **Returns:** Worker Result Contract with the retro path, lessons in `findings`, follow-ups with `handoff.next_phase` and owners, and `open_decisions` for human-owned items.

## Done when

- The retro records what completed/changed/failed with lessons, every lesson has a routed follow-up (preferring a gate/invariant/test change) with an owner, incident scope includes a gate-escape analysis, and the result contract is returned.
