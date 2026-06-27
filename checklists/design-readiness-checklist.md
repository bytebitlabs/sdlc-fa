# Checklist: design-readiness

**Informs:** the design → plan transition (design is ready to slice into stories)
**Evaluates:** `.sdlcfa/design/prd.md`, `.sdlcfa/design/architecture.md`, `.sdlcfa/design/ux-spec.md` (if UX applies)
**Run by:** `execute-checklist` (John / Paul before handing to Sol; Ada at the gate)
**Pass rule:** every item passes or is recorded as a blocker. Any unresolved fail, or any unresolved human-decision item, means design is not ready — route back to the owning design role.

## Traceability
- [ ] Each functional requirement maps to at least one planned capability — *evidence: requirements-trace findings*
- [ ] Each nonfunctional requirement has an owner or a test strategy — *evidence: NFR table with owner/test column*
- [ ] UX requirements become acceptance criteria or explicit non-goals — *evidence: ux-spec acceptance/non-goal list*
- [ ] Architecture decisions constrain implementation choices and cite their source — *evidence: ADRs / architecture doc citations*
- [ ] Deferred work is labeled outside the first build path — *evidence: out-of-scope / later section*

## Consistency
- [ ] No unresolved contradictions across PRD, UX, and architecture — *evidence: readiness-check findings*
- [ ] Each major requirement/decision cites the discovery or source artifact behind it — *evidence: inline source citations*
- [ ] External dependencies are explicit and have an owner — *evidence: dependency list*

## Human-decision items (never inferred)
- [ ] Every product/UX/architecture/data/safety/spend decision that blocks planning is resolved or recorded as an explicit gate — *owner: named human; evidence: recorded decision*
