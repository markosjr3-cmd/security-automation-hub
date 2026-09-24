"""Local, deterministic triage of synthetic security events (Python 3.10+)."""

import argparse
from datetime import datetime
import ipaddress
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
DOMAIN_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


class ValidationError(ValueError):
    """Input cannot be treated as a valid event or fixture."""


def nonempty_string(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    return value.strip()


def normalize_indicator(indicator):
    if not isinstance(indicator, dict):
        raise ValidationError("indicator must be an object")
    kind = indicator.get("type")
    value = nonempty_string(indicator.get("value"), "indicator.value")
    if kind == "ip":
        try:
            return {"type": kind, "value": str(ipaddress.ip_address(value))}
        except ValueError as exc:
            raise ValidationError("indicator.value must be a valid IP address") from exc
    if kind == "domain":
        domain = value.rstrip(".").lower()
        labels = domain.split(".")
        if (
            len(domain) > 253
            or len(labels) < 2
            or any(not DOMAIN_LABEL.fullmatch(label) for label in labels)
        ):
            raise ValidationError("indicator.value must be a valid ASCII domain")
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            return {"type": kind, "value": domain}
        raise ValidationError("indicator.value is an IP address, not a domain")
    raise ValidationError("indicator.type must be 'ip' or 'domain'")


def validate_event(event):
    if not isinstance(event, dict):
        raise ValidationError("event must be a JSON object")
    event_id = nonempty_string(event.get("event_id"), "event_id")
    timestamp = nonempty_string(event.get("timestamp"), "timestamp")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError("timestamp must be an ISO 8601 date and time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValidationError("timestamp must include a timezone")
    source = nonempty_string(event.get("source"), "source")
    observation = nonempty_string(event.get("observation"), "observation")
    indicator = normalize_indicator(event.get("indicator"))
    return {
        "event_id": event_id,
        "timestamp": parsed.isoformat(),
        "source": source,
        "indicator": indicator,
        "observation": observation,
    }


def triage(event, fixture):
    clean = validate_event(event)
    if not isinstance(fixture, dict) or not isinstance(fixture.get("indicators"), list):
        raise ValidationError("fixture must contain an indicators array")
    indicator = clean["indicator"]
    matches = [
        item for item in fixture["indicators"]
        if isinstance(item, dict)
        and item.get("type") == indicator["type"]
        and item.get("value") == indicator["value"]
    ]
    if len(matches) > 1:
        raise ValidationError("fixture contains duplicate indicator entries")
    if matches:
        note = nonempty_string(matches[0].get("note"), "fixture note")
        status = "review"
        evidence = [f"Synthetic fixture match: {note}"]
        enrichment = "matched_local_fixture"
    else:
        status = "unknown"
        evidence = ["No match in the local synthetic fixture; reputation is unknown."]
        enrichment = "no_local_match"
    return {
        "event_id": clean["event_id"],
        "timestamp": clean["timestamp"],
        "source": clean["source"],
        "indicator": indicator,
        "observation": clean["observation"],
        "enrichment": enrichment,
        "classification": status,
        "evidence": evidence,
        "data_source": "local synthetic fixture",
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", type=Path, help="JSON event file")
    parser.add_argument("--fixture", type=Path, default=ROOT / "examples" / "context.json")
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "triage.json")
    args = parser.parse_args(argv)
    try:
        event = json.loads(args.event.read_text(encoding="utf-8"))
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        result = triage(event, fixture)
        rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(rendered, end="")
    print(f"Saved investigation record: {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
