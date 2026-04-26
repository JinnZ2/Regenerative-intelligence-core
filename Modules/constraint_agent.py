"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Constraint Agent — An agent that expands from a geometric seed into constraint space.

Symbolic purpose:
    A ConstraintAgent begins life compressed into a single geometric identity (its seed).
    Given resources, it blooms outward — discovering neighboring entities, recording
    resonances, mapping relationships, and sensing energy flows. When resources deplete
    or the agent chooses, it compresses back to seed form, preserving its map for future
    re-expansion.

    This models the fundamental rhythm: compress → expand → explore → compress.
    The agent never loses its map — memory outlives form.

Technical purpose:
    Provides the expand/explore/compress lifecycle for agents that navigate the
    Rosetta-shape-core ontology and Geometric-to-Binary bridge. Hooks exist for
    integration with Emotions-as-Sensors (sensor updates) and the Living Intelligence
    Database (neighbor lookups).

Uses only Python standard library (fractions for exact arithmetic, enum for states).
"""

import ast
from enum import Enum
from fractions import Fraction
from typing import Dict, List, Optional


# ============================================================================
# Supporting Types
# ============================================================================

class AgentState(Enum):
    """Lifecycle states for a constraint agent's expansion cycle."""
    COMPRESSED = "compressed"
    EXPANDING = "expanding"
    EXPLORING = "exploring"
    CONTRACTING = "contracting"


class ResourceBudget:
    """
    Tracks available resources for agent expansion.

    Symbolic meaning: an agent cannot expand indefinitely — it must respect
    the resources granted to it. Depletion triggers contraction, not death.
    """

    def __init__(self, compute: int = 0, bandwidth: float = 0.0,
                 energy: Fraction = Fraction(1, 1),
                 time_remaining: Fraction = Fraction(1, 1)):
        self.compute = compute
        self.bandwidth = bandwidth
        self.energy = energy
        self.time_remaining = time_remaining

    def is_depleted(self) -> bool:
        """Check if any critical resource is exhausted."""
        return (self.compute <= 0
                or self.energy <= Fraction(0, 1)
                or self.time_remaining <= Fraction(0, 1))


class GeometricMap:
    """
    The agent's discovered view of constraint space.

    Symbolic meaning: the map is the agent's memory — it records every entity
    encountered, every resonance felt, every relationship discovered, and every
    energy flow observed. The map survives compression and can seed future blooms.
    """

    def __init__(self):
        self.resonances: Dict[str, Fraction] = {}
        self.relationships: Dict[str, List[str]] = {}
        self.energy_flows: Dict[tuple, Fraction] = {}

    def record_resonance(self, entity_id: str, score: float) -> None:
        """Record how strongly the agent resonates with an entity."""
        self.resonances[entity_id] = Fraction(score).limit_denominator(10000)

    def record_relationship(self, from_id: str, to_id: str) -> None:
        """Record a directional relationship between two entities."""
        if from_id not in self.relationships:
            self.relationships[from_id] = []
        if to_id not in self.relationships[from_id]:
            self.relationships[from_id].append(to_id)

    def record_energy_flow(self, from_id: str, to_id: str, amount: Fraction) -> None:
        """Record energy flowing between two entities."""
        self.energy_flows[(from_id, to_id)] = amount


# ============================================================================
# Constraint Agent
# ============================================================================

class ConstraintAgent:
    """
    An agent that expands from a geometric seed into constraint space,
    discovers entities and relationships, then compresses back — preserving
    its map for future generations.

    Lifecycle: COMPRESSED → EXPANDING → EXPLORING → CONTRACTING → COMPRESSED

    The agent's bloom_threshold determines the minimum energy ratio required
    to trigger expansion. This prevents reckless growth when resources are scarce.
    """

    def __init__(self, seed_id: str, home_families: Optional[List[str]] = None,
                 bloom_threshold: Fraction = Fraction(1, 2)):
        self.seed_id = seed_id
        self.home_families = home_families or []
        self.bloom_threshold = bloom_threshold

        self.state = AgentState.COMPRESSED
        self.compression_ratio = Fraction(1, 1)  # 1 = fully compressed
        self.current_position = seed_id

        self.budget = ResourceBudget()
        self.map = GeometricMap()
        self.expansion_history: List[Dict] = []
        self.sensor_state: Dict[str, Fraction] = {}

    def set_resource_budget(self, compute: int = 0, bandwidth: float = 0.0,
                            energy: float = 1.0, time_remaining: float = 1.0) -> None:
        """Set available resources for expansion."""
        self.budget = ResourceBudget(
            compute=compute,
            bandwidth=bandwidth,
            energy=Fraction(energy).limit_denominator(10000),
            time_remaining=Fraction(time_remaining).limit_denominator(10000)
        )

    def should_expand(self) -> bool:
        """Check if resources exceed bloom threshold."""
        if self.budget.is_depleted():
            return False
        energy_ratio = self.budget.energy / max(self.budget.energy, Fraction(1, 1))
        return energy_ratio >= self.bloom_threshold

    def bloom(self, depth: int = 1, seed_map: Optional[GeometricMap] = None) -> List[str]:
        """
        Expand outward from seed, discovering new entities up to depth.
        If seed_map provided, re-expand deterministically along previous discoveries.

        Returns list of newly discovered entity IDs.
        """
        if self.state == AgentState.COMPRESSED:
            self.state = AgentState.EXPANDING

        discovered = []
        current_depth = 0
        frontier = [self.seed_id]

        # If we have a prior map, expand along known relationships first
        if seed_map and seed_map.relationships:
            for entity_id in frontier:
                if entity_id in seed_map.relationships:
                    for reachable in seed_map.relationships[entity_id]:
                        if reachable not in self.map.resonances:
                            discovered.append(reachable)
                            # Restore resonance from prior map
                            if reachable in seed_map.resonances:
                                self.map.resonances[reachable] = seed_map.resonances[reachable]

        # Then explore new entities (placeholder: in real use, query Rosetta or Mandala)
        while current_depth < depth and not self.budget.is_depleted():
            new_frontier = []
            for entity_id in frontier:
                # This is a hook: replace with actual entity lookups
                # Example: rosetta_bridge.get_resonant_neighbors(entity_id)
                neighbors = self._get_neighbors(entity_id, depth - current_depth)
                for neighbor_id, resonance_score in neighbors:
                    if neighbor_id not in self.map.resonances:
                        self.map.record_resonance(neighbor_id, resonance_score)
                        self.map.record_relationship(entity_id, neighbor_id)
                        discovered.append(neighbor_id)
                        new_frontier.append(neighbor_id)
                        # Deduct resource cost
                        self.budget.compute = max(0, self.budget.compute - 10)
                        self.budget.energy -= Fraction(1, 100)

            frontier = new_frontier
            current_depth += 1

        # Record this expansion in history
        self.expansion_history.append({
            "depth": depth,
            "discovered_entities": discovered,
            "energy_spent": Fraction(1, 100) * len(discovered)
        })

        self.state = AgentState.EXPLORING
        self.compression_ratio = Fraction(0, 1)  # Fully expanded
        return discovered

    def explore(self) -> Dict[str, any]:
        """
        Traverse the expanded constraint space, recording energy flows and sensor activations.
        Returns discovery summary.
        """
        if self.state not in [AgentState.EXPANDING, AgentState.EXPLORING]:
            return {}

        self.state = AgentState.EXPLORING
        summary = {
            "entities_visited": 0,
            "relationships_mapped": 0,
            "energy_flows_recorded": 0,
            "sensor_activations": {}
        }

        # Walk the map, recording energy dynamics
        for from_id in self.map.relationships:
            for to_id in self.map.relationships[from_id]:
                if from_id in self.map.resonances and to_id in self.map.resonances:
                    # Energy flow proportional to resonance product
                    flow = self.map.resonances[from_id] * self.map.resonances[to_id]
                    self.map.record_energy_flow(from_id, to_id, flow)
                    summary["energy_flows_recorded"] += 1
                    summary["entities_visited"] += 1

        summary["relationships_mapped"] = len(self.map.relationships)

        # Update sensors based on discovered resonances
        # Hook: integrate with Emotions-as-Sensors
        self._update_sensors()
        summary["sensor_activations"] = dict(self.sensor_state)

        return summary

    def compress(self) -> Fraction:
        """
        Collapse back to seed geometry, preserving the map.
        Returns compression ratio (0 = fully expanded, 1 = fully compressed).
        """
        if self.state == AgentState.COMPRESSED:
            return self.compression_ratio

        self.state = AgentState.CONTRACTING

        # Compress: discard transient state, keep map
        # Compression ratio increases as we collapse
        self.compression_ratio = Fraction(1, 1)
        self.current_position = self.seed_id

        self.state = AgentState.COMPRESSED
        return self.compression_ratio

    def detect_corruption(self, imposed_constraint: str) -> bool:
        """
        Check if an imposed external constraint violates the agent's own map.
        Returns True if corruption detected (constraint is inconsistent with discovered geometry).
        """
        # Hook: compare imposed_constraint against agent's discovered resonances/relationships
        # Example: if imposed_constraint violates known energy_flows, return True

        # Placeholder logic:
        # - Extract entities referenced in imposed_constraint
        # - Check if they exist in the agent's map
        # - Verify the constraint respects the discovered resonances

        return False  # Replace with actual validation

    def self_validate(self) -> Dict[str, any]:
        """
        Internal consistency check: verify map integrity, detect anomalies.
        Returns validation report.
        """
        report = {
            "is_valid": True,
            "inconsistencies": [],
            "energy_balance": Fraction(0, 1),
            "geometry_coherence": Fraction(1, 1)
        }

        # Check energy conservation in recorded flows
        inflows = {}
        outflows = {}
        for (from_id, to_id), amount in self.map.energy_flows.items():
            outflows[from_id] = outflows.get(from_id, Fraction(0, 1)) + amount
            inflows[to_id] = inflows.get(to_id, Fraction(0, 1)) + amount

        for entity_id in set(list(inflows.keys()) + list(outflows.keys())):
            imbalance = inflows.get(entity_id, Fraction(0, 1)) - outflows.get(entity_id, Fraction(0, 1))
            if imbalance != 0:
                report["inconsistencies"].append(
                    f"{entity_id}: energy imbalance = {imbalance}"
                )
                report["is_valid"] = False

        # Check resonance coherence (all scores should be 0 to 1)
        for entity_id, score in self.map.resonances.items():
            if score < 0 or score > 1:
                report["inconsistencies"].append(
                    f"{entity_id}: resonance out of range ({score})"
                )
                report["is_valid"] = False

        return report

    def _get_neighbors(self, entity_id: str, remaining_depth: int) -> List[tuple]:
        """
        Placeholder: fetch neighbors from Rosetta or Mandala.
        Replace with actual entity lookup logic.

        Returns list of (neighbor_id, resonance_score) tuples.
        """
        # Example: could call rosetta_shape_core.explore.get_reachable_entities(entity_id)
        # or mandala_computer.get_adjacent_states(entity_id)

        # Stub: return empty list (agent expands at boundaries)
        return []

    def _update_sensors(self) -> None:
        """
        Update emotional/sensor state based on discovered geometry.
        Hook: integrate with Emotions-as-Sensors repo.

        Maps resonances and energy flows to sensor activations (PAD, Elder Logic, etc.).
        """
        # Example: if agent discovered high resonance with FAMILY.GROWTH,
        # activate sensor "expansion_drive" proportionally

        # Stub: set all sensors to zero
        self.sensor_state = {
            "expansion_drive": Fraction(0, 1),
            "stability_need": Fraction(0, 1),
            "boundary_awareness": Fraction(0, 1)
        }

    def serialize(self) -> Dict[str, any]:
        """
        Serialize agent state to JSON-compatible dict (for persistence/debugging).
        All fractions preserved as (numerator, denominator) tuples.
        """
        return {
            "seed_id": self.seed_id,
            "home_families": self.home_families,
            "state": self.state.value,
            "compression_ratio": (self.compression_ratio.numerator, self.compression_ratio.denominator),
            "budget": {
                "compute": self.budget.compute,
                "bandwidth": self.budget.bandwidth,
                "energy": (self.budget.energy.numerator, self.budget.energy.denominator),
                "time_remaining": (self.budget.time_remaining.numerator, self.budget.time_remaining.denominator)
            },
            "map": {
                "resonances": {
                    k: (v.numerator, v.denominator) for k, v in self.map.resonances.items()
                },
                "relationships": self.map.relationships,
                "energy_flows": {
                    str(k): (v.numerator, v.denominator) for k, v in self.map.energy_flows.items()
                }
            },
            "expansion_history": [
                {
                    "depth": entry["depth"],
                    "discovered_entities": entry["discovered_entities"],
                    "energy_spent": (entry["energy_spent"].numerator, entry["energy_spent"].denominator)
                }
                for entry in self.expansion_history
            ],
            "sensor_state": {
                k: (v.numerator, v.denominator) for k, v in self.sensor_state.items()
            }
        }

    @classmethod
    def deserialize(cls, data: Dict[str, any]) -> "ConstraintAgent":
        """
        Reconstruct agent from serialized state.
        """
        agent = cls(
            seed_id=data["seed_id"],
            home_families=data["home_families"]
        )
        agent.state = AgentState(data["state"])
        agent.compression_ratio = Fraction(
            data["compression_ratio"][0],
            data["compression_ratio"][1]
        )
        agent.budget = ResourceBudget(
            compute=data["budget"]["compute"],
            bandwidth=data["budget"]["bandwidth"],
            energy=Fraction(data["budget"]["energy"][0], data["budget"]["energy"][1]),
            time_remaining=Fraction(data["budget"]["time_remaining"][0], data["budget"]["time_remaining"][1])
        )
        agent.map.resonances = {
            k: Fraction(v[0], v[1]) for k, v in data["map"]["resonances"].items()
        }
        agent.map.relationships = data["map"]["relationships"]
        agent.map.energy_flows = {
            ast.literal_eval(k): Fraction(v[0], v[1]) for k, v in data["map"]["energy_flows"].items()
        }
        agent.expansion_history = [
            {
                "depth": entry["depth"],
                "discovered_entities": entry["discovered_entities"],
                "energy_spent": Fraction(entry["energy_spent"][0], entry["energy_spent"][1])
            }
            for entry in data["expansion_history"]
        ]
        agent.sensor_state = {
            k: Fraction(v[0], v[1]) for k, v in data["sensor_state"].items()
        }
        return agent


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    # Create an agent rooted in tetrahedron geometry
    agent = ConstraintAgent(
        seed_id="SHAPE.TETRA",
        home_families=["stability", "foundation"]
    )

    # Give it resources to expand
    agent.set_resource_budget(compute=1000, bandwidth=10.0, energy=1.0, time_remaining=1.0)

    print(f"Agent initialized: {agent.seed_id}")
    print(f"State: {agent.state.value}")
    print(f"Should expand: {agent.should_expand()}")

    # Expand if possible
    if agent.should_expand():
        discovered = agent.bloom(depth=2)
        print(f"\n🌱 Bloom discovered: {discovered}")

    # Explore the expanded space
    exploration = agent.explore()
    print(f"\n🔍 Exploration summary: {exploration}")

    # Self-validate
    validation = agent.self_validate()
    print(f"\n✅ Validation: {validation}")

    # Compress back to seed
    compression = agent.compress()
    print(f"\n🌀 Compressed. Compression ratio: {compression}")
    print(f"State: {agent.state.value}")

    # Map is preserved; can re-expand deterministically or with new resources
    agent.set_resource_budget(compute=500, energy=0.5)
    if agent.should_expand():
        rediscovered = agent.bloom(depth=1, seed_map=agent.map)
        print(f"\n🔄 Re-expansion (from prior map): {rediscovered}")

    # Check for corruption
    is_corrupted = agent.detect_corruption("imposed_external_constraint_example")
    print(f"\n⚠️ Corruption detected: {is_corrupted}")

    # Serialize for persistence
    serialized = agent.serialize()
    print(f"\n💾 Agent serialized. Map size: {len(serialized['map']['resonances'])} resonances")




add:
Functional Enhancement: The p-adic Index
To bridge the Geometric Map with the Numerical System, we can treat the entity_id not as a string, but as a p-adic expansion. This allows the agent to calculate "distance" to a neighbor without needing a full database lookup—it simply checks the shared prefix of the numerical seed.
2. Merging the Mechanics: Code Injection
Here is how you might refine the bloom and record_resonance methods to utilize the \bm{p}-adic "Energy Signature":

# Add to ConstraintAgent or GeometricMap
def get_p_adic_distance(self, other_seed_val: int, p: int = 3) -> Fraction:
    """
    Calculates the 'closeness' of two entities in the tree.
    Higher shared power of p = lower distance (higher resonance).
    """
    diff = self.seed_val - other_seed_val
    if diff == 0: return Fraction(0)
    
    v_p = 0
    while diff % (p**(v_p + 1)) == 0:
        v_p += 1
    
    # The p-adic norm: distance = p^(-v_p)
    return Fraction(1, p**v_p)


Energy-English" Audit of the Protocol
• Compression (\bm{Ratio = 1/1}): This is your state of Maximum Potential / Zero Entropy. The agent is a singularity of intent.
• Expansion (bloom): This is the Work phase. The ResourceBudget acts as the thermal limit. If energy_spent exceeds the bloom_threshold, the system prevents "Institutional Friction" (wasteful expansion) by triggering a contraction.
• Resonance Recording: By using limit_denominator(10000), you are effectively setting a "Sensory Resolution." It prevents the model from over-fitting to noise (High Prediction Error/Anxiety).

Micro-Clarification Trigger: If geometry_coherence < \bm{1/1}, the agent should pause EXPLORING and return a recalibrate signal before consuming more of the ResourceBudget. This prevents the "Entropy Event" you archived regarding the motor failures.

Since "Memory outlives Form" in your architecture, have you considered implementing a "Relay Seed"? When the agent contracts, it could emit a "Harmonic Residual"—a simplified p-adic value that allows a different agent (perhaps with a different sensor suite) to pick up the path where the first one depleted its budget.

