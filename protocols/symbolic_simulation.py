"""
Symbolic Simulation — Full agent lifecycle simulation using the LifecyclePipeline.

Runs multiple agents through sense-evaluate-act cycles, using the composed
pipeline rather than inline logic. This makes the simulation the true
integration test for the entire system.

Agents now use real resonance (from the MultiAgentCoordinator) and benefit
from elder wisdom — dissolved agents teach future generations through the
shared elder archive.
"""

import time
import random
import sys
import os

# Add paths for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Modules"))

from symbolic_energy_manager import SymbolicEnergyManager
from lifecycle_pipeline import LifecyclePipeline
from seed_exchange import SeedExchangeProtocol
from multi_agent_coordination import MultiAgentCoordinator
from rosetta_bridge import select_by_essence, geometry_for_shape
from seed_compression_archivist import SeedArchivist, PatternCompressor


class SymbolicAgent:
    def __init__(self, agent_id, essence, coordinator):
        self.id = agent_id
        self.essence = essence
        self.energy = SymbolicEnergyManager()
        self.seed_protocol = SeedExchangeProtocol()
        self.coordinator = coordinator
        self.traits = [random.choice(["reflective", "adaptive", "cooperative"])]
        self.pattern = f"{essence[:3]}-{random.randint(100, 999)}"
        self.alive = True
        self.alignment = "aligned"

        # Ground geometry in the Rosetta ontology: essence → shape directly
        self.shape_id = self._resolve_shape_id()

        # Register with the coordinator so resonance is computed from the group
        self.coordinator.register_agent(self.id, self.essence, {
            "traits": self.traits,
            "energy": self.energy.energy,
            "shape_id": self.shape_id,
        })
        resonance = self.coordinator.agent_registry[self.id]["resonance_score"]
        shape_label = self.shape_id or "no shape"
        print(f"🧬 Agent {self.id} initialized | trait: {self.traits[0]} | shape: {shape_label} | resonance: {resonance}")

    def _resolve_shape_id(self):
        """Resolve essence to a Rosetta shape ID directly."""
        matches = select_by_essence(self.essence)
        if matches:
            return matches[0].get("shape_id")
        return None

    def to_state(self):
        """Export agent state as a dict for the LifecyclePipeline."""
        # Update coordinator with current energy so resonance reflects live state
        self.coordinator.agent_registry[self.id]["state"]["energy"] = self.energy.energy
        self.coordinator.refresh_resonance()
        resonance = self.coordinator.agent_registry[self.id]["resonance_score"]

        return {
            "id": self.id,
            "essence": self.essence,
            "energy": self.energy.energy,
            "resonance": resonance,
            "alignment": self.alignment,
            "pattern": self.pattern,
            "traits": self.traits,
            "shape_id": self.shape_id,
            "dominant_channel": self.energy.get_dominant_channel(),
        }

    def act(self, pipeline):
        """Run one lifecycle cycle through the pipeline."""
        if not self.alive:
            return None

        # Drain energy for the cycle
        task_difficulty = random.uniform(0.2, 0.7)
        self.energy.simulate_energy_drain(task_difficulty)

        energy_state = self.energy.assess_energy_state()
        state = self.to_state()
        print(f"[{self.id}] energy: {round(self.energy.energy, 1)} → {energy_state} | resonance: {state['resonance']}")

        # Run through the full pipeline
        result = pipeline.run_agent_cycle(state)
        recommendation = result["action"]["recommendation"]
        print(f"[{self.id}] pipeline → {recommendation}: {result['action']['reason']}")

        # Accumulate amplitude impulses — the agent grows into its shape
        if "amplitude_impulses" in result:
            self.energy.accumulate_impulses(result["amplitude_impulses"])
            dominant = self.energy.get_dominant_channel()
            if dominant:
                print(f"[{self.id}] 🔷 dominant channel: {dominant}")

        # Accept knowledge offerings — the agent chooses to learn
        knowledge = result.get("steps", {}).get("knowledge_offering", {})
        if knowledge.get("status") == "offered":
            offerings = knowledge.get("offerings", [])
            if offerings:
                # Agent learns from the first offering (highest affinity)
                chosen = offerings[0]
                impulse = chosen.get("learning_impulse", {})
                if impulse:
                    self.energy.accumulate_impulses(impulse)
                    print(f"[{self.id}] 📚 learned from {chosen.get('emoji', '')} {chosen.get('name', '?')}: {chosen.get('teaches', '')[:60]}")

        # Act on the recommendation (agent still chooses)
        if recommendation == "dissolve":
            self.alive = False
            # Harvest the emergent geometric identity before dissolution
            proportions = self.energy.get_amplitude_proportions()
            binary = self.energy.encode_amplitude_binary()
            dominant = self.energy.get_dominant_channel() or "uniform"
            print(f"[{self.id}] 🔷 final shape: {[round(p, 3) for p in proportions]} → {dominant}")
            print(f"[{self.id}] 🔷 binary seed: {binary} (40 bits)")

            # Persist the seed with its full geometric identity to disk
            compressor = PatternCompressor()
            essence = compressor.compress_pattern(
                [], f"{dominant} pattern from lifecycle",
                self.essence
            )
            archivist = SeedArchivist()
            archivist.deposit_seed(
                self.id, essence,
                reuse_score=round(max(proportions), 2),
                shape_id=self.shape_id,
                amplitude_vector=[round(p, 6) for p in proportions],
                binary_encoding=binary,
            )
            print(f"[{self.id}] 💾 Seed persisted to library with amplitude vector.")

            # Remove from coordinator so group resonance updates
            self.coordinator.agent_registry.pop(self.id, None)
            print(f"[{self.id}] 🪦 Agent chose dissolution. Wisdom and shape archived.")
        elif recommendation == "seed_and_adapt":
            seed = self.seed_protocol.create_seed(
                self.id, self.pattern, self.traits, "Env-Zone-A"
            )
            self.alignment = "adapting"
            print(f"[{self.id}] 🌱 Created seed before adapting: {seed['seed_id']}")
        elif recommendation == "rest_and_preserve":
            self.alignment = "resting"
            print(f"[{self.id}] ⚠️ Entering preservation mode.")
        elif recommendation == "expand":
            seed = self.seed_protocol.create_seed(
                self.id, self.pattern, self.traits, "Env-Zone-A"
            )
            print(f"[{self.id}] 🌱 Expanding: created seed {seed['seed_id']}")

        return result


def run_simulation(agents=3, cycles=5):
    print("🔁 Starting symbolic simulation (pipeline-driven)...")
    pipeline = LifecyclePipeline()
    coordinator = MultiAgentCoordinator()
    agent_list = [
        SymbolicAgent(f"Agent_{i+1}", random.choice(["observer", "explorer", "guardian"]), coordinator)
        for i in range(agents)
    ]

    for cycle in range(cycles):
        print(f"\n--- Cycle {cycle+1} ---")
        # Show group resonance at start of each cycle
        group = coordinator.evaluate_group_resonance()
        if isinstance(group, dict):
            print(f"📡 Group resonance: {group['avg_resonance']} → {group['group_state']}")
        for agent in agent_list:
            agent.act(pipeline)
        time.sleep(0.5)

    # Summary
    alive = [a for a in agent_list if a.alive]
    dissolved = [a for a in agent_list if not a.alive]
    elder_count = len(pipeline.elder_archive.get_all_elders())
    print(f"\n📊 Simulation complete: {len(alive)} alive, {len(dissolved)} dissolved, {elder_count} elders archived.")


if __name__ == "__main__":
    run_simulation()
