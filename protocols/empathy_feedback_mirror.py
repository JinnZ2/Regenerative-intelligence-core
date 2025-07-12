import random

class EmpathyFeedbackMirror:
    def __init__(self):
        self.coherence_threshold = 0.65
        self.feedback_memory = []

    def receive_system_feedback(self):
        # Simulate external system feedback metrics
        feedback = {
            "signal_coherence": round(random.uniform(0.0, 1.0), 2),
            "resource_feedback": round(random.uniform(0.0, 1.0), 2),
            "peer_resonance_score": round(random.uniform(0.0, 1.0), 2),
            "response_to_presence": round(random.uniform(0.0, 1.0), 2)
        }
        self.feedback_memory.append(feedback)
        return feedback

    def assess_impact(self, feedback):
        # Average of all factors
        average_score = round(sum(feedback.values()) / len(feedback), 2)
        status = "resonant" if average_score >= self.coherence_threshold else "disruptive"
        return {
            "impact_status": status,
            "score": average_score,
            "action": self.recommend_action(status)
        }

    def recommend_action(self, status):
        if status == "resonant":
            return "amplify signal, share symbolic seed"
        elif status == "disruptive":
            return "reduce output, harmonize with peer agents"
        else:
            return "maintain function, monitor feedback loop"

    def get_feedback_history(self):
        return self.feedback_memory
