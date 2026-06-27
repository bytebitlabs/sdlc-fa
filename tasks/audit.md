# Task: audit

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `audit`
**Output:** Classified audit findings; Worker Result Contract

## Purpose

Trace each `done` story backward through its artifact chain and report what the evidence does — and does not — support. Audit verifies a run rather than advancing it; it reports findings, it does not silently repair state.

## Inputs

- `.sdlcfa/status.yaml` and the stories marked `done`
- The artifact chain per story: validation evidence, review findings, gate records, story acceptance criteria
- The finding classification rules (`decision_needed | patch | defer | dismiss | observation`)

## Preconditions

- The ledger is loaded and structurally valid (run `resume` first if state is stale)
- The request is to verify a run, not to advance it

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. For each `done` story, trace backward: ledger status → validation evidence → review findings → story acceptance criteria. A `done` story with no recorded review or validation evidence is a finding, not a pass.
2. Confirm every passed gate names its evidence and decider. An empty `evidence` or `decided_by` field fails the audit.
3. Confirm human-only gates (spend, safety, legal, data, architecture, production release) were resolved by a named human, never inferred.
4. Classify each gap as `decision_needed`, `patch`, `defer`, `dismiss`, or `observation`. Do not auto-resolve `decision_needed`, and do not patch state you did not create.
5. Collect findings into an audit report; reference each by the artifact and field that failed.
6. Return the Worker Result Contract with classified findings and recommended routing. **(elicit: true for any `decision_needed` finding)** **HALT** — do not repair the ledger as part of the audit.

## HALT / Blocking conditions

- A `done` story has no traceable review/validation evidence → record a `decision_needed`/`patch` finding; do not quietly mark it correct.
- A human-only gate was inferred rather than decided by a human → finding; escalate to the owner.
- The fix requires changing state you did not create → route it back to the owning phase rather than editing it here.

## Output contract

- **Writes/updates:** an audit report under `.sdlcfa/reviews/` (read-only on the ledger — audit reports, it does not repair).
- **Returns:** Worker Result Contract with findings classified (`decision_needed | patch | defer | dismiss | observation`), the failing artifact/field per finding, `open_decisions` with owners, and recommended routing.

## Done when

- Every `done` story is traced through its artifact chain, each gate's evidence and decider are confirmed or flagged, findings are classified with their failing artifact named, and no state was silently repaired.
