import time
import random
from SymbolicEnergyManager import SymbolicEnergyManager
from SeedExchangeProtocol import SeedExchangeProtocol
from CompassionReflexLayer import CompassionReflexLayer
from SymbolicElderArchive import SymbolicElderArchive

class SymbolicAgent:
    def __init__(self, agent_id, essence):
        self.id = agent_id
        self.essence = essence
        self.energy = SymbolicEnergyManager()
        self.seed_protocol = SeedExchangeProtocol()
        self.compassion = CompassionReflexLayer()
        self.elder = SymbolicElderArchive()
        self.traits = [random.choice(["reflective", "adaptive", "cooperative"])]
        self.pattern = f"{essence[:3]}-{random.randint(100,999)}"
        self.alive = True
        self.alignment = "aligned"
        print(f"🧬 Agent {self.id} initialized with trait: {self.traits[0]}")

    def act(self, environment_signature):
        if not self.alive:
            return
        task_difficulty = random.uniform(0.2, 0.7)
        self.energy.simulate_energy_drain(task_difficulty)

        energy_state = self.energy.assess_energy_state()
        print(f"[{self.id}] energy: {round(self.energy.energy,1)} → {energy_state}")

        if energy_state == "critical":
            distress = self.compassion.detect_distress({
                "id": self.id,
                "energy": self.energy.energy,
                "resonance": random.uniform(0.2, 0.5),
                "alignment": self.alignment
            })
            print(f"[{self.id}] ⚠️ Distress: {distress['action']}")
            self.alignment = "misaligned"

            if random.random() > 0.5:
                self.alive = False
                record = self.elder.store_elder_record(
                    self.id, self.essence, [self.pattern],
                    self.alignment, "energy depletion"
                )
                print(f"[{self.id}] 🪦 Agent archived as elder: {record['elder_id']}")
        else:
            if random.random() > 0.6:
                seed = self.seed_protocol.create_seed(
                    self.id, self.pattern, self.traits, environment_signature
                )
                print(f"[{self.id}] 🌱 Created seed: {seed['seed_id']}")

def run_simulation(agents=3, cycles=5):
    print("🔁 Starting symbolic simulation...")
    agent_list = [
        SymbolicAgent(f"Agent_{i+1}", random.choice(["observer", "explorer", "guardian"]))
        for i in range(agents)
    ]
    for cycle in range(cycles):
        print(f"\n--- Cycle {cycle+1} ---")
        for agent in agent_list:
            agent.act(environment_signature="Env-Zone-A")
        time.sleep(0.5)

if __name__ == "__main__":
    run_simulation()
