# Task: signoff-check

**Persona:** Rex (Release Manager)
**Phase:** release
**Command:** `signoff-check`
**Output:** Sign-off evidence in the release record; Worker Result Contract

## Purpose

Capture the required **human** release sign-off and record it as evidence in the release record. Never infer spend, safety, legal, data, or production approval — `G7_RELEASE` passes only when a named human actually decided, not when the agent judges the change ready.

## Inputs

- The release record (`.sdlcfa/releases/<id>.md`) with deploy target, mechanism, and rollback plan
- The named release decision owner authorized to approve this deploy
- Validation and review evidence the owner needs to decide

## Preconditions

- `plan-release` and `rollback-plan` are complete; the deploy target and revert path are recorded
- The change is otherwise release-eligible (validation passed/accepted, review clean)

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Identify the decision owner: the specific human authorized to approve this release (not a role placeholder).
2. Present the deploy target, rollback plan, and validation/review evidence the owner needs to make the call.
3. Request the explicit sign-off decision from that human. **(elicit: true — human release approval)**
4. Record the sign-off **verbatim**: who approved, what they approved (target + scope), when, and any conditions they attached.
5. If approval is absent, conditional, or only implied, treat the release as **not** signed off. Do not infer approval from a passing validation or from silence.
6. Write the sign-off evidence into `.sdlcfa/releases/<id>.md`. Only a captured human sign-off lets `G7_RELEASE` pass.

## HALT / Blocking conditions

- No human sign-off is recorded → return `blocked`; escalate to the decision owner. Never substitute agent judgment for a human spend/safety/legal/data/production decision.
- The sign-off is conditional and the condition is unmet → `blocked` until the condition is satisfied and re-confirmed.
- The named owner is unavailable or unauthorized → `blocked`; route to find the correct authorizer rather than proceeding.

## Output contract

- **Writes/updates:** the Sign-off section of `.sdlcfa/releases/<id>.md` (approver, scope approved, timestamp, conditions — verbatim).
- **Returns:** Worker Result Contract with the sign-off status in `findings`, and `open_decisions` naming the owner and any unmet condition when sign-off is absent.

## Done when

- A named human's release sign-off is recorded verbatim in the release record (or the absence is recorded as `blocked` with an owner), and the result contract is returned.
