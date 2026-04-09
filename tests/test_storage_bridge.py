"""Tests for storage bridge — thin interface to resilient storage backends."""

import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from storage_bridge import (
    LocalJsonBackend, get_storage_backend, is_resilient_storage_available,
)


class TestLocalJsonBackend(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w")
        self.tmp.close()
        self.filepath = self.tmp.name
        self.backend = LocalJsonBackend(seed_file=self.filepath)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_deposit_and_retrieve(self):
        seed = {"id": "s1", "agent_id": "a1", "essence": "observer", "geometry": "spiral"}
        self.backend.deposit("s1", seed)
        retrieved = self.backend.retrieve("s1")
        self.assertEqual(retrieved["id"], "s1")
        self.assertEqual(retrieved["essence"], "observer")

    def test_retrieve_nonexistent(self):
        self.assertIsNone(self.backend.retrieve("nope"))

    def test_list_seeds(self):
        self.backend.deposit("s1", {"id": "s1", "agent_id": "a1", "essence": "x", "geometry": "y"})
        self.backend.deposit("s2", {"id": "s2", "agent_id": "a2", "essence": "x", "geometry": "y"})
        ids = self.backend.list_seeds()
        self.assertEqual(sorted(ids), ["s1", "s2"])

    def test_deposit_replaces_existing(self):
        seed_v1 = {"id": "s1", "agent_id": "a1", "essence": "old", "geometry": "spiral"}
        seed_v2 = {"id": "s1", "agent_id": "a1", "essence": "new", "geometry": "hexagon"}
        self.backend.deposit("s1", seed_v1)
        self.backend.deposit("s1", seed_v2)
        retrieved = self.backend.retrieve("s1")
        self.assertEqual(retrieved["essence"], "new")
        self.assertEqual(len(self.backend.list_seeds()), 1)

    def test_verify_valid(self):
        seed = {"id": "s1", "agent_id": "a1", "essence": "observer", "geometry": "spiral"}
        self.backend.deposit("s1", seed)
        self.assertTrue(self.backend.verify("s1"))

    def test_verify_missing(self):
        self.assertFalse(self.backend.verify("nope"))

    def test_verify_incomplete_seed(self):
        """Seed missing required fields should fail verification."""
        seed = {"id": "s1", "agent_id": "a1"}  # missing essence, geometry
        self.backend.deposit("s1", seed)
        self.assertFalse(self.backend.verify("s1"))

    def test_empty_file_handled(self):
        backend = LocalJsonBackend(seed_file=self.filepath)
        self.assertEqual(backend.list_seeds(), [])

    def test_corrupted_file_handled(self):
        with open(self.filepath, "w") as f:
            f.write("not json{{{")
        backend = LocalJsonBackend(seed_file=self.filepath)
        self.assertEqual(backend.list_seeds(), [])

    def test_persists_to_disk(self):
        seed = {"id": "s1", "agent_id": "a1", "essence": "x", "geometry": "y"}
        self.backend.deposit("s1", seed)
        # New backend instance reading same file
        backend2 = LocalJsonBackend(seed_file=self.filepath)
        self.assertEqual(backend2.retrieve("s1")["id"], "s1")


class TestGetStorageBackend(unittest.TestCase):

    def test_returns_local_when_no_resilient(self):
        backend = get_storage_backend()
        self.assertIsInstance(backend, LocalJsonBackend)

    def test_resilient_not_available(self):
        self.assertFalse(is_resilient_storage_available())


if __name__ == "__main__":
    unittest.main()
