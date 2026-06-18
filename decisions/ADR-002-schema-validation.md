# ADR-002: JSON Schema Draft-07 for Artefact Validation

**Status:** Accepted
**Date:** 2026-06-18
**Deciders:** Business Architecture Practice Lead, Platform Engineering

## Context

With artefacts stored as YAML, there is a risk that contributors add fields
with incorrect types, omit mandatory data, or use free-form strings where
controlled vocabularies are required (e.g., capability `status`). Without
automated validation, the repository degrades into an unstructured document
store.

Options considered:

1. No validation — rely on peer review alone.
2. Custom Python/Node validation scripts.
3. JSON Schema with a standard CLI validator (ajv-cli).
4. OpenAPI schemas (a superset of JSON Schema).

## Decision

We will use **JSON Schema draft-07** validated by **ajv-cli** in a GitHub
Actions workflow that runs on every PR and push to main.

## Rationale

- **Draft-07** is the most widely supported version across validators,
  IDE plugins, and language libraries. Draft 2020-12 improves on it but has
  materially less tooling support as of 2026.
- **ajv** is the de-facto standard JSON Schema validator for Node.js;
  `ajv-cli` provides a one-line command suitable for CI.
- **JSON Schema** (not YAML Schema) is used because the schemas themselves
  need to be shareable with downstream tools that may consume them via HTTP —
  JSON is the lingua franca of APIs.
- YAML files are converted to JSON via PyYAML before validation; no extra
  Node dependencies are required.

## Consequences

**Positive:**
- Schema violations are caught in CI before merge.
- IDE plugins (e.g., YAML Language Server with `yaml.schemas` config) can
  give real-time feedback to authors.
- Schemas are themselves artefacts, version-controlled alongside the data.

**Negative / Risks:**
- JSON Schema cannot enforce referential integrity between files
  (e.g., that a `parent_id` CAP-NNN actually exists). A separate lint
  step is needed for cross-file checks.
- Schema evolution requires a migration strategy; removing a required field
  is a breaking change for all existing YAML files.
