# Task: resume

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `resume`
**Output:** Reconciled ledger + lowest-unmet-gate resume point; Worker Result Contract

## Purpose

Reconcile on-disk state against reality before acting on a resumed run, so a resumed agent does not trust a stale ledger and ship the wrong thing. Run this before any phase work whenever `.sdlcfa/` already exists.

## Inputs

- `.sdlcfa/status.yaml` and the most recent handoff in `.sdlcfa/handoffs/`
- Repository/branch/worktree state and last validation evidence
- Open assignment results in `.sdlcfa/assignments/`

## Preconditions

- `.sdlcfa/` (or the project's equivalent SDLC tree) exists
- No phase work has begun this session

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read `.sdlcfa/status.yaml` and the most recent handoff in `.sdlcfa/handoffs/`.
2. Validate the ledger structurally: `python3 scripts/validate_artifacts.py --type ledger .sdlcfa/status.yaml`. Treat a non-zero exit as a blocker to fix before trusting status.
3. Reconcile the ledger against reality: repository state, branch/worktree, last validation evidence, and any open assignment results. Where the ledger and reality disagree, the ledger is wrong — correct it or route back to the owning phase, and record the correction (via `status`).
4. Identify the lowest unmet gate for the active story and set the resume point to the phase that owns it — not where chat left off.
5. Mark superseded handoffs as historical so they cannot be mistaken for current status.
6. Return the Worker Result Contract with the reconciled state, the resume point, and the next action. **(elicit: true if reconciliation surfaces an unresolved human-decision gate)**

## HALT / Blocking conditions

- The ledger fails structural validation → `blocked`; fix it before any phase work.
- The ledger and reality disagree in a way that cannot be corrected from evidence (e.g. story `done` but no validation/review evidence) → `blocked`; route to `audit`.
- Reconciliation reveals an unresolved human-decision gate → `blocked`; escalate to the owner.

## Output contract

- **Writes/updates:** corrections to `.sdlcfa/status.yaml`; superseded handoffs marked historical (Ada owns these writes).
- **Returns:** Worker Result Contract stating reconciliation corrections, the lowest-unmet-gate resume point, `open_decisions` with owners, and `handoff.next_phase`.

## Done when

- The ledger passes structural validation and matches reality, every correction is recorded, the resume point is the lowest unmet gate of the active story, and superseded handoffs are historical.
