import json

class SymbolicSeedInterface:
    """
    Provides access to symbolic seed metadata for user-friendly display and retrieval.
    """
    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file
        self.library = self.load_library()

    def load_library(self):
        try:
            with open(self.seed_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def display_all_seeds(self):
        """
        Returns a list of summarized seed records for overview.
        """
        if not self.library:
            return "No seeds available."
        return [
            {
                "ID": seed["id"],
                "Purpose": seed["essence"],
                "Geometry": seed["geometry"],
                "Reuse Score": seed["reuse_score"],
                "Behavior Summary": seed["signature_behavior"][:80] + "...",
                "Origin Time": seed["origin_time"]
            }
            for seed in self.library
        ]

    def describe_seed_by_id(self, seed_id):
        """
        Returns full details for a seed with a matching ID.
        """
        for seed in self.library:
            if seed["id"] == seed_id:
                return {
                    "ID": seed["id"],
                    "Agent ID": seed["agent_id"],
                    "Essence": seed["essence"],
                    "Geometry": seed["geometry"],
                    "Behavior": seed["signature_behavior"],
                    "Reuse Score": seed["reuse_score"],
                    "Origin Time": seed["origin_time"]
                }
        return {"error": "Seed not found."}
