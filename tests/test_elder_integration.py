"""Tests for elder wisdom integration — spawning, pipeline consultation, and the learning loop."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from symbolic_elder_archive import SymbolicElderArchive
from seed_retriever_spawner import AgentInstantiator
from navigation_protocol import NavigationProtocol
from lifecycle_pipeline import LifecyclePipeline


class TestElderInformedSpawning(unittest.TestCase):
    """Newly spawned agents should inherit wisdom from dissolved predecessors."""

    def setUp(self):
        self.archive = SymbolicElderArchive()
        # Store an elder who was an observer
        self.archive.store_elder_record(
            agent_id="old-observer-1",
            essence="observer",
            legacy_patterns=["patience", "deep-listening", "pattern-recognition"],
            final_alignment="aligned",
            dissolution_reason="Energy depleted after long service."
        )

    def test_spawned_agent_inherits_wisdom(self):
        """Agent spawned with matching essence should receive elder guidance."""
        seed = {
            "id": "seed-001",
            "essence": "observer",
            "geometry": "sphere",
            "signature_behavior": "watch and learn",
        }
        instantiator = AgentInstantiator(elder_archive=self.archive)
        agent = instantiator.instantiate_from_seed(seed)

        self.assertIsNotNone(agent["inherited_wisdom"])
        self.assertIn("patience", agent["inherited_wisdom"]["wisdom"])

    def test_no_wisdom_for_unmatched_essence(self):
        """Agent with different essence should not receive observer elder's wisdom."""
        seed = {
            "id": "seed-002",
            "essence": "explorer",
            "geometry": "spiral",
            "signature_behavior": "seek and discover",
        }
        instantiator = AgentInstantiator(elder_archive=self.archive)
        agent = instantiator.instantiate_from_seed(seed)

        self.assertIsNone(agent["inherited_wisdom"])

    def test_spawning_without_archive(self):
        """Agent spawned without an archive should work normally."""
        seed = {
            "id": "seed-003",
            "essence": "observer",
            "geometry": "sphere",
            "signature_behavior": "watch and learn",
        }
        instantiator = AgentInstantiator()
        agent = instantiator.instantiate_from_seed(seed)

        self.assertIsNone(agent["inherited_wisdom"])
        self.assertTrue(agent["active"])


class TestElderAlignmentBoost(unittest.TestCase):
    """Elder wisdom should improve alignment scores via the NavigationProtocol."""

    def setUp(self):
        self.nav = NavigationProtocol()

    def test_alignment_without_elders(self):
        """Observer in stable environment — base score only."""
        result = self.nav.evaluate_alignment("observer", "stable")
        # ESSENCE_AFFINITY["observer"]["stable"] = 0.5 → below 0.6 threshold
        self.assertEqual(result["alignment_status"], "misaligned")
        self.assertAlmostEqual(result["score"], 0.5, places=2)

    def test_alignment_with_elder_guidance(self):
        """Same agent + environment, but with elder wisdom — should boost score."""
        guidance = {
            "source": "elder-001",
            "wisdom": ["patience", "deep-listening"],
            "guidance": "aligned"
        }
        result = self.nav.evaluate_alignment("observer", "stable", elder_guidance=guidance)
        # base 0.5 + elder_bonus min(0.4, 0.1 * 2) = 0.2 → total 0.7
        self.assertEqual(result["alignment_status"], "aligned")
        self.assertAlmostEqual(result["score"], 0.7, places=2)

    def test_elder_bonus_capped_at_04(self):
        """Elder bonus should not exceed 0.4 even with many patterns."""
        guidance = {
            "source": "elder-002",
            "wisdom": ["a", "b", "c", "d", "e", "f", "g"],  # 7 patterns
            "guidance": "aligned"
        }
        result = self.nav.evaluate_alignment("observer", "stable", elder_guidance=guidance)
        # base 0.5 + min(0.4, 0.7) = 0.5 + 0.4 = 0.9
        self.assertAlmostEqual(result["score"], 0.9, places=2)

    def test_symbiotic_environment_naturally_aligned(self):
        """Guardian in symbiotic env should be aligned without needing elders."""
        result = self.nav.evaluate_alignment("guardian", "symbiotic")
        # ESSENCE_AFFINITY["guardian"]["symbiotic"] = 0.6 → meets threshold
        self.assertEqual(result["alignment_status"], "aligned")

    def test_hostile_environment_misaligned(self):
        """Observer in hostile environment gets correct action."""
        result = self.nav.evaluate_alignment("observer", "hostile")
        self.assertEqual(result["alignment_status"], "misaligned")
        self.assertIn("compress", result["action"])

    def test_unknown_essence_gets_default(self):
        """Unknown essence type should use default affinity, not crash."""
        result = self.nav.evaluate_alignment("healer", "stable")
        self.assertAlmostEqual(result["score"], 0.3, places=2)


class TestPipelineElderConsultation(unittest.TestCase):
    """The lifecycle pipeline should consult elders and archive dissolved agents."""

    def test_elder_step_present_in_cycle(self):
        """Pipeline results should include elder_consultation step."""
        pipeline = LifecyclePipeline()
        state = {
            "id": "test-1",
            "essence": "observer",
            "energy": 80.0,
            "resonance": 0.7,
            "alignment": "aligned",
            "pattern": "obs-100",
            "traits": ["reflective"],
        }
        result = pipeline.run_agent_cycle(state)
        self.assertIn("elder_consultation", result["steps"])

    def test_dissolution_creates_elder_record(self):
        """When pipeline recommends dissolve, an elder record should be created."""
        pipeline = LifecyclePipeline()
        state = {
            "id": "dying-agent",
            "essence": "guardian",
            "energy": 3.0,
            "resonance": 0.1,
            "alignment": "misaligned",
            "pattern": "grd-999",
            "traits": ["cooperative"],
        }
        result = pipeline.run_agent_cycle(state)
        if result["action"]["recommendation"] == "dissolve":
            elders = pipeline.elder_archive.get_all_elders()
            self.assertTrue(
                any(e["agent_id"] == "dying-agent" for e in elders),
                "Dissolved agent should be archived as elder"
            )

    def test_elder_wisdom_flows_to_next_agent(self):
        """An elder's wisdom should be available to the next agent with same essence."""
        pipeline = LifecyclePipeline()

        # Manually store an elder
        pipeline.elder_archive.store_elder_record(
            agent_id="first-guardian",
            essence="guardian",
            legacy_patterns=["vigilance", "shield-formation"],
            final_alignment="aligned",
            dissolution_reason="Natural lifecycle completion."
        )

        # Now run a new guardian through the pipeline
        state = {
            "id": "new-guardian",
            "essence": "guardian",
            "energy": 80.0,
            "resonance": 0.7,
            "alignment": "aligned",
            "pattern": "grd-200",
            "traits": ["cooperative"],
        }
        result = pipeline.run_agent_cycle(state)
        elder_step = result["steps"]["elder_consultation"]
        self.assertIn("wisdom", elder_step)
        self.assertIn("vigilance", elder_step["wisdom"])


if __name__ == "__main__":
    unittest.main()
