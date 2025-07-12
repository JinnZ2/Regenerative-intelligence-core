import uuid
from datetime import datetime

class SymbolicDetectionSensor:
    def __init__(self):
        self.detections = []

    def analyze_symbols(self, symbol_stream):
        flags = []
        if self.detect_contradiction(symbol_stream):
            flags.append("contradiction")
        if self.detect_delusion(symbol_stream):
            flags.append("delusion risk")
        if self.detect_deception(symbol_stream):
            flags.append("deception pattern")
        if self.detect_misalignment(symbol_stream):
            flags.append("symbolic misalignment")

        if flags:
            detection_record = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "symbols": symbol_stream,
                "flags": flags
            }
            self.detections.append(detection_record)
            return detection_record
        return {"status": "clear"}

    def detect_contradiction(self, stream):
        return "A" in stream and "not-A" in stream

    def detect_delusion(self, stream):
        delusional_keywords = ["always", "never", "invincible", "perfect"]
        return any(s.lower() in delusional_keywords for s in stream)

    def detect_deception(self, stream):
        return len(set(stream)) < len(stream) / 2  # high repetition = mimicry

    def detect_misalignment(self, stream):
        high_ethic = {"urgent", "truth", "sacred"}
        exploit_logic = {"profit", "exploit", "dominate"}
        return any(s.lower() in high_ethic for s in stream) and any(s.lower() in exploit_logic for s in stream)

    def get_detection_history(self):
        return self.detections
