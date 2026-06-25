# Worked Example: a full sdlc-fa run

This is a frozen, end-to-end run of the skill on one realistic feature, so you can see what the artifacts actually look like instead of only their templates. It is documentation, not a live project — the `app/` code it refers to is illustrative.

**Scenario.** Project `acme-api` gets the request: *"Add per-API-key rate limiting to the public `/v1/search` endpoint."* This touches a production execution path, so the orchestrator classifies it **high risk** and runs the **full lifecycle**.

All artifacts live under [`rate-limiting/.sdlcfa/`](rate-limiting/.sdlcfa). Read this file top-to-bottom; each phase links to the artifact it produced.

## How the run flowed

| Phase | Gate | What happened | Artifact |
|---|---|---|---|
| Discover | — | Framed one question, pulled evidence (incident INC-204), surfaced **3 human decisions** instead of guessing them. | [discovery/brief.md](rate-limiting/.sdlcfa/discovery/brief.md) |
| Design | — | Resolved the 3 decisions *with humans*, wrote PRD + architecture, declared invariants (INV1 fail-open). | [design/prd.md](rate-limiting/.sdlcfa/design/prd.md), [design/architecture.md](rate-limiting/.sdlcfa/design/architecture.md) |
| Plan | G0–G2 | Sliced one bounded story with a 3-file write scope and validation commands. | [stories/STORY-001.md](rate-limiting/.sdlcfa/stories/STORY-001.md) |
| Build | G3 | One Build Worker, explicit assignment packet → result contract. | [assignments/STORY-001.packet.yaml](rate-limiting/.sdlcfa/assignments/STORY-001.packet.yaml), [.result.yaml](rate-limiting/.sdlcfa/assignments/STORY-001.result.yaml) |
| Review | G4 | Two independent layers (blind diff + acceptance audit). 1 patch, 1 decision routed, 1 defer, 1 dismiss. | [reviews/STORY-001.md](rate-limiting/.sdlcfa/reviews/STORY-001.md) |
| Validate | G5 | Story tests → full suite → fault-injection + latency NFR. | [validation/STORY-001.md](rate-limiting/.sdlcfa/validation/STORY-001.md) |
| Release | G7 | Deploy target, rollback = flag flip, **human sign-off captured**, post-release monitors. | [releases/STORY-001.md](rate-limiting/.sdlcfa/releases/STORY-001.md) |
| Learn | G6 | Retro + doc sync + 3 routed follow-ups. | [retros/rate-limiting.md](rate-limiting/.sdlcfa/retros/rate-limiting.md) |

Authoritative live state for the whole run: [status.yaml](rate-limiting/.sdlcfa/status.yaml).
Resume/closing handoff: [handoffs/STORY-001-complete.md](rate-limiting/.sdlcfa/handoffs/STORY-001-complete.md).

## The five things this example is meant to teach

1. **Stop at human-decision gates.** Discovery found three product/safety decisions (threshold, store-down behavior, internal-key exemption). The run did **not** infer them — design halted until a human resolved each, and the PRD records who decided and when. The fail-open vs fail-closed choice is exactly the kind of safety decision the skill refuses to guess.

2. **Durable artifacts, not chat memory.** Every phase wrote a file under `.sdlcfa/`. A new agent could open `status.yaml` and resume without re-reading any conversation — which is the whole point of the control plane.

3. **Independent review catches different risks.** The blind diff caught an off-by-one `Retry-After` bug (patched); the acceptance audit raised a scope question (routed to product, not auto-resolved); a real-but-out-of-scope issue was **deferred** with an owner (STORY-003); and a plausible-looking race was **dismissed** with evidence. Four findings, four different classifications.

4. **Release is a real phase with its own gate.** `G7_RELEASE` required a deploy target, a rollback trigger, a captured human sign-off, and post-release validation — none of which the build/validate phases cover.

5. **The contracts are machine-checkable.** The ledger, the assignment packet, and the worker result all pass the bundled validator:

   ```bash
   python3 scripts/validate_artifacts.py --type ledger     examples/rate-limiting/.sdlcfa/status.yaml
   python3 scripts/validate_artifacts.py --type assignment examples/rate-limiting/.sdlcfa/assignments/STORY-001.packet.yaml
   python3 scripts/validate_artifacts.py --type result     examples/rate-limiting/.sdlcfa/assignments/STORY-001.result.yaml
   # -> OK / OK / OK
   ```

   That is the deterministic check standing behind G3/G6: a contract either has its required fields or the gate fails.

## What a *compressed* run would drop

A small, low-risk change (say, fixing a typo in an error string) would skip discover/design/plan/release and run only **build → review → learn**, with no `G7_RELEASE`. The full lifecycle here is a function of the production-path risk, not ceremony.
