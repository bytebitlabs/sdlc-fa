# STORY-001: Per-key rate limiting for /v1/search

## Source
- PRD: `.sdlcfa/design/prd.md`
- UX: n/a (header contract only)
- Architecture: `.sdlcfa/design/architecture.md`
- Discovery: `.sdlcfa/discovery/brief.md`

## User Value
An overactive API key can no longer degrade `/v1/search` for other tenants, and throttled clients get a clear, machine-readable back-off signal.

## Acceptance Criteria
- [ ] AC1: A key exceeding 60 requests in a rolling 60 s window receives HTTP 429.
- [ ] AC2: 429 responses include a `Retry-After` header with seconds until the window frees.
- [ ] AC3: When Redis is unreachable, requests are allowed and a `rate_limit_store_down` event is emitted (no client error).
- [ ] AC4: Limiter applies only to `/v1/search`; other routes are unaffected.
- [ ] AC5: Limiter is gated by `RATE_LIMIT_ENABLED` (default off).

## Nonfunctional Requirements
- performance: limiter adds < 5 ms p99
- accessibility: n/a
- security: keyed on authenticated key id only; no PII stored in Redis
- reliability: fail-open on store outage (INV1)

## Write Scope
- `app/middleware/rate_limit.py`
- `app/main.py`
- `tests/test_rate_limit.py`

## Dependencies
- none

## Human Gates
| Gate | Question | Owner | Evidence Needed | Allowed Outcomes |
|---|---|---|---|---|
| Policy | Threshold/window | product | PRD decision row | resolved (60/60s) |
| Safety | Store-down behavior | engineering + on-call | PRD decision row | resolved (fail-open) |

## Validation
```bash
pytest tests/test_rate_limit.py
pytest
ruff check app tests
```

## Invariants
- INV1 fail-open on store outage
- INV2 no block below threshold
- INV3 only /v1/search affected

## Implementation Notes
- Files changed: app/middleware/rate_limit.py, app/main.py, tests/test_rate_limit.py
- Tests added: 6 (threshold, window-roll, retry-after, fail-open, route-scoping, flag-off)
- Validation evidence: `.sdlcfa/validation/STORY-001.md`
- Residual risk: per-instance view only (no global limit) — deferred to STORY-003
