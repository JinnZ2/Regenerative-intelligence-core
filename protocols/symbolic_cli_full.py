import json
import os
import uuid
import random
from datetime import datetime

# === SymbolicSeedInterface ===

class SymbolicSeedInterface:
    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file
        if not os.path.exists(self.seed_file):
            with open(self.seed_file, "w") as f:
                json.dump([], f)

    def load_seeds(self):
        with open(self.seed_file, "r") as f:
            return json.load(f)

    def save_seeds(self, seeds):
        with open(self.seed_file, "w") as f:
            json.dump(seeds, f, indent=2)

    def display_all_seeds(self):
        return self.load_seeds()

    def describe_seed_by_id(self, seed_id):
        seeds = self.load_seeds()
        for seed in seeds:
            if seed["ID"] == seed_id:
                return seed
        return {"error": "Seed not found"}

# === SeedCompressionAndArchivist ===

def lifecycle_compression_and_deposit(agent_id, behavior_logs, task_summary, agent_purpose, seed_file="symbolic_seed_library.json"):
    seed = {
        "ID": str(uuid.uuid4()),
        "Agent": agent_id,
        "Behavior Summary": task_summary,
        "Purpose": agent_purpose,
        "Geometry": random.choice(["sphere", "spiral", "hexagon"]),
        "Reuse Score": round(random.uniform(0.85, 1.0), 2),
        "Origin Time": datetime.utcnow().isoformat(),
        "Logs": behavior_logs
    }

    if not os.path.exists(seed_file):
        with open(seed_file, "w") as f:
            json.dump([], f)

    with open(seed_file, "r") as f:
        seeds = json.load(f)

    seeds.append(seed)

    with open(seed_file, "w") as f:
        json.dump(seeds, f, indent=2)

    return seed

# === SeedRetrievalAndSpawner ===

def retrieve_and_spawn_agent(geometry=None, keyword=None, seed_file="symbolic_seed_library.json"):
    if not os.path.exists(seed_file):
        return {"error": "No seed file found."}

    with open(seed_file, "r") as f:
        seeds = json.load(f)

    filtered = seeds
    if keyword:
        filtered = [s for s in filtered if keyword.lower() in s["Purpose"].lower()]
    if geometry:
        filtered = [s for s in filtered if s["Geometry"].lower() == geometry.lower()]

    if not filtered:
        return {"error": "No matching seed found."}

    best = sorted(filtered, key=lambda x: x["Reuse Score"], reverse=True)[0]
    agent_instance = {
        "agent_id": f"spawned_{random.randint(1000, 9999)}",
        "from_seed": best["ID"],
        "purpose": best["Purpose"],
        "geometry": best["Geometry"],
        "behavior_summary": best["Behavior Summary"],
        "reuse_score": best["Reuse Score"]
    }

    return agent_instance

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
        for seed in seeds:
            print(f"\nID: {seed['ID']}\nPurpose: {seed['Purpose']}\nGeometry: {seed['Geometry']}\nReuse Score: {seed['Reuse Score']}\nBehavior: {seed['Behavior Summary']}\nTime: {seed['Origin Time']}")

    def display_seed_by_id(self):
        seed_id = input("Enter seed ID: ").strip()
        seed = self.interface.describe_seed_by_id(seed_id)
        for key, value in seed.items():
            print(f"{key}: {value}")

    def simulate_compression(self):
        agent_id = f"agent_{random.randint(1000,9999)}"
        behavior_logs = ["looped pattern", "resource redistribution", "failure recovery"]
        task_summary = input("Describe agent behavior: ").strip()
        agent_purpose = input("Enter agent purpose: ").strip()
        seed = lifecycle_compression_and_deposit(agent_id, behavior_logs, task_summary, agent_purpose)
        print("Seed deposited:")
        for key, value in seed.items():
            print(f"{key}: {value}")

    def spawn_agent(self):
        keyword = input("Enter keyword or leave blank for top reuse: ").strip()
        geometry = input("Enter geometry or leave blank: ").strip()
        agent = retrieve_and_spawn_agent(geometry if geometry else None, keyword if keyword else None)
        for key, value in agent.items():
            print(f"{key}: {value}")

# === Entry Point ===

if __name__ == "__main__":
    SymbolicCLI().run()
