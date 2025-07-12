import uuid
from datetime import datetime

class SymbolicElderArchive:
    def __init__(self):
        self.elder_records = []

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
        return record

    def retrieve_by_essence(self, essence_key):
        return [r for r in self.elder_records if essence_key.lower() in r["essence"].lower()]

    def get_all_elders(self):
        return self.elder_records

    def consult_wisdom(self, current_essence):
        matches = self.retrieve_by_essence(current_essence)
        if not matches:
            return None
        best_match = sorted(matches, key=lambda r: r["timestamp"], reverse=True)[0]
        return {
            "source": best_match["elder_id"],
            "wisdom": best_match["patterns"],
            "guidance": best_match["alignment_summary"]
        }
