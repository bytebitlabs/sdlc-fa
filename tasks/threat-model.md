# Task: threat-model

**Persona:** Sam (Security Reviewer)
**Phase:** review
**Command:** `threat-model`
**Output:** `.sdlcfa/reviews/<id>.threat.md`; Worker Result Contract

## Purpose

Enumerate what the change exposes — assets, entry points, trust boundaries, threats — and name the security **invariants** that must hold, assuming hostile input. Unresolved security risk is a decision blocker, never silently dismissed.

## Inputs

- The diff and the architecture/context it touches
- The trust boundaries and sensitive-data map for the affected surface
- Any named security invariants the story or architecture already declares

## Preconditions

- The change touches a security boundary, sensitive sink, authn/authz, secrets, or untrusted input
- The change is available to read and the review id is assigned

## Procedure (SEQUENTIAL — do not proceed until the current step is complete)

1. **Inventory assets.** List what an attacker would want: data, credentials, capabilities, funds, compute, and the integrity of high-impact state.
2. **Map entry points.** Enumerate where untrusted input enters the change: requests, params, headers, files, queues, model output, and tool/agent inputs.
3. **Draw trust boundaries.** Mark where data crosses from untrusted to trusted, and where privilege changes. Treat model and tool output as untrusted across the boundary.
4. **Enumerate threats.** For each boundary, reason adversarially — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege — and the injection/authz/secret-exposure paths specific to this change.
5. **Name invariants.** For each credible threat, state the security invariant that must hold (e.g. "no user-supplied path reaches the filesystem un-normalized", "authz is checked server-side before any state write").
6. **Classify residual risk** per finding: `decision_needed` (human security call), `patch` (unambiguous fix), `defer` (real, outside this change), or `dismiss` (false positive, with reason). Never silently dismiss live security risk.
7. Write `.sdlcfa/reviews/<id>.threat.md`: assets, entry points, boundaries, threats, invariants, and classified residual risk. Flag human security decisions. **(elicit: true for any security risk only a human can accept)**

## HALT / Blocking conditions

- The change touches a boundary whose data map or trust context is undefined → return `blocked`; route back rather than modeling blind.
- A threat's acceptance is a human security/safety/legal decision → record it in `open_decisions` with an owner; never accept it by inference.

## Output contract

- **Writes/updates:** `.sdlcfa/reviews/<id>.threat.md` (the threat model only).
- **Returns:** Worker Result Contract with the asset/boundary inventory, threats and required invariants in `findings`, classified residual risk, security decisions in `open_decisions` with owners, and `handoff` → `sink-scan` or `qa-gate`.

## Done when

- Assets, entry points, trust boundaries, threats, and required invariants are recorded, each residual risk is classified (none silently dismissed), the threat file exists, and the result contract is returned.
