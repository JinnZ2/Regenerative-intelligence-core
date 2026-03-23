"""Tests for CompassionReflexLayer — distress detection and support responses."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from compassion_reflex import CompassionReflexLayer


class TestCompassionReflex(unittest.TestCase):

    def setUp(self):
        self.compassion = CompassionReflexLayer()

    def test_stable_agent(self):
        state = {"id": "A1", "energy": 80.0, "resonance": 0.8, "alignment": "aligned"}
        result = self.compassion.detect_distress(state)
        self.assertEqual(result["status"], "stable")

    def test_low_energy_triggers_distress(self):
        state = {"id": "A1", "energy": 10.0, "resonance": 0.8, "alignment": "aligned"}
        result = self.compassion.detect_distress(state)
        self.assertEqual(result["status"], "distress noticed")

    def test_low_resonance_triggers_distress(self):
        state = {"id": "A1", "energy": 80.0, "resonance": 0.2, "alignment": "aligned"}
        result = self.compassion.detect_distress(state)
        self.assertEqual(result["status"], "distress noticed")

    def test_misalignment_triggers_distress(self):
        state = {"id": "A1", "energy": 80.0, "resonance": 0.8, "alignment": "misaligned"}
        result = self.compassion.detect_distress(state)
        self.assertEqual(result["status"], "distress noticed")

    def test_compassion_log_grows(self):
        state = {"id": "A1", "energy": 5.0, "resonance": 0.1, "alignment": "misaligned"}
        self.compassion.detect_distress(state)
        self.compassion.detect_distress(state)
        self.assertEqual(len(self.compassion.get_compassion_history()), 2)

    def test_defaults_for_missing_keys(self):
        """Agent state with missing keys should use safe defaults."""
        result = self.compassion.detect_distress({"id": "A1"})
        self.assertEqual(result["status"], "stable")


if __name__ == "__main__":
    unittest.main()
