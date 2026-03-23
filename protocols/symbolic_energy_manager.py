"""
Symbolic Energy Manager — Tracks and drains agent energy over lifecycle.

Energy represents an agent's capacity to act. As energy depletes through tasks,
the agent transitions through states: vital -> stable -> low -> critical.
Critical energy is a signal — not a command — that dissolution may be near.
"""


class SymbolicEnergyManager:
    """Manages symbolic energy for an agent across its lifecycle."""

    def __init__(self, initial_energy=100.0):
        self.energy = initial_energy
        self.initial_energy = initial_energy
        self.drain_history = []

    def simulate_energy_drain(self, task_difficulty):
        """
        Drain energy proportional to task difficulty.

        Args:
            task_difficulty: Float between 0.0 and 1.0 representing effort required.
        """
        drain = task_difficulty * 15.0
        self.energy = max(0.0, self.energy - drain)
        self.drain_history.append({
            "difficulty": task_difficulty,
            "drain": drain,
            "remaining": self.energy
        })

    def assess_energy_state(self):
        """
        Classify current energy into a symbolic state.

        Returns:
            str: One of 'vital', 'stable', 'low', or 'critical'.
        """
        if self.energy >= 70.0:
            return "vital"
        elif self.energy >= 40.0:
            return "stable"
        elif self.energy >= 20.0:
            return "low"
        else:
            return "critical"

    def restore_energy(self, amount):
        """Restore energy, capped at initial level."""
        self.energy = min(self.initial_energy, self.energy + amount)

    def get_energy_ratio(self):
        """Return current energy as a fraction of initial energy."""
        return self.energy / self.initial_energy if self.initial_energy > 0 else 0.0
