# Task: readiness-check

**Persona:** John (Solution Architect)
**Phase:** design
**Command:** `readiness-check`
**Output:** Readiness findings and planning blockers; Worker Result Contract

## Purpose

Verify the design is internally consistent and traceable before planning begins, and emit the explicit planning blockers that must be resolved first. The goal is to catch contradictions and gaps at design time, not in build.

## Inputs

- PRD (`.sdlcfa/design/prd.md`), UX spec, architecture (`.sdlcfa/design/architecture.md`), and accepted ADRs
- Discovery brief and any `tech-eval` matrices
- The `design-readiness-checklist`
- The list of decisions only a human can make

## Preconditions

- The design artifacts to check exist (PRD and architecture at minimum)
- Requirements, NFRs, and invariants are recorded somewhere checkable

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Run the `design-readiness-checklist` via `execute-checklist`. Any failed item is a candidate blocker.
2. Check traceability: every functional requirement maps to at least one planned capability or architecture component; every NFR has an owner or test strategy.
3. Check consistency: architecture decisions, ADRs, and invariants do not contradict each other or the requirements they cite.
4. Check completeness: UX requirements are acceptance criteria or explicit non-goals; deferred work is labeled outside the first build path.
5. Check that human-decision gates and external dependencies are explicit, not buried as assumptions. **(elicit: true to confirm any unresolved human decision with its owner)**
6. Classify each gap as a **planning blocker** (must resolve before planning) or **deferred** (safe to plan around), naming the exact missing decision or artifact for each.
7. Record readiness findings and the blocker list; do not silently repair the design — route fixes to the owning design command.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- A required design artifact (PRD or architecture) is missing → route back to the owning command before judging readiness.
- A contradiction can only be resolved by a human product/architecture/data decision → record it as a blocker with the owner.
- Traceability cannot be established because a requirement has no source → flag it; do not assume intent.

## Output contract

- **Writes/updates:** readiness findings and the planning-blocker list (in `.sdlcfa/design/` notes; the orchestrator records gate status).
- **Returns:** Worker Result Contract with readiness verdict (ready / not-ready) in `summary`, gaps in `findings`, the exact missing decisions/artifacts in `open_decisions` with owners, and `handoff` → `plan` (if ready) or the owning design command.

## Done when

- The checklist has run, traceability/consistency/completeness are verified, every gap is classified as blocker or deferred with the exact missing decision/artifact named, and the result contract states whether design is ready to plan.
