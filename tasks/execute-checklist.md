# Task: execute-checklist

**Persona:** Ada (Delivery Orchestrator) — shared subroutine, also invoked by any role
**Phase:** orchestrate (dependency task; not a phase command)
**Command:** `execute-checklist`
**Output:** Per-item pass/fail record for the named checklist; Worker Result Contract

## Purpose

Run a named checklist from `checklists/` item by item and record pass/fail per item, so content gates (design-readiness, story-draft, story-dod, release) are decided deterministically rather than by eye. This is a generic runner other tasks call; it never decides the gate itself.

## Inputs

- The checklist name to run (e.g. `design-readiness`, `story-draft`, `story-dod`, `release`)
- The artifact(s) the checklist evaluates (story, design doc, release record)
- The evidence each item requires

## Preconditions

- The named checklist exists under `checklists/`
- The artifact(s) under check are on disk and identified

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Load the named checklist from `checklists/<name>.md`. If it is missing, stop and report — do not improvise items.
2. Take the next unrun item in order. Read what evidence it requires.
3. Evaluate the item against the artifact/evidence, not against narrative or intent. Record `pass` or `fail` with the concrete evidence (file, command output, or named human).
4. For any item requiring a human decision, do not infer it — record `fail`/`pending` until a human has decided. **(elicit: true for human-decision items)**
5. Repeat steps 2–4 until every item has a recorded result. Do not skip items for time or convenience.
6. Summarize the run: total items, passes, fails/pending, and the evidence per item. Any failed item means the checklist did not pass — surface that to the caller.
7. Return the per-item record to the calling task (gate-check or a worker). **HALT** — the caller decides the gate; this runner only records results.

## HALT / Blocking conditions

- The named checklist file is missing or unparseable → `blocked`; do not invent items.
- An item needs a human decision that has not been recorded → mark it `pending`; do not pass it by inference.
- The artifact under check is absent → `blocked`; the item cannot be evaluated without evidence.

## Output contract

- **Writes/updates:** the per-item pass/fail record (returned to the caller; the caller persists any gate result to `.sdlcfa/status.yaml`).
- **Returns:** Worker Result Contract with each item's `pass`/`fail`/`pending` and evidence, the failed-item count, and `open_decisions` for any human items.

## Done when

- Every checklist item has a recorded result with concrete evidence, failed/pending items are surfaced, and the per-item record is returned to the calling task without the runner deciding the gate.
