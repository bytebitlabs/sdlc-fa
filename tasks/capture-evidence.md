# Task: capture-evidence

**Persona:** Val (Validation Runner)
**Phase:** validate
**Command:** `capture-evidence`
**Output:** Validation record entries; Worker Result Contract

## Purpose

Record exact command, result, and concise evidence per check into the validation record, so a later agent trusts the outcome from disk instead of re-running it. Evidence, not instructions: capture what happened, not what should happen.

## Inputs

- One or more executed (or inspected) checks with their real commands and outputs
- The target validation record (`.sdlcfa/validation/<id>.md`) for the story
- Pass criteria and any human acceptance of a skipped check

## Preconditions

- The check has actually been run or inspected (by `run-validations` or a worker)
- The validation record exists or can be created for this story

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. For each check, record its name/purpose and the **exact** command invoked (copy-pasteable, with flags).
2. Record the result classification: `pass`, `fail`, `blocked`, or `skipped`.
3. Record concise evidence — the load-bearing output line(s), exit code, or artifact path. Trim noise; keep what proves the result.
4. For `fail`/`blocked`, record the failure summary and the follow-up owner/phase (fixing is a Build assignment, not done here).
5. For `skipped`, mark it as residual risk unless a human has explicitly accepted the skip; record that acceptance and the accepting human verbatim. **(elicit: true when a human accepts a skipped check)**
6. Append entries into `.sdlcfa/validation/<id>.md` without overwriting prior evidence; keep the record append-only and ordered.

## HALT / Blocking conditions

- A check's command or result is unknown/unverified → do not record it as `pass`; mark it `blocked` pending a real run.
- A skip would be treated as accepted without a named human → record it as residual risk, not accepted, and surface it in `open_decisions`.

## Output contract

- **Writes/updates:** validation record entries in `.sdlcfa/validation/<id>.md` (append-only command/result/evidence rows).
- **Returns:** Worker Result Contract listing entries written, residual risk for skipped checks, and `open_decisions` for any human acceptance still pending.

## Done when

- Every check has a record entry with its exact command, result, and concise evidence; skipped checks are flagged as residual risk unless a named human accepted them; and the result contract is returned.
