# Task: create-architecture

**Persona:** John (Solution Architect)
**Phase:** design
**Command:** `create-architecture`
**Output:** `.sdlcfa/design/architecture.md`; Worker Result Contract

## Purpose

Produce or update the architecture of record so planning and build have one durable, source-cited technical contract. Prefer boring technology and progressive complexity; name the invariants and implementation guardrails planning must respect. Architecture is decided on evidence, never inferred over a human decision.

## Inputs

- Discovery brief (`.sdlcfa/discovery/brief.md`) and PRD (`.sdlcfa/design/prd.md`)
- Nonfunctional requirements, existing architecture notes, and constraints
- Any `tech-eval` decision matrices and accepted ADRs under `.sdlcfa/design/adr/`
- Human decisions that cannot be inferred (architecture, data, spend, security)

## Preconditions

- Discovery and requirements exist and are sufficient; if the core problem, users, or requirements are unclear, route back to discovery/PRD
- Nonfunctional requirements and known invariants are available

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Restate the functional and nonfunctional requirements the architecture must satisfy; cite each to the PRD/brief section it comes from.
2. Define the system context: components, boundaries, data flows, and external dependencies. Prefer boring, proven technology; justify any novel choice.
3. Record the key technology decisions. For any decision with real tradeoffs, reference a `tech-eval` matrix or `write-adr` rather than deciding inline. **(elicit: true for any human architecture/data/spend decision)**
4. Name the **invariants** — constraints that must remain true at every layer (security, data integrity, consistency, idempotency).
5. Name the **implementation guardrails** planning and build must follow (allowed dependencies, module boundaries, error/secret handling, write-scope hints).
6. Record open technical risks, deferred decisions, and the human decisions still outstanding.
7. Write `.sdlcfa/design/architecture.md`. Cite every source. Do not invent facts to fill a section — mark unknowns as unknown. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- Requirements or discovery are too thin to ground an architecture → route back to design/discovery.
- A load-bearing choice requires a human architecture, data, security, or spend decision → record it, do not infer it.
- Two requirements or invariants conflict and only a human can adjudicate scope.

## Output contract

- **Writes/updates:** `.sdlcfa/design/architecture.md` (context, decisions, invariants, guardrails, risks), citing sources.
- **Returns:** Worker Result Contract with the architecture path, decisions and invariants in `findings`, outstanding human decisions in `open_decisions` with owners, and `handoff` → `plan` (or `readiness-check`).

## Done when

- The architecture doc exists with requirements traced to sources, technology decisions with rationale, named invariants and implementation guardrails, recorded risks, and explicit open human decisions — and the result contract is returned.
