# Task: ui-prompt

**Persona:** Uma (UX Designer)
**Phase:** design
**Command:** `ui-prompt`
**Output:** UI generation prompt; Worker Result Contract

## Purpose

Generate a prompt for an AI UI tool (e.g. v0, Lovable) **from** the UX spec, so generated UI traces to specified flows, states, and acceptance criteria rather than to the model's invention. The prompt carries the spec's requirements forward verbatim; it does not introduce new UX decisions.

## Inputs

- `.sdlcfa/design/ux-spec.md` (flows, states, edge cases, accessibility, acceptance criteria, non-goals)
- The target AI UI tool and any design-system / component-library constraints
- Open UX decisions still recorded in the spec

## Preconditions

- `.sdlcfa/design/ux-spec.md` exists and its acceptance criteria are stable
- No open UX decision blocks the surface being prompted (else prompt only the settled surfaces)

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** UX spec. Select the surface(s) to generate and confirm none depend on an unresolved open decision.
2. Extract from the spec, citing each: the flow, every required state, accessibility requirements, and the acceptance criteria the output must satisfy.
3. Assemble the prompt: context and target tool, the flow, required states, accessibility/platform constraints, the design-system/component constraints, and the explicit **non-goals** (so the tool does not add unspecified scope).
4. State the acceptance criteria inside the prompt as the bar the generated UI must meet, so the output can be checked against the spec, not against taste.
5. Mark anything the spec leaves open as a placeholder the human must fill — do **not** invent copy, data, or design decisions to complete the prompt. **(elicit: true for any open UX decision)**
6. Emit the prompt as the deliverable (and save it alongside the spec if the project keeps prompt artifacts). **(elicit: false — agent-authored)**

## HALT / Blocking conditions

- A surface to be prompted depends on an unresolved UX decision → record it in `open_decisions`; prompt only the settled surfaces or `blocked`.
- The spec lacks the states/criteria needed to constrain generation → `blocked`; route back to `create-ux-spec`.
- Completing the prompt would require inventing a UX decision → **HALT**; that is the spec owner's call.

## Output contract

- **Writes/updates:** the UI generation prompt (returned; saved next to `.sdlcfa/design/ux-spec.md` if the project keeps prompt artifacts). Does not modify the spec.
- **Returns:** Worker Result Contract with the prompt, the spec-criteria-to-prompt mapping in `findings`, any open UX decisions left as placeholders in `open_decisions` with owners, and `handoff.next_phase`.

## Done when

- A prompt exists that carries the selected surface's flow, all required states, accessibility constraints, design-system constraints, non-goals, and acceptance criteria from the spec verbatim, with every unsettled UX decision left as an owned placeholder rather than invented.
