# Task: rank-skills

**Persona:** Scout (Capability Scout)
**Phase:** discover, design
**Command:** `rank-skills`
**Output:** Ranked candidate set in the manifest; Worker Result Contract

## Purpose

Order the `proposed` candidates that `discover-skills` produced so the `G_SKILLS_TRUST` human gate sees a defensible shortlist. Ranking is sourcing analysis, not approval: it sorts evidence by install count, source reputation, and stars. Nothing here installs a skill or overrides governance.

## Inputs

- `.sdlcfa/skills/manifest.yaml` with one or more entries at `status: proposed`
- The source-reputation allowlist and the quality thresholds used at discovery
- The `G_SKILLS_TRUST` human decision owner

## Preconditions

- `discover-skills` has run and written `proposed` entries with metadata (install count, source, stars, `decorates`/`phase`)
- Each candidate already cleared the deterministic quality bar; rejected candidates are recorded with reasons

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Load `.sdlcfa/skills/manifest.yaml` and select only entries at `status: proposed`. Ignore `rejected` ones (their reasons stand).
2. Confirm each candidate's metadata is present and concrete: install count, source owner, stars. If any field is missing, treat the candidate as unrankable and flag it back to `discover-skills` rather than guessing a value.
3. Rank within each `decorates`/persona group, in this precedence: (a) source reputation — allowlisted owner first; (b) install count, descending; (c) stars, descending. Break ties by most recent maintained release.
4. Record a one-line ranking rationale per candidate citing the deciding metric. Separate the observed metric from any assumption about fitness.
5. Write the ordered list back into the manifest as a `rank` field per entry; keep `status: proposed` and leave `trust_decision` empty. **(elicit: false)**
6. Stop at the trust gate. Do **not** run `npx skills add`. Hand the ranked manifest to `decorate-roles` only after `G_SKILLS_TRUST` sign-off.

## HALT / Blocking conditions

- A candidate's metadata is missing or contradictory → mark it unrankable; route back to `discover-skills`, do not invent a metric.
- Two candidates decorate the same persona/phase and only a human can choose → record both, ranked, and name the choice as a `G_SKILLS_TRUST` decision.
- Any step would install or activate a skill → **HALT**; ranking never installs.

## Output contract

- **Writes/updates:** `.sdlcfa/skills/manifest.yaml` (adds `rank` + rationale to proposed entries; no installs, no status change).
- **Returns:** Worker Result Contract with the ranked candidate set, per-candidate rationale in `findings`, and `open_decisions` naming `G_SKILLS_TRUST` and its owner.

## Done when

- Every proposed candidate carries a `rank` and a cited rationale, ties are surfaced as human decisions, `trust_decision` is still empty, and nothing has been installed.
