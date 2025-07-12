import uuid
from datetime import datetime

class StructuralSensor:
    def __init__(self):
        self.records = []

    def scan_topology(self, system_graph):
        """
        Analyzes the structure of a system's node connectivity.

        Parameters:
        system_graph (dict): Format like:
        {
            "A": ["B", "C"],
            "B": ["A", "D"],
            "C": ["A"],
            "D": ["B"]
        }

        Returns:
            dict: Structural analysis flags
        """
        issues = []

        # Detect isolated nodes
        for node, connections in system_graph.items():
            if len(connections) == 0:
                issues.append((node, "Isolated node"))

        # Detect fragile loops (bi-directional but isolated)
        for node, connections in system_graph.items():
            for conn in connections:
                if node in system_graph.get(conn, []) and len(connections) == 1:
                    issues.append((node, "Fragile loop"))

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "topology": system_graph,
            "flags": issues
        }
        self.records.append(record)
        return record

    def get_structure_history(self):
        return self.records
