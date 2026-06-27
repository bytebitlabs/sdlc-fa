# Checklist: release

**Informs gate:** `G7_RELEASE` (a validated change is ready to ship — high-risk releases)
**Evaluates:** `.sdlcfa/releases/<id>.md` + the story's review/validation evidence
**Run by:** `execute-checklist` (Rex during `plan-release`; Ada at `G7_RELEASE`)
**Pass rule:** every item passes or is recorded as a blocker. A missing sign-off or absent rollback path means the gate does not pass — do not ship. Never infer release approval.

## Preconditions
- [ ] `G5_VALIDATE` passed, or its failures were explicitly accepted by the decision owner — *evidence: validation record + acceptance*
- [ ] `G4_REVIEW` is complete with no unresolved `decision_needed` finding — *evidence: review reports / qa-gate*

## Release plan
- [ ] The deploy target and mechanism (who or what executes the release) are identified — *evidence: release record*
- [ ] A rollback plan is recorded: how to revert, the trigger, and who can pull it — *evidence: Rollback section*
- [ ] A safe rollback path exists; if none exists, that is a gate failure to escalate — *evidence: rollback mechanism*
- [ ] Post-release validation is defined (the checks that confirm health after ship) — *evidence: post-release checks*

## Human-decision items (never inferred)
- [ ] The required human release sign-off is captured (spend/safety/legal/data/production approval is never inferred) — *owner: named human; evidence: recorded sign-off*
