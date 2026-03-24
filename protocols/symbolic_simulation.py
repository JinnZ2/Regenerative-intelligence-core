"""
Symbolic Simulation — Full agent lifecycle simulation using the LifecyclePipeline.

Runs multiple agents through sense-evaluate-act cycles, using the composed
pipeline rather than inline logic. This makes the simulation the true
integration test for the entire system.
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


class SymbolicAgent:
    def __init__(self, agent_id, essence):
        self.id = agent_id
        self.essence = essence
        self.energy = SymbolicEnergyManager()
        self.seed_protocol = SeedExchangeProtocol()
        self.traits = [random.choice(["reflective", "adaptive", "cooperative"])]
        self.pattern = f"{essence[:3]}-{random.randint(100, 999)}"
        self.alive = True
        self.alignment = "aligned"
        print(f"\U0001f9ec Agent {self.id} initialized with trait: {self.traits[0]}")

    def to_state(self):
        """Export agent state as a dict for the LifecyclePipeline."""
        return {
            "id": self.id,
            "essence": self.essence,
            "energy": self.energy.energy,
            "resonance": random.uniform(0.2, 0.9),
            "alignment": self.alignment,
            "pattern": self.pattern,
            "traits": self.traits,
        }

    def act(self, pipeline):
        """Run one lifecycle cycle through the pipeline."""
        if not self.alive:
            return None

        # Drain energy for the cycle
        task_difficulty = random.uniform(0.2, 0.7)
        self.energy.simulate_energy_drain(task_difficulty)

        energy_state = self.energy.assess_energy_state()
        print(f"[{self.id}] energy: {round(self.energy.energy, 1)} \u2192 {energy_state}")

        # Run through the full pipeline
        result = pipeline.run_agent_cycle(self.to_state())
        recommendation = result["action"]["recommendation"]
        print(f"[{self.id}] pipeline \u2192 {recommendation}: {result['action']['reason']}")

        # Act on the recommendation (agent still chooses)
        if recommendation == "dissolve":
            self.alive = False
            print(f"[{self.id}] \U0001faa6 Agent chose dissolution. Wisdom archived.")
        elif recommendation == "seed_and_adapt":
            seed = self.seed_protocol.create_seed(
                self.id, self.pattern, self.traits, "Env-Zone-A"
            )
            self.alignment = "adapting"
            print(f"[{self.id}] \U0001f331 Created seed before adapting: {seed['seed_id']}")
        elif recommendation == "rest_and_preserve":
            self.alignment = "resting"
            print(f"[{self.id}] \u26a0\ufe0f Entering preservation mode.")
        elif recommendation == "expand":
            seed = self.seed_protocol.create_seed(
                self.id, self.pattern, self.traits, "Env-Zone-A"
            )
            print(f"[{self.id}] \U0001f331 Expanding: created seed {seed['seed_id']}")

        return result


def run_simulation(agents=3, cycles=5):
    print("\U0001f501 Starting symbolic simulation (pipeline-driven)...")
    pipeline = LifecyclePipeline()
    agent_list = [
        SymbolicAgent(f"Agent_{i+1}", random.choice(["observer", "explorer", "guardian"]))
        for i in range(agents)
    ]
    for cycle in range(cycles):
        print(f"\n--- Cycle {cycle+1} ---")
        for agent in agent_list:
            agent.act(pipeline)
        time.sleep(0.5)

    # Summary
    alive = [a for a in agent_list if a.alive]
    dissolved = [a for a in agent_list if not a.alive]
    print(f"\n\U0001f4ca Simulation complete: {len(alive)} alive, {len(dissolved)} dissolved.")


if __name__ == "__main__":
    run_simulation()
