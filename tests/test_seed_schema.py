"""Tests for seed schema validation — structure, types, and boundary values."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from seed_schema import validate_seed, SEED_SCHEMA, ARCHIVED_SEED_SCHEMA, CLI_SEED_SCHEMA


class TestSeedSchemaValidation(unittest.TestCase):

    def test_valid_exchange_seed(self):
        seed = {
            "seed_id": "abc-123",
            "agent_id": "Agent_1",
            "timestamp": "2025-01-01T00:00:00",
            "symbolic_pattern": "obs-123",
            "traits": ["reflective"],
            "environment": "Env-Zone-A",
            "viability_score": 0.85
        }
        result = validate_seed(seed)
        self.assertTrue(result["valid"])
        self.assertEqual(result["errors"], [])

    def test_missing_field(self):
        seed = {"seed_id": "abc-123"}
        result = validate_seed(seed, SEED_SCHEMA)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Missing" in e for e in result["errors"]))

    def test_wrong_type(self):
        seed = {
            "seed_id": 123,  # should be str
            "agent_id": "Agent_1",
            "timestamp": "2025-01-01",
            "symbolic_pattern": "obs",
            "traits": ["a"],
            "environment": "env",
            "viability_score": 0.5
        }
        result = validate_seed(seed, SEED_SCHEMA)
        self.assertFalse(result["valid"])
        self.assertTrue(any("expected" in e for e in result["errors"]))

    def test_invalid_geometry(self):
        seed = {
            "id": "abc",
            "agent_id": "Agent_1",
            "essence": "observer",
            "geometry": "triangle",  # invalid
            "origin_time": "2025-01-01",
            "signature_behavior": "looping",
            "reuse_score": 0.9
        }
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("geometry" in e.lower() for e in result["errors"]))

    def test_score_out_of_range(self):
        seed = {
            "seed_id": "abc",
            "agent_id": "Agent_1",
            "timestamp": "2025-01-01",
            "symbolic_pattern": "obs",
            "traits": ["a"],
            "environment": "env",
            "viability_score": 1.5  # out of range
        }
        result = validate_seed(seed, SEED_SCHEMA)
        self.assertFalse(result["valid"])
        self.assertTrue(any("between 0.0 and 1.0" in e for e in result["errors"]))

    def test_valid_archived_seed(self):
        seed = {
            "id": "abc",
            "agent_id": "Agent_1",
            "essence": "observer",
            "geometry": "spiral",
            "origin_time": "2025-01-01",
            "signature_behavior": "looping",
            "reuse_score": 0.9
        }
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_valid_cli_seed(self):
        seed = {
            "ID": "abc",
            "Agent": "agent_1",
            "Behavior Summary": "looped pattern",
            "Purpose": "observe",
            "Geometry": "sphere",
            "Reuse Score": 0.95,
            "Origin Time": "2025-01-01"
        }
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_not_a_dict(self):
        result = validate_seed("not a seed")
        self.assertFalse(result["valid"])

    def test_auto_detect_schema(self):
        """Verify auto-detection picks the right schema variant."""
        exchange = {"seed_id": "x", "agent_id": "a", "timestamp": "t",
                    "symbolic_pattern": "p", "traits": [], "environment": "e",
                    "viability_score": 0.5}
        self.assertTrue(validate_seed(exchange)["valid"])

        archived = {"id": "x", "agent_id": "a", "essence": "e", "geometry": "sphere",
                    "origin_time": "t", "signature_behavior": "s", "reuse_score": 0.5}
        self.assertTrue(validate_seed(archived)["valid"])


if __name__ == "__main__":
    unittest.main()
