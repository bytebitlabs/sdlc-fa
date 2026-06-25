# Sub-Agent Contracts

Read this reference before delegating SDLC work. Use these contracts whenever the runtime supports subagents and the user has authorized delegation. If delegation is not available, run the same contract inline and still produce the specified output artifact. `agents/subagents.yaml` is the canonical, machine-readable role registry — read each worker's prompt from there; the Role Registry table below is only a human-readable index.

## Delegation Rules

- The orchestrator chooses the sub-agent role, prepares the input packet, and owns all status ledger writes.
- Do not spawn a generic "helpful agent." Pick one contract below and keep the assignment bounded to one phase, story, review layer, validation set, or artifact.
- Give each worker only the minimum repo context, artifacts, write scope, and commands needed for its assignment.
- Make write scopes explicit. Workers may read outside scope when needed for context, but may only edit paths listed in the assignment.
- Require a structured result from every worker. Treat missing fields as incomplete work and route back to the worker or record a blocker.
- Use parallel workers only when their write scopes are disjoint or the work is read-only. Serialize all shared artifact and status updates through the orchestrator.

## Assignment Packet

Every delegated task must include this packet.

```yaml
assignment_id: "short-stable-id"
role: "one role from this file"
phase: "discover | design | plan | build | review | validate | release | learn"
objective: "one-sentence task"
inputs:
  user_request: "verbatim or concise summary"
  source_artifacts:
    - "path or external reference"
  status_snapshot: "current ledger state relevant to this task"
  constraints:
    - "system, repo, product, UX, architecture, data, safety, or scope constraint"
  human_decisions:
    - "known decision, owner, or unresolved question"
scope:
  read_paths:
    - "path or glob"
  write_paths:
    - "path or glob, or [] for read-only"
validation:
  commands:
    - "command the worker may run"
  required_evidence:
    - "test output, source citation, review finding, or artifact path"
output:
  artifact_path: "where the worker should write or propose output"
  response_format: "Worker Result Contract"
stop_conditions:
  - "conditions that require returning blocked instead of guessing"
```

## Worker Result Contract

Every worker returns this shape in the final message or writes it to the requested artifact path.

```yaml
assignment_id: "same as input"
role: "same as input"
status: "completed | blocked | partial"
summary: "what was done or learned"
artifacts:
  created_or_updated:
    - "path"
  proposed_only:
    - "path or description"
write_scope_used:
  - "path actually edited, or []"
validation:
  ran:
    - command: "exact command or manual check"
      result: "pass | fail | blocked"
      evidence: "short output summary or artifact path"
  not_run:
    - command: "command"
      reason: "why not"
findings:
  - classification: "decision_needed | patch | defer | dismiss | observation"
    severity: "critical | high | medium | low | info"
    target: "file, artifact, requirement, or story"
    detail: "specific finding"
    recommendation: "next action"
open_decisions:
  - decision: "question"
    owner: "human | product | UX | architecture | data | safety | engineering"
    blocks: "phase, story, or artifact"
handoff:
  next_phase: "discover | design | plan | build | review | validate | release | learn | none"
  next_action: "concrete next step"
```

## Role Registry

`agents/subagents.yaml` is the **canonical** registry. It holds each role's `use_when`, `required_inputs`, `prompt`, and `expected_outputs` in machine-readable form. Read the per-role `prompt` from there verbatim when spawning a worker — do not retype prompts here, so the two files cannot drift.

This table is the human-readable index. For any role, open `agents/subagents.yaml` for its full assignment prompt and field-level input/output requirements.

| Role | Phase | Use when | Returns |
|---|---|---|---|
| Discovery Researcher | discover | Independent product, domain, market, technical, brownfield, or evidence questions before design or planning | Evidence-backed observations, citations, assumptions, decision points with owners, next phase |
| Design Synthesizer | design | Discovery exists and the project needs PRD, UX, architecture decisions, readiness checks, or contradiction analysis | Design artifact, traceability notes, contradictions and planning blockers, human-decision list |
| Planning Slicer | plan | Ready design must become epics, stories, dependencies, write scopes, gates, validation commands, and live status fields | Epics or story list, dependency graph, write scopes and validation plan, status ledger update, readiness blockers |
| Build Worker | build | Exactly one ready story or scoped change is ready to implement | Scoped implementation or patch, file list, acceptance coverage, validation evidence, residual risk |
| Review Auditor | review | Independent review after build or before marking artifacts done; one mode per assignment (blind diff, edge-case, acceptance audit, human-checkpoint prep, QA generation) | Findings by severity, classification per finding, patch recommendations or decision blockers, status recommendation |
| Validation Runner | validate | Required checks must be executed or inspected and recorded as durable evidence | Command evidence, pass/fail/blocked/skipped per check, failure follow-ups, residual risk |
| Learning Scribe | learn | A story, batch, sprint, incident, or review cycle needs retrospective learning, doc sync, and follow-up routing | Retrospective artifact, lessons and follow-ups, doc-sync proposal, next phase and owner per follow-up |

Selection rules:

- Pick the role whose `phase` matches the work. Do not blend two roles in one assignment.
- Each role takes the shared Assignment Packet above plus its `required_inputs` from `agents/subagents.yaml`, and returns the Worker Result Contract.
- When a role's prompt or contract changes, edit `agents/subagents.yaml` only; this table holds no prompt text to update.
