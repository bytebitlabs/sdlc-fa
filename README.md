# sdlc-fa — SDLC for AI Agents

An [agent skill](https://github.com/vercel-labs/skills) that acts as a control plane for AI-assisted software delivery. It turns chat-driven work into durable artifacts, explicit gates, bounded write scopes, independent review, and lessons that improve future runs.

Instead of relying on transcript memory, `sdlc-fa` runs work through a structured lifecycle — discovery, design, planning, scoped build, independent review, validation, release handoff, and learning — and records every phase to disk so any later agent can resume from state rather than chat.

## Why

- **Durable over ephemeral.** Requirements, decisions, status, validation, and handoffs live in files, not in a conversation that gets compacted.
- **Orchestrator/worker separation.** The orchestrator owns routing, gates, status, and handoffs; each worker owns one phase, artifact, story, or write scope.
- **Deterministic gates.** Structural gates are enforced by a validator, not by eye, so the contract and the registry cannot drift.
- **Human-decision gates stay human.** Product, UX, architecture, legal, safety, data, spend, and production-impact decisions are never resolved by inference.

## Installation

This is an agent skill following the [Agent Skills specification](https://github.com/vercel-labs/skills). Install it into your project (or globally) with the `skills` CLI:

```bash
npx skills add bytebitlabs/sdlc-fa
```

The skill is agent-agnostic — it works with any agent supported by the `skills` CLI (Claude Code, Codex, Cursor, OpenCode, and others). Once installed, the agent loads [`SKILL.md`](SKILL.md) and invokes it when you ask to create, govern, resume, audit, or improve AI-agent SDLC work.

## How it works

All durable artifacts are written under `.sdlcfa/` at the root of the project that uses the skill:

```text
.sdlcfa/
  status.yaml            # the one authoritative status ledger
  discovery/             # discovery briefs
  design/                # PRD, UX, architecture, readiness findings
  stories/               # STORY-<id>.md story contracts
  assignments/           # worker assignment packets and returned results
  reviews/               # review reports
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

See [SKILL.md](SKILL.md) for the full operating model, gate definitions, multi-agent rules, and high-risk defaults.

## Validating artifacts

Structural gates are enforced deterministically. The validator reads its required-field lists from the canonical registry [`agents/subagents.yaml`](agents/subagents.yaml):

```bash
python3 scripts/validate_artifacts.py --type result     .sdlcfa/assignments/<id>.result.yaml
python3 scripts/validate_artifacts.py --type assignment .sdlcfa/assignments/<id>.packet.yaml
python3 scripts/validate_artifacts.py --type ledger     .sdlcfa/status.yaml
```

A non-zero exit means the artifact is missing required fields — treat that as the gate failing. PyYAML is used when installed; otherwise a small built-in parser handles the indent-based YAML subset these contracts use.

## Repository layout

```text
SKILL.md                  # the skill definition and operating model
agents/                   # machine-readable role registry and worker interface
references/               # lifecycle playbooks, agent contracts, templates
examples/                 # a complete worked run (rate-limiting) plus walkthrough
evals/                    # evaluation cases
scripts/                  # validate_artifacts.py
```

A complete end-to-end example — discovery through release with every `.sdlcfa/` artifact filled in — lives in [`examples/`](examples/) and [`examples/walkthrough.md`](examples/walkthrough.md).

## License

Licensed under the [Apache License 2.0](LICENSE).
