"""Tests for Modules/constraint_agent.py — ConstraintAgent lifecycle."""

import unittest
from fractions import Fraction

from Modules.constraint_agent import (
    AgentState,
    ConstraintAgent,
    GeometricMap,
    ResourceBudget,
)


class TestResourceBudget(unittest.TestCase):
    """ResourceBudget depletion logic."""

    def test_fresh_budget_not_depleted(self):
        budget = ResourceBudget(compute=100, energy=Fraction(1, 1),
                                time_remaining=Fraction(1, 1))
        self.assertFalse(budget.is_depleted())

    def test_zero_compute_depleted(self):
        budget = ResourceBudget(compute=0, energy=Fraction(1, 1),
                                time_remaining=Fraction(1, 1))
        self.assertTrue(budget.is_depleted())

    def test_zero_energy_depleted(self):
        budget = ResourceBudget(compute=100, energy=Fraction(0, 1),
                                time_remaining=Fraction(1, 1))
        self.assertTrue(budget.is_depleted())

    def test_zero_time_depleted(self):
        budget = ResourceBudget(compute=100, energy=Fraction(1, 1),
                                time_remaining=Fraction(0, 1))
        self.assertTrue(budget.is_depleted())


class TestGeometricMap(unittest.TestCase):
    """GeometricMap recording methods."""

    def test_record_resonance(self):
        gmap = GeometricMap()
        gmap.record_resonance("A", 0.75)
        self.assertEqual(gmap.resonances["A"], Fraction(3, 4))

    def test_record_relationship(self):
        gmap = GeometricMap()
        gmap.record_relationship("A", "B")
        self.assertIn("B", gmap.relationships["A"])

    def test_record_relationship_no_duplicates(self):
        gmap = GeometricMap()
        gmap.record_relationship("A", "B")
        gmap.record_relationship("A", "B")
        self.assertEqual(gmap.relationships["A"].count("B"), 1)

    def test_record_energy_flow(self):
        gmap = GeometricMap()
        gmap.record_energy_flow("A", "B", Fraction(1, 2))
        self.assertEqual(gmap.energy_flows[("A", "B")], Fraction(1, 2))


class TestConstraintAgentInit(unittest.TestCase):
    """Initial state of a freshly created agent."""

    def test_starts_compressed(self):
        agent = ConstraintAgent(seed_id="SHAPE.TETRA")
        self.assertEqual(agent.state, AgentState.COMPRESSED)

    def test_compression_ratio_starts_at_one(self):
        agent = ConstraintAgent(seed_id="SHAPE.TETRA")
        self.assertEqual(agent.compression_ratio, Fraction(1, 1))

    def test_default_home_families_empty(self):
        agent = ConstraintAgent(seed_id="SHAPE.TETRA")
        self.assertEqual(agent.home_families, [])

    def test_custom_home_families(self):
        agent = ConstraintAgent(seed_id="X", home_families=["a", "b"])
        self.assertEqual(agent.home_families, ["a", "b"])


class TestSetResourceBudget(unittest.TestCase):
    """set_resource_budget correctly populates budget fields."""

    def test_sets_compute(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=500)
        self.assertEqual(agent.budget.compute, 500)

    def test_sets_energy_as_fraction(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(energy=0.5)
        self.assertEqual(agent.budget.energy, Fraction(1, 2))


class TestShouldExpand(unittest.TestCase):
    """Bloom threshold gating."""

    def test_should_expand_with_full_resources(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        self.assertTrue(agent.should_expand())

    def test_should_not_expand_when_depleted(self):
        agent = ConstraintAgent(seed_id="X")
        # Default budget has compute=0
        self.assertFalse(agent.should_expand())

    def test_threshold_respected(self):
        agent = ConstraintAgent(seed_id="X", bloom_threshold=Fraction(3, 4))
        agent.set_resource_budget(compute=100, energy=0.5, time_remaining=1.0)
        # energy_ratio = 0.5/max(0.5,1) = 0.5 < 0.75 threshold
        self.assertFalse(agent.should_expand())


class TestBloom(unittest.TestCase):
    """Bloom expansion lifecycle."""

    def test_bloom_transitions_to_exploring(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        self.assertEqual(agent.state, AgentState.EXPLORING)

    def test_bloom_sets_compression_ratio_zero(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        self.assertEqual(agent.compression_ratio, Fraction(0, 1))

    def test_bloom_records_history(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=2)
        self.assertEqual(len(agent.expansion_history), 1)
        self.assertEqual(agent.expansion_history[0]["depth"], 2)

    def test_bloom_with_seed_map_restores_resonances(self):
        prior_map = GeometricMap()
        prior_map.record_resonance("N1", 0.8)
        prior_map.record_relationship("X", "N1")

        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        discovered = agent.bloom(depth=1, seed_map=prior_map)

        self.assertIn("N1", discovered)
        self.assertEqual(agent.map.resonances["N1"], Fraction(4, 5))


class TestExplore(unittest.TestCase):
    """Explore traversal."""

    def test_explore_returns_empty_when_compressed(self):
        agent = ConstraintAgent(seed_id="X")
        self.assertEqual(agent.explore(), {})

    def test_explore_records_energy_flows(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)

        # Manually populate map for testing
        agent.map.record_resonance("A", 0.5)
        agent.map.record_resonance("B", 0.5)
        agent.map.record_relationship("A", "B")

        summary = agent.explore()
        self.assertEqual(summary["energy_flows_recorded"], 1)
        self.assertIn(("A", "B"), agent.map.energy_flows)


class TestCompress(unittest.TestCase):
    """Compress back to seed."""

    def test_compress_returns_one(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        ratio = agent.compress()
        self.assertEqual(ratio, Fraction(1, 1))

    def test_compress_sets_state_compressed(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        agent.compress()
        self.assertEqual(agent.state, AgentState.COMPRESSED)

    def test_compress_resets_position_to_seed(self):
        agent = ConstraintAgent(seed_id="SEED")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        agent.compress()
        self.assertEqual(agent.current_position, "SEED")

    def test_compress_preserves_map(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(compute=100, energy=1.0, time_remaining=1.0)
        agent.bloom(depth=1)
        agent.map.record_resonance("Z", 0.9)
        agent.compress()
        self.assertIn("Z", agent.map.resonances)

    def test_compress_noop_when_already_compressed(self):
        agent = ConstraintAgent(seed_id="X")
        ratio = agent.compress()
        self.assertEqual(ratio, Fraction(1, 1))


class TestSelfValidate(unittest.TestCase):
    """Internal consistency checks."""

    def test_valid_when_empty(self):
        agent = ConstraintAgent(seed_id="X")
        report = agent.self_validate()
        self.assertTrue(report["is_valid"])

    def test_detects_resonance_out_of_range(self):
        agent = ConstraintAgent(seed_id="X")
        agent.map.resonances["BAD"] = Fraction(3, 2)  # 1.5, out of range
        report = agent.self_validate()
        self.assertFalse(report["is_valid"])
        self.assertTrue(any("BAD" in i for i in report["inconsistencies"]))

    def test_detects_energy_imbalance(self):
        agent = ConstraintAgent(seed_id="X")
        agent.map.energy_flows[("A", "B")] = Fraction(1, 1)
        # A sends 1 to B, but B sends nothing back — imbalance expected
        report = agent.self_validate()
        self.assertFalse(report["is_valid"])


class TestSerializeDeserialize(unittest.TestCase):
    """Round-trip serialization."""

    def test_round_trip(self):
        agent = ConstraintAgent(seed_id="SHAPE.TETRA", home_families=["stability"])
        agent.set_resource_budget(compute=1000, energy=0.75, time_remaining=0.5)
        agent.bloom(depth=1)
        agent.map.record_resonance("N1", 0.6)
        agent.map.record_relationship("SHAPE.TETRA", "N1")
        agent.map.record_energy_flow("SHAPE.TETRA", "N1", Fraction(1, 4))
        agent.explore()

        data = agent.serialize()
        restored = ConstraintAgent.deserialize(data)

        self.assertEqual(restored.seed_id, agent.seed_id)
        self.assertEqual(restored.home_families, agent.home_families)
        self.assertEqual(restored.state, agent.state)
        self.assertEqual(restored.compression_ratio, agent.compression_ratio)
        self.assertEqual(restored.budget.compute, agent.budget.compute)
        self.assertEqual(restored.budget.energy, agent.budget.energy)
        self.assertEqual(restored.map.resonances, agent.map.resonances)
        self.assertEqual(restored.map.relationships, agent.map.relationships)
        self.assertEqual(restored.map.energy_flows, agent.map.energy_flows)

    def test_serialized_fractions_are_tuples(self):
        agent = ConstraintAgent(seed_id="X")
        agent.set_resource_budget(energy=0.5)
        data = agent.serialize()
        self.assertIsInstance(data["budget"]["energy"], tuple)
        self.assertEqual(data["budget"]["energy"], (1, 2))


class TestDetectCorruption(unittest.TestCase):
    """Corruption detection (placeholder behavior)."""

    def test_returns_false_by_default(self):
        agent = ConstraintAgent(seed_id="X")
        self.assertFalse(agent.detect_corruption("anything"))


if __name__ == "__main__":
    unittest.main()
