# Task: plan-release

**Persona:** Rex (Release Manager)
**Phase:** release
**Command:** `plan-release`
**Output:** `.sdlcfa/releases/<id>.md`; Worker Result Contract

## Purpose

Identify the deploy target and the mechanism that executes the release, and assemble the durable release record so `G7_RELEASE` is decided on evidence. Rollback-first: no release record is complete without a revert path and a human sign-off slot.

## Inputs

- Validation evidence (`.sdlcfa/validation/<id>.md`) and review status for the story
- The deploy target (environment) and the mechanism (who or what ships it)
- The release decision owner and the rollback mechanism

## Preconditions

- `G5_VALIDATE` passed, or its failures are explicitly accepted by the decision owner
- `G4_REVIEW` is complete with no unresolved `decision_needed` finding

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Confirm the change is release-eligible: validation passed (or accepted) and review is clean. If not, route back; do not plan a release on unproven work.
2. Identify the **deploy target**: the exact environment (e.g. production, staging) the change ships to.
3. Identify the **mechanism**: who or what executes the release (pipeline, command, human operator), and whether this runtime can execute it or must hand off.
4. Assemble `.sdlcfa/releases/<id>.md` with deploy target, mechanism, the linked validation/review evidence, and slots for rollback plan, sign-off, and post-release checks.
5. Invoke `rollback-plan` to record the revert path and trigger, `signoff-check` for the human sign-off, and `post-release-check` for health checks — `G7_RELEASE` needs all three.
6. If this runtime cannot execute the deploy, produce a release handoff in the record so a human or downstream agent can ship from disk.

## HALT / Blocking conditions

- The deploy target is ambiguous or the mechanism is unknown → return `blocked`; do not guess where or how it ships.
- Validation failed and no human accepted the residual risk → `blocked`; route to the decision owner.
- No rollback path can be defined for the target → `blocked`; that absence is itself a release-gate failure to escalate.

## Output contract

- **Writes/updates:** `.sdlcfa/releases/<id>.md` (deploy target, mechanism, evidence links, and the rollback/sign-off/post-release slots).
- **Returns:** Worker Result Contract with the release record path, target and mechanism in `findings`, and `open_decisions` naming the `G7_RELEASE` sign-off owner and any unfilled slot.

## Done when

- The release record exists with a concrete deploy target and mechanism, evidence is linked, the rollback/sign-off/post-release slots are routed to their tasks, and the result contract is returned.
