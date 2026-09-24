import copy
import json
from pathlib import Path
import tempfile
import unittest

from triage import ValidationError, main, triage


ROOT = Path(__file__).resolve().parents[1]
EVENT = json.loads((ROOT / "examples/event.json").read_text(encoding="utf-8"))
FIXTURE = json.loads((ROOT / "examples/context.json").read_text(encoding="utf-8"))


class TriageTests(unittest.TestCase):
    def test_fixture_match_is_review_with_explicit_evidence(self):
        result = triage(EVENT, FIXTURE)
        self.assertEqual(result["classification"], "review")
        self.assertEqual(result["enrichment"], "matched_local_fixture")
        self.assertIn("Synthetic fixture match", result["evidence"][0])

    def test_unknown_address_is_not_marked_safe(self):
        event = copy.deepcopy(EVENT)
        event["indicator"]["value"] = "198.51.100.8"
        result = triage(event, FIXTURE)
        self.assertEqual(result["classification"], "unknown")
        self.assertEqual(result["enrichment"], "no_local_match")

    def test_domain_is_normalized_before_lookup(self):
        event = copy.deepcopy(EVENT)
        event["indicator"] = {"type": "domain", "value": "ALERTS.EXAMPLE.COM."}
        result = triage(event, FIXTURE)
        self.assertEqual(result["indicator"]["value"], "alerts.example.com")
        self.assertEqual(result["classification"], "review")

    def test_invalid_input_is_rejected(self):
        for change in (
            {"indicator": {"type": "ip", "value": "999.2.3.4"}},
            {"indicator": {"type": "domain", "value": "bad domain.com"}},
            {"timestamp": "2026-09-24T12:00:00"},
        ):
            with self.subTest(change=change):
                with self.assertRaises(ValidationError):
                    triage({**EVENT, **change}, FIXTURE)

    def test_cli_writes_record_only_for_valid_event(self):
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / "record.json"
            self.assertEqual(main([str(ROOT / "examples/event.json"), "--output", str(record)]), 0)
            self.assertEqual(json.loads(record.read_text())["classification"], "review")
            record.unlink()
            bad_event = Path(directory) / "bad.json"
            bad_event.write_text("{invalid", encoding="utf-8")
            self.assertEqual(main([str(bad_event), "--output", str(record)]), 1)
            self.assertFalse(record.exists())


if __name__ == "__main__":
    unittest.main()
