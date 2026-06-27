# Task: tech-eval

**Persona:** John (Solution Architect)
**Phase:** design
**Command:** `tech-eval`
**Output:** Decision matrix in `.sdlcfa/design/architecture.md`; Worker Result Contract

## Purpose

Evaluate technology options against the actual requirements and constraints with a transparent decision matrix, so the architecture choice is defensible and source-cited rather than fashion-driven. Bias toward boring, proven technology; make any novel choice earn its place.

## Inputs

- The decision under evaluation and the candidate options
- PRD/architecture requirements, nonfunctional requirements, and hard constraints
- Discovery evidence, vendor docs, benchmarks, and existing-stack facts (cited)
- Spend, licensing, and operational constraints; human decisions that cannot be inferred

## Preconditions

- The decision is bounded and there is more than one credible option
- The requirements and constraints to score against are written and stable enough to compare

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. State the decision in one sentence and the requirements/constraints that act as evaluation criteria (correctness, fit, NFRs, operability, cost, maturity, lock-in).
2. Enumerate the candidate options, including the boring/default/"do nothing new" option as a baseline.
3. Build the matrix: criteria as rows, options as columns. Score each cell against evidence, not preference; cite the source for each material score.
4. Note disqualifiers — any option that violates a hard constraint or invariant is out regardless of other scores.
5. Recommend the option that best satisfies the criteria, preferring the proven choice when scores are close. State the key tradeoff accepted.
6. Record assumptions, open risks, and any decision that only a human can sign off. **(elicit: true for spend/licensing/architecture human decisions)**
7. Write the matrix and recommendation into `.sdlcfa/design/architecture.md` (and seed a `write-adr` for the chosen decision). Mark unknowns as unknown.

## HALT / Blocking conditions

Return `status: blocked` (do not guess) when:

- The evaluation criteria depend on requirements not yet decided → route back to PRD/architecture.
- The recommendation hinges on a spend, licensing, or architecture decision only a human can make → record it in `open_decisions`.
- No option satisfies a hard constraint → report the gap rather than forcing a pick.

## Output contract

- **Writes/updates:** the decision matrix and recommendation section in `.sdlcfa/design/architecture.md`, citing sources.
- **Returns:** Worker Result Contract with the matrix location, the recommendation and accepted tradeoff in `findings`, human sign-offs in `open_decisions`, and `handoff` → `write-adr` or `create-architecture`.

## Done when

- A cited options-vs-criteria matrix exists with a recommendation, the accepted tradeoff and disqualifiers named, open human decisions explicit, and the result contract returned.
