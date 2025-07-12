import json
import random

class SeedSelector:
    """
    Loads and queries symbolic seeds based on geometry, function, or reuse priority.
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

    def find_seeds_by_geometry(self, geometry):
        return [seed for seed in self.library if seed["geometry"].lower() == geometry.lower()]

    def find_top_reuse_seeds(self, top_n=5):
        sorted_seeds = sorted(self.library, key=lambda x: x.get("reuse_score", 0), reverse=True)
        return sorted_seeds[:top_n]

    def find_seeds_by_function(self, keyword):
        return [seed for seed in self.library if keyword.lower() in seed["essence"].lower()]

    def random_seed(self):
        return random.choice(self.library) if self.library else None


class AgentInstantiator:
    """
    Creates new symbolic agent instances from seeds.
    """
    def __init__(self):
        self.agents_spawned = []

    def instantiate_from_seed(self, seed):
        new_agent = {
            "agent_id": f"agent_{random.randint(1000,9999)}",
            "purpose": seed["essence"],
            "geometry": seed["geometry"],
            "behavior_template": seed["signature_behavior"],
            "origin_seed": seed["id"],
            "active": True
        }
        self.agents_spawned.append(new_agent)
        return new_agent


# 🔁 External interface function for reuse in CLI or simulations
def retrieve_and_spawn_agent(geometry=None, keyword=None):
    selector = SeedSelector()
    instantiator = AgentInstantiator()

    if geometry:
        seeds = selector.find_seeds_by_geometry(geometry)
    elif keyword:
        seeds = selector.find_seeds_by_function(keyword)
    else:
        seeds = selector.find_top_reuse_seeds()

    if seeds:
        chosen_seed = random.choice(seeds)
        return instantiator.instantiate_from_seed(chosen_seed)
    else:
        return {"error": "No matching seeds found"}
