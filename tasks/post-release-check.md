# Task: post-release-check

**Persona:** Rex (Release Manager)
**Phase:** release
**Command:** `post-release-check`
**Output:** Post-release validation result or pending owner; Worker Result Contract

## Purpose

Define and run the checks that confirm the change is healthy after it ships — or mark them pending with a named owner. Post-release validation is part of `G7_RELEASE`: a deploy without health confirmation is unverified, and a failed check is the trigger to switch to the Incident loop.

## Inputs

- The release record (`.sdlcfa/releases/<id>.md`) with deploy target, rollback plan, and sign-off
- The rollback trigger defined in the rollback plan
- Health signals available for the target (smoke checks, metrics, error rates)

## Preconditions

- `signoff-check` captured the human sign-off and the change is shipping or shipped
- The rollback plan and its trigger are recorded, so a failed check has a defined response

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Define the post-release checks: the concrete signals that confirm the change is healthy in the deploy target (smoke test, key metric, error rate, data integrity).
2. Tie each check to its pass criterion and to the rollback trigger it would fire on failure.
3. If the deploy has executed, run each check and capture the exact command/result and concise evidence into the release record.
4. If the deploy has not yet executed (handed off), mark each check **pending** with a named owner who must run it post-ship. Do not record pending as passed.
5. Evaluate results: if all pass, the release is confirmed healthy. If any fails, **stop the forward lifecycle** and switch to the Incident and Rollback loop — contain with the rollback plan before root-causing.
6. Record the outcome (confirmed healthy / pending owner / failed → incident opened) in `.sdlcfa/releases/<id>.md`.

## HALT / Blocking conditions

- A post-release check fails or the rollback trigger fires → switch to the Incident loop; open `INC-<id>`, contain first, set the story `rolled-back`.
- The checks cannot be defined for this target → return `blocked`; an undefinable health check means `G7_RELEASE` cannot pass.
- The deploy is handed off and no owner will run the pending checks → `blocked`; route to name an owner.

## Output contract

- **Writes/updates:** the Post-release section of `.sdlcfa/releases/<id>.md` (checks, criteria, results or pending owners).
- **Returns:** Worker Result Contract with health results in `validation.ran`/`validation.not_run`, pending owners in `open_decisions`, and `handoff` → `learn` on success or the Incident loop on failure.

## Done when

- Each post-release check is defined and either run with recorded evidence or marked pending with a named owner; a failed check has switched to the Incident loop; and the result contract is returned.
