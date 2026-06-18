# ideal-fiesta

[![Validate Architecture Artefacts](https://github.com/kjh235/ideal-fiesta/actions/workflows/validate.yml/badge.svg)](https://github.com/kjh235/ideal-fiesta/actions/workflows/validate.yml)

A Git-based Business Architecture Repository applying "Architecture as Code" (AaC) practices. All business architecture artefacts — capability maps, value streams, organisation structures, and information concepts — are stored as version-controlled YAML files validated by JSON Schema on every pull request.

---

## Directory Structure

| Directory | Contents |
|-----------|----------|
| `schemas/` | JSON Schema draft-07 files that define and validate each domain |
| `capabilities/` | Business capability definitions (hierarchical, CAP-NNN IDs) |
| `organization/` | Organisation unit and team definitions (ORG-NNN IDs) |
| `value-streams/` | End-to-end value stream definitions (VS-NNN IDs) |
| `information/` | Business information concept glossary (INF-NNN IDs) |
| `decisions/` | Architecture Decision Records (ADRs) |
| `diagrams/` | Mermaid diagram source files (render natively on GitHub) |
| `.github/workflows/` | CI validation workflow |

---

## Schemas

| Schema | Validates | ID Pattern |
|--------|-----------|------------|
| [`schemas/capability.schema.json`](schemas/capability.schema.json) | `capabilities/*.yaml` | `CAP-NNN` |
| [`schemas/organization.schema.json`](schemas/organization.schema.json) | `organization/*.yaml` | `ORG-NNN` |
| [`schemas/valuestream.schema.json`](schemas/valuestream.schema.json) | `value-streams/*.yaml` | `VS-NNN` |
| [`schemas/information.schema.json`](schemas/information.schema.json) | `information/*.yaml` | `INF-NNN` |

---

## Adding a New Artefact

1. Choose the appropriate directory and copy an existing YAML file as a template.
2. Assign the next available ID in the domain sequence (e.g., `CAP-106`).
3. Fill in all required fields — the schema `required` array lists them.
4. For cross-references (e.g., `parent_id`, `owner_org_id`), ensure the referenced ID already exists as a file.
5. Open a pull request — the CI workflow will validate your YAML automatically.

---

## Running Validation Locally

Install dependencies:

```bash
pip install yamllint pyyaml
npm install -g ajv-cli@5.0.0
```

Lint YAML syntax:

```bash
yamllint -d relaxed capabilities/ organization/ value-streams/ information/
```

Validate a single file against its schema (example for capabilities):

```bash
python3 -c "
import yaml, json
with open('capabilities/billing.yaml') as f:
    data = yaml.safe_load(f)
with open('/tmp/out.json', 'w') as out:
    json.dump(data, out)
"
ajv validate -s schemas/capability.schema.json -d /tmp/out.json --spec=draft7 --all-errors
```

---

## Architecture Decisions

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-001](decisions/ADR-001-architecture-as-code.md) | Architecture as Code Using Git and YAML | Accepted |
| [ADR-002](decisions/ADR-002-schema-validation.md) | JSON Schema Draft-07 for Artefact Validation | Accepted |

---

## Diagrams

Mermaid diagrams render natively when viewed on GitHub:

- [`diagrams/capability-map.mmd`](diagrams/capability-map.mmd) — Business capability hierarchy
- [`diagrams/order-to-cash.mmd`](diagrams/order-to-cash.mmd) — Order to Cash value stream flow

---

## Licence

GNU General Public License v3.0 — see [LICENSE](LICENSE).
