# Task: init-ledger

**Persona:** Sol (Planning Lead)
**Phase:** plan
**Command:** `init-ledger`
**Output:** `.sdlcfa/status.yaml`; Worker Result Contract

## Purpose

Initialize the one authoritative status ledger and its story entries so live state has a single home, separate from the historical story specs. The ledger holds what is true now (status, gates, evidence); the story files hold the specification. After this, any later agent resumes from disk, not chat.

## Inputs

- The drafted stories (`.sdlcfa/stories/STORY-<id>.md`) and the `slice-stories` backlog
- The `status-ledger` template and the `validate_artifacts.py` checker
- Per-story write scopes, validation commands, invariants, dependencies, and gates
- Any existing `.sdlcfa/status.yaml` (this may be an update, not a fresh init)

## Preconditions

- Stories are drafted (or at least sliced) with write scopes, dependencies, and validation
- If a ledger already exists, treat this as a reconcile-and-extend, not an overwrite

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Load the `status-ledger` template. If `.sdlcfa/status.yaml` exists, read it first and preserve live state — do not clobber in-progress/done stories.
2. Set `version`, `updated_at`, and `owner: "orchestrator"`.
3. For each story, add an entry with `title`, initial `status` (`ready` if dependencies are met and gates resolvable, else `blocked`), `epic`, `priority`, `dependencies`, and `blocked_by`.
4. Copy each story's `write_scope`, `validation_commands`, and `invariants` from its contract so the ledger is checkable without opening every story.
5. Initialize the `gates` block per story (`G0_PRECHECK` … as applicable) with `decision: not-run` and empty evidence/decider — these are filled by the orchestrator at gate time, not here.
6. Initialize each story's `audit` block (commit, completed_at, validation_artifact, last_run_id, status_reason, blocked_reason) to null.
7. Write `.sdlcfa/status.yaml`, then run `python3 scripts/validate_artifacts.py --type ledger .sdlcfa/status.yaml`. A non-zero exit means the ledger is incomplete — fix it before handing off. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- The structural validator fails and the missing field cannot be supplied from the story contracts.
- A story references a dependency or write scope that no contract defines → route back to `slice-stories`/`draft-story`.
- An existing ledger's live state conflicts with the new entries in a way only a human can reconcile.

## Output contract

- **Writes/updates:** `.sdlcfa/status.yaml` (story entries, scopes, validation, invariants, gate stubs, audit stubs), validator-clean.
- **Returns:** Worker Result Contract with the ledger path, the validator result in `validation.ran`, initial per-story status in `findings`, any unreconciled conflict in `open_decisions`, and `handoff` → `build` (or `gate-check` for `G1_READY`).

## Done when

- `.sdlcfa/status.yaml` exists with one entry per story (status, scope, validation, invariants, gate and audit stubs), live state is preserved across updates, the structural validator passes, and the result contract is returned.
