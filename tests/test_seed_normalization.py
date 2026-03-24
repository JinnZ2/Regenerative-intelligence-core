"""Tests for seed normalization — converting between schema variants."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from seed_schema import normalize_seed, to_cli_format, _detect_variant


class TestDetectVariant(unittest.TestCase):

    def test_detect_exchange(self):
        seed = {"seed_id": "x", "agent_id": "a"}
        self.assertEqual(_detect_variant(seed), "exchange")

    def test_detect_cli(self):
        seed = {"ID": "x", "Agent": "a"}
        self.assertEqual(_detect_variant(seed), "cli")

    def test_detect_archived(self):
        seed = {"id": "x", "essence": "e"}
        self.assertEqual(_detect_variant(seed), "archived")

    def test_detect_unknown(self):
        seed = {"foo": "bar"}
        self.assertEqual(_detect_variant(seed), "unknown")


class TestNormalizeSeed(unittest.TestCase):

    def test_normalize_exchange(self):
        seed = {
            "seed_id": "abc-123",
            "agent_id": "Agent_1",
            "timestamp": "2025-01-01T00:00:00",
            "symbolic_pattern": "obs-123",
            "traits": ["reflective"],
            "environment": "Env-Zone-A",
            "viability_score": 0.85
        }
        norm = normalize_seed(seed)
        self.assertEqual(norm["id"], "abc-123")
        self.assertEqual(norm["agent_id"], "Agent_1")
        self.assertEqual(norm["essence"], "obs-123")
        self.assertEqual(norm["reuse_score"], 0.85)

    def test_normalize_cli(self):
        seed = {
            "ID": "cli-1",
            "Agent": "agent_1",
            "Behavior Summary": "looped pattern",
            "Purpose": "observe",
            "Geometry": "sphere",
            "Reuse Score": 0.95,
            "Origin Time": "2025-01-01"
        }
        norm = normalize_seed(seed)
        self.assertEqual(norm["id"], "cli-1")
        self.assertEqual(norm["essence"], "observe")
        self.assertEqual(norm["geometry"], "sphere")

    def test_normalize_archived_is_identity(self):
        seed = {
            "id": "arc-1",
            "agent_id": "A1",
            "essence": "observer",
            "geometry": "spiral",
            "origin_time": "2025-01-01",
            "signature_behavior": "looping",
            "reuse_score": 0.9
        }
        norm = normalize_seed(seed)
        self.assertEqual(norm, seed)

    def test_normalize_non_dict(self):
        self.assertIsNone(normalize_seed("not a dict"))
        self.assertIsNone(normalize_seed(42))

    def test_normalize_unknown(self):
        self.assertIsNone(normalize_seed({"foo": "bar"}))


class TestToCliFormat(unittest.TestCase):

    def test_archived_to_cli(self):
        seed = {
            "id": "arc-1",
            "agent_id": "A1",
            "essence": "observer",
            "geometry": "spiral",
            "origin_time": "2025-01-01",
            "signature_behavior": "looping",
            "reuse_score": 0.9
        }
        cli = to_cli_format(seed)
        self.assertEqual(cli["ID"], "arc-1")
        self.assertEqual(cli["Purpose"], "observer")
        self.assertEqual(cli["Geometry"], "spiral")
        self.assertEqual(cli["Reuse Score"], 0.9)

    def test_exchange_to_cli(self):
        seed = {
            "seed_id": "exc-1",
            "agent_id": "A2",
            "timestamp": "2025-01-01",
            "symbolic_pattern": "guard",
            "traits": ["adaptive"],
            "environment": "Env-A",
            "viability_score": 0.7
        }
        cli = to_cli_format(seed)
        self.assertEqual(cli["ID"], "exc-1")
        self.assertEqual(cli["Purpose"], "guard")


if __name__ == "__main__":
    unittest.main()
