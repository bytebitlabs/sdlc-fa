# Task: rollback-plan

**Persona:** Rex (Release Manager)
**Phase:** release
**Command:** `rollback-plan`
**Output:** Rollback plan in the release record; Worker Result Contract

## Purpose

Record how to revert the change, the trigger that fires the revert, and who can pull it — before the change ships. A release without a verified rollback path is a release-gate failure, not a detail to fill in later. Contain first, explain later starts here.

## Inputs

- The release record (`.sdlcfa/releases/<id>.md`) and its deploy target/mechanism
- The available rollback mechanism (flag flip, revert commit, redeploy previous)
- The named human who is authorized to pull the rollback

## Preconditions

- `plan-release` has assembled the release record with a deploy target and mechanism
- The deploy mechanism's reversibility is known or can be determined

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Choose the **reversible action**: flag flip, revert commit, or redeploy previous version — the fastest safe way to restore the prior state.
2. Record the exact steps/commands to execute that revert, so it can be run under incident pressure without re-deriving them.
3. Define the **trigger**: the concrete condition (failed post-release check, error-rate threshold, symptom) that fires the rollback.
4. Name **who can pull it**: the authorized human or role, so containment is not blocked waiting on an unclear owner.
5. State the expected resulting state after rollback (fully reverted, partial, mitigated) so Stabilize can confirm the symptom cleared.
6. Write the rollback plan into `.sdlcfa/releases/<id>.md`. If a rollback trigger later fires, switch to the Incident and Rollback loop — contain with this plan before root-causing.

## HALT / Blocking conditions

- No safe rollback exists for this change → return `blocked`; escalate to the human owner. That absence is a release-gate failure, not an acceptable risk.
- The revert trigger or the authorized puller cannot be named → `blocked`; an unnamed trigger or owner means containment will stall.

## Output contract

- **Writes/updates:** the Rollback Plan section of `.sdlcfa/releases/<id>.md` (action, steps, trigger, authorized puller, expected resulting state).
- **Returns:** Worker Result Contract with the rollback action and trigger in `findings`, and `open_decisions` naming the authorized puller and any unresolved reversibility gap.

## Done when

- The release record contains a concrete revert action with steps, a named trigger, the authorized puller, and the expected resulting state — and the result contract is returned.
