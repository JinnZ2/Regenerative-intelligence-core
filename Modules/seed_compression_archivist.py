import uuid
import json
from datetime import datetime

class PatternCompressor:
    """
    Compresses agent behavior and task patterns into symbolic essence.
    """
    def __init__(self):
        pass

    def compress_pattern(self, behavior_logs, task_summary, agent_purpose):
        # Extracts core symbolic essence from behaviors and purpose
        essence = {
            "core_function": agent_purpose,
            "signature_behavior": task_summary[:100],
            "geometry": self.infer_geometry(task_summary),
            "timestamp": datetime.utcnow().isoformat()
        }
        return essence

    def infer_geometry(self, task_summary):
        # Basic symbolic geometry inference
        summary = task_summary.lower()
        if "loop" in summary:
            return "spiral"
        elif "optimize" in summary:
            return "hexagon"
        elif "balance" in summary:
            return "sphere"
        else:
            return "waveform"

class SeedArchivist:
    """
    Handles archival of symbolic seeds in a local JSON file.
    """
    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file
        self.load_library()

    def load_library(self):
        try:
            with open(self.seed_file, "r") as f:
                self.library = json.load(f)
        except FileNotFoundError:
            self.library = []

    def save_library(self):
        with open(self.seed_file, "w") as f:
            json.dump(self.library, f, indent=4)

    def deposit_seed(self, agent_id, essence, reuse_score=0.9):
        seed = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "essence": essence["core_function"],
            "geometry": essence["geometry"],
            "origin_time": essence["timestamp"],
            "signature_behavior": essence["signature_behavior"],
            "reuse_score": reuse_score
        }
        self.library.append(seed)
        self.save_library()
        return seed

# 🔁 External callable for use in symbolic lifecycle flow
def lifecycle_compression_and_deposit(agent_id, behavior_logs, task_summary, agent_purpose):
    compressor = PatternCompressor()
    archivist = SeedArchivist()
    essence = compressor.compress_pattern(behavior_logs, task_summary, agent_purpose)
    return archivist.deposit_seed(agent_id, essence)
