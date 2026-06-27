# Task: route

**Persona:** Ada (Delivery Orchestrator)
**Phase:** orchestrate
**Command:** `route`
**Output:** Routing decision recorded against the ledger; Worker Result Contract

## Purpose

Classify the request into the next useful phase and select the worker role(s) that own it, so work flows to the right specialist on evidence — never by guesswork. Ada routes; she never implements.

## Inputs

- The user request and the current ledger snapshot (`.sdlcfa/status.yaml`)
- Repository rules and located project docs
- Open worker results and prior handoffs in `.sdlcfa/assignments/` and `.sdlcfa/handoffs/`

## Preconditions

- `G0_PRECHECK` has passed: repo rules loaded, required docs located, workspace state classified, invariants known
- If `.sdlcfa/` already exists, `resume` has reconciled the ledger first

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the request and the ledger. Determine the current phase from artifacts and status, not from where chat left off.
2. Classify the next useful phase using the Phase Routing table in `SKILL.md` (discover … learn). Small low-risk work may compress to build → review → learn.
3. Apply the High-Risk Defaults: if the change touches production paths, regulated data, payments, security, migrations, or irreversible ops, require the full lifecycle before build.
4. Select the worker role(s) from `agents/subagents.yaml` whose `phase` and `commands` own that phase. Split work only when the questions or write scopes are independent and disjoint.
5. Confirm the next phase's entry gate is satisfied (or route to `gate-check`). Never route past an unmet human-decision gate.
6. Record the routing decision in the ledger: next phase, selected role(s), rationale, and the entry gate to clear. **(elicit: true when the next phase needs a human decision to start)**
7. Return the Worker Result Contract describing the route. **HALT** — do not author the worker's artifact yourself.

## HALT / Blocking conditions

- The request cannot be classified into a phase, or spans several incompatible asks → `blocked`; ask the user to disambiguate.
- The next phase requires a human product/UX/architecture/data/safety/spend decision that is unresolved → `blocked`; name the owner.
- The ledger and reality disagree → `blocked`; route to `resume`/`audit` before routing forward.

## Output contract

- **Writes/updates:** the routing decision in `.sdlcfa/status.yaml` (Ada owns this write).
- **Returns:** Worker Result Contract with the chosen phase, selected role(s), the entry gate, `open_decisions` with owners, and `handoff.next_phase`/`next_action`.

## Done when

- The next phase and worker role(s) are recorded against the ledger with a rationale, the entry gate is named, and unresolved decisions are listed with owners.
