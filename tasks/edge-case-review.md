# Task: edge-case-review

**Persona:** Reva (Review Auditor)
**Phase:** review
**Command:** `edge-case-review`
**Output:** `.sdlcfa/reviews/<id>.md`; Worker Result Contract

## Purpose

Review the diff with **project read access** to probe the edge cases a blind diff cannot see: boundary inputs, error and concurrency paths, and interactions with callers and shared state elsewhere in the codebase. Read access is for probing, not for absorbing the builder's reasoning.

## Inputs

- The diff under review and read access to the surrounding project (callers, callees, shared modules, fixtures)
- The review `id` and the story/run it belongs to
- The risk classification and the finding-classification rules

## Preconditions

- Project read access is available; builder Implementation Notes and private rationale are **not** the basis for findings
- The finding classifications are known: `decision_needed | patch | defer | dismiss | observation`

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the diff, then read the project code it touches and is touched by: callers, callees, shared state, configuration, and existing tests.
2. Enumerate edge cases: empty/null/boundary inputs, error and exception paths, concurrency/ordering, large/zero inputs, unicode/encoding, partial failure, and idempotency.
3. For each, trace through the changed code plus its real neighbors to decide whether the case is handled. Treat unhandled cases as concrete findings with location and a triggering scenario.
4. Check interaction risk: does the change break an assumption a caller elsewhere relies on, or leave shared state inconsistent? Reason from the code you read, not the builder's account.
5. Classify **every** finding: `patch` (unambiguous defect from this change), `decision_needed` (needs human product/UX/architecture/data/safety input), `defer` (real but out of this change), `dismiss` (false positive/handled), or `observation`.
6. Do **not** patch. Propose fixes as recommendations; never auto-resolve a `decision_needed`.
7. Sort findings by severity, form a status recommendation, and write the report to `.sdlcfa/reviews/<id>.md`. **(elicit: false — auditor-authored)**

## HALT / Blocking conditions

- Probing an edge case would require running code or a human safety/data decision → record it as a finding/`decision_needed`; do not act on the decision.
- Required project files are unreadable so an edge case cannot be assessed → note the gap as residual risk; do not assume the case is safe.
- A fix would require a human decision → it stays `decision_needed`, never `patch`.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.md` (edge cases probed, findings, classifications, status recommendation). No source edits.
- **Returns:** Worker Result Contract with findings sorted by severity and classified in `findings`, edge cases left unverified as residual risk, decision blockers in `open_decisions` with owners, and a `handoff` carrying the status recommendation.

## Done when

- The enumerated edge cases are each traced through the changed code and its real neighbors, every finding is classified, no `decision_needed` was auto-resolved, unverified cases are recorded as residual risk, and the report is written to `.sdlcfa/reviews/<id>.md`.
