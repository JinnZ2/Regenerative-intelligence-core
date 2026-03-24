"""Tests for real resonance — trait overlap, essence alignment, and energy signals."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))


from multi_agent_coordination import MultiAgentCoordinator


class TestResonanceComputation(unittest.TestCase):
    """Resonance should reflect real signals, not randomness."""

    def setUp(self):
        self.coordinator = MultiAgentCoordinator()

    def test_single_agent_gets_baseline_resonance(self):
        """One agent alone has no peers — gets 0.5 baseline + energy component."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 100.0,
        })
        score = self.coordinator.agent_registry["A1"]["resonance_score"]
        # 0.5 baseline + 0.2 * (100/100) = 0.7
        self.assertAlmostEqual(score, 0.7, places=2)

    def test_matching_traits_increase_resonance(self):
        """Agents sharing traits should have higher resonance than mismatched ones."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective", "cooperative"],
            "energy": 80.0,
        })
        self.coordinator.register_agent("A2", "observer", {
            "traits": ["reflective", "cooperative"],
            "energy": 80.0,
        })
        self.coordinator.refresh_resonance()
        score = self.coordinator.agent_registry["A1"]["resonance_score"]
        # trait_score = 2/2 = 1.0 → 0.5*1.0 = 0.5
        # essence_score = 1/1 = 1.0 → 0.3*1.0 = 0.3
        # energy = 0.8 → 0.2*0.8 = 0.16
        # total = 0.96
        self.assertGreater(score, 0.9)

    def test_mismatched_traits_lower_resonance(self):
        """Agents with no shared traits should have low resonance."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 80.0,
        })
        self.coordinator.register_agent("A2", "explorer", {
            "traits": ["adaptive"],
            "energy": 80.0,
        })
        self.coordinator.refresh_resonance()
        score_a1 = self.coordinator.agent_registry["A1"]["resonance_score"]
        # trait_score = 0/1 = 0.0, essence_score = 0/1 = 0.0, energy = 0.16
        self.assertAlmostEqual(score_a1, 0.16, places=2)

    def test_low_energy_reduces_resonance(self):
        """An agent with depleted energy should have lower resonance."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 100.0,
        })
        score_full = self.coordinator.agent_registry["A1"]["resonance_score"]

        coordinator2 = MultiAgentCoordinator()
        coordinator2.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 10.0,
        })
        score_low = coordinator2.agent_registry["A1"]["resonance_score"]
        self.assertGreater(score_full, score_low)

    def test_refresh_resonance_updates_all(self):
        """Adding a new agent and refreshing should change existing scores."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 80.0,
        })
        score_alone = self.coordinator.agent_registry["A1"]["resonance_score"]

        self.coordinator.register_agent("A2", "observer", {
            "traits": ["reflective"],
            "energy": 80.0,
        })
        self.coordinator.refresh_resonance()
        score_with_peer = self.coordinator.agent_registry["A1"]["resonance_score"]
        # Adding a matching peer should increase resonance
        self.assertGreater(score_with_peer, score_alone)

    def test_group_resonance_coherent(self):
        """A group of matching agents should be coherent."""
        for i in range(3):
            self.coordinator.register_agent(f"A{i}", "guardian", {
                "traits": ["cooperative"],
                "energy": 90.0,
            })
        result = self.coordinator.evaluate_group_resonance()
        self.assertEqual(result["group_state"], "coherent")

    def test_group_resonance_fragmented(self):
        """A group of totally mismatched agents should be fragmented."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": ["reflective"],
            "energy": 30.0,
        })
        self.coordinator.register_agent("A2", "explorer", {
            "traits": ["adaptive"],
            "energy": 30.0,
        })
        self.coordinator.register_agent("A3", "guardian", {
            "traits": ["cooperative"],
            "energy": 30.0,
        })
        result = self.coordinator.evaluate_group_resonance()
        self.assertEqual(result["group_state"], "fragmented")

    def test_empty_traits_handled(self):
        """Agent with no traits should not crash resonance computation."""
        self.coordinator.register_agent("A1", "observer", {
            "traits": [],
            "energy": 80.0,
        })
        self.coordinator.register_agent("A2", "observer", {
            "traits": ["reflective"],
            "energy": 80.0,
        })
        self.coordinator.refresh_resonance()
        # Should not raise; trait_score = 0 for empty traits
        score = self.coordinator.agent_registry["A1"]["resonance_score"]
        self.assertGreaterEqual(score, 0.0)


if __name__ == "__main__":
    unittest.main()
