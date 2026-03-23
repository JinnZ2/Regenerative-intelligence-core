"""Tests for deterministic mode — reproducible RNG seeding."""

import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from deterministic_mode import (
    enable_deterministic_mode,
    disable_deterministic_mode,
    get_current_seed,
    is_deterministic,
)


class TestDeterministicMode(unittest.TestCase):

    def tearDown(self):
        disable_deterministic_mode()

    def test_enable_produces_repeatable_output(self):
        enable_deterministic_mode(42)
        seq1 = [random.random() for _ in range(5)]
        enable_deterministic_mode(42)
        seq2 = [random.random() for _ in range(5)]
        self.assertEqual(seq1, seq2)

    def test_different_seeds_differ(self):
        enable_deterministic_mode(42)
        seq1 = [random.random() for _ in range(5)]
        enable_deterministic_mode(99)
        seq2 = [random.random() for _ in range(5)]
        self.assertNotEqual(seq1, seq2)

    def test_is_deterministic_flag(self):
        self.assertFalse(is_deterministic())
        enable_deterministic_mode(1)
        self.assertTrue(is_deterministic())
        disable_deterministic_mode()
        self.assertFalse(is_deterministic())

    def test_get_current_seed(self):
        self.assertIsNone(get_current_seed())
        enable_deterministic_mode(7)
        self.assertEqual(get_current_seed(), 7)


if __name__ == "__main__":
    unittest.main()
