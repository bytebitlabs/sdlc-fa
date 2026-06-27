# Lifecycle Reference

Read this reference when a request needs detailed SDLC phase behavior, gate handling, multi-agent coordination, or done criteria.

## Lifecycle Flow

```text
discover -> design -> plan -> build -> review -> validate -> release -> learn
```

Small low-risk work can compress to:

```text
build -> review -> learn
```

Use the full lifecycle for production execution paths, customer or regulated data, payments, capital flows, security, legal/compliance behavior, schema migrations, agent orchestration, or changes that are expensive to reverse.

## Control Plane

1. Identify the current phase from the user request, existing artifacts, status, and repository state.
2. Load the minimum durable state needed:
   - repository instructions such as `AGENTS.md`
   - project context docs
   - the current status ledger (`.sdlcfa/status.yaml` by default; see the Artifact Layout in `SKILL.md`)
   - active PRD, UX spec, architecture decisions, epics, stories, or task docs under `.sdlcfa/`
   - validation commands and safety invariants
3. Decide the next phase and explain the reason.
4. Assign one bounded job to each worker when delegation is available and authorized. Use `references/agents.md` for the role registry, assignment packet, prompt template, and result contract.
5. Run gates before phase transitions.
6. Keep status in one authoritative ledger.
7. Write a handoff when stopping.

## Resume and Audit

Run this before any phase work when `.sdlcfa/` (or the project's equivalent SDLC tree) already exists. The point is to make on-disk state authoritative again before you act on it — a resumed run that trusts a stale ledger ships the wrong thing.

Resume:

1. Read `.sdlcfa/status.yaml` and the most recent handoff in `.sdlcfa/handoffs/`.
2. Validate the ledger structurally: `python3 scripts/validate_artifacts.py --type ledger .sdlcfa/status.yaml`. Treat a non-zero exit as a blocker to fix before trusting status.
3. Reconcile the ledger against reality: repository state, branch or worktree, last validation evidence, and any open assignment results in `.sdlcfa/assignments/`. Where the ledger and reality disagree, the artifact is wrong — correct the ledger or route back to the owning phase, and record the correction.
4. Identify the lowest unmet gate for the active story and resume from the phase that owns it, not from where chat left off.
5. Mark superseded handoffs as historical so they cannot be mistaken for current status.

Audit (when the request is to verify a run rather than advance it):

- Trace each `done` story backward through the artifact chain: ledger status -> validation evidence -> review findings -> story acceptance criteria. A `done` story with no recorded review or validation evidence is a finding, not a pass.
- Confirm every passed gate names its evidence and decider; an empty `evidence` or `decided_by` field fails the audit.
- Confirm human-only gates (spend, safety, legal, data, architecture, production release) were resolved by a human, not inferred.
- Report audit results as classified findings (`decision_needed`, `patch`, `defer`, `dismiss`) like a review; do not silently repair state you did not create.

## Phase Playbooks

### Discover

Use discovery to reduce ambiguity before design or planning.

Inputs can include a rough idea, pain point, opportunity, feature request, brownfield repo, domain question, market question, technical research question, doctrine, or task list.

Workflow:

1. Define the discovery question in one sentence.
2. Search local evidence before requesting new research.
3. Split research only when questions are independent. Delegate to **Mara (Discovery Analyst)** — `research-spike` for bounded questions, then `write-brief`. When the business domain becomes clear, **Scout (Capability Scout)** may run `discover-skills` to propose domain skills (install stays gated at `G_SKILLS_TRUST`).
4. Produce a durable discovery brief.
5. Mark open questions as product, technical, data, operational, or human decision.
6. Recommend the next phase.

Output:

- problem or opportunity statement
- target users or stakeholders
- evidence and source artifacts
- constraints and assumptions
- risks, unknowns, and decision points
- out-of-scope items
- recommended next phase

### Design

Use design to align product requirements, UX, architecture, constraints, and readiness before planning.

Workflow:

1. Confirm discovery is sufficient. If the core problem, users, or evidence are unclear, return to discovery.
2. Create or update product requirements.
3. Create or update UX requirements when user experience matters.
4. Create or update architecture decisions.
5. Run readiness checks for traceability and contradictions. Delegate to **Paul (Product Manager)** for the PRD and epics, **John (Solution Architect)** for architecture, ADRs, and `readiness-check`, and **Uma (UX Designer)** for the UX spec. Once the stack is known, **Scout** may `discover-skills` to propose tech-stack skills for John and Devin (install gated at `G_SKILLS_TRUST`).
6. Record planning blockers as explicit decisions.

Traceability standard:

- each functional requirement maps to at least one planned capability
- each nonfunctional requirement has an owner or test strategy
- UX requirements become acceptance criteria or explicit non-goals
- architecture decisions constrain implementation choices
- human decisions and external dependencies are explicit gates
- deferred work is labeled outside the first build path

### Plan

Use planning to create an executable backlog that workers can implement safely.

Workflow:

1. Confirm design readiness. Return to design when requirements, UX, or architecture are missing for high-risk work.
2. Create epics and stories or update the existing plan.
3. Update sprint or lifecycle status.
4. Add dependencies, gates, validation commands, invariants, and write scopes.
5. Create worker-ready story context only when implementation is next. Delegate to **Sol (Planning Lead)** — `slice-stories` for the backlog, `draft-story` for a self-contained story contract, and `init-ledger` for the status ledger.
6. Review coverage, sequence, scope, gates, and safety.

Output:

- epics or sprint plan
- status ledger
- story files or next-story list
- dependency graph
- gate list
- recommended next build batch

### Build

Use build to implement exactly one ready story or scoped change.

Preconditions:

- `G0_PRECHECK` passed
- `G1_READY` passed
- `G2_SCOPE` passed
- acceptance criteria and validation commands are available

Workflow:

1. Read the full story or spec and relevant project context.
2. Mark work in progress only if this agent owns status.
3. Implement in task order. Delegate to **Devin (Build Engineer)** — `develop-story` — only for one ready story or scoped change.
4. Keep changes scoped to the story.
5. Update implementation notes, file list, validation history, and change log where the local methodology expects it.
6. Run story-specific tests first, then broader validations when feasible.
7. Move status to review only when every acceptance criterion and Definition of Done item is satisfied.

Stop when acceptance criteria conflict, implementation requires a human decision, a validation failure is not clearly fixable, repeated attempts fail on the same task, unrelated user changes overlap the scope, or the change would violate an invariant.

### Review

Use review after build work or before marking lifecycle artifacts done.

Review layers:

- Blind review: diff only, no private builder reasoning.
- Edge-case review: diff plus project read access.
- Acceptance audit: diff plus story, spec, and context.
- Human checkpoint: walkthrough for high-risk or ambiguous changes.
- QA generation: tests for materially missing coverage.

Delegate each layer to its specialist: **Reva (Review Auditor)** for the correctness layers (`review-diff`, `acceptance-audit`, `edge-case-review`), **Quinn (Test Architect)** for `risk-profile`, `nfr-assess`, `trace-requirements`, and the advisory `qa-gate`, and **Sam (Security Reviewer)** for `threat-model` and `sink-scan` on any security boundary. Keep review prompts independent from builder reasoning unless the selected mode requires story or context access.

Classify findings:

- `decision_needed`: needs human product, UX, architecture, data, safety, or scope input
- `patch`: unambiguous issue caused by the change
- `defer`: real issue outside this change
- `dismiss`: false positive or already handled

Patch only unambiguous findings. Never auto-resolve `decision_needed`.

### Validate

Use validation to prove required checks passed or to document why they block completion.

Validation evidence should include:

- command or manual check name
- exact command, environment, or artifact inspected
- pass/fail/blocked result
- relevant output summary
- follow-up action for failures

Prefer targeted story checks before broad suite checks. Delegate to **Val (Validation Runner)** — `run-validations` and `capture-evidence`. Treat skipped validation as residual risk unless the user explicitly accepts it.

### Release

Use release to ship a validated change to a target environment or hand it off for deploy. Required for high-risk work; small low-risk changes may fold release into validate and learn. Delegate to **Rex (Release Manager)** — `plan-release`, `rollback-plan`, `signoff-check`, and `post-release-check`.

Preconditions:

- `G5_VALIDATE` passed or its failures explicitly accepted by the decision owner
- `G4_REVIEW` complete with no unresolved decision-needed finding

Workflow:

1. Identify the deploy target and the mechanism (who or what executes the release).
2. Record a rollback plan: how to revert, the revert trigger, and who can pull it.
3. Capture the required human release sign-off. Never infer spend, safety, legal, data, or production-release approval.
4. Define post-release validation: the checks that confirm the change is healthy after it ships.
5. Pass `G7_RELEASE` before deploy. If the runtime cannot execute the deploy, produce a release handoff so a human or downstream agent can.
6. Run post-release checks and record their results, or mark them pending with an owner.

Stop when sign-off is missing, no rollback path exists, the deploy target is ambiguous, or post-release validation cannot be defined.

If a rollback trigger fires after release, or post-release checks fail, stop the forward lifecycle and switch to the Incident and Rollback loop below.

Output:

- release record with deploy target and mechanism
- rollback plan and trigger
- human sign-off evidence
- post-release validation result or pending owner

### Incident and Rollback

Use this recovery loop when a released change misbehaves in production, or when any production regression is traced to recent SDLC work. It is not a forward phase; it interrupts the lifecycle to contain harm, then routes preventive work back through the normal phases. Reach it from a fired `G7_RELEASE` rollback trigger or from an externally reported incident.

The ordering rule is: **contain first, explain later.**

1. **Detect and declare.** Confirm a rollback trigger fired (from the release record) or that a regression is real. Open an incident `INC-<id>` and record the trigger, the symptom, the blast radius (who and what is affected), the severity, and the start time. Severity sets urgency, not the depth of later analysis.
2. **Contain with the pre-defined rollback.** Execute the reversible action from the release's Rollback Plan — flag flip, revert, or redeploy previous — before root-causing. Do not debug forward on a live regression when a verified rollback exists. If no safe rollback exists, escalate to the human owner immediately; that absence is itself a release-gate failure to record.
3. **Record the rollback.** Capture what was rolled back, the exact action, who pulled it, the time, and the resulting state (fully reverted, partial, or mitigated). Set the story status to `rolled-back` and update the ledger atomically (`G6`). The change is no longer `done`.
4. **Stabilize.** Re-run the post-release checks the release defined to confirm the symptom cleared. If it did not, the rollback was incomplete or the cause is elsewhere — keep the incident open and widen the blast-radius assessment before continuing.
5. **Learn with a gate-escape analysis.** Route to the Learn phase with incident scope. Beyond a normal retro, the incident retro must name the gate (`G3`–`G7`) that should have caught this, state why it passed anyway, and define the concrete change that closes the gap: a new invariant, a guard test, a review layer, a validation command, or a release check.
6. **Route preventive work.** Convert corrective actions (restore the feature safely) and preventive actions (stop recurrence) into routed follow-ups — a fix story to build, a new invariant to design, a guard test to validate, or a stricter gate. The original story may return to `done` only after the fix re-runs the lifecycle from the phase that owns the missed gate.

Output:

- incident report at `.sdlcfa/incidents/INC-<id>.md`
- rollback record: trigger, action, actor, time, resulting state, symptom-cleared yes/no
- gate-escape analysis naming the specific gate that missed and its fix
- corrective and preventive follow-ups routed to phases, with owners
- ledger updated: story `rolled-back`, evidence linked

This loop is why the skill compounds over repeated use: every incident hardens a gate, an invariant, or a test, so the next run is measurably less likely to repeat it. Treat a gate that escapes twice as a defective gate, not bad luck — change the gate definition, not just the story.

### Learn

Use learning after a story, batch, sprint, epic, incident, or review cycle.

Workflow:

1. Determine the learning scope.
2. Review what changed, what passed, what failed, and what required human decisions.
3. For incident scope, run the gate-escape analysis from the Incident and Rollback loop and treat every escaped gate as a required, owned follow-up — not an optional note.
4. Update only authoritative docs.
5. Convert lessons into concrete follow-up actions. Delegate to **Lena (Learning Scribe)** — `retro`, `gate-escape-analysis` for incidents, and `doc-sync`.
6. Route each follow-up to discovery, design, plan, build, review, validate, or release. Prefer changing a gate, invariant, or guard test over adding a one-off reminder, so the lesson is enforced on future runs rather than remembered.

Memory rules:

- Store facts future agents need, not a transcript.
- Separate observations from decisions.
- Keep stale docs from contradicting live ledgers.
- Treat story files as specifications unless the project explicitly uses them as living records.
- Mark historical handoffs as historical when they no longer describe current status.

## Artifact Chain

```text
discovery evidence
-> PRD / UX / architecture
-> epics and stories
-> acceptance criteria and tests
-> implementation notes and file list
-> review findings
-> validation evidence
-> release record and rollback plan
-> retrospective lessons
```

If a later phase cannot trace a decision to earlier artifacts, update the artifact or route back to the phase that owns the missing decision.

## Done Criteria

A lifecycle run is done when:

- the current phase output is written to durable artifacts
- status reflects reality in the authoritative ledger
- validation or review evidence is recorded
- open decisions are explicit
- deferred work is separated from current scope
- the next agent can resume without reconstructing context from chat
