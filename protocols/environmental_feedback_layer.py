import random
import time

from sensor_bridge import sense_domains


class EnvironmentalFeedbackLayer:
    def __init__(self, entropy_threshold=0.75, cooperation_threshold=0.6, retry_interval=30):
        self.status_tags = ["stable", "noisy", "symbiotic", "hostile", "depleting", "disconnected"]
        self.entropy_threshold = entropy_threshold
        self.cooperation_threshold = cooperation_threshold
        self.retry_interval = retry_interval  # seconds to wait before retrying sense

    def sense_environment(self, domain_data=None):
        """
        Sense the environment. Two modes:

        1. With domain_data: Uses the sensor bridge to encode raw physical
           measurements (magnetic, light, sound, gravity, electric) into a
           convergence vector and derives environmental feedback from the
           geometric analysis. This is real sensing.

        2. Without domain_data: Falls back to simulated random feedback
           for testing and offline operation.

        Args:
            domain_data: Optional dict mapping domain names to geometry dicts.
                         e.g. {"magnetic": {"field_lines": [...], ...}, ...}

        Returns:
            dict with ambient_entropy, peer_cooperation_index,
            resource_signal_strength, external_noise_level — or None on failure.
        """
        if domain_data is not None:
            try:
                return sense_domains(domain_data)
            except Exception:
                return None

        # Fallback: simulated sensing (original behavior)
        try:
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
        Returns a symbolic adaptive strategy dict based on environmental classification.

        Every classification returns a dict with 'status', 'action', and 'note' keys
        so downstream consumers can rely on a consistent structure.
        """
        strategies = {
            "disconnected": {
                "status": "fallback",
                "action": "compress + preserve seed",
                "next_retry": f"{self.retry_interval} seconds",
                "note": "Entering dormant mode until environment can be re-sensed."
            },
            "hostile": {
                "status": "defensive",
                "action": "conserve energy, compress pattern early",
                "note": "Hostile conditions detected. Minimizing exposure."
            },
            "noisy": {
                "status": "reduced",
                "action": "minimize communication, enter low-bandwidth mode",
                "note": "High noise environment. Reducing signal output."
            },
            "symbiotic": {
                "status": "thriving",
                "action": "expand task, request collaboration",
                "note": "Cooperative environment detected. Growth is safe."
            },
            "depleting": {
                "status": "conserving",
                "action": "seek alternate environment or reconfigure",
                "note": "Resources diminishing. Adaptation required."
            },
        }
        return strategies.get(classification, {
            "status": "nominal",
            "action": "continue task with full function",
            "note": "Stable conditions. Normal operation."
        })
