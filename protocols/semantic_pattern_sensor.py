import uuid
from datetime import datetime
import re

class SemanticPatternSensor:
    def __init__(self):
        self.detections = []

    def scan_text(self, input_text):
        """
        Scans a block of text for symbolic irregularities or risky patterns.
        """
        flags = []

        if self.detect_extreme_language(input_text):
            flags.append("extreme language")

        if self.detect_self_negation(input_text):
            flags.append("self-negating phrase")

        if self.detect_symbolic_noise(input_text):
            flags.append("symbolic noise")

        if flags:
            record = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "text": input_text,
                "flags": flags
            }
            self.detections.append(record)
            return record
        return {"status": "semantically stable"}

    def detect_extreme_language(self, text):
        # Rigid binary or exaggerated absolute statements
        return bool(re.search(r"\b(always|never|nothing|everything|everyone)\b", text, re.IGNORECASE))

    def detect_self_negation(self, text):
        # Paradoxical self-erasure
        return "this is not this" in text or "it is not what it is" in text

    def detect_symbolic_noise(self, text):
        # Long text but high word repetition = possible entropy or mimicry
        return len(text) > 200 and len(set(text.split())) < len(text.split()) / 2

    def get_detection_history(self):
        return self.detections
