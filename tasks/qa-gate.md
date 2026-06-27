# Task: qa-gate

**Persona:** Quinn (Test Architect)
**Phase:** review
**Command:** `qa-gate`
**Output:** `.sdlcfa/reviews/<id>.gate.yaml`; Worker Result Contract

## Purpose

Emit one advisory quality gate decision — `PASS | CONCERNS | FAIL | WAIVED` — that consolidates the risk profile, NFR assessment, and requirements trace. This **feeds, it does not replace,** the orchestrator's `G4_REVIEW` decision: a `FAIL` is required evidence Ada must resolve, not a unilateral stop.

## Inputs

- `.sdlcfa/reviews/<id>.risk.md`, `.sdlcfa/reviews/<id>.nfr.md`, and the requirements traceability matrix for this review
- Any security findings from Sam (`threat-model`, `sink-scan`) and Review Auditor findings for `<id>`
- The gate decision owner (for any `WAIVED` path)

## Preconditions

- The upstream assessments exist for this review id, or their absence is recorded
- `G3_DEV_DONE` has passed for this story

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Gather the risk band, NFR statuses, traceability coverage, and any open security findings for `<id>`.
2. Apply the decision rule, worst-input-wins: any risk `>= 9`, any NFR `FAIL`, an unresolved security blocker, or a `none`-coverage criterion on a high-risk path → **FAIL**. Any risk `>= 6`, NFR `CONCERNS`, or `partial` coverage → **CONCERNS**. Clean across all inputs → **PASS**.
3. Set `WAIVED` only when a **named human** explicitly accepts a `FAIL`/`CONCERNS` with a recorded reason and expiry. Never infer a waiver. **(elicit: true — human decision owner required)**
4. List the top issues that drove the decision, each pointing at its source artifact as evidence.
5. State the recommended next action: advance, return to build with required fixes, or escalate the named decision.
6. Write `.sdlcfa/reviews/<id>.gate.yaml`: `decision`, `evidence` (paths), `top_issues`, `waiver` (owner/reason/expiry or empty), and a note that this is advisory input to `G4_REVIEW`.
7. Return the contract. **HALT** — do not record `G4_REVIEW` yourself; that is Ada's gate write.

## HALT / Blocking conditions

- A `FAIL` is set → do not soften it to pass review; surface it as a decision blocker for the orchestrator.
- A waiver is requested without a named human, reason, and expiry → leave the decision as `FAIL`/`CONCERNS`; escalate to the owner.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.gate.yaml` (the advisory gate only; never `status.yaml`).
- **Returns:** Worker Result Contract with the gate decision, the driving issues and evidence in `findings`, any waiver request in `open_decisions` with its owner, and `handoff` → orchestrator for `G4_REVIEW`.

## Done when

- The gate file records `PASS|CONCERNS|FAIL|WAIVED` with evidence and top issues, any waiver names a human/reason/expiry, the advisory-not-authoritative note is present, and the result contract is returned to the orchestrator.
