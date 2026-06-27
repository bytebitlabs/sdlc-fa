# Task: status

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `status`
**Output:** `.sdlcfa/status.yaml`; Worker Result Contract

## Purpose

Update the one authoritative ledger atomically so live state always reflects reality. Ada owns every write to `.sdlcfa/status.yaml`; workers propose, she records.

## Inputs

- The state change to record (status transition, gate result, evidence link, next action)
- The worker result or gate record that justifies the change
- The current ledger snapshot

## Preconditions

- The justifying artifact (worker result, gate record, validation/review evidence) exists on disk
- For structural transitions (`G3_DEV_DONE`, `G4_REVIEW`, `G6_STATUS`), the validator has been run

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the current ledger and confirm it is structurally valid: `python3 scripts/validate_artifacts.py --type ledger .sdlcfa/status.yaml`.
2. Identify the exact entry to change (story id, phase, gate) and the evidence that justifies it. Reject any change with no on-disk evidence.
3. Apply the change as a single atomic write: status, gate decision, `evidence`, `decided_by`, `decided_at`, and the next action — together, never piecemeal.
4. Keep live state in the ledger only; do not duplicate it into story files or handoffs (those are supporting artifacts).
5. Re-run the ledger validator. A non-zero exit means the write is incomplete — fix it before returning, do not leave the ledger invalid.
6. Mark any superseded handoff or stale entry as historical so it cannot be mistaken for current status.
7. Return the Worker Result Contract noting what changed and the evidence. **(elicit: true when the change records a human-decision gate)**

## HALT / Blocking conditions

- The requested change has no backing evidence on disk → `blocked`; route to the owning phase to produce it.
- The validator fails after the write → `blocked`; the ledger must not be left structurally invalid.
- A status transition would mark work `done` past an unmet human-decision gate → `blocked`; escalate to the owner.

## Output contract

- **Writes/updates:** `.sdlcfa/status.yaml` (the single authoritative ledger; Ada's exclusive write).
- **Returns:** Worker Result Contract naming the entry changed, the evidence, and the resulting state.

## Done when

- The ledger reflects reality in one atomic write, passes the structural validator, superseded entries are marked historical, and the change is justified by a named artifact.
