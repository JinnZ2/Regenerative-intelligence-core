"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Symbolic Intelligence CLI — Interactive interface for seed management.

This CLI provides a human-facing interface to the seed lifecycle:
compression, archival, retrieval, and spawning. It delegates to the
actual Modules (SeedArchivist, SeedSelector, AgentInstantiator) rather
than duplicating their logic, ensuring a single source of truth.
"""

import sys
import os
import random

# Add paths for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Modules"))

from seed_compression_archivist import PatternCompressor, SeedArchivist, lifecycle_compression_and_deposit
from seed_retriever_spawner import SeedSelector, AgentInstantiator, retrieve_and_spawn_agent
from seed_schema import to_cli_format


# === SymbolicSeedInterface ===

class SymbolicSeedInterface:
    """Thin wrapper that reads the seed library via SeedSelector."""

    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file
        self.selector = SeedSelector(seed_file=self.seed_file)

    def display_all_seeds(self):
        self.selector.library = self.selector.load_library()
        return [to_cli_format(s) for s in self.selector.library if to_cli_format(s)]

    def describe_seed_by_id(self, seed_id):
        self.selector.library = self.selector.load_library()
        for seed in self.selector.library:
            cli_seed = to_cli_format(seed)
            if cli_seed and cli_seed["ID"] == seed_id:
                return cli_seed
        return {"error": "Seed not found"}


# === SymbolicCLI ===

class SymbolicCLI:
    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file
        self.interface = SymbolicSeedInterface(seed_file=self.seed_file)

    def run(self):
        print("\n=== SYMBOLIC INTELLIGENCE CLI INTERFACE ===")
        while True:
            print("\nOptions:")
            print("1. View all seeds")
            print("2. View seed by ID")
            print("3. Simulate compression and deposit")
            print("4. Spawn agent from seed")
            print("5. Exit")

            choice = input("\nEnter choice (1-5): ").strip()
            if choice == '1':
                self.display_all_seeds()
            elif choice == '2':
                self.display_seed_by_id()
            elif choice == '3':
                self.simulate_compression()
            elif choice == '4':
                self.spawn_agent()
            elif choice == '5':
                print("Exiting symbolic interface.")
                break
            else:
                print("Invalid choice. Please select 1-5.")

    def display_all_seeds(self):
        seeds = self.interface.display_all_seeds()
        if not seeds:
            print("\n(No seeds in archive)")
            return
        for seed in seeds:
            print(f"\nID: {seed['ID']}\nPurpose: {seed['Purpose']}\n"
                  f"Geometry: {seed['Geometry']}\nReuse Score: {seed['Reuse Score']}\n"
                  f"Behavior: {seed['Behavior Summary']}\nTime: {seed['Origin Time']}")

    def display_seed_by_id(self):
        seed_id = input("Enter seed ID: ").strip()
        seed = self.interface.describe_seed_by_id(seed_id)
        for key, value in seed.items():
            print(f"{key}: {value}")

    def simulate_compression(self):
        agent_id = f"agent_{random.randint(1000, 9999)}"
        behavior_logs = ["looped pattern", "resource redistribution", "failure recovery"]
        task_summary = input("Describe agent behavior: ").strip()
        agent_purpose = input("Enter agent purpose: ").strip()
        seed = lifecycle_compression_and_deposit(agent_id, behavior_logs, task_summary, agent_purpose)
        print("🌱 Seed deposited:")
        cli_seed = to_cli_format(seed)
        if cli_seed:
            for key, value in cli_seed.items():
                print(f"  {key}: {value}")
        else:
            for key, value in seed.items():
                print(f"  {key}: {value}")

    def spawn_agent(self):
        keyword = input("Enter keyword or leave blank for top reuse: ").strip()
        geometry = input("Enter geometry or leave blank: ").strip()
        agent = retrieve_and_spawn_agent(
            geometry if geometry else None,
            keyword if keyword else None
        )
        for key, value in agent.items():
            print(f"{key}: {value}")


# === Entry Point ===

if __name__ == "__main__":
    SymbolicCLI().run()
