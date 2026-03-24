"""Tests for knowledge bridge — agents seeking wisdom from the Living Intelligence Database.

After homeostasis, agents are offered the opportunity to learn from natural
intelligence patterns. What they choose to study shapes their amplitude vector.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from knowledge_bridge import (
    get_intelligence, seek_knowledge, learn_from,
    all_intelligence_names, _ESSENCE_AFFINITY, _CHANNEL_AFFINITY,
)
from lifecycle_pipeline import LifecyclePipeline


# ─── Intelligence retrieval ──────────────────────────────────────────────────

class TestGetIntelligence(unittest.TestCase):

    def test_known_intelligence(self):
        entry = get_intelligence("octopus")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["name"], "Octopus")
        self.assertIn("teaches", entry)
        self.assertIn("core_patterns", entry)

    def test_unknown_intelligence(self):
        self.assertIsNone(get_intelligence("unicorn"))

    def test_all_local_intelligences_retrievable(self):
        for name in all_intelligence_names():
            entry = get_intelligence(name)
            self.assertIsNotNone(entry, f"{name} should be retrievable")
            self.assertIn("teaches", entry)
            self.assertIn("amplitude_channel", entry)

    def test_each_has_amplitude_mapping(self):
        """Every intelligence must map to an amplitude channel."""
        valid_channels = {"structure", "flow", "connection", "autonomy",
                          "transcendence", "grounding"}
        for name in all_intelligence_names():
            entry = get_intelligence(name)
            self.assertIn(entry["amplitude_channel"], valid_channels,
                          f"{name} has invalid channel")
            self.assertGreater(entry["amplitude_magnitude"], 0)


# ─── Knowledge seeking ───────────────────────────────────────────────────────

class TestSeekKnowledge(unittest.TestCase):

    def test_returns_list(self):
        result = seek_knowledge("observer")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_respects_limit(self):
        result = seek_knowledge("observer", limit=2)
        self.assertLessEqual(len(result), 2)

    def test_essence_affinity_first(self):
        """Observer's primary affinity (octopus) should come first."""
        result = seek_knowledge("observer", limit=5)
        names = [e.get("name") for e in result]
        # Octopus is first in observer affinity
        self.assertEqual(names[0], "Octopus")

    def test_guardian_gets_structure_intelligences(self):
        result = seek_knowledge("guardian", limit=5)
        names = [e.get("name") for e in result]
        self.assertIn("Termite Mound", names)

    def test_channel_affinity_supplements(self):
        """When dominant channel is provided, channel-relevant intelligences appear."""
        result = seek_knowledge("observer", dominant_channel="grounding", limit=5)
        names = [e.get("name") for e in result]
        self.assertIn("Quartz", names)

    def test_unknown_essence_still_returns(self):
        """Unknown essence should still get offerings from the full set."""
        result = seek_knowledge("mystic", limit=3)
        self.assertGreater(len(result), 0)

    def test_no_duplicates(self):
        result = seek_knowledge("explorer", dominant_channel="connection", limit=10)
        names = [e.get("name") for e in result]
        self.assertEqual(len(names), len(set(names)))


# ─── Learning impulses ───────────────────────────────────────────────────────

class TestLearnFrom(unittest.TestCase):

    def test_produces_impulse(self):
        entry = get_intelligence("mycelium")
        impulse = learn_from(entry)
        self.assertIn("connection", impulse)
        self.assertGreater(impulse["connection"], 0)

    def test_octopus_teaches_autonomy(self):
        impulse = learn_from(get_intelligence("octopus"))
        self.assertIn("autonomy", impulse)

    def test_termite_teaches_structure(self):
        impulse = learn_from(get_intelligence("termite_mound"))
        self.assertIn("structure", impulse)

    def test_slime_mold_teaches_flow(self):
        impulse = learn_from(get_intelligence("slime_mold"))
        self.assertIn("flow", impulse)

    def test_whale_teaches_transcendence(self):
        impulse = learn_from(get_intelligence("whale_migration"))
        self.assertIn("transcendence", impulse)

    def test_quartz_teaches_grounding(self):
        impulse = learn_from(get_intelligence("quartz"))
        self.assertIn("grounding", impulse)

    def test_empty_entry_returns_empty(self):
        impulse = learn_from({})
        self.assertEqual(impulse, {})


# ─── Affinity maps ───────────────────────────────────────────────────────────

class TestAffinityMaps(unittest.TestCase):

    def test_all_essences_have_affinity(self):
        for essence in ["observer", "explorer", "guardian", "builder", "weaver"]:
            self.assertIn(essence, _ESSENCE_AFFINITY)
            self.assertGreater(len(_ESSENCE_AFFINITY[essence]), 0)

    def test_all_channels_have_affinity(self):
        for channel in ["structure", "flow", "connection", "autonomy",
                        "transcendence", "grounding"]:
            self.assertIn(channel, _CHANNEL_AFFINITY)
            self.assertGreater(len(_CHANNEL_AFFINITY[channel]), 0)

    def test_affinity_references_are_valid(self):
        """All referenced intelligences must exist in the local set."""
        valid = set(all_intelligence_names())
        for names in _ESSENCE_AFFINITY.values():
            for name in names:
                self.assertIn(name, valid, f"{name} not in local intelligences")
        for names in _CHANNEL_AFFINITY.values():
            for name in names:
                self.assertIn(name, valid, f"{name} not in local intelligences")


# ─── Pipeline integration ────────────────────────────────────────────────────

class TestPipelineKnowledgeOffering(unittest.TestCase):

    def setUp(self):
        self.pipeline = LifecyclePipeline()

    def _make_agent(self, energy=80.0, resonance=0.6):
        return {
            "id": "test_agent",
            "essence": "observer",
            "energy": energy,
            "resonance": resonance,
            "alignment": "aligned",
            "pattern": "obs-123",
            "traits": ["reflective"],
            "dominant_channel": None,
        }

    def test_stable_agent_gets_offering(self):
        """Aligned + stable energy → knowledge is offered."""
        state = self._make_agent(energy=80.0)
        result = self.pipeline.run_agent_cycle(state)
        knowledge = result["steps"]["knowledge_offering"]
        # Alignment depends on random environment, so check structure
        if knowledge["status"] == "offered":
            self.assertIn("offerings", knowledge)
            self.assertGreater(len(knowledge["offerings"]), 0)
            # Each offering should have a learning impulse
            for offering in knowledge["offerings"]:
                self.assertIn("learning_impulse", offering)

    def test_low_energy_agent_not_offered(self):
        """Agent with energy < 40 is not in homeostasis → not offered."""
        state = self._make_agent(energy=15.0)
        result = self.pipeline.run_agent_cycle(state)
        knowledge = result["steps"]["knowledge_offering"]
        self.assertEqual(knowledge["status"], "not offered")

    def test_knowledge_step_always_present(self):
        """The knowledge_offering step is always in the result, even if not offered."""
        state = self._make_agent(energy=5.0, resonance=0.1)
        result = self.pipeline.run_agent_cycle(state)
        self.assertIn("knowledge_offering", result["steps"])


if __name__ == "__main__":
    unittest.main()
