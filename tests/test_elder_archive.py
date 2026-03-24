"""Tests for SymbolicElderArchive — persistence, retrieval, and wisdom consultation."""

import json
import os
import tempfile
import unittest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from symbolic_elder_archive import SymbolicElderArchive


class TestElderArchiveInMemory(unittest.TestCase):
    """Backward-compat: archive without a file still works in-memory."""

    def test_store_and_retrieve(self):
        archive = SymbolicElderArchive()
        record = archive.store_elder_record(
            "A1", "observer", ["pattern-loop"], "aligned", "energy depletion"
        )
        self.assertEqual(record["agent_id"], "A1")
        self.assertEqual(len(archive.get_all_elders()), 1)

    def test_retrieve_by_essence(self):
        archive = SymbolicElderArchive()
        archive.store_elder_record("A1", "observer", [], "aligned", "done")
        archive.store_elder_record("A2", "guardian", [], "misaligned", "done")
        results = archive.retrieve_by_essence("observer")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["agent_id"], "A1")

    def test_consult_wisdom(self):
        archive = SymbolicElderArchive()
        archive.store_elder_record("A1", "explorer", ["seek"], "aligned", "done")
        wisdom = archive.consult_wisdom("explorer")
        self.assertIsNotNone(wisdom)
        self.assertEqual(wisdom["wisdom"], ["seek"])

    def test_consult_wisdom_no_match(self):
        archive = SymbolicElderArchive()
        self.assertIsNone(archive.consult_wisdom("nonexistent"))


class TestElderArchivePersistence(unittest.TestCase):
    """New: archive persists to and loads from JSON."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        )
        self.tmp.close()
        self.filepath = self.tmp.name

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_persist_and_reload(self):
        archive = SymbolicElderArchive(archive_file=self.filepath)
        archive.store_elder_record("A1", "observer", ["loop"], "aligned", "done")
        archive.store_elder_record("A2", "guardian", ["shield"], "misaligned", "done")

        # Reload from disk in a new instance
        archive2 = SymbolicElderArchive(archive_file=self.filepath)
        self.assertEqual(len(archive2.get_all_elders()), 2)
        self.assertEqual(archive2.get_all_elders()[0]["agent_id"], "A1")

    def test_empty_file_loads_clean(self):
        archive = SymbolicElderArchive(archive_file=self.filepath)
        self.assertEqual(len(archive.get_all_elders()), 0)

    def test_corrupted_file_loads_clean(self):
        with open(self.filepath, "w") as f:
            f.write("not valid json{{{")
        archive = SymbolicElderArchive(archive_file=self.filepath)
        self.assertEqual(len(archive.get_all_elders()), 0)

    def test_consult_wisdom_persisted(self):
        archive = SymbolicElderArchive(archive_file=self.filepath)
        archive.store_elder_record("A1", "explorer", ["wander"], "aligned", "done")

        archive2 = SymbolicElderArchive(archive_file=self.filepath)
        wisdom = archive2.consult_wisdom("explorer")
        self.assertIsNotNone(wisdom)
        self.assertEqual(wisdom["wisdom"], ["wander"])


if __name__ == "__main__":
    unittest.main()
