# Task: shard-doc

**Persona:** Paul (Product Manager)
**Phase:** design
**Command:** `shard-prd` (this generic sharder; invoked as `shard-prd` to shard the PRD)
**Output:** `.sdlcfa/design/prd/` (one file per section); Worker Result Contract

## Purpose

Split one large design document into per-section files so downstream phases load only the slice they need. This is the **generic** sharding procedure; `shard-prd` runs it against `.sdlcfa/design/prd.md` to produce one file per epic. Sharding is a mechanical, lossless split — it reorganizes content, it does not author or decide anything.

## Inputs

- The source document to shard (default: `.sdlcfa/design/prd.md`) and its section boundaries
- The target directory (default: `.sdlcfa/design/prd/`) and the split key (default: per epic / top-level heading)
- Any existing shards from a prior run

## Preconditions

- The source document exists and is the authoritative version (not a stale draft)
- The split key yields unambiguous, non-overlapping sections (e.g. one heading per epic)

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. Read the **entire** source document. Confirm it is current; if an open decision would rewrite it, stop and shard later.
2. Identify the split boundaries from the split key (each top-level section / epic heading). Confirm sections are disjoint and collectively cover the whole document.
3. Create the target directory. For each section, write one file named from its key (e.g. `epic-<id>.md`), preserving the heading, body, and any requirement citations **verbatim**.
4. Write an index/`README` in the target directory listing each shard, its source section, and what it covers, so the set is navigable.
5. Verify losslessness: every section of the source appears in exactly one shard, and no content was added, dropped, or paraphrased. **(elicit: false — mechanical)**
6. Leave the source document in place as the authoritative whole; mark the shards as derived so they are not edited independently of the source.

## HALT / Blocking conditions

- Sections overlap or the split key is ambiguous (content belongs to two epics) → `blocked`; route back to `create-epic` to resolve boundaries.
- The source is stale or has unresolved open decisions that would change its content → `blocked`; do not shard a moving target.
- A round-trip check shows content lost or altered → `blocked`; do not ship a lossy shard.

## Output contract

- **Writes/updates:** per-section files plus an index under the target directory (default `.sdlcfa/design/prd/`); the source document is unchanged.
- **Returns:** Worker Result Contract with the shard file list, the source-to-shard mapping in `findings`, any boundary ambiguities in `open_decisions`, and `handoff.next_phase` (planning).

## Done when

- The target directory holds one file per section with an index, every source section maps to exactly one shard with no content lost or altered, and the source document remains the authoritative whole.
