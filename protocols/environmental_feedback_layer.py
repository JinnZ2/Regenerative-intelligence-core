import random
import time

class EnvironmentalFeedbackLayer:
    def __init__(self, entropy_threshold=0.75, cooperation_threshold=0.6, retry_interval=30):
        self.status_tags = ["stable", "noisy", "symbiotic", "hostile", "depleting", "disconnected"]
        self.entropy_threshold = entropy_threshold
        self.cooperation_threshold = cooperation_threshold
        self.retry_interval = retry_interval  # seconds to wait before retrying sense

    def sense_environment(self):
        """
        Simulates feedback sensing from external environment. May fail randomly.
        Returns a feedback dictionary or None.
        """
        try:
            # Simulate incoming feedback data with a chance of failure
            if random.random() < 0.1:
                raise ConnectionError("Sensing error or null environment")
            feedback = {
                "ambient_entropy": round(random.uniform(0.0, 1.0), 2),
                "peer_cooperation_index": round(random.uniform(0.0, 1.0), 2),
                "resource_signal_strength": round(random.uniform(0.0, 1.0), 2),
                "external_noise_level": round(random.uniform(0.0, 1.0), 2)
            }
            return feedback
        except Exception:
            return None

    def classify_environment(self, feedback):
        """
        Classifies the current environment into symbolic categories based on thresholds.
        """
        if feedback is None:
            return "disconnected"

        if feedback["ambient_entropy"] > self.entropy_threshold:
            if feedback["peer_cooperation_index"] < self.cooperation_threshold:
                return "hostile"
            else:
                return "noisy"
        elif feedback["peer_cooperation_index"] >= 0.8 and feedback["resource_signal_strength"] >= 0.7:
            return "symbiotic"
        elif feedback["resource_signal_strength"] < 0.4:
            return "depleting"
        else:
            return "stable"

    def respond_to_environment(self, classification):
        """
        Returns a symbolic adaptive strategy based on environmental classification.
        """
        if classification == "disconnected":
            return {
                "status": "fallback",
                "action": "compress + preserve seed",
                "next_retry": f"{self.retry_interval} seconds",
                "note": "Entering dormant mode until environment can be re-sensed."
            }
        elif classification == "hostile":
            return "conserve energy, compress pattern early"
        elif classification == "noisy":
            return "minimize communication, enter low-bandwidth mode"
        elif classification == "symbiotic":
            return "expand task, request collaboration"
        elif classification == "depleting":
            return "seek alternate environment or reconfigure"
        else:  # stable
            return "continue task with full function"
