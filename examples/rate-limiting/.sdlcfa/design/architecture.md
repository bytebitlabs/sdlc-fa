# Architecture Decision: Rate limiter for /v1/search

## Source
- PRD: `.sdlcfa/design/prd.md`

## Decision
Implement an ASGI middleware (`app/middleware/rate_limit.py`) that runs only for `/v1/search`, keyed by the authenticated key id, backed by Redis using a sliding-window counter (sorted set per key).

## Rationale
- Redis is already deployed; no new infrastructure.
- Middleware keeps the limiter out of endpoint business logic and makes the write scope small.
- Sliding window with a sorted set gives accurate 60 s windows without a background sweep.

## Invariants (must hold after implementation)
- INV1: A limiter-store failure never propagates an error to the client (fail-open).
- INV2: The limiter never blocks a request whose key is not yet at the threshold.
- INV3: The limiter only applies to `/v1/search`; other routes are untouched.

## Constraints on Implementation
- Behind config flag `RATE_LIMIT_ENABLED` (default off) so release can ramp and roll back instantly.
- No new request-path dependency may be synchronous-blocking beyond the existing Redis client timeout (50 ms).

## Readiness
- Traceability: FR1->limit check, FR2->429+Retry-After, FR3->fail-open branch. All NFRs have a test strategy. Ready to plan.
