import json
import random
import uuid


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

    When an elder_archive is provided, newly spawned agents consult the
    wisdom of dissolved predecessors. Elder patterns are injected into
    the agent's initial state so that memory truly outlives form.
    """
    def __init__(self, elder_archive=None):
        self.agents_spawned = []
        self.elder_archive = elder_archive

    def instantiate_from_seed(self, seed):
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        essence = seed["essence"]

        new_agent = {
            "agent_id": agent_id,
            "purpose": essence,
            "geometry": seed["geometry"],
            "behavior_template": seed["signature_behavior"],
            "origin_seed": seed["id"],
            "active": True,
            "inherited_wisdom": None,
        }

        # 🧓 Consult elder archive — let dissolved agents teach the next generation
        if self.elder_archive:
            guidance = self.elder_archive.consult_wisdom(essence)
            if guidance:
                new_agent["inherited_wisdom"] = guidance
                print(f"🧓 Agent {agent_id} inherited wisdom from elder {guidance['source']}")

        self.agents_spawned.append(new_agent)
        return new_agent


# 🔁 External interface function for reuse in CLI or simulations
def retrieve_and_spawn_agent(geometry=None, keyword=None, elder_archive=None):
    """
    Select and spawn an agent from the seed library.

    Args:
        geometry: Filter seeds by geometric shape.
        keyword: Filter seeds by essence keyword.
        elder_archive: Optional SymbolicElderArchive instance. When provided,
            the new agent will consult elder wisdom before starting its lifecycle.
    """
    selector = SeedSelector()
    instantiator = AgentInstantiator(elder_archive=elder_archive)

    if geometry:
        seeds = selector.find_seeds_by_geometry(geometry)
    elif keyword:
        seeds = selector.find_seeds_by_function(keyword)
    else:
        seeds = selector.find_top_reuse_seeds()

    if seeds:
        # Pick the highest reuse_score seed rather than random — respect the ranking
        chosen_seed = max(seeds, key=lambda s: s.get("reuse_score", 0))
        return instantiator.instantiate_from_seed(chosen_seed)
    else:
        return {"error": "No matching seeds found"}
