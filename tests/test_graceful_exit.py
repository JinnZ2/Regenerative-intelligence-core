"""Tests for GracefulExitProtocol — dignified dissolution with memory preservation."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from graceful_exit import GracefulExitProtocol


class TestGracefulExit(unittest.TestCase):

    def setUp(self):
        self.exit_protocol = GracefulExitProtocol()

    def test_exit_archives_seed(self):
        result = self.exit_protocol.prepare_exit("A1", "energy depletion", ["looped"], "stable")
        self.assertEqual(result["status"], "graceful exit initialized")
        self.assertIn("archive", result)
        self.assertEqual(result["archive"]["agent_id"], "A1")

    def test_exit_log_grows(self):
        self.exit_protocol.prepare_exit("A1", "reason1", [], "stable")
        self.exit_protocol.prepare_exit("A2", "reason2", [], "hostile")
        history = self.exit_protocol.get_exit_history()
        self.assertEqual(len(history), 2)

    def test_summarize_exits(self):
        self.exit_protocol.prepare_exit("A1", "r1", [], "s")
        self.exit_protocol.prepare_exit("A1", "r2", [], "s")
        self.exit_protocol.prepare_exit("A2", "r3", [], "s")
        summary = self.exit_protocol.summarize_exits()
        self.assertEqual(summary["total_exits"], 3)
        self.assertEqual(summary["unique_agents"], 2)

    def test_empty_summary(self):
        summary = self.exit_protocol.summarize_exits()
        self.assertEqual(summary["total_exits"], 0)
        self.assertIsNone(summary["last_exit"])


if __name__ == "__main__":
    unittest.main()
