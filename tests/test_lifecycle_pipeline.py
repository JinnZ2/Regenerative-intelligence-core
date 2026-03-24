"""Tests for LifecyclePipeline — end-to-end agent lifecycle integration."""

import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from deterministic_mode import enable_deterministic_mode, disable_deterministic_mode
from lifecycle_pipeline import LifecyclePipeline


class TestLifecyclePipeline(unittest.TestCase):

    def setUp(self):
        enable_deterministic_mode(42)
        self.pipeline = LifecyclePipeline()

    def tearDown(self):
        disable_deterministic_mode()

    def test_healthy_agent_cycle(self):
        state = {
            "id": "A1",
            "essence": "observer",
            "energy": 90.0,
            "resonance": 0.8,
            "alignment": "aligned",
            "pattern": "obs-123",
            "traits": ["reflective"],
            "last_seed_time": "2025-01-01T00:00:00"
        }
        result = self.pipeline.run_agent_cycle(state)
        self.assertEqual(result["agent_id"], "A1")
        self.assertIn("environment", result["steps"])
        self.assertIn("alignment", result["steps"])
        self.assertIn("conflict", result["steps"])
        self.assertIn("compassion", result["steps"])
        self.assertIn("action", result)

    def test_distressed_agent_gets_compassion(self):
        state = {
            "id": "A2",
            "essence": "guardian",
            "energy": 5.0,
            "resonance": 0.1,
            "alignment": "misaligned",
            "pattern": "grd-001",
            "traits": ["cooperative"],
        }
        result = self.pipeline.run_agent_cycle(state)
        self.assertEqual(result["steps"]["compassion"]["status"], "distress noticed")

    def test_critical_agent_dissolution_recommended(self):
        state = {
            "id": "A3",
            "essence": "explorer",
            "energy": 3.0,
            "resonance": 0.1,
            "alignment": "misaligned",
            "pattern": "exp-999",
            "traits": ["adaptive"],
        }
        result = self.pipeline.run_agent_cycle(state)
        self.assertIn(result["action"]["recommendation"], ["dissolve", "seed_and_adapt", "rest_and_preserve"])

    def test_pipeline_returns_all_steps(self):
        state = {
            "id": "A4",
            "essence": "observer",
            "energy": 50.0,
            "resonance": 0.5,
            "alignment": "aligned",
            "pattern": "obs-444",
            "traits": ["reflective"],
        }
        result = self.pipeline.run_agent_cycle(state)
        expected_steps = {"environment", "alignment", "conflict", "compassion", "elder_consultation"}
        self.assertEqual(set(result["steps"].keys()), expected_steps)

    def test_deterministic_reproducibility(self):
        state = {
            "id": "A5",
            "essence": "guardian",
            "energy": 60.0,
            "resonance": 0.6,
            "alignment": "aligned",
            "pattern": "grd-555",
            "traits": ["cooperative"],
        }
        enable_deterministic_mode(99)
        r1 = self.pipeline.run_agent_cycle(state)
        enable_deterministic_mode(99)
        pipeline2 = LifecyclePipeline()
        r2 = pipeline2.run_agent_cycle(state)
        self.assertEqual(r1["action"]["recommendation"], r2["action"]["recommendation"])


if __name__ == "__main__":
    unittest.main()
