# Checklist: story-draft

**Informs gate:** `G1_READY` (a story is ready to build)
**Evaluates:** `.sdlcfa/stories/STORY-<id>.md`
**Run by:** `execute-checklist` (Sol after `draft-story`; Ada at `G1_READY`)
**Pass rule:** every item passes or is recorded as a blocker. Any unresolved fail means the story is not ready — return it `blocked` with the exact missing decision or artifact.

## Value and acceptance
- [ ] The story states user/system value in one line — *evidence: User Value section*
- [ ] Acceptance criteria are observable and independently testable — *evidence: checkbox criteria with concrete behavior*

## Scope and dependencies
- [ ] The write scope is bounded and disjoint from any parallel story's scope — *evidence: Write Scope paths; cross-check sibling stories*
- [ ] Dependencies are listed and complete (no `blocked_by` open) — *evidence: Dependencies section + ledger*
- [ ] The story is self-contained: it cites the design sources the build agent needs so it need not re-read the PRD/architecture — *evidence: Source citations in the story*

## Execution contract
- [ ] Validation commands are specified — *evidence: Validation section*
- [ ] Invariants that must remain true are named — *evidence: Invariants section*
- [ ] Stop conditions are present — *evidence: stop-condition list*
- [ ] Risk level is set; high-risk stories name domain invariants and a review layer — *evidence: risk tag + invariants*

## Human-decision items (never inferred)
- [ ] Any human gate the story depends on is identified with owner and allowed outcomes — *owner: named human; evidence: Human Gates table*
