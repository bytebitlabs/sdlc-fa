# Task: create-ux-spec

**Persona:** Uma (UX Designer)
**Phase:** design
**Command:** `create-ux-spec`
**Output:** `.sdlcfa/design/ux-spec.md`; Worker Result Contract

## Purpose

Turn the product requirements into an experience specification concrete enough that its UX requirements become acceptance criteria. Every flow, state, and edge case traces to a PRD requirement; every UX requirement becomes an acceptance criterion or an explicit non-goal; UX choices only a human can make are recorded as open decisions, never inferred.

## Inputs

- `.sdlcfa/design/prd.md` and the discovery brief
- Existing UX conventions, design system, accessibility, and platform requirements
- Any existing `.sdlcfa/design/ux-spec.md` and human UX decisions in the packet

## Preconditions

- A PRD exists and user experience materially affects the change
- Accessibility and platform targets are known or recorded as open decisions

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** PRD and brief. List the requirements that have a UX surface, citing each.
2. Define the primary user **flows** end to end. For each step name the screen/surface and the requirement it satisfies.
3. Specify **states** for every surface: default, loading, empty, error, success, and permission/disabled. Do not leave a state undefined.
4. Specify **edge cases and accessibility**: keyboard/focus, contrast, screen-reader semantics, and platform constraints. Make accessibility concrete, not aspirational.
5. Convert each UX requirement into either an **acceptance criterion** (testable, Given-When-Then where useful) or an **explicit non-goal**. Nothing is left in between.
6. Surface UX choices only a human can make (brand direction, tradeoffs that change scope, sensitive flows) as `open_decisions` with owners. **(elicit: true)** Never resolve by inference.
7. Write `.sdlcfa/design/ux-spec.md` using the `ux-spec` template: flows, states, edge cases, accessibility, acceptance criteria, non-goals, open decisions. **(elicit: false — agent-authored)**

## HALT / Blocking conditions

- A flow depends on a UX decision only a human can make → record it in `open_decisions`; do not pick a direction.
- A required experience conflicts with a PRD requirement or platform constraint → `blocked`; route back to `create-prd`.
- Accessibility or platform targets are undefined and cannot be assumed → record as `open_decisions`.

## Output contract

- **Writes/updates:** `.sdlcfa/design/ux-spec.md`.
- **Returns:** Worker Result Contract with the spec path, UX-requirement-to-acceptance/non-goal mapping in `findings`, UX decisions in `open_decisions` with owners, and `handoff.next_phase` (architecture, requirements-trace, or planning).

## Done when

- The spec exists with flows, all states per surface, edge cases, concrete accessibility, every UX requirement as an acceptance criterion or explicit non-goal each citing a PRD source, and open UX decisions with owners.
