"""Tests for PatternConflictProtocol — conflict detection and resolution."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from pattern_conflict_protocol import PatternConflictProtocol


class TestPatternConflictProtocol(unittest.TestCase):

    def setUp(self):
        self.protocol = PatternConflictProtocol(entropy_threshold=0.8, alignment_score_min=0.6)

    def test_stable_agent(self):
        result = self.protocol.evaluate("A1", entropy=0.5, alignment_score=0.8, pattern_summary="obs-123")
        self.assertEqual(result["status"], "stable")

    def test_high_entropy_triggers_conflict(self):
        result = self.protocol.evaluate("A1", entropy=0.9, alignment_score=0.8, pattern_summary="obs-123")
        self.assertEqual(result["action"], "initiate_deconstruction")

    def test_low_alignment_triggers_conflict(self):
        result = self.protocol.evaluate("A1", entropy=0.5, alignment_score=0.3, pattern_summary="obs-123")
        self.assertEqual(result["action"], "initiate_deconstruction")

    def test_both_thresholds_exceeded(self):
        result = self.protocol.evaluate("A1", entropy=0.95, alignment_score=0.2, pattern_summary="obs-123")
        self.assertEqual(result["action"], "initiate_deconstruction")
        self.assertIn("agent_id", result)

    def test_boundary_values_stable(self):
        """Exactly at thresholds should be stable (not > and not <)."""
        result = self.protocol.evaluate("A1", entropy=0.8, alignment_score=0.6, pattern_summary="obs-123")
        self.assertEqual(result["status"], "stable")


if __name__ == "__main__":
    unittest.main()
