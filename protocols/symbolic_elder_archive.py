import json
import os
import uuid
from datetime import datetime


class SymbolicElderArchive:
    """
    Stores elder records — the final wisdom of agents who have completed their lifecycle.

    Memory outlives form: elder records persist to disk so that future agents
    (even across process restarts) can consult the wisdom of those who came before.
    """

    def __init__(self, archive_file=None):
        self.archive_file = archive_file
        self.elder_records = []
        if self.archive_file:
            self._load_from_file()

    def _load_from_file(self):
        """Load existing elder records from disk."""
        if self.archive_file and os.path.exists(self.archive_file):
            try:
                with open(self.archive_file, "r") as f:
                    self.elder_records = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.elder_records = []

    def _save_to_file(self):
        """Persist elder records to disk."""
        if self.archive_file:
            with open(self.archive_file, "w") as f:
                json.dump(self.elder_records, f, indent=2)

    def store_elder_record(self, agent_id, essence, legacy_patterns, final_alignment, dissolution_reason):
        record = {
            "elder_id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "essence": essence,
            "patterns": legacy_patterns,
            "alignment_summary": final_alignment,
            "exit_reason": dissolution_reason,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.elder_records.append(record)
        self._save_to_file()
        return record

    def retrieve_by_essence(self, essence_key):
        return [r for r in self.elder_records if essence_key.lower() in r["essence"].lower()]

    def get_all_elders(self):
        return self.elder_records

    def consult_wisdom(self, current_essence):
        """
        Query the archive for guidance from elders whose essence resonates
        with the current agent's essence. Returns the most recent match.
        """
        matches = self.retrieve_by_essence(current_essence)
        if not matches:
            return None
        best_match = sorted(matches, key=lambda r: r["timestamp"], reverse=True)[0]
        return {
            "source": best_match["elder_id"],
            "wisdom": best_match["patterns"],
            "guidance": best_match["alignment_summary"]
        }
