# ADR-001: Architecture as Code Using Git and YAML

**Status:** Accepted
**Date:** 2026-06-18
**Deciders:** Business Architecture Practice Lead, Enterprise Architecture Team

## Context

Business architecture artefacts (capability maps, value streams, organisation
structures, information models) have historically been maintained in
presentation tools (PowerPoint, Visio) or locked inside enterprise architecture
tools (Sparx EA, ArchiMate tools). This creates several problems:

- Artefacts are not version-controlled; change history is lost.
- Review and approval happens outside normal engineering workflows.
- Tooling is expensive and requires specialist licences.
- Artefacts drift out of sync with the systems they describe.

The team evaluated three approaches:

1. Continue using Sparx Enterprise Architect (status quo)
2. Migrate to a SaaS architecture tool (LeanIX, Ardoq)
3. Store artefacts as text files in Git ("Architecture as Code")

## Decision

We will store all business architecture artefacts as YAML files in a Git
repository, validated by JSON Schema, with CI/CD enforcing correctness on
every change.

## Rationale

- **Version control is free and universal.** Every change is auditable via
  `git log`; branching supports speculative modelling.
- **Pull request reviews** bring architecture governance into the same
  workflow used for software changes.
- **JSON Schema** provides machine-readable contracts that prevent schema
  drift without requiring a proprietary tool.
- **Plain text** survives tool obsolescence; YAML files from 2026 will be
  readable in 2036.
- **Cost.** There are no per-seat licences.

## Consequences

**Positive:**
- Architecture changes are reviewed, approved, and auditable like code.
- Artefacts can be parsed by downstream tooling (dashboards, reports).
- No tool lock-in.

**Negative / Risks:**
- Architects unfamiliar with Git require onboarding.
- Diagrams are written in Mermaid (text), not drag-and-drop tools; initial
  learning curve expected.
- Cross-referential integrity (e.g., `parent_id` must exist as a file) is not
  enforced by JSON Schema alone — requires a supplementary CI script.
