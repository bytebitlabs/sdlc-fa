# Templates

Read this reference when you need durable SDLC artifacts. Adapt field names to the repository's existing conventions when they already exist.

Write each artifact to its default location under `.sdlcfa/` (see the Artifact Layout in `SKILL.md`), unless the project already has an equivalent home:

| Artifact | Default path |
|---|---|
| Status Ledger | `.sdlcfa/status.yaml` |
| Discovery Brief | `.sdlcfa/discovery/brief.md` |
| PRD | `.sdlcfa/design/prd.md` |
| Architecture | `.sdlcfa/design/architecture.md` |
| ADR | `.sdlcfa/design/adr/<id>.md` |
| UX Spec | `.sdlcfa/design/ux-spec.md` |
| Skills Manifest | `.sdlcfa/skills/manifest.yaml` |
| Story Contract | `.sdlcfa/stories/STORY-<id>.md` |
| Gate Record | inline in the ledger, or `.sdlcfa/<phase>/` notes |
| Handoff | `.sdlcfa/handoffs/<name>.md` |
| Review Report | `.sdlcfa/reviews/<id>.md` |
| Risk Profile | `.sdlcfa/reviews/<id>.risk.md` |
| QA Gate | `.sdlcfa/reviews/<id>.gate.yaml` |
| Validation Record | `.sdlcfa/validation/<id>.md` |
| Release Record | `.sdlcfa/releases/<id>.md` |
| Incident / Rollback Record | `.sdlcfa/incidents/INC-<id>.md` |
| Retrospective | `.sdlcfa/retros/<scope>.md` |
| Worker Assignment | `.sdlcfa/assignments/<id>.packet.yaml` |
| Worker Result | `.sdlcfa/assignments/<id>.result.yaml` |

The Status Ledger, Worker Assignment, and Worker Result are field-checked by `scripts/validate_artifacts.py` (types `ledger`, `assignment`, `result`). The QA Gate and Skills Manifest are YAML contracts with the required fields shown below; the validator also field-checks them (types `gate`, `skills-manifest`). Run the relevant check before using any of these to pass a gate.

## Section Ownership

The Story Contract carries **per-section ownership**: a section names its `owner` (the role that authors it) and the `editors` allowed to change it. A worker edits **only** the sections it owns or co-edits — Devin updates Implementation Notes and the File List, Quinn writes QA Results, Reva writes the Review summary, never the requirements. This mirrors the write-scope discipline at the document level. The ownership map is declared inline in the Story Contract below.

## Status Ledger

Use one live ledger for current state.

```yaml
version: 1
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
owner: "orchestrator"
stories:
  STORY-001:
    title: "Short user-value title"
    status: "ready | in-progress | review | done | blocked | deferred | rolled-back"
    epic: "EPIC-001"
    sprint: "Sprint name or null"
    priority: "P0 | P1 | P2"
    dependencies: []
    blocked_by: []
    write_scope:
      - "path/or/module"
    validation_commands:
      - "command to run"
    invariants:
      - "constraint that must remain true"
    gates:
      G0_PRECHECK:
        decision: "pass | blocked | not-run"
        evidence: "artifact, command, or note"
        decided_by: "agent or human"
        decided_at: "YYYY-MM-DDTHH:MM:SSZ"
    audit:
      commit: null
      completed_at: null
      validation_artifact: null
      last_run_id: null
      status_reason: null
      blocked_reason: null
```

## Story Contract

````markdown
# STORY-001: Title

<!-- Section ownership — owner authors; editors may change; no one else edits.
     Source..Invariants: owner Sol (Planning Lead), editors [Sol]
     Implementation Notes + File List: owner Devin (Build Engineer), editors [Devin]
     QA Results: owner Quinn (Test Architect), editors [Quinn]
     Review: owner Reva (Review Auditor), editors [Reva, Sam]
     Status: owner Ada (Delivery Orchestrator), editors [Ada] -->

## Source            <!-- owner: Sol -->
- PRD:
- UX:
- Architecture:
- Discovery:

## User Value        <!-- owner: Sol -->

## Acceptance Criteria   <!-- owner: Sol -->
- [ ] Criterion with observable behavior

## Nonfunctional Requirements   <!-- owner: Sol -->
- performance:
- accessibility:
- security:
- reliability:

## Write Scope       <!-- owner: Sol -->
- `path/or/module`

## Dependencies      <!-- owner: Sol -->
- STORY-000

## Human Gates       <!-- owner: Sol -->
| Gate | Question | Owner | Evidence Needed | Allowed Outcomes |
|---|---|---|---|---|

## Validation        <!-- owner: Sol -->
```bash
command-to-run
```

## Invariants        <!-- owner: Sol -->
- Constraint that cannot be violated

## Implementation Notes   <!-- owner: Devin; editors: [Devin] -->
- Files changed (File List):
- Tests added:
- Validation evidence:
- Residual risk:

## QA Results        <!-- owner: Quinn; editors: [Quinn] -->
- Risk band:
- NFR assessment:
- Advisory gate (PASS | CONCERNS | FAIL | WAIVED):

## Review            <!-- owner: Reva; editors: [Reva, Sam] -->
- Findings summary:
- Status recommendation:

## Status            <!-- owner: Ada; editors: [Ada] -->
- ready | in-progress | review | done | blocked | deferred | rolled-back
````

## Gate Record

```markdown
## Gate: G1_READY

Status: pass | blocked | not-run
Decision owner:
Evidence:
Blocked stories:
Reason:
Next action:
Decided at:
```

## Handoff

```markdown
# Handoff: Run or Story Name

## Current Phase

## Completed

## Artifacts Updated
- path:

## Status Changes

## Validations
| Check | Result | Evidence |
|---|---|---|

## Open Decisions
| Decision | Owner | Blocks | Evidence Needed |
|---|---|---|---|

## Next Recommended Phase

## Resume Instructions
```

## Review Report

```markdown
# Review Report

## Target
- Diff, branch, commit, story, or artifact:
- Spec context:

## Findings
| Classification | Severity | File/Artifact | Finding | Recommendation |
|---|---|---|---|---|

## Patches Applied

## Decisions Blocked

## Validations

## Status Recommendation
done | patch again | return to build | return to plan | ask human
```

## Retrospective

```markdown
# Retrospective

## Scope

## What Completed

## What Changed Compared With Plan

## What Failed or Blocked

## Review and Validation Gaps

## Lessons
| Observation | Decision | Follow-Up Phase | Owner |
|---|---|---|---|

## Docs Updated

## Deferred Work
```

## Incident / Rollback Record

Use when a released change is rolled back or a production regression is traced to recent SDLC work. Pairs with the Incident and Rollback loop in `references/lifecycle.md`.

```markdown
# Incident INC-<id>: Short title

## Summary
- Trigger:            # which release rollback trigger fired, or external report
- Symptom:
- Blast radius:       # who and what was affected
- Severity:           # sev1 | sev2 | sev3
- Detected at:
- Resolved at:

## Linked Work
- Story:              # STORY-<id>, now `rolled-back`
- Release record:     # .sdlcfa/releases/<id>.md

## Rollback
| Field | Value |
|---|---|
| Action taken |       <!-- flag flip / revert / redeploy previous --> |
| Pulled by | |
| Time | |
| Resulting state |    <!-- fully reverted / partial / mitigated --> |
| Symptom cleared? |   <!-- yes / no, after rollback --> |

## Gate-Escape Analysis
| Escaped Gate | Why it passed | Fix that closes the gap | Follow-Up Phase | Owner |
|---|---|---|---|---|

## Corrective Actions (restore the feature safely)
-

## Preventive Actions (stop recurrence)
-

## Status
Ledger updated: story `rolled-back`; follow-ups routed with owners.
```

## Worker Assignment

Use this template before spawning or simulating any subagent. See the Role Registry index in `references/agents.md` and the command surface in `references/commands.md`; read each persona block and the command's task from the canonical `agents/subagents.yaml`.

```yaml
assignment_id: "short-stable-id"
role: "<persona display_name, e.g. Devin (Build Engineer)>"
command: "<the persona's command, e.g. develop-story>"
phase: "discover | design | plan | build | review | validate | release | learn"
objective: "one-sentence task"
inputs:
  user_request: ""
  source_artifacts: []
  status_snapshot: ""
  constraints: []
  human_decisions: []
scope:
  read_paths: []
  write_paths: []
validation:
  commands: []
  required_evidence: []
output:
  artifact_path: ""
  response_format: "Worker Result Contract"
stop_conditions: []
```

## Worker Result

Require this shape from every subagent before using its result for gates or status changes.

```yaml
assignment_id: ""
role: ""
status: "completed | blocked | partial"
summary: ""
artifacts:
  created_or_updated: []
  proposed_only: []
write_scope_used: []
validation:
  ran: []
  not_run: []
findings: []
open_decisions: []
handoff:
  next_phase: ""
  next_action: ""
```

## Discovery Brief

Owner: Mara (Discovery Analyst). Output of `write-brief`.

```markdown
# Discovery Brief: <topic>

## Problem / Opportunity
<one sentence>

## Users / Stakeholders

## Evidence
| Observation | Source | Evidence or assumption |
|---|---|---|

## Constraints

## Risks & Unknowns

## Decision Points
| Decision | Type (product/technical/data/operational/human) | Owner |
|---|---|---|

## Out of Scope

## Recommended Next Phase
```

## PRD

Owner: Paul (Product Manager). Output of `create-prd` / `create-epic`.

```markdown
# PRD: <product or feature>

## Source
- Discovery:

## Problem & Goals

## Users & Personas

## Functional Requirements
| ID | Requirement | Source | Maps to capability |
|---|---|---|---|

## Nonfunctional Requirements
| ID | NFR | Owner | Test strategy |
|---|---|---|---|

## Epics
| Epic | Goal | Acceptance theme |
|---|---|---|

## Out of Scope

## Open Decisions
| Decision | Owner | Blocks |
|---|---|---|
```

## Architecture

Owner: John (Solution Architect). Output of `create-architecture` / `tech-eval`.

```markdown
# Architecture: <system or feature>

## Source
- PRD:

## Context & Constraints

## Decisions
| ID | Decision | Rationale | ADR |
|---|---|---|---|

## Components & Data Flow

## Invariants
- Constraint that must remain true

## Implementation Guardrails

## Risks & Tradeoffs

## Open Decisions
| Decision | Owner | Blocks |
|---|---|---|
```

## ADR

Owner: John (Solution Architect). Output of `write-adr`. One decision per file.

```markdown
# ADR-<id>: <title>

## Status
proposed | accepted | superseded by ADR-<id>

## Context

## Decision

## Consequences

## Alternatives Considered
```

## UX Spec

Owner: Uma (UX Designer). Output of `create-ux-spec`.

```markdown
# UX Spec: <feature>

## Source
- PRD:

## Flows

## States & Edge Cases

## Accessibility

## UX Acceptance Criteria
- [ ] Observable UX behavior

## Non-Goals

## Open Decisions
| Decision | Owner | Blocks |
|---|---|---|
```

## Risk Profile

Owner: Quinn (Test Architect). Output of `risk-profile`. Score = probability x impact (each 1–3, so 1–9). Bands: `>= 9` FAIL, `>= 6` CONCERNS, else acceptable.

```markdown
# Risk Profile: STORY-<id>

## Risks
| Risk | Probability (1-3) | Impact (1-3) | Score | Band |
|---|---|---|---|---|

## Top Risks & Mitigations

## Residual Risk
```

## QA Gate

Owner: Quinn (Test Architect). Output of `qa-gate`. Advisory input to `G4_REVIEW` — a `FAIL` is required evidence the orchestrator must resolve, not a unilateral stop. Field-checked by `validate_artifacts.py --type gate`.

```yaml
review_id: ""
story: ""
decision: "PASS | CONCERNS | FAIL | WAIVED"
evidence:
  - "path to risk/nfr/trace artifact"
top_issues:
  - "issue that drove the decision"
waiver:
  owner: null            # named human; required only for WAIVED
  reason: null
  expiry: null
note: "Advisory input to G4_REVIEW; the orchestrator records the gate."
decided_by: ""
decided_at: ""
```

## Validation Record

Owner: Val (Validation Runner). Output of `run-validations` / `capture-evidence`.

```markdown
# Validation Record: STORY-<id>

## Environment

## Checks
| Check | Command | Result | Evidence |
|---|---|---|---|
<!-- Result: pass | fail | blocked | skipped -->

## Failures & Follow-ups

## Residual Risk
```

## Release Record

Owner: Rex (Release Manager). Output of `plan-release` / `rollback-plan` / `signoff-check` / `post-release-check`. Required for high-risk releases (`G7_RELEASE`).

```markdown
# Release Record: <id>

## Change
- Story:

## Preconditions
- G4_REVIEW: <complete, no unresolved decision_needed>
- G5_VALIDATE: <passed, or failures accepted by owner>

## Deploy
- Target:
- Mechanism (who or what executes):

## Rollback Plan
| Field | Value |
|---|---|
| Action |   <!-- flag flip / revert / redeploy previous --> |
| Trigger | |
| Who can pull | |

## Human Sign-Off
| Approver | Decision | Time |
|---|---|---|
<!-- never inferred -->

## Post-Release Validation
| Check | Result | Owner |
|---|---|---|
```

## Skills Manifest

Owner: Scout (Capability Scout). Output of `discover-skills` / `rank-skills` / `decorate-roles`. The project's capability decoration registry. No skill is installed before its `trust_decision` is recorded by a human at `G_SKILLS_TRUST`. Field-checked by `validate_artifacts.py --type skills-manifest`.

```yaml
version: 1
discovered_at: "YYYY-MM-DDTHH:MM:SSZ"
skills:
  - name: "nextjs"
    source: "vercel-labs/skills@nextjs"
    install_count: 12000
    stars: 800
    reputation: "trusted-owner"          # allowlist hit | unknown
    decorates: ["John (Solution Architect)", "Devin (Build Engineer)"]
    phase: ["design", "build"]
    status: "proposed | approved | installed | rejected"
    rank: null
    trust_decision:
      decided_by: null                    # named human; required before install
      decided_at: null
      rationale: null
```
