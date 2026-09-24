# Security Automation Hub

A hands-on cybersecurity portfolio project focused on security event enrichment and triage. It draws on my background in industrial automation and networking, with an OT/ICS module planned for a later stage.

> **Status:** project scaffold. The enrichment workflow, integrations and alerting are planned; they are not implemented yet.

## First milestone

Build a small, reproducible workflow that:

1. Receives a **synthetic** security event containing an IP address or domain.
2. Validates and normalizes the indicator.
3. Adds context from a documented source or local test data.
4. Produces a structured triage result with a reason for its classification.
5. Stores a local investigation record without credentials or client data.

The first version will run locally and use safe example data. API lookups and n8n/Docker integration can follow after the basic workflow is working.

## Current contents

- [Architecture](docs/architecture.md): planned data flow and design choices.
- [First milestone](docs/first-milestone.md): acceptance criteria and build order.
- [Example event](examples/event.json): synthetic input for the future workflow.
- [MIT license](LICENSE).

## Planned portfolio direction

After the first milestone, explore network monitoring and a lab-only OT/ICS case using simulated assets and sanitized examples. Document assumptions, test evidence and limitations alongside each feature.

## Working locally

Clone the repository to follow or contribute to the project:

```bash
git clone https://github.com/markosjr3-cmd/security-automation-hub.git
cd security-automation-hub
git status
```

There is no runnable application yet; the next step is the event validator and a small test using `examples/event.json`.

## Public repository hygiene

Use synthetic events and reserved example addresses. Never commit credentials, tokens, customer IP ranges, packet captures from production, company code, or internal diagrams. A `.gitignore` helps prevent accidental commits but does not replace reviewing `git status` and `git diff --staged` before each push.
