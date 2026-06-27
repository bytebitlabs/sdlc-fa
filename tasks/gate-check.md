# Task: gate-check

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `gate-check`
**Output:** Gate record (`pass | blocked | not-run`) with evidence and decider; Worker Result Contract

## Purpose

Evaluate one gate (`G0_PRECHECK` … `G7_RELEASE`) against its required evidence before allowing a phase transition. Gates are decided on recorded evidence, never by eye.

## Inputs

- The gate to evaluate and the story/run it applies to
- The story's ledger entry and the artifacts that gate cites as evidence
- For structural gates, the relevant artifact files (assignment, result, ledger, qa-gate, skills-manifest)

## Preconditions

- The authoritative ledger (`.sdlcfa/status.yaml`) is loaded and structurally valid
- The owning phase's worker result(s), if any, are available

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Identify the gate's required evidence from the gate table in `SKILL.md`.
2. For **structural** gates (`G2_SCOPE`, `G3_DEV_DONE`, `G4_REVIEW`, `G6_STATUS`), run the deterministic field check first:
   - `python3 scripts/validate_artifacts.py --type result <path>` / `--type assignment <path>` / `--type ledger <path>`
   - A non-zero exit means the gate **fails** — record it as `blocked`, not a formatting nit.
3. For **content** gates, run the matching checklist via `execute-checklist` (e.g. `design-readiness`, `story-draft`, `story-dod`, `release`). Any failed item fails the gate.
4. For **human-decision** gates (`G7_RELEASE` sign-off, `G_SKILLS_TRUST`, and any spend/safety/legal/data/architecture decision), confirm a **human** recorded the decision. Never infer it. Absent sign-off → `blocked`.
5. Confirm the evidence is concrete: the `evidence` and `decided_by` fields are non-empty and point at a real artifact, command, or named human.
6. Record the gate result in the ledger: `decision`, `evidence`, `decided_by`, `decided_at`. **(elicit: true when the decision owner is human)**
7. If the gate passes, signal the next phase. If it fails, route back to the owning phase or to the named decision owner.

## HALT / Blocking conditions

- The validator or a checklist fails → gate `blocked`; do not pass it because the remaining issue is inconvenient.
- A human-only decision has no recorded human sign-off → `blocked`, escalate to the owner.
- The ledger and reality disagree (e.g. story `done` but no validation evidence) → `blocked`; route to `resume`/`audit`.

## Output contract

- **Writes/updates:** the gate record in `.sdlcfa/status.yaml` (Ada owns this write).
- **Returns:** Worker Result Contract noting the gate, its decision, the evidence, the decider, and the next phase or the owning phase to route back to.

## Done when

- The gate is recorded as `pass`/`blocked`/`not-run` with concrete evidence and a decider, and the next action (advance vs route-back vs escalate) is stated.
