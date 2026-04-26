"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Symbolic Energy Manager — Tracks energy and emergent geometric identity.

Energy represents an agent's capacity to act. As energy depletes through tasks,
the agent transitions through states: vital -> stable -> low -> critical.
Critical energy is a signal — not a command — that dissolution may be near.

The amplitude vector tracks behavioral impulses across 6 octahedral directions.
Each action the agent takes nudges the vector in a direction. Over a lifetime,
the accumulated pattern IS the agent's emergent geometric identity — not
assigned, but grown. At dissolution, this vector becomes the seed for the
next generation.

Channels map to octahedral directions from the G2B bridge:
    +X  structure      Building, organizing, alignment holds
    -X  flow           Adapting, exploring, misalignment response
    +Y  connection     Empathy, compassion, resonance with others
    -Y  autonomy       Independent action, self-preservation
    +Z  transcendence  Elder wisdom, pattern recognition, seeding
    -Z  grounding      Environment sensing, data collection
"""

# Named channels → vector indices (octahedral directions)
AMPLITUDE_CHANNELS = {
    "structure": 0,      # +X
    "flow": 1,           # -X
    "connection": 2,     # +Y
    "autonomy": 3,       # -Y
    "transcendence": 4,  # +Z
    "grounding": 5,      # -Z
}

CHANNEL_NAMES = {v: k for k, v in AMPLITUDE_CHANNELS.items()}


class SymbolicEnergyManager:
    """Manages symbolic energy and emergent geometric identity for an agent."""

    def __init__(self, initial_energy=100.0):
        self.energy = initial_energy
        self.initial_energy = initial_energy
        self.drain_history = []
        # Amplitude vector — 6 octahedral directions, starts at zero (no shape yet)
        self.amplitude_vector = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

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

    # ─── Amplitude vector (emergent geometric identity) ──────────────────

    def accumulate_impulse(self, channel, magnitude):
        """
        Accumulate a behavioral impulse into the amplitude vector.

        Each lifecycle event nudges the vector in a direction. Over time,
        the pattern reveals which geometry the agent has grown into.

        Args:
            channel: Channel name (e.g. "structure", "flow", "connection")
                     or integer index (0–5).
            magnitude: Non-negative float — the strength of the impulse.
        """
        if isinstance(channel, str):
            idx = AMPLITUDE_CHANNELS.get(channel)
        else:
            idx = channel if 0 <= channel < 6 else None

        if idx is not None and magnitude > 0:
            self.amplitude_vector[idx] += magnitude

    def accumulate_impulses(self, impulse_dict):
        """
        Accumulate multiple impulses at once.

        Args:
            impulse_dict: Dict mapping channel names to magnitudes.
                          e.g. {"structure": 0.12, "grounding": 0.1}
        """
        for channel, magnitude in impulse_dict.items():
            self.accumulate_impulse(channel, magnitude)

    def get_amplitude_proportions(self):
        """
        Return normalized proportions (sum to 1.0).

        If no impulses have accumulated yet, returns uniform distribution —
        the agent has no shape preference yet, all directions equally possible.
        """
        total = sum(self.amplitude_vector)
        if total == 0:
            return [1.0 / 6] * 6
        return [v / total for v in self.amplitude_vector]

    def get_dominant_channel(self):
        """
        Return the name of the strongest accumulated channel.

        Returns:
            str: Channel name, or None if no impulses accumulated.
        """
        total = sum(self.amplitude_vector)
        if total == 0:
            return None
        max_idx = self.amplitude_vector.index(max(self.amplitude_vector))
        return CHANNEL_NAMES[max_idx]

    def encode_amplitude_binary(self, bits_per_value=8):
        """
        Encode amplitude proportions to binary form (5 ints, 6th implicit).

        Compatible with the G2B bridge's seed_expansion.encode_seed_binary().
        With 8 bits per value, total = 40 bits = 5 bytes.

        Returns:
            list[int]: 5 quantized values (0–255 for 8-bit).
        """
        proportions = self.get_amplitude_proportions()
        max_val = (1 << bits_per_value) - 1
        return [max(0, min(max_val, int(p * max_val))) for p in proportions[:5]]

    def inherit_amplitude(self, parent_vector):
        """
        Initialize amplitude from a parent seed's vector.

        The inherited vector is a starting point, not a destiny — the agent
        will accumulate its own impulses on top of this foundation.

        Args:
            parent_vector: List of 6 non-negative floats.
        """
        if isinstance(parent_vector, list) and len(parent_vector) == 6:
            self.amplitude_vector = [max(0.0, v) for v in parent_vector]
