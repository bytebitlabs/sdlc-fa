# Task: run-validations

**Persona:** Val (Validation Runner)
**Phase:** validate
**Command:** `run-validations`
**Output:** `.sdlcfa/validation/<id>.md`; Worker Result Contract

## Purpose

Run or inspect the required checks for one story and record what actually happened as durable validation evidence — exact command, pass/fail/blocked/skipped, and concise output. Prove the checks passed or document why they block completion. This task does **not** fix failures; fixing is a separate Build assignment.

## Inputs

- The story (`.sdlcfa/stories/STORY-<id>.md`) and its `validation_commands`
- Environment notes and any known flaky or expensive checks
- Expected artifacts or pass criteria for each check

## Preconditions

- `G3_DEV_DONE` has passed: the story is implemented with notes recorded
- The validation commands and their pass criteria are available and unambiguous

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Assemble the required check list for the story: story-specific guard tests first, then the broader suite/lint.
2. Note the environment (branch/worktree, toolchain) so the run is reproducible.
3. Run each check in order. Capture the **exact** command invoked and its real result — do not paraphrase or assume.
4. Classify each result as `pass`, `fail`, `blocked`, or `skipped`. A check not run for time or cost is `skipped`, not `pass`.
5. Hand each result to `capture-evidence` to record the command, outcome, and concise evidence into `.sdlcfa/validation/<id>.md`.
6. For any `fail`/`blocked`, write a one-line failure summary and name the follow-up — a **Build** assignment to fix it. Do not patch the code here.
7. Summarize residual risk: every `skipped`/`blocked` check is residual risk unless a human explicitly accepts it.

## HALT / Blocking conditions

- A required check cannot run (missing dependency, broken environment) → record it `blocked` with the reason; do not mark it `pass`.
- The same check fails 3 times for the same reason → stop re-running; record `fail` and route to Build.
- A check requires a human to accept a skip or residual risk → record it in `open_decisions` with an owner; do not accept it yourself.

## Output contract

- **Writes/updates:** `.sdlcfa/validation/<id>.md` (the validation record; evidence only, no code).
- **Returns:** Worker Result Contract with each check's result in `validation.ran`/`validation.not_run`, failure summaries and Build follow-ups in `findings`, residual risk, and `open_decisions` for any human-accepted skip.

## Done when

- Every required check is recorded as `pass`/`fail`/`blocked`/`skipped` with its exact command and evidence in `.sdlcfa/validation/<id>.md`, failures are routed to Build, residual risk is stated, and the result contract is returned.
