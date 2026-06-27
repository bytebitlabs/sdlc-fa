# Task: develop-story

**Persona:** Devin (Build Engineer)
**Phase:** build
**Command:** `develop-story`
**Output:** Scoped implementation + updated story `Implementation Notes`; Worker Result Contract

## Purpose

Implement exactly one ready story end to end, within its write scope, with tests and validation evidence — using a strict order-of-execution loop so the agent never marks work done before it is proven.

## Inputs

- One story contract (`.sdlcfa/stories/STORY-<id>.md`) with acceptance criteria, write scope, invariants, and validation commands
- Current status snapshot for this story (must be `ready`/`in-progress`)
- Any `decorations` (skills the Capability Scout attached for this story's stack)

## Preconditions

- `G0_PRECHECK`, `G1_READY`, and `G2_SCOPE` have passed for this story
- Acceptance criteria and validation commands are available and unambiguous
- This agent owns status, or status ownership is explicitly delegated by the orchestrator

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** story contract and only the project context it cites. Do not load the PRD/architecture unless the story's notes direct you to. Load any `decorations` relevant to the write scope.
2. Mark the story `in-progress` in the ledger **only if** this agent owns status (otherwise note it for the orchestrator).
3. Select the next unchecked task/subtask in the story, in order.
4. Implement that task and its subtasks. Edit only paths inside the declared **write scope**.
5. Write or update tests that prove the task's acceptance criterion.
6. Run the story-specific validations for this task (`validation_commands`).
7. Only if **all** validations for the task pass: mark the task `[x]` in the story and update the story **File List**.
8. Repeat steps 3–7 until every task is `[x]`.
9. Run the full validation set (story tests, then the broader suite/lint). **Execute all tests — do not skip for time.**
10. Run the `story-dod-checklist` via `execute-checklist`. Resolve every item or record it as a blocker.
11. Update the story `Implementation Notes`: files changed, tests added, validation evidence, residual risk. **(elicit: false — agent-authored)**
12. Set the story status to `review` and return the Worker Result Contract. **HALT** — do not self-review or proceed to the next story.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- Acceptance criteria conflict with each other or with an invariant.
- The write scope is insufficient to satisfy a criterion, or the change would touch paths outside scope.
- An unapproved new dependency is required.
- The same validation fails 3 times for the same reason.
- A regression appears in tests outside the story's scope.
- Unrelated user edits overlap the write scope mid-build.
- Any step requires a human product/UX/architecture/data/safety/spend decision.

## Output contract

- **Writes/updates:** files within the write scope; the story's File List, Tasks checkboxes, Implementation Notes, Status (and nothing else in the story).
- **Returns:** Worker Result Contract with files changed, acceptance coverage, validation evidence (`ran`/`not_run`), residual risk, `findings`, `open_decisions`, and `handoff` → `review`.

## Done when

- Every task is `[x]` with passing tests, the full suite + lint pass (or failures are recorded as blockers), the DoD checklist is satisfied, the story status is `review`, and the result contract is returned.
