# Checklist: story-dod

**Informs gate:** `G3_DEV_DONE` (definition of done for a built story)
**Evaluates:** the diff + `.sdlcfa/stories/STORY-<id>.md` (Implementation Notes, File List)
**Run by:** `execute-checklist` (Devin at the end of `develop-story`; Ada at `G3_DEV_DONE`)
**Pass rule:** every item passes or is recorded as a blocker. Any unresolved fail means the story is not done — keep it `in-progress`, do not move it to `review`.

## Implementation
- [ ] Every acceptance criterion is implemented — *evidence: criterion → code/test mapping*
- [ ] Only paths inside the declared write scope were changed — *evidence: File List vs Write Scope*
- [ ] No new dependency was added without recorded approval — *evidence: dependency diff*
- [ ] Named invariants still hold — *evidence: invariant checks/tests*

## Tests and validation
- [ ] Tests were added or updated for each acceptance criterion — *evidence: new/updated test files*
- [ ] Story-specific validations pass; the broader suite + lint pass or failures are recorded as blockers — *evidence: command output*

## Record
- [ ] The story File List and Implementation Notes are updated (files changed, tests added, evidence, residual risk) — *evidence: Implementation Notes*
- [ ] Residual risk is stated explicitly (or "none") — *evidence: Residual risk line*

## Human-decision items (never inferred)
- [ ] Any decision surfaced during build that needs product/UX/architecture/data/safety input is recorded as an open decision, not resolved by guess — *owner: named human; evidence: open_decisions*
