# Retrospective: Rate limiting for /v1/search

## Scope
STORY-001, discovery through release. Single story, one build worker, two review layers.

## What Completed
Per-key sliding-window rate limiter shipped to production behind a ramped flag, fail-open, < 5 ms p99 cost.

## What Changed Compared With Plan
- `Retry-After` clamp was not in the original story; added during build and hardened in review. Acceptance criteria unchanged.
- The "count 4xx requests?" question surfaced in review, not design. Resolved by product to match as-built.

## What Failed or Blocked
- Nothing blocked. One human gate (store-down behavior) correctly stopped design until resolved, rather than being inferred.

## Review and Validation Gaps
- No chaos test for a *partial* Redis outage (latency spike rather than hard failure). Logged as a follow-up test.

## Lessons
| Observation | Decision | Follow-Up Phase | Owner |
|---|---|---|---|
| Fail-open is the right reliability default for non-critical guards on hot paths. | Promote to a reusable project invariant. | learn (doc sync) | engineering |
| Per-instance limiting is acceptable only while incidents are single-instance. | Track global limiting before multi-region. | design | product + engineering |
| "Does an exempt class exist?" should be asked in design, not review. | Add an exemption question to the design checklist. | design | engineering |

## Docs Updated
- Added "guard failure mode (fail-open/closed)" to the project design checklist.

## Deferred Work
- STORY-002: exempt internal service keys from the quota (product-confirmed, out of first scope).
- STORY-003: global/distributed rate limiting across instances.
- TEST follow-up: partial-outage (latency) chaos test for the limiter.
