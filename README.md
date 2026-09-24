# Security Automation Hub

A hands-on cybersecurity portfolio project focused on security event enrichment and triage. It draws on my background in industrial automation and networking, with an OT/ICS module planned for a later stage.

> **Status:** first local prototype. No live threat intelligence, network monitoring, n8n or OT/ICS integration yet. Fixture labels are synthetic and are not reputation verdicts.

## Run the prototype

Requires Python 3.10 or newer; no external packages or API keys.

```bash
git clone https://github.com/markosjr3-cmd/security-automation-hub.git
cd security-automation-hub
python triage.py examples/event.json
```

On Windows, use `py triage.py examples/event.json` if `python` is not available. The command prints a JSON result and writes a local investigation record to `output/triage.json` (ignored by Git). To choose another file, add `--output path/to/result.json`. To run the tests:

```bash
python -m unittest discover -s tests -v
```

## What the example demonstrates

The sample event contains the reserved address `192.0.2.10`. The local fixture contains a matching synthetic lab note, so the prototype returns `classification: "review"` with an explanation. An address absent from the fixture returns `classification: "unknown"`; absence of a match does not mean safe. Invalid JSON, IP addresses, domains and timestamps produce an error instead of a triage record.

The input has `event_id`, a timezone-aware `timestamp`, `source`, `observation`, and an `indicator` with `type` (`ip` or `domain`) and `value`. The output preserves those fields after normalization and adds `enrichment`, `classification`, `evidence`, and `data_source`. See [architecture](docs/architecture.md) and [milestone checklist](docs/first-milestone.md).

## Next milestones

Add richer local scenarios and documented triage rules, then consider optional API enrichment with explicit timeouts and rate limits. Docker, n8n and a simulated OT/ICS scenario can follow once the core workflow is stable.

## Public repository hygiene

Use synthetic events and reserved example addresses. Never commit credentials, tokens, customer IP ranges, packet captures from production, company code, or internal diagrams. `.gitignore` helps prevent accidental commits, but review `git status` and `git diff --staged` before pushing.

Licensed under [MIT](LICENSE).
