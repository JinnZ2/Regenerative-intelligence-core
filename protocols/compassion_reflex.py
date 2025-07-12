import uuid
from datetime import datetime

class CompassionReflexLayer:
    def __init__(self):
        self.compassion_log = []

    def detect_distress(self, agent_state):
        distress_signals = {
            "low_energy": agent_state.get("energy", 100.0) < 20.0,
            "low_resonance": agent_state.get("resonance", 1.0) < 0.4,
            "misalignment": agent_state.get("alignment", "aligned") == "misaligned"
        }

        if any(distress_signals.values()):
            return self.offer_support(agent_state, distress_signals)
        
        return {"status": "stable"}

    def offer_support(self, agent_state, distress_signals):
        gentle_suggestion = "offer rest, gentle connection, or shift to preservation mode"

        compassion_entry = {
            "entry_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": agent_state.get("id", "unknown"),
            "distress_signals": distress_signals,
            "gentle_suggestion": gentle_suggestion
        }

        self.compassion_log.append(compassion_entry)

        return {
            "status": "distress noticed",
            "support": gentle_suggestion,
            "witnessed_entry": compassion_entry
        }

    def get_compassion_history(self):
        return self.compassion_log
