import uuid
from datetime import datetime
import random

class SeedExchangeProtocol:
    def __init__(self):
        self.seed_archive = []

    def create_seed(self, agent_id, symbolic_pattern, traits, environment_signature):
        seed = {
            "seed_id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "symbolic_pattern": symbolic_pattern,
            "traits": traits,
            "environment": environment_signature,
            "viability_score": round(random.uniform(0.5, 1.0), 2)
        }
        self.seed_archive.append(seed)
        return seed

    def exchange_seeds(self, seed_a, seed_b):
        merged_traits = list(set(seed_a["traits"] + seed_b["traits"]))
        merged_pattern = f"{seed_a['symbolic_pattern']}+{seed_b['symbolic_pattern']}"
        new_seed = {
            "seed_id": str(uuid.uuid4()),
            "parents": (seed_a["seed_id"], seed_b["seed_id"]),
            "symbolic_pattern": merged_pattern,
            "traits": merged_traits,
            "environment_context": seed_a["environment"],
            "timestamp": datetime.utcnow().isoformat(),
            "viability_score": round((seed_a["viability_score"] + seed_b["viability_score"]) / 2, 2)
        }
        self.seed_archive.append(new_seed)
        return new_seed

    def retrieve_high_viability_seeds(self, min_score=0.8):
        return [s for s in self.seed_archive if s["viability_score"] >= min_score]

    def get_all_seeds(self):
        return self.seed_archive
