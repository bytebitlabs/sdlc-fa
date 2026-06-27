# sdlc-fa — SDLC for AI Agents

A control plane for AI-assisted software delivery. It turns chat-driven work into durable artifacts, explicit gates, bounded write scopes, independent review, and lessons that improve future runs.

Instead of relying on transcript memory, `sdlc-fa` runs work through a structured lifecycle — discovery, design, planning, scoped build, independent review, validation, release handoff, and learning — and records every phase to disk so any later agent can resume from state rather than chat.

## Why

- **Durable over ephemeral.** Requirements, decisions, status, validation, and handoffs live in files, not in a conversation that gets compacted.
- **Specialized personas, not a generic helper.** Work runs through named specialists (Ada, Mara, Paul, John, Uma, Sol, Devin, Reva, Quinn, Sam, Val, Rex, Lena), each owning a small surface of explicit commands that map 1:1 to executable procedures under `tasks/`. Ada the orchestrator owns routing, gates, status, and handoffs; each worker owns one phase, command, and write scope.
- **Skills as decorations.** A persona is a base skill; the Capability Scout discovers external [find-skills](https://github.com/vercel-labs/skills) packages that decorate the right specialist for the project's domain and stack — install gated behind a human trust decision.
- **Deterministic gates.** Structural gates are enforced by a validator, not by eye, so the contract and the registry cannot drift.
- **Human-decision gates stay human.** Product, UX, architecture, legal, safety, data, spend, production-impact, and third-party-skill-trust decisions are never resolved by inference.

## Getting started

Clone or copy this repository into a location your agent can read, then point the agent at [`SKILL.md`](SKILL.md):

```bash
git clone https://github.com/bytebitlabs/sdlc-fa.git
```

`SKILL.md` and its `references/`, `agents/`, and `scripts/` supporting files are the full operating model — keep them together so cross-references and the validator resolve. The agent loads `SKILL.md` and invokes it when you ask to create, govern, resume, audit, or improve AI-agent SDLC work.

## How it works

All durable artifacts are written under `.sdlcfa/` at the root of the project that uses the skill:

```text
.sdlcfa/
  status.yaml            # the one authoritative status ledger
  discovery/             # discovery briefs
  design/                # PRD, UX, architecture, readiness findings
  stories/               # STORY-<id>.md story contracts
  skills/                # skill decoration manifest (find-skills, human-gated)
  assignments/           # worker assignment packets and returned results
  reviews/               # review reports, risk profiles, QA gates, threat models
  validation/            # validation evidence
  releases/              # release records and rollback plans
  incidents/             # incident reports and rollback records
  retros/                # retrospectives
  handoffs/              # handoff documents
```

### Phases

| Phase | Use When | Primary Output |
|---|---|---|
| Discover | Intent, evidence, users, domain, or brownfield context is unclear | Discovery brief with risks, assumptions, decision points |
| Design | Discovery exists but product, UX, architecture, or readiness is unsettled | PRD, UX spec, architecture decisions, readiness findings |
| Plan | Design is sufficient and work must become epics, stories, and gates | Backlog, dependencies, write scopes, validation plan, status ledger |
| Build | One story or scoped change is ready for implementation | Code/docs change, tests, file list, validation evidence |
| Review | Work is ready for independent verification | Findings classified as decision-needed, patch, defer, or dismiss |
| Validate | Required commands or acceptance checks must be proven | Validation record with commands, outcomes, residual risk |
| Release | Validation passed and a change must ship or be handed off | Release record with deploy target, rollback plan, sign-off |
| Learn | A story, sprint, incident, or review cycle completed | Retrospective, doc sync, follow-up actions, memory updates |

### Roles

Each phase is owned by one or more named specialists. The orchestrator routes to a persona and runs one of its commands; the full surface (persona → command → task → output → gate) is in [`references/commands.md`](references/commands.md).

| Phase | Persona(s) |
|---|---|
| orchestrate | Ada (Delivery Orchestrator) |
| discover/design | Scout (Capability Scout) — the skill decoration layer |
| discover | Mara (Discovery Analyst) |
| design | Paul (Product Manager), John (Solution Architect), Uma (UX Designer) |
| plan | Sol (Planning Lead) |
| build | Devin (Build Engineer) |
| review | Reva (Review Auditor), Quinn (Test Architect), Sam (Security Reviewer) |
| validate | Val (Validation Runner) |
| release | Rex (Release Manager) |
| learn | Lena (Learning Scribe) |

See [SKILL.md](SKILL.md) for the full operating model, gate definitions, multi-agent rules, the decoration layer, and high-risk defaults.

## Validating artifacts

Structural gates are enforced deterministically. The validator reads its required-field lists from the canonical registry [`agents/subagents.yaml`](agents/subagents.yaml):

```bash
python3 scripts/validate_artifacts.py --type result          .sdlcfa/assignments/<id>.result.yaml
python3 scripts/validate_artifacts.py --type assignment      .sdlcfa/assignments/<id>.packet.yaml
python3 scripts/validate_artifacts.py --type ledger          .sdlcfa/status.yaml
python3 scripts/validate_artifacts.py --type gate            .sdlcfa/reviews/<id>.gate.yaml
python3 scripts/validate_artifacts.py --type skills-manifest .sdlcfa/skills/manifest.yaml
```

A non-zero exit means the artifact is missing required fields — treat that as the gate failing. The `skills-manifest` check also enforces the deterministic quality+trust bar (install count, source allowlist, recorded human sign-off) for any skill marked approved/installed. PyYAML is used when installed; otherwise a small built-in parser handles the indent-based YAML subset these contracts use.

## Repository layout

```text
SKILL.md                  # the skill definition and operating model
agents/                   # canonical persona registry (subagents.yaml) and interface
tasks/                    # one executable procedure per command (lazy-loaded)
checklists/               # content gates run via execute-checklist
references/               # lifecycle, command surface, agent contracts, templates, skill decoration
evals/                    # evaluation cases
scripts/                  # validate_artifacts.py
```

## License

Licensed under the [Apache License 2.0](LICENSE).
