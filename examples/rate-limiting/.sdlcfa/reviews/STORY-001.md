# Review Report: STORY-001

## Target
- Diff, branch, commit, story, or artifact: branch `feat/rate-limit-search`, story STORY-001
- Spec context: `.sdlcfa/stories/STORY-001.md`, `.sdlcfa/design/architecture.md`

Run as two independent layers from the build context:
1. Blind diff review (diff only, no builder notes).
2. Acceptance audit (diff + story + architecture).

## Findings
| Classification | Severity | File/Artifact | Finding | Recommendation |
|---|---|---|---|---|
| patch | medium | `app/middleware/rate_limit.py` | `Retry-After` computed from window start, off by the request's own timestamp — can return `0`. | Clamp to `max(1, seconds_left)`. Unambiguous; patch. |
| decision_needed | medium | PRD scope | Should the limiter also count requests that 4xx upstream (bad query)? Affects fairness. | Route to product; do not guess. |
| defer | low | architecture | Per-instance Redis view means the effective global limit is `60 * instance_count`. | Real but outside this change. Open STORY-003 (global limiting). |
| dismiss | info | `rate_limit.py` | Reviewer flagged a possible race on the sorted-set update. | False positive: `ZADD`+`ZREMRANGEBYSCORE` run in a single `MULTI`. Dismissed. |

## Patches Applied
- Clamped `Retry-After` to `>= 1`; added `test_retry_after_minimum`.

## Decisions Blocked
- `decision_needed` (count-4xx-requests) routed to product. STORY-001 may proceed: PRD FR1 already says "requests", and product confirmed within the hour that 4xx requests **do** count (matches as-built). No code change required; recorded for traceability.

## Validations
- Re-ran story tests after patch: 7 passed (added test). Deferred full-suite + load test to the Validation phase.

## Status Recommendation
patch again -> done: all findings resolved or deferred with owners; no unresolved `decision_needed`. Proceed to validate.
