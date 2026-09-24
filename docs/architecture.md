# Architecture (planned)

## Initial local workflow

```text
Synthetic JSON event
       ↓
Validate schema and normalize indicator
       ↓
Enrich from local fixture or documented source
       ↓
Apply explicit triage rules
       ↓
Structured result + local investigation record
```

The first implementation should separate input validation, enrichment and classification so each step can be checked independently. When an indicator is invalid or context is unavailable, the result should say so instead of asserting that it is safe.

## Data contract (draft)

The sample event in [../examples/event.json](../examples/event.json) uses an event ID, UTC timestamp, indicator type and value, event source and a short observation. The exact schema can change as the code is built; record any changes here.

## Later extensions

- Containerized runtime and n8n orchestration after the local workflow works.
- Rate limits, timeouts and explicit handling of API failures for optional external enrichment.
- A simulated OT/ICS network scenario with sanitized topology and no production data.

This document describes an intended design, not a deployed security service.
