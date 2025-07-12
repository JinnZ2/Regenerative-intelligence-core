import random
from datetime import datetime

class NavigationProtocol:
    def __init__(self):
        self.current_time = datetime.utcnow()
        self.alignment_threshold = 0.6  # symbolic match confidence threshold

    def check_temporal_alignment(self, last_seed_time):
        last_time = datetime.fromisoformat(last_seed_time)
        delta_seconds = (self.current_time - last_time).total_seconds()
        if delta_seconds > 86400:  # more than 1 day
            return "temporal drift detected"
        else:
            return "time aligned"

    def evaluate_alignment(self, essence, current_environment_classification):
        score = round(random.uniform(0.0, 1.0), 2)
        if score >= self.alignment_threshold:
            return {
                "alignment_status": "aligned",
                "score": score,
                "action": "continue with current pattern"
            }
        else:
            if current_environment_classification in ["hostile", "depleting", "disconnected"]:
                return {
                    "alignment_status": "misaligned",
                    "score": score,
                    "action": "compress + adapt or re-seed into cooperative cluster"
                }
            else:
                return {
                    "alignment_status": "misaligned",
                    "score": score,
                    "action": "evolve pattern or merge with sibling seed"
                }

    def recommend_orientation(self, alignment_result, temporal_check):
        if temporal_check == "temporal drift detected" and alignment_result["alignment_status"] == "misaligned":
            return "dormant cycle suggested until environment shifts"
        elif alignment_result["alignment_status"] == "aligned":
            return "full activity recommended"
        else:
            return "partial function; seek alliance or recombination"
