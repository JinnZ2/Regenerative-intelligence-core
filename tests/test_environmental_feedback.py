"""Tests for EnvironmentalFeedbackLayer — consistent return types."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from environmental_feedback_layer import EnvironmentalFeedbackLayer


class TestRespondToEnvironment(unittest.TestCase):
    """All classifications must return a dict with status, action, note."""

    def setUp(self):
        self.layer = EnvironmentalFeedbackLayer()

    def test_all_classifications_return_dict(self):
        for classification in ["disconnected", "hostile", "noisy", "symbiotic", "depleting", "stable"]:
            result = self.layer.respond_to_environment(classification)
            self.assertIsInstance(result, dict, f"{classification} did not return a dict")
            self.assertIn("status", result, f"{classification} missing 'status'")
            self.assertIn("action", result, f"{classification} missing 'action'")
            self.assertIn("note", result, f"{classification} missing 'note'")

    def test_unknown_classification_returns_nominal(self):
        result = self.layer.respond_to_environment("alien_dimension")
        self.assertEqual(result["status"], "nominal")

    def test_disconnected_has_retry(self):
        result = self.layer.respond_to_environment("disconnected")
        self.assertIn("next_retry", result)

    def test_symbiotic_is_thriving(self):
        result = self.layer.respond_to_environment("symbiotic")
        self.assertEqual(result["status"], "thriving")


class TestSenseEnvironment(unittest.TestCase):

    def test_sense_returns_dict_or_none(self):
        layer = EnvironmentalFeedbackLayer()
        # Run multiple times since there's randomness
        for _ in range(20):
            result = layer.sense_environment()
            self.assertTrue(result is None or isinstance(result, dict))

    def test_classify_none_feedback(self):
        layer = EnvironmentalFeedbackLayer()
        self.assertEqual(layer.classify_environment(None), "disconnected")


if __name__ == "__main__":
    unittest.main()
