# Checklist: security

**Informs gate:** `G4_REVIEW` (security coverage for changes touching a security boundary)
**Evaluates:** the diff + `.sdlcfa/reviews/<id>.threat.md` and architecture context
**Run by:** `execute-checklist` (Sam during `threat-model`/`sink-scan`; Ada at `G4_REVIEW`)
**Pass rule:** every item passes or is recorded. Any unresolved security risk is a decision blocker, never silently dismissed — surface it to the orchestrator.

## Boundaries and access
- [ ] Trust boundaries and untrusted-input entry points are identified — *evidence: threat model*
- [ ] Authentication and authorization are enforced on every sensitive operation — *evidence: authz checks in the change*
- [ ] Least privilege is preserved (no broadened scope/role/permission without reason) — *evidence: diff review*

## Data and sinks
- [ ] Untrusted input reaching a sensitive sink (SQL, command, path, template, deserialization) is parameterized or escaped — *evidence: sink-scan findings*
- [ ] Secrets are not hardcoded, logged, or exposed in responses/errors — *evidence: secret/log scan*
- [ ] Sensitive data is not over-exposed in responses, logs, or error messages — *evidence: response/error review*

## Assurance
- [ ] Security invariants are named and testable — *evidence: invariant list*
- [ ] High-risk changes have a recorded threat model — *evidence: `.sdlcfa/reviews/<id>.threat.md`*

## Human-decision items (never inferred)
- [ ] Any accepted residual security risk is signed off by a named human owner with rationale — *owner: named human; evidence: recorded acceptance*
