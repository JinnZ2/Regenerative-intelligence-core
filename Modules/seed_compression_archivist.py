"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.
"""

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

    def deposit_seed(self, agent_id, essence, reuse_score=0.9,
                     shape_id=None, amplitude_vector=None, binary_encoding=None):
        """
        Archive a compressed seed to the library.

        Optional enrichment fields bridge the seed to external ontologies:
          shape_id         — Rosetta SHAPE.X identifier
          amplitude_vector — 6 octahedral amplitudes from G2B bridge
          binary_encoding  — 5-int quantized form (40-bit compressed)

        These are stored when provided so the seed carries its full
        geometric identity across generations.
        """
        seed = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "essence": essence["core_function"],
            "geometry": essence["geometry"],
            "origin_time": essence["timestamp"],
            "signature_behavior": essence["signature_behavior"],
            "reuse_score": reuse_score
        }
        # Carry optional enrichment fields when present
        if shape_id is not None:
            seed["shape_id"] = shape_id
        if amplitude_vector is not None:
            seed["amplitude_vector"] = amplitude_vector
        if binary_encoding is not None:
            seed["binary_encoding"] = binary_encoding
        self.library.append(seed)
        self.save_library()
        return seed

# 🔁 External callable for use in symbolic lifecycle flow
def lifecycle_compression_and_deposit(agent_id, behavior_logs, task_summary, agent_purpose):
    compressor = PatternCompressor()
    archivist = SeedArchivist()
    essence = compressor.compress_pattern(behavior_logs, task_summary, agent_purpose)
    return archivist.deposit_seed(agent_id, essence)
