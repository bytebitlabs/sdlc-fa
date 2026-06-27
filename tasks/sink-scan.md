# Task: sink-scan

**Persona:** Sam (Security Reviewer)
**Phase:** review
**Command:** `sink-scan`
**Output:** Security findings classified by severity; Worker Result Contract

## Purpose

Scan the change for sensitive sinks and unsafe data flows — injection, authn/authz, secrets, and data exposure — tracing untrusted input to the sink that can harm. Assume hostile input. Unresolved security risk is a decision blocker, never silently dismissed.

## Inputs

- The diff under review and the surrounding files the flows touch
- The trust boundaries and required invariants from `threat-model` (`.sdlcfa/reviews/<id>.threat.md`) if available
- The sensitive-data map for the affected surface

## Preconditions

- The change is available to read and the review id is assigned
- A threat model exists for `<id>`, or its absence is recorded so boundaries are inferred conservatively

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. **Locate sensitive sinks** in the change: query/exec/eval, command and shell, filesystem paths, deserializers, template/HTML rendering, redirects, outbound requests, and tool/agent invocations.
2. **Trace each flow back** from sink to source. A sink is a finding when untrusted input reaches it without validation, parameterization, encoding, or an authz check.
3. **Check authn/authz.** Confirm every state-changing or data-returning path enforces identity and authorization server-side; flag missing, client-only, or bypassable checks.
4. **Check secrets and data exposure.** Scan for hardcoded credentials, secrets in logs/errors/responses, over-broad data returns, and missing redaction.
5. **Test the invariants.** For each invariant from the threat model, confirm the code upholds it; a violated invariant is at least `high`.
6. **Classify each finding by severity** (`critical|high|medium|low`) and by disposition (`decision_needed | patch | defer | dismiss`). Patch only unambiguous fixes; a `dismiss` must carry a concrete reason. Never silently drop a live finding.
7. Record findings into `.sdlcfa/reviews/<id>.md` with file/line evidence, the flow, and the fix or the invariant it violates. Flag any human security decision. **(elicit: true for any security risk only a human can accept)**

## HALT / Blocking conditions

- A flow cannot be cleared because the boundary or data sensitivity is undefined → return `blocked`; do not mark it safe by assumption.
- A `critical`/`high` finding's resolution is a human security/safety/legal call → record it in `open_decisions` with an owner; it is a decision blocker, not a dismiss.

## Output contract

- **Writes/updates:** the security findings in the review report for `<id>` (proposed patches only; no scope-external edits).
- **Returns:** Worker Result Contract with findings sorted by severity and disposition in `findings`, unresolved security risk as decision blockers in `open_decisions` with owners, and `handoff` → build (patches) or `qa-gate`.

## Done when

- Every sensitive sink and unsafe flow in the change is traced, classified by severity and disposition, evidenced by file/line, no live finding is silently dismissed, and the result contract is returned.
