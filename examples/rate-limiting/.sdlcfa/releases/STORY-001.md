# Release Record: STORY-001

High-risk release (production execution path). G7_RELEASE required.

## Deploy Target & Mechanism
- Target: production `acme-api`, all instances.
- Mechanism: standard CD pipeline deploy of branch `feat/rate-limit-search`, then config ramp of `RATE_LIMIT_ENABLED`.
- Ramp: deploy with flag **off** -> enable for 1 canary instance -> 10% -> 100% over 24h.

## Rollback Plan
- Trigger: 429 rate > 2% of `/v1/search` traffic OR p99 latency regression > 5 ms OR any `rate_limit_store_down` storm.
- Action: set `RATE_LIMIT_ENABLED=0` (instant, no redeploy). Flag flip reverts to pre-change behavior.
- Who can pull it: on-call engineer or eng lead.

## Human Sign-off
| Approver | Role | Decision | Date |
|---|---|---|---|
| J. Okafor | Eng lead | Approved production release with staged ramp | 2026-06-24 |

> Sign-off captured from a human; not inferred. Spend/safety/production-release gate is human-only.

## Post-Release Validation
| Check | Window | Result |
|---|---|---|
| 429 rate within expected band (< 0.5% steady state) | 30 min post-100% | pass (0.18%) |
| p99 latency delta | 30 min | pass (+2.1 ms) |
| `rate_limit_store_down` alerts | 30 min | none |

## Result
G7_RELEASE: pass. Shipped to 100% on 2026-06-24. Rollback path verified on canary (flag flip tested).
