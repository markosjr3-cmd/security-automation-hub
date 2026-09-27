# Case 002 — Unknown indicator

## Scenario
A synthetic authentication event reports repeated failed sign-in attempts from
198.51.100.8. This is a reserved documentation address, not a real incident.

## Evidence
- Event ID: lab-002
- Source: synthetic-auth-log
- Indicator: 198.51.100.8
- Local enrichment: no match in the synthetic fixture

## Assessment
The tool returned `unknown`. A missing fixture match provides no basis to label
the address safe or malicious. The observation warrants further investigation,
but the current event does not establish the cause of the failed attempts.

## Next checks in a real investigation
- Confirm the time window and number of failed attempts.
- Check whether any attempt succeeded afterward.
- Correlate the affected account, host and other authentication events.
- Review available context before deciding on escalation.

## Reproduce
`py triage.py examples/event-unknown.json --output output/unknown.json`