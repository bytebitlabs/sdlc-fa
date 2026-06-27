# Task: brainstorm

**Persona:** Mara (Discovery Analyst)
**Phase:** discover
**Command:** `brainstorm`
**Output:** Brainstorm output appended to the brief; Worker Result Contract

## Purpose

Facilitate structured ideation on one topic and capture the result as durable options in the discovery brief, not chat. Brainstorming widens then narrows the option space; it never decides — it hands ranked options and open decisions to the human and to design.

## Inputs

- The ideation topic or framing question
- The discovery brief and any `research-spike` evidence for grounding
- Known constraints, out-of-scope items, and the evaluation criteria
- Stop conditions

## Preconditions

- The topic is framed in a single sentence and tied to a discovery question
- The brief exists or is being authored in the same run, so options have a durable home

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. State the ideation topic in one sentence and the criteria options will be judged against.
2. Diverge: generate a broad set of candidate ideas/approaches. Do not filter for feasibility yet; quantity first.
3. Converge: cluster the ideas, remove duplicates, and discard those that violate a known constraint or out-of-scope boundary.
4. For each surviving option, note the supporting evidence (cite it) versus the assumption it rests on. Keep the two separate.
5. Evaluate options against the criteria; record tradeoffs, not a winner. Where a human must choose direction, tag it as a decision with an owner. **(elicit: true for any human direction-setting decision)**
6. Append the structured output (topic, options, tradeoffs, decisions, discarded ideas with reasons) to `.sdlcfa/discovery/brief.md`. Do not invent evidence to favor an option.

## HALT / Blocking conditions

- The topic is too broad to ideate usefully → return `blocked`; route back to `research-spike` or ask the human to narrow it.
- Converging requires a product/strategy decision only a human can make → record it in `open_decisions` with an owner; present options, do not pick one.
- Ideas depend on facts not yet in evidence → mark them assumptions and flag the spike needed.

## Output contract

- **Writes/updates:** the brainstorm section of `.sdlcfa/discovery/brief.md` (options, tradeoffs, discarded ideas with reasons).
- **Returns:** Worker Result Contract with ranked options and tradeoffs in `findings`, direction decisions in `open_decisions` with owners, and `handoff.next_phase`.

## Done when

- The brief carries a structured option set with tradeoffs, evidence separated from assumption, discarded ideas reasoned, and any direction-setting decision named with an owner — no decision was made for the human.
