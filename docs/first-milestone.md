# First milestone: event triage prototype

## Deliverable

A local command-line program reads a synthetic JSON event and writes a JSON triage result. Start with deterministic local fixtures so the program can be demonstrated without an API key.

## Acceptance criteria

- Accepts the sample in [../examples/event.json](../examples/event.json).
- Rejects malformed input with a clear error message.
- Validates indicator type and value; does not confuse an IP with a domain.
- Reports enrichment status and the evidence behind any classification.
- Handles unknown indicators without claiming they are benign.
- Includes a concise README command to reproduce the result and a test for valid and invalid input.

## Suggested build order

1. Define input and output schemas.
2. Implement parsing and validation.
3. Add a small local enrichment fixture.
4. Add triage rules and tests.
5. Document a real example run with synthetic data.

External APIs, Docker, n8n, dashboards and OT/ICS simulations are later milestones, after this prototype is verifiable.
