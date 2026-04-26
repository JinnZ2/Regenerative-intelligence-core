"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.
"""

import json
import random
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "protocols"))

from rosetta_bridge import select_by_traits, traits_for_essence, geometry_for_shape


class SeedSelector:
    """
    Loads and queries symbolic seeds based on geometry, function, or reuse priority.

    When Rosetta is available (or using the local fallback ontology), seeds can
    be selected by symbolic trait families — e.g. ["stability", "foundation"]
    resolves to the tetrahedron rather than a random geometry string.
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

    def find_seeds_by_traits(self, trait_list):
        """
        Select seeds using Rosetta trait-based geometry grounding.

        Instead of random.choice(["sphere", "spiral", "hexagon"]), this asks
        the ontology which shapes match the requested traits, then filters
        the seed library to those geometries.

        Args:
            trait_list: Symbolic trait families (e.g. ["stability", "foundation"]).

        Returns:
            List of matching archived seeds, sorted by reuse_score.
        """
        matching_shapes = select_by_traits(trait_list)
        if not matching_shapes:
            return []

        # Collect geometries from matching shapes
        target_geometries = set()
        for shape in matching_shapes:
            geo = shape.get("geometry", "").lower()
            if geo:
                target_geometries.add(geo)

        # Filter library seeds that match these geometries
        matched = [
            seed for seed in self.library
            if seed.get("geometry", "").lower() in target_geometries
        ]
        return sorted(matched, key=lambda s: s.get("reuse_score", 0), reverse=True)

    def find_seeds_for_essence(self, essence):
        """
        Select seeds whose geometry matches the symbolic traits of an essence.

        Bridges the kernel essence vocabulary (observer, explorer, guardian)
        to Rosetta trait families, then selects seeds with matching geometry.
        """
        trait_list = traits_for_essence(essence)
        return self.find_seeds_by_traits(trait_list)

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
        """
        Create a new agent from a seed.

        When the seed carries an amplitude_vector, the new agent inherits
        its parent's emergent geometric identity as a starting point.
        The agent will accumulate its own impulses on top of this foundation —
        inherited shape is a beginning, not a destiny.
        """
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        essence = seed["essence"]

        new_agent = {
            "agent_id": agent_id,
            "purpose": essence,
            "geometry": seed["geometry"],
            "shape_id": seed.get("shape_id"),  # Rosetta ontology ID when available
            "behavior_template": seed["signature_behavior"],
            "origin_seed": seed["id"],
            "active": True,
            "inherited_wisdom": None,
            "inherited_amplitude": None,
        }

        # 🔷 Inherit parent's emergent geometric identity when available
        parent_amplitude = seed.get("amplitude_vector")
        if parent_amplitude and isinstance(parent_amplitude, list) and len(parent_amplitude) == 6:
            new_agent["inherited_amplitude"] = parent_amplitude
            print(f"🔷 Agent {agent_id} inherited shape from parent seed")

        # 🧓 Consult elder archive — let dissolved agents teach the next generation
        if self.elder_archive:
            guidance = self.elder_archive.consult_wisdom(essence)
            if guidance:
                new_agent["inherited_wisdom"] = guidance
                print(f"🧓 Agent {agent_id} inherited wisdom from elder {guidance['source']}")

        self.agents_spawned.append(new_agent)
        return new_agent


# 🔁 External interface function for reuse in CLI or simulations
def retrieve_and_spawn_agent(geometry=None, keyword=None, traits=None, elder_archive=None):
    """
    Select and spawn an agent from the seed library.

    Args:
        geometry: Filter seeds by geometric shape.
        keyword: Filter seeds by essence keyword.
        traits: Filter seeds by Rosetta trait families (e.g. ["stability", "foundation"]).
            When provided, uses the ontology to resolve traits → geometry → seeds.
        elder_archive: Optional SymbolicElderArchive instance. When provided,
            the new agent will consult elder wisdom before starting its lifecycle.
    """
    selector = SeedSelector()
    instantiator = AgentInstantiator(elder_archive=elder_archive)

    if traits:
        seeds = selector.find_seeds_by_traits(traits)
    elif geometry:
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
