# Task: nfr-assess

**Persona:** Quinn (Test Architect)
**Phase:** review
**Command:** `nfr-assess`
**Output:** `.sdlcfa/reviews/<id>.nfr.md`; Worker Result Contract

## Purpose

Assess the change against its non-functional requirements — security, performance, reliability, and maintainability — so quality attributes are evaluated on evidence, not assumed. This is advisory input to `G4_REVIEW`; it does not hard-block.

## Inputs

- The story contract, its acceptance criteria, and the diff under review
- The NFR targets the story or architecture declares (latency, throughput, availability, error budgets, security invariants)
- Any `risk-profile` output (`.sdlcfa/reviews/<id>.risk.md`) for this review

## Preconditions

- Build is complete and the change is available to read
- `G3_DEV_DONE` has passed for this story
- The review id is assigned so artifacts share `<id>`

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the story, the diff, and any declared NFR targets. If a target is missing, treat it as unknown — do not assume one.
2. Assess **security**: authn/authz, secrets handling, input validation, data exposure. Defer deep sink analysis to Sam; record what you can see and any boundary you cannot clear.
3. Assess **performance**: hot paths, query/loop cost, payload size against any stated target.
4. Assess **reliability**: error handling, retries, idempotency, failure modes, and observability.
5. Assess **maintainability**: test coverage for the change, complexity, duplication, and clarity.
6. Give each attribute a status: `PASS` (target met with evidence), `CONCERNS` (gap or unverified target), or `FAIL` (target violated). Cite the evidence for each.
7. Write `.sdlcfa/reviews/<id>.nfr.md`: per-attribute status, evidence, gaps, and recommended follow-up. Mark any target that needs a human to set or accept. **(elicit: true for any NFR target only a human can set or waive)**

## HALT / Blocking conditions

- A target required to judge an attribute is undefined and only a human can set it → record it in `open_decisions`; do not invent a threshold.
- The diff is unavailable or unclear → return `blocked`; route back rather than guessing.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.nfr.md` (the NFR assessment only).
- **Returns:** Worker Result Contract with per-attribute status, evidence and gaps in `findings`, undefined targets in `open_decisions` with owners, and `handoff` → remaining review work or `qa-gate`.

## Done when

- Security, performance, reliability, and maintainability each carry a status and cited evidence, gaps and follow-ups are recorded, the NFR file exists, and the result contract is returned for the gate to consume.
