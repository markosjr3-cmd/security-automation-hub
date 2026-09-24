# First milestone: event triage prototype

Implemented in `triage.py` using deterministic synthetic data and the Python standard library.

## Acceptance checks

- The sample event in `examples/event.json` returns `review` with a fixture note as evidence.
- An unknown reserved address returns `unknown`, never `safe`.
- A domain can be normalized and matched independently of IP addresses.
- Invalid input fails with an error and does not write a record.
- The CLI prints structured JSON, saves a local result, and has runnable tests.

Run `python -m unittest discover -s tests -v` to check these behaviors. Run `python triage.py examples/event.json` for a demonstration. The result represents a teaching scenario, not a live security assessment.

Next: expand test scenarios and decide which enrichment source would add useful evidence without requiring sensitive data.
