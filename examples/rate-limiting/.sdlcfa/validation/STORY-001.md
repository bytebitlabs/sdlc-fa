# Validation Evidence: STORY-001

Targeted story checks first, then the broader suite and the NFR load check.

| Check | Command / Method | Result | Evidence | Follow-up |
|---|---|---|---|---|
| Story tests | `pytest tests/test_rate_limit.py` | pass | 7 passed in 2.0s | — |
| Full suite | `pytest` | pass | 412 passed, 0 failed | — |
| Lint | `ruff check app tests` | pass | All checks passed | — |
| Fault injection (INV1) | unit test forces `ConnectionError` from Redis client | pass | request returns 200; `rate_limit_store_down` emitted once | — |
| Latency (NFR1) | load test, 500 rps for 60s, limiter on | pass | added p99 +2.3 ms (budget 5 ms) | — |
| Flag-off (AC5) | suite run with `RATE_LIMIT_ENABLED=0` | pass | no 429s; middleware short-circuits | — |

## Residual Risk
- Per-instance limiting only; effective global limit scales with instance count (deferred STORY-003). Accepted for first release because the incident driver was a single key against a single instance.

## Result
G5_VALIDATE: pass. No blocking failures. Proceed to release.
