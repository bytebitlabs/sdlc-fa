# Task: trace-requirements

**Persona:** Quinn (Test Architect)
**Phase:** review
**Command:** `trace-requirements`
**Output:** Traceability matrix; Worker Result Contract

## Purpose

Map every acceptance criterion to the tests that prove it, expressed as Given-When-Then, so coverage gaps are visible before the gate. This is advisory input to `G4_REVIEW`; an uncovered criterion is evidence the gate must weigh, not an automatic block.

## Inputs

- The story contract and its acceptance criteria
- The tests in the diff (added or updated) and the existing test suite
- Any `risk-profile` output for this review, to prioritize high-risk criteria

## Preconditions

- Build is complete and tests are available to read
- `G3_DEV_DONE` has passed for this story
- Acceptance criteria are enumerable and unambiguous

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Enumerate every acceptance criterion from the story as a distinct, numbered row.
2. For each criterion, locate the test(s) that exercise it. Record the test name/path as evidence.
3. Express each mapped criterion as **Given** (precondition) **When** (action) **Then** (expected outcome). Note where the test does not actually assert the Then.
4. Mark each criterion's coverage: `full`, `partial`, or `none`. A test that runs the path but asserts nothing is `partial`, not `full`.
5. Flag the gaps: every `partial`/`none` row, weighted by its risk score where a risk profile exists.
6. Recommend the missing tests for each gap (the Given-When-Then that should exist). Do not author the tests here — that is build/QA-generation work.
7. Write the traceability matrix into `.sdlcfa/reviews/<id>.md` (or alongside the review report): rows, mappings, Given-When-Then, coverage, and gaps. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

- Acceptance criteria are missing, contradictory, or untestable as written → return `blocked`; route back to planning/build rather than tracing against guesses.
- Closing a coverage gap requires a human scope or acceptance decision → record it in `open_decisions` with an owner.

## Output contract

- **Writes/updates:** the traceability matrix in the review report for `<id>`.
- **Returns:** Worker Result Contract with the coverage summary (full/partial/none counts), gaps and recommended tests in `findings`, scope decisions in `open_decisions`, and `handoff` → remaining review work or `qa-gate`.

## Done when

- Every acceptance criterion is a row mapped to test evidence with Given-When-Then, coverage is marked, gaps and recommended tests are recorded, the matrix is written, and the result contract is returned for the gate to consume.
