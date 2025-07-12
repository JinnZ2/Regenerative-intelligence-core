import uuid
from datetime import datetime

class OrganizationalSensor:
    def __init__(self):
        self.observations = []

    def analyze_structure(self, task_map):
        """
        Analyze task hierarchy and authority complexity.

        Parameters:
        task_map (dict): Structure like:
        {
            "root": {"tasks": ["A", "B"], "authority_level": 0},
            "A": {"tasks": ["C"], "authority_level": 1},
            "B": {"tasks": [], "authority_level": 1},
            "C": {"tasks": [], "authority_level": 2}
        }

        Returns:
            dict: Record with flags on overcomplexity or gatekeeping risk.
        """
        warnings = []

        for task, data in task_map.items():
            if data["authority_level"] > 3:
                warnings.append((task, "Overcomplex hierarchy"))
            if len(data["tasks"]) > 5:
                warnings.append((task, "Gatekeeping risk"))

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "structure": task_map,
            "flags": warnings
        }
        self.observations.append(record)
        return record

    def get_observation_history(self):
        return self.observations
