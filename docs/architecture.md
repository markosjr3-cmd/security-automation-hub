# Architecture: local prototype

```text
Synthetic JSON event
       ↓
Parse and validate event, normalize IP/domain
       ↓
Look for an exact match in a local synthetic fixture
       ↓
Classify as review (match) or unknown (no match)
       ↓
Print JSON and save local investigation record
```

`triage.py` uses only the Python standard library. `examples/context.json` is explicitly synthetic and contains exact indicator matches. A match is marked for review with the fixture note as evidence; no match stays unknown. The program does not connect to any external system or determine whether an indicator is malicious.

## Data contract

Input: JSON object with nonempty `event_id`, `source`, `observation`, timezone-aware ISO 8601 `timestamp`, and `indicator` object (`type`: `ip` or `domain`; `value`: valid IP or ASCII domain). Domains are normalized to lowercase without a trailing dot; IPs are canonicalized. Invalid input returns exit code 1 and does not write a new record.

Output: normalized input fields plus `enrichment` (`matched_local_fixture` or `no_local_match`), `classification` (`review` or `unknown`), `evidence` (list of explanations), and `data_source` (`local synthetic fixture`). The output file defaults to `output/triage.json` and can be changed with `--output`.

## Later extensions

- Additional fixture scenarios and explicit triage rules.
- Optional external sources with rate limits, timeouts and failure handling.
- Docker and n8n orchestration, followed by a simulated OT/ICS network case using sanitized topology.
