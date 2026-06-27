# Task: requirements-trace

**Persona:** Paul (Product Manager)
**Phase:** design
**Command:** `requirements-trace`
**Output:** Traceability findings; Worker Result Contract

## Purpose

Check that every requirement is accounted for before planning starts: each functional requirement maps to at least one planned capability, each nonfunctional requirement has an owner or test strategy, each UX requirement becomes an acceptance criterion or an explicit non-goal, and every gap is a finding — not something to wave through.

## Inputs

- `.sdlcfa/design/prd.md` (functional + nonfunctional requirements) and its epics/shards
- `.sdlcfa/design/ux-spec.md` and `.sdlcfa/design/architecture.md` if present
- The planned capabilities, epics, or stories the requirements should map onto

## Preconditions

- The PRD exists and its requirements are stable enough to trace
- Epics or candidate capabilities exist to trace requirements against

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Build the requirement inventory from the PRD (functional, nonfunctional) and the UX spec (UX requirements), citing each source.
2. For each **functional requirement**, find the planned capability/epic/story that delivers it. No mapping → record an `uncovered` finding.
3. For each **nonfunctional requirement**, confirm a named owner **and** a test strategy. Missing either → record a finding.
4. For each **UX requirement**, confirm it became an acceptance criterion or an explicit non-goal. Neither → record a finding.
5. Check the reverse direction: flag any planned capability that traces to no requirement (scope creep) and any deferred work that is mislabeled as in-scope.
6. Classify every gap (`decision_needed`, `patch`, `defer`, `dismiss`) and assemble the traceability findings, citing the source artifact behind each requirement. **(elicit: false — agent-authored)**
7. Decide planning readiness: planning may start only when there is no unresolved `decision_needed` gap. State this explicitly.

## HALT / Blocking conditions

- A requirement cannot be traced without a human product/UX/architecture decision → record it as `decision_needed` in `open_decisions`; do not invent the mapping.
- The PRD and UX/architecture artifacts contradict each other on a requirement → `blocked`; route back to the owning design task.
- Any unresolved `decision_needed` gap remains → readiness is **not** met; do not signal plan.

## Output contract

- **Writes/updates:** traceability findings (in the result; appended to the readiness record if the project keeps one). Does not rewrite the PRD.
- **Returns:** Worker Result Contract with the requirement-to-capability matrix in `findings` classified by type, unresolved gaps in `open_decisions` with owners, and `handoff.next_phase` (plan if clean, else back to the owning design task).

## Done when

- Every functional requirement maps to a capability, every NFR has an owner and test strategy, every UX requirement is an acceptance criterion or explicit non-goal, reverse-direction scope creep is flagged, gaps are classified, and planning readiness is stated with no unresolved decision-needed finding.
