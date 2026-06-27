# Task: risk-profile

**Persona:** Quinn (Test Architect)
**Phase:** review
**Command:** `risk-profile`
**Output:** `.sdlcfa/reviews/<id>.risk.md`; Worker Result Contract

## Purpose

Score the risks a story carries on a probability x impact basis so review effort and the advisory gate are driven by evidence, not gut feel. This is advisory authority: it informs `G4_REVIEW`, it does not hard-block.

## Inputs

- The story contract (`.sdlcfa/stories/STORY-<id>.md`), its acceptance criteria, and the diff under review
- The risk classification and any high-risk triggers the story declares (security boundaries, schema migration, agent orchestration, payments, regulated data)
- The architecture/invariant context the story cites

## Preconditions

- Build is complete and the change is available to read
- `G3_DEV_DONE` has passed for this story
- The review id is assigned so artifacts share `<id>`

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the story, its acceptance criteria, and the diff. Note every high-risk trigger present.
2. Enumerate discrete risks across categories: technical, security, performance, data, operational, and business.
3. For each risk, score **probability** (1 low, 2 medium, 3 high) and **impact** (1 minor, 2 degraded, 3 severe).
4. Compute `score = probability x impact` (1–9) per risk and sort descending.
5. Apply the band: any risk `>= 9` -> **FAIL**; any risk `>= 6` -> **CONCERNS**; otherwise the profile is clean.
6. For each scored risk, record a concrete mitigation or test focus the reviewer/builder must cover; flag any residual risk that only a human can accept. **(elicit: true for any risk acceptance only a human can make)**
7. Write `.sdlcfa/reviews/<id>.risk.md`: the risk table, scores, bands, top risks, and recommended test focus. Do not invent risks to fill the table; mark unknowns as unknown.

## HALT / Blocking conditions

- The diff or acceptance criteria are unavailable or ambiguous → return `blocked`; route back rather than scoring blind.
- A risk's acceptance is a human product/safety/data/spend decision → record it in `open_decisions` with an owner; never accept it by inference.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.risk.md` (the risk profile only).
- **Returns:** Worker Result Contract with the highest score, the band (FAIL/CONCERNS/clean), top risks and mitigations in `findings`, human risk acceptances in `open_decisions`, and `handoff` → remaining review work or `qa-gate`.

## Done when

- Every identified risk is scored `probability x impact`, the band is set, mitigations/test focus are recorded, the risk file exists, and the result contract is returned for the gate to consume.
