# Templates

Read this reference when you need durable SDLC artifacts. Adapt field names to the repository's existing conventions when they already exist.

Write each artifact to its default location under `.sdlcfa/` (see the Artifact Layout in `SKILL.md`), unless the project already has an equivalent home:

| Artifact | Default path |
|---|---|
| Status Ledger | `.sdlcfa/status.yaml` |
| Story Contract | `.sdlcfa/stories/STORY-<id>.md` |
| Gate Record | inline in the ledger, or `.sdlcfa/<phase>/` notes |
| Handoff | `.sdlcfa/handoffs/<name>.md` |
| Review Report | `.sdlcfa/reviews/<id>.md` |
| Release Record | `.sdlcfa/releases/<id>.md` |
| Incident / Rollback Record | `.sdlcfa/incidents/INC-<id>.md` |
| Retrospective | `.sdlcfa/retros/<scope>.md` |
| Worker Assignment | `.sdlcfa/assignments/<id>.packet.yaml` |
| Worker Result | `.sdlcfa/assignments/<id>.result.yaml` |

The Status Ledger, Worker Assignment, and Worker Result are field-checked by `scripts/validate_artifacts.py` (types `ledger`, `assignment`, `result`). Run it before using any of them to pass a gate.

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

## Source
- PRD:
- UX:
- Architecture:
- Discovery:

## User Value

## Acceptance Criteria
- [ ] Criterion with observable behavior

## Nonfunctional Requirements
- performance:
- accessibility:
- security:
- reliability:

## Write Scope
- `path/or/module`

## Dependencies
- STORY-000

## Human Gates
| Gate | Question | Owner | Evidence Needed | Allowed Outcomes |
|---|---|---|---|---|

## Validation
```bash
command-to-run
```

## Invariants
- Constraint that cannot be violated

## Implementation Notes
- Files changed:
- Tests added:
- Validation evidence:
- Residual risk:
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

Use this template before spawning or simulating any subagent. See the Role Registry index in `references/agents.md`; read role-specific prompt templates from the canonical `agents/subagents.yaml`.

```yaml
assignment_id: "short-stable-id"
role: "Discovery Researcher | Design Synthesizer | Planning Slicer | Build Worker | Review Auditor | Validation Runner | Learning Scribe"
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
