# Task: review-diff

**Persona:** Reva (Review Auditor)
**Phase:** review
**Command:** `review-diff`
**Output:** `.sdlcfa/reviews/<id>.md`; Worker Result Contract

## Purpose

Review the change as a **blind diff** — the diff only, with no builder reasoning, story narrative, or implementation notes — so defects are caught by reasoning from the code itself, not from the author's account of it. This is the most independent review layer.

## Inputs

- The diff under review (and only the diff)
- The review `id` and the story/run it belongs to
- The risk classification and the finding-classification rules

## Preconditions

- The diff is available in isolation; builder Implementation Notes, story acceptance criteria, and private reasoning are **withheld** for this mode
- The finding classifications are known: `decision_needed | patch | defer | dismiss | observation`

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the diff end to end without seeking outside context. Do not request the story, notes, or builder rationale — this mode is deliberately blind.
2. Reason from the change alone: correctness, logic errors, missing null/error handling, off-by-one, resource/state leaks, broken contracts, and regressions implied by what the diff touches.
3. For each suspected defect, record a concrete finding: location, what is wrong, and why it matters. No vague concerns.
4. Classify **every** finding: `patch` (unambiguous defect caused by this change), `decision_needed` (needs human product/UX/architecture/data/safety/scope input), `defer` (real issue outside this change), `dismiss` (false positive/already handled), or `observation`.
5. Do **not** patch. This assignment is review-only; propose patches as recommendations and never auto-resolve a `decision_needed`.
6. Sort findings by severity and form a status recommendation (`approve` / `changes-requested` / `blocked-on-decision`).
7. Write the report to `.sdlcfa/reviews/<id>.md` using the `review-report` template. **(elicit: false — auditor-authored)**

## HALT / Blocking conditions

- The diff is incomplete, truncated, or unreadable → return `blocked`; request the full diff rather than reviewing a fragment.
- A finding hinges on intent that only the story can settle → classify it `decision_needed` and name the owner; do **not** pull in the story to resolve it in this blind mode.
- Any proposed fix would require a human decision → it stays `decision_needed`, never `patch`.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.md` (findings, classifications, status recommendation). No source edits.
- **Returns:** Worker Result Contract with findings sorted by severity, a classification per finding in `findings`, decision blockers in `open_decisions` with owners, and a `handoff` carrying the status recommendation.

## Done when

- Every suspected defect is a concrete, located finding with a classification, no `decision_needed` was auto-resolved or patched, a status recommendation is given, and the report is written to `.sdlcfa/reviews/<id>.md`.
