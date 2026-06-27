# Task: run-tests

**Persona:** Devin (Build Engineer)
**Phase:** build
**Command:** `run-tests`
**Output:** Test evidence; Worker Result Contract

## Purpose

Prove a story's behavior with tests: run the story-specific tests first, then the broader suite and lint, and capture exact commands and outputs as durable evidence — so `G3_DEV_DONE` and `G5_VALIDATE` rest on recorded results, not a claim that tests "should" pass.

## Inputs

- The story contract (`.sdlcfa/stories/STORY-<id>.md`) with its `validation_commands` and acceptance criteria
- The File List of paths changed during `develop-story`
- Current status snapshot (story should be `in-progress`/`review`)
- Any `decorations` relevant to the test/build stack

## Preconditions

- The story's implementation tasks are complete or being verified incrementally
- The validation commands and test entry points are known and runnable in this environment

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Identify the story-specific tests that cover this story's acceptance criteria (named test files, modules, or test IDs in the story).
2. Run those story-specific tests first. Record the **exact** command and a concise pass/fail summary for each.
3. If a story-specific test fails, fix within the write scope and re-run. After 3 failures for the same reason, stop and return `blocked` — do not weaken the test.
4. Run the broader suite next: the full test command, then lint/typecheck. **Execute all tests — do not skip any for time or cost.**
5. Capture exact commands, exit status, and concise output evidence for every check into the result. Mark any check you could not run as `not_run` with the reason.
6. If a regression appears in tests outside the story's scope, stop and return `blocked`; do not edit out-of-scope code to make it green.
7. Return the Worker Result Contract with the test evidence. **HALT** — do not advance the story or self-review.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- The same test fails 3 times for the same reason.
- A regression appears in tests outside the story's write scope.
- A required test command cannot run in this environment (missing dep, service, or credential).
- Making a test pass would require a human product/data/safety decision or an unapproved dependency.

## Output contract

- **Writes/updates:** test evidence in the story's Implementation Notes (commands, results); no source changes beyond in-scope test fixes.
- **Returns:** Worker Result Contract with each check's exact command and result in `validation.ran`/`validation.not_run`, residual risk, `findings`, `open_decisions`, and `handoff` → `review`.

## Done when

- The story-specific tests have run with recorded evidence, the broader suite and lint have run (or are documented as blockers), every command and result is captured verbatim, and the result contract is returned.
