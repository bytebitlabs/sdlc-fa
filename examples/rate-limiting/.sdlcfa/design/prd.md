# PRD: Per-key rate limiting for /v1/search

## Source
- Discovery: `.sdlcfa/discovery/brief.md`
- Incident: INC-204

## Goal
Protect `/v1/search` and its tenants from a single API key consuming disproportionate capacity, without making the endpoint fragile.

## Human Decisions Resolved (during design)
| Decision | Owner | Resolution | Recorded |
|---|---|---|---|
| Limit threshold + window | product | 60 requests / 60 s per key, sliding window | 2026-06-20 |
| Behavior when limiter store is unreachable | engineering + on-call | **fail-open** (allow the request) and emit a `rate_limit_store_down` alert | 2026-06-20 |
| Internal service keys share quota? | product | **No** — internal keys are exempt. Deferred to a follow-up story to keep the first change bounded. | 2026-06-20 |

## Functional Requirements
- FR1: Each external API key may make at most 60 `/v1/search` requests per rolling 60 s.
- FR2: Requests over the limit receive HTTP 429 with a `Retry-After` header.
- FR3: When the limiter store is unreachable, requests are allowed (fail-open) and an alert is emitted.

## Nonfunctional Requirements
- NFR1 (performance): limiter adds < 5 ms p99 to the endpoint. Test strategy: latency assertion in load test.
- NFR2 (reliability): limiter store outage must not return errors to clients. Test strategy: fault-injection unit test.
- NFR3 (observability): expose `rate_limited_total` and `rate_limit_store_down` metrics. Owner: platform.

## Non-Goals
- Distributed/global limiting across instances (follow-up).
- Internal-key exemption implementation (follow-up STORY-002).

## Acceptance (UX-level)
- A throttled client can read remaining quota from `Retry-After` and back off.
