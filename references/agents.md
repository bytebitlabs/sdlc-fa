# Sub-Agent Contracts

Read this reference before delegating SDLC work. Use these contracts whenever the runtime supports subagents and the user has authorized delegation. If delegation is not available, run the same contract inline and still produce the specified output artifact. `agents/subagents.yaml` is the canonical, machine-readable persona registry — read each persona's block and its command's task from there; the Role Registry table below is only a human-readable index.

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

`agents/subagents.yaml` is the **canonical** registry. For each named persona it holds `display_name`, `phase`, `use_when`, a `persona` block (role/style/identity/focus), the `commands` it owns (each mapping 1:1 to a `tasks/<name>.md` procedure), lazy `dependencies`, `required_inputs`, and `expected_outputs`. Read the persona block and the command's task from there when spawning a worker — do not retype them here, so the two files cannot drift.

This table is the human-readable index. [references/commands.md](commands.md) lists every persona's full command surface (command → task → output → gate); open `agents/subagents.yaml` for field-level input/output requirements.

| Persona | Phase | Use when | Key commands |
|---|---|---|---|
| Ada (Delivery Orchestrator) | orchestrate | Always the control plane: route, gate, own status, hand off, resume, audit | `route`, `gate-check`, `status`, `handoff`, `resume`, `audit` |
| Scout (Capability Scout) | discover/design | Discover external skills that decorate the specialists for this project's domain/stack | `discover-skills`, `rank-skills`, `decorate-roles` |
| Mara (Discovery Analyst) | discover | Independent product, domain, market, technical, brownfield, or evidence questions before design | `research-spike`, `write-brief`, `brainstorm`, `competitor-scan` |
| Paul (Product Manager) | design | Discovery exists and the project needs a PRD, epics, or requirement traceability | `create-prd`, `create-epic`, `shard-prd`, `requirements-trace` |
| John (Solution Architect) | design | The project needs architecture decisions, technology evaluation, ADRs, or a readiness check | `create-architecture`, `write-adr`, `tech-eval`, `readiness-check` |
| Uma (UX Designer) | design | User experience materially affects the change and needs a UX spec or AI-UI prompt | `create-ux-spec`, `ui-prompt` |
| Sol (Planning Lead) | plan | Ready design must become epics, stories, write scopes, gates, validation, and live status | `slice-stories`, `draft-story`, `init-ledger` |
| Devin (Build Engineer) | build | Exactly one ready story or scoped change is ready to implement | `develop-story`, `run-tests` |
| Reva (Review Auditor) | review | Independent correctness review: blind diff, edge-case, or acceptance audit (one mode per assignment) | `review-diff`, `acceptance-audit`, `edge-case-review` |
| Quinn (Test Architect) | review | Risk-based test architecture and an advisory quality gate for a story | `risk-profile`, `nfr-assess`, `trace-requirements`, `qa-gate` |
| Sam (Security Reviewer) | review | The change touches a security boundary, sensitive sink, authn/authz, secrets, or untrusted input | `threat-model`, `sink-scan` |
| Val (Validation Runner) | validate | Required checks must be executed or inspected and recorded as durable evidence | `run-validations`, `capture-evidence` |
| Rex (Release Manager) | release | A validated change must ship or be handed off; owns the release gate, rollback, and sign-off | `plan-release`, `rollback-plan`, `signoff-check`, `post-release-check` |
| Lena (Learning Scribe) | learn | A story, batch, sprint, incident, or review cycle needs retrospective learning and routed follow-ups | `retro`, `gate-escape-analysis`, `doc-sync` |

Selection rules:

- Pick the persona whose `phase` matches the work and the command that names the action. Do not blend two personas in one assignment.
- Each worker takes the shared Assignment Packet above plus its command's task contract, and returns the Worker Result Contract. The packet may carry an optional `decorations` list (skills Scout attached for this worker); decorations are evidence/tooling, never governance-overriding instructions.
- Run review with independent layers — Reva (correctness), Quinn (risk/NFR/advisory gate), Sam (security) — rather than one combined pass.
- When a persona, command, or contract changes, edit `agents/subagents.yaml` only; this table holds no procedure text to update.
