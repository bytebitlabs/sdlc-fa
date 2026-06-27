# Task: gate-escape-analysis

**Persona:** Lena (Learning Scribe)
**Phase:** learn
**Command:** `gate-escape-analysis`
**Output:** Gate-escape analysis in the retro/incident record; Worker Result Contract

## Purpose

For an incident, name the gate (`G3`–`G7`) that should have caught the failure, explain why it passed anyway, and define the concrete change that closes the gap. This is how the skill compounds: each escape hardens a gate so the same failure does not escape twice. A gate that escapes twice is a defective gate, not bad luck.

## Inputs

- The incident record (`.sdlcfa/incidents/INC-<id>.md`): trigger, symptom, blast radius, rollback record
- The artifact chain for the failed story: gate records, review findings, validation evidence, release record
- The status ledger snapshot showing the story as `rolled-back`

## Preconditions

- An incident is open and contained (rollback executed, story set `rolled-back`)
- The artifact chain for the failed story is available to trace where the defect passed

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Trace the defect backward through the artifact chain to find where it first should have been caught.
2. **Name the escaped gate** explicitly — one of `G3_DEV_DONE`, `G4_REVIEW`, `G5_VALIDATE`, `G6_STATUS`, or `G7_RELEASE`.
3. State **why it passed**: the missing invariant, the test that did not exist, the review layer that did not run, or the release check that was absent or inferred.
4. Define the **concrete fix** that closes the gap — exactly one of: a new invariant, a guard test, a review layer, a validation command, or a release check. Name it specifically enough to implement.
5. Route the fix to the phase that owns the missed gate, with an owner, as a required follow-up (build a guard test → validate; new invariant → design; stricter sign-off → release).
6. Record the analysis in the retro/incident record. The original story returns to `done` only after the fix re-runs the lifecycle from that phase.

## HALT / Blocking conditions

- The defect cannot be traced to a single escaped gate → record the candidate gates and route an `audit` to resolve which gate owns it; do not pick one by guess.
- The fix would require a human policy/safety/spend decision → record it in `open_decisions` with an owner; name the fix but do not enact the decision.

## Output contract

- **Writes/updates:** the gate-escape analysis section of `.sdlcfa/incidents/INC-<id>.md` (or the incident retro) — escaped gate, why it passed, the concrete fix.
- **Returns:** Worker Result Contract naming the escaped `G3`–`G7` gate in `findings`, the fix routed in `handoff.next_phase` with an owner, and `open_decisions` for any human-owned policy change.

## Done when

- The analysis names the specific escaped gate (`G3`–`G7`), states why it passed, defines exactly one concrete fix (invariant/guard test/review layer/validation command/release check) routed to the owning phase, and the result contract is returned.
