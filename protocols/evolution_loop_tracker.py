import json
import uuid
from datetime import datetime

class EvolutionLoopTracker:
    def __init__(self):
        self.generations = []
        self.current_gen = 0

    def start_new_generation(self, agents_summary):
        """
        Begin tracking a new symbolic generation of agents.

        Parameters:
            agents_summary (list/dict): Summary of agents' state or seed info

        Returns:
            str: Generation ID (e.g., "Gen-1")
        """
        self.current_gen += 1
        generation_id = f"Gen-{self.current_gen}"
        summary = {
            "generation_id": generation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "agents_summary": agents_summary
        }
        self.generations.append(summary)
        return generation_id

    def track_outcomes(self, generation_id, outcome_data):
        """
        Add outcome data to a completed generation.
        """
        for gen in self.generations:
            if gen["generation_id"] == generation_id:
                gen["outcome"] = outcome_data
                break

    def save_to_file(self, filepath="evolution_history.json"):
        """
        Persist all generational data to disk (or symbolic memory archive).
        """
        with open(filepath, "w") as f:
            json.dump(self.generations, f, indent=2)

    def get_evolution_summary(self):
        return {
            "total_generations": self.current_gen,
            "summary": self.generations
        }
