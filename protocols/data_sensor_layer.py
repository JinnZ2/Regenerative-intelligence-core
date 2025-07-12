import uuid
from datetime import datetime
import random

class DataSensorLayer:
    def __init__(self):
        self.data_snapshots = []

    def simulate_data_feed(self, stream_type="energy", volatility=0.2):
        """
        Generate a simulated data value for a given stream.

        Parameters:
            stream_type (str): Type of stream ("energy", "temperature", etc.)
            volatility (float): Max % fluctuation allowed

        Returns:
            float: Simulated dynamic value
        """
        base_values = {
            "energy": 100,
            "temperature": 22,
            "resource_flux": 50,
            "data_entropy": 0.5
        }
        base = base_values.get(stream_type, 0)
        fluctuation = base * volatility * random.uniform(-1, 1)
        return round(base + fluctuation, 2)

    def collect_data_point(self, stream_type, volatility=0.2):
        """
        Record a dynamic data point from a simulated stream.
        """
        value = self.simulate_data_feed(stream_type, volatility)
        timestamp = datetime.utcnow().isoformat()
        snapshot = {
            "id": str(uuid.uuid4()),
            "type": stream_type,
            "value": value,
            "timestamp": timestamp
        }
        self.data_snapshots.append(snapshot)
        return snapshot

    def analyze_trend(self, recent_count=5):
        """
        Analyze trend direction from recent data points.

        Returns:
            dict: Trend report or None if insufficient data.
        """
        if len(self.data_snapshots) < recent_count:
            return None
        recent = self.data_snapshots[-recent_count:]
        trend = "rising" if all(r["value"] < recent[-1]["value"] for r in recent[:-1]) else "fluctuating"
        return {
            "trend": trend,
            "recent_values": [r["value"] for r in recent]
        }

    def get_data_history(self):
        return self.data_snapshots
