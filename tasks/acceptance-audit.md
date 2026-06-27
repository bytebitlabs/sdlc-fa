# Task: acceptance-audit

**Persona:** Reva (Review Auditor)
**Phase:** review
**Command:** `acceptance-audit`
**Output:** `.sdlcfa/reviews/<id>.md`; Worker Result Contract

## Purpose

Audit the change against the story's **acceptance criteria** — does the diff actually satisfy each criterion, with evidence — so a story cannot reach `done` on criteria that were missed, partially met, or silently reinterpreted. This mode is granted the story, spec, and context.

## Inputs

- The diff under review and the story contract (`.sdlcfa/stories/STORY-<id>.md`) with its acceptance criteria
- Relevant spec/PRD/architecture context the story cites
- The review `id`, risk classification, and finding-classification rules

## Preconditions

- The story's acceptance criteria are available and unambiguous
- This mode is explicitly permitted story + spec + context access (it is not blind)

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Enumerate every acceptance criterion from the story as a checklist; include any UX/non-functional criteria the story made acceptance.
2. For each criterion, trace it to the specific diff hunk(s) and test(s) that satisfy it. Mark it `met`, `partially-met`, `unmet`, or `untestable-as-written`.
3. Reason independently from the code, not the builder's narrative: confirm the change truly satisfies the criterion rather than appearing to.
4. Flag criteria with no implementing change, no covering test, or coverage that contradicts the spec as concrete findings with location and evidence.
5. Classify **every** finding: `patch` (unambiguous gap caused by this change), `decision_needed` (criterion ambiguous or needs human product/UX/scope input), `defer` (real but out of this change), `dismiss` (already satisfied), or `observation`.
6. Do **not** patch. Propose fixes as recommendations; never auto-resolve a `decision_needed` or reinterpret a criterion to make it pass.
7. Form a status recommendation and write the report (with the per-criterion coverage matrix) to `.sdlcfa/reviews/<id>.md`. **(elicit: false — auditor-authored)**

## HALT / Blocking conditions

- A criterion is ambiguous or self-contradictory → classify `decision_needed` and name the owner; do not invent the intended behavior.
- The story or its acceptance criteria are missing → return `blocked`; an acceptance audit cannot run without criteria.
- Closing a coverage gap would require a human product/UX/architecture decision → `decision_needed`, never `patch`.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.md` (criterion-by-criterion coverage matrix, findings, classifications, status recommendation). No source edits.
- **Returns:** Worker Result Contract with coverage per criterion and findings in `findings`, decision blockers in `open_decisions` with owners, and a `handoff` carrying the status recommendation feeding `G4_REVIEW`.

## Done when

- Every acceptance criterion is traced to implementing change/test and marked met/partial/unmet, all findings are classified, no `decision_needed` was auto-resolved, a status recommendation is given, and the report is written to `.sdlcfa/reviews/<id>.md`.
