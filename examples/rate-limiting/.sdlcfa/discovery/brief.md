# Discovery Brief: Rate limiting for /v1/search

## Discovery Question
Should `acme-api` add per-API-key rate limiting to the public `/v1/search` endpoint, and what evidence constrains the design?

## Problem / Opportunity
`/v1/search` is the most expensive public endpoint (fan-out to the search cluster). A single key recently issued ~40k requests in 5 minutes during an integration bug, degrading p99 latency for all tenants. There is no per-key throttle today; only a global nginx connection cap exists.

## Target Users / Stakeholders
- External API consumers (per-key quota)
- Internal services that call `/v1/search` on behalf of the web app
- On-call engineers who absorb latency incidents

## Evidence
- Incident INC-204 (search latency, 2026-05) — single key, no per-key limit. Source: `.sdlcfa/discovery/brief.md` references ops postmortem.
- nginx config caps connections, not request rate per key.
- Redis is already deployed for session storage (reusable as a limiter store).

## Constraints / Assumptions
- Must not add a hard dependency that takes the endpoint down if it fails.
- Latency budget: limiter check must add < 5 ms p99.
- API keys are already authenticated upstream; the key id is available in request context.

## Risks, Unknowns, Decision Points
- `decision_needed` (product): limit threshold and window. **Owner: product.**
- `decision_needed` (reliability/safety): fail-open vs fail-closed when the limiter store is unreachable. **Owner: engineering + on-call.**
- `decision_needed` (product): do internal service keys share the same quota? **Owner: product.**

## Out of Scope
- Distributed rate limiting across app instances (each instance has a local view today).
- Billing/quota tiers.

## Recommended Next Phase
design — the problem and evidence are clear; three human decisions must be resolved during design before planning.
