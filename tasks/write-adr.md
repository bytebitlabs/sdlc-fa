# Task: write-adr

**Persona:** John (Solution Architect)
**Phase:** design
**Command:** `write-adr`
**Output:** `.sdlcfa/design/adr/<id>.md`; Worker Result Contract

## Purpose

Record exactly one architecture decision as a durable ADR — its context, the decision, and its consequences — so later phases can trace why a choice was made and what it constrains. One decision per file; never bundle unrelated choices.

## Inputs

- The single decision to record and the requirement/constraint that forces it
- Architecture doc (`.sdlcfa/design/architecture.md`) and any `tech-eval` matrix for this decision
- Existing ADRs under `.sdlcfa/design/adr/` (to assign the next `<id>` and find superseded ADRs)
- Human decisions that cannot be inferred

## Preconditions

- The decision is bounded to one question with real tradeoffs worth recording
- Evidence (a `tech-eval` matrix, benchmark, or cited source) supports the chosen option

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Assign the next sequential `<id>` and a short title naming the decision.
2. Write **Context**: the forces, requirements, and constraints that make this decision necessary; cite the PRD/architecture/tech-eval source for each.
3. Write **Decision**: the single option chosen, stated plainly, and the options rejected with the reason each lost. Prefer the boring, proven option absent evidence to do otherwise. **(elicit: true if the decision is a human architecture/data/spend call)**
4. Write **Consequences**: what this enables, what it costs, the new invariants/guardrails it imposes, and follow-on work it triggers.
5. Set the ADR status (`proposed | accepted | superseded`). If it supersedes a prior ADR, link both directions.
6. Write `.sdlcfa/design/adr/<id>.md` using the `adr` template. Do not infer a human decision — record it as `proposed` pending the owner.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- The decision belongs to a human (architecture, data, security, spend) and no owner has decided → record `proposed`, name the owner.
- The decision cannot be made without evidence that does not yet exist → route to `tech-eval` or `research-spike`.
- The choice would violate an accepted invariant or a prior accepted ADR.

## Output contract

- **Writes/updates:** `.sdlcfa/design/adr/<id>.md` (context, decision, consequences, status) — and the superseded ADR's status if applicable.
- **Returns:** Worker Result Contract with the ADR path, the decision and new invariants in `findings`, any pending human owner in `open_decisions`, and `handoff` → `create-architecture` or `plan`.

## Done when

- A single-decision ADR exists with cited context, a stated decision and rejected alternatives, consequences and new invariants, a status, and supersession links — and the result contract is returned.
