# Task: doc-sync

**Persona:** Lena (Learning Scribe)
**Phase:** learn
**Command:** `doc-sync`
**Output:** Doc-sync proposal or updates; Worker Result Contract

## Purpose

Update **only** authoritative docs so they match reality after a cycle, without rewriting historical specs. Keep stale docs from contradicting the live ledger. Story files and past PRDs are specifications, not living records — they stay as written; living docs get corrected.

## Inputs

- The completed work summary and the status ledger snapshot
- The current authoritative docs (READMEs, runbooks, architecture-of-record, config references)
- Review/validation/retro evidence describing what actually changed

## Preconditions

- The cycle's outcome is known and recorded (retro or validation evidence exists)
- Which docs are authoritative vs historical is established for this project

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. List the docs that describe current behavior and could now be stale.
2. Separate **authoritative/living** docs (update in scope) from **historical specs** (story files, past PRDs/ADRs — do not rewrite).
3. For each authoritative doc, compare it against reality (evidence, ledger) and identify the specific drift.
4. Update only the drifted authoritative content to match reality; do not invent or expand beyond what the evidence supports. **(elicit: false — agent-authored from evidence)**
5. Where a doc is owned by a human or the correct content needs a human decision, produce a **proposal** instead of editing. **(elicit: true for human-owned docs)**
6. Mark superseded handoffs/docs as historical so they cannot be mistaken for current status.
7. Record the updates/proposals; route anything requiring a human decision to its owner.

## HALT / Blocking conditions

- A change would rewrite a historical spec (story file, past PRD/ADR) → do not; record the divergence as a follow-up instead.
- The correct content requires a human product/architecture/safety decision → produce a proposal and record it in `open_decisions` with an owner; do not decide it.
- Docs and the ledger disagree about reality → return `blocked`; route to `audit`/`resume` before syncing to an unverified state.

## Output contract

- **Writes/updates:** only authoritative/living docs (or a doc-sync proposal for human-owned docs); superseded handoffs marked historical.
- **Returns:** Worker Result Contract listing docs updated vs proposed in `artifacts`, divergences left for follow-up in `findings`, and `open_decisions` for human-owned doc changes.

## Done when

- Authoritative docs match reality (or proposals are filed for human-owned ones), historical specs are left intact, superseded docs are marked historical, and the result contract is returned.
