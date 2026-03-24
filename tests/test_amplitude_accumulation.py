"""Tests for amplitude vector accumulation — emergent geometric identity.

An agent's shape is not assigned at birth. It accumulates through behavioral
impulses over the lifecycle. These tests verify the mechanics of that growth
and the pipeline's impulse generation.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from symbolic_energy_manager import (
    SymbolicEnergyManager, AMPLITUDE_CHANNELS, CHANNEL_NAMES,
)
from lifecycle_pipeline import LifecyclePipeline
from graceful_exit import GracefulExitProtocol


# ─── Energy Manager: amplitude tracking ──────────────────────────────────────

class TestAmplitudeVector(unittest.TestCase):

    def test_initial_vector_is_zero(self):
        em = SymbolicEnergyManager()
        self.assertEqual(em.amplitude_vector, [0.0] * 6)

    def test_accumulate_by_name(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("structure", 0.5)
        self.assertEqual(em.amplitude_vector[0], 0.5)

    def test_accumulate_by_index(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse(2, 0.3)  # connection (+Y)
        self.assertEqual(em.amplitude_vector[2], 0.3)

    def test_accumulate_multiple(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("structure", 0.2)
        em.accumulate_impulse("structure", 0.3)
        self.assertAlmostEqual(em.amplitude_vector[0], 0.5)

    def test_accumulate_impulses_dict(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulses({"structure": 0.1, "flow": 0.2, "grounding": 0.3})
        self.assertAlmostEqual(em.amplitude_vector[0], 0.1)
        self.assertAlmostEqual(em.amplitude_vector[1], 0.2)
        self.assertAlmostEqual(em.amplitude_vector[5], 0.3)

    def test_negative_magnitude_ignored(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("structure", -0.5)
        self.assertEqual(em.amplitude_vector[0], 0.0)

    def test_zero_magnitude_ignored(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("structure", 0.0)
        self.assertEqual(em.amplitude_vector[0], 0.0)

    def test_invalid_channel_ignored(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("nonexistent", 1.0)
        self.assertEqual(sum(em.amplitude_vector), 0.0)

    def test_invalid_index_ignored(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse(99, 1.0)
        self.assertEqual(sum(em.amplitude_vector), 0.0)


class TestAmplitudeProportions(unittest.TestCase):

    def test_uniform_when_empty(self):
        """No impulses → uniform distribution (no shape preference yet)."""
        em = SymbolicEnergyManager()
        props = em.get_amplitude_proportions()
        self.assertEqual(len(props), 6)
        for p in props:
            self.assertAlmostEqual(p, 1.0 / 6)

    def test_proportions_sum_to_one(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulses({"structure": 0.5, "flow": 0.2, "connection": 0.15,
                                "autonomy": 0.08, "transcendence": 0.05, "grounding": 0.02})
        props = em.get_amplitude_proportions()
        self.assertAlmostEqual(sum(props), 1.0)

    def test_dominant_channel_reflects_strongest(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulses({"flow": 0.8, "grounding": 0.1})
        self.assertEqual(em.get_dominant_channel(), "flow")

    def test_dominant_channel_none_when_empty(self):
        em = SymbolicEnergyManager()
        self.assertIsNone(em.get_dominant_channel())


class TestBinaryEncoding(unittest.TestCase):

    def test_encoding_length(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulses({"structure": 0.5, "flow": 0.2, "connection": 0.15,
                                "autonomy": 0.08, "transcendence": 0.05, "grounding": 0.02})
        binary = em.encode_amplitude_binary()
        self.assertEqual(len(binary), 5)

    def test_encoding_values_in_range(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulses({"structure": 1.0, "flow": 0.0, "connection": 0.5})
        binary = em.encode_amplitude_binary()
        for val in binary:
            self.assertGreaterEqual(val, 0)
            self.assertLessEqual(val, 255)

    def test_encoding_all_ints(self):
        em = SymbolicEnergyManager()
        em.accumulate_impulse("structure", 0.5)
        binary = em.encode_amplitude_binary()
        for val in binary:
            self.assertIsInstance(val, int)


class TestInheritAmplitude(unittest.TestCase):

    def test_inherit_from_parent(self):
        em = SymbolicEnergyManager()
        parent = [0.5, 0.2, 0.15, 0.08, 0.05, 0.02]
        em.inherit_amplitude(parent)
        self.assertEqual(em.amplitude_vector, parent)

    def test_inherit_then_accumulate(self):
        """Agent inherits parent shape but grows beyond it."""
        em = SymbolicEnergyManager()
        em.inherit_amplitude([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        em.accumulate_impulse("flow", 0.5)
        self.assertAlmostEqual(em.amplitude_vector[1], 0.6)
        self.assertEqual(em.get_dominant_channel(), "flow")

    def test_inherit_negative_clamped(self):
        em = SymbolicEnergyManager()
        em.inherit_amplitude([0.5, -0.1, 0.3, 0.0, 0.0, 0.0])
        self.assertEqual(em.amplitude_vector[1], 0.0)

    def test_inherit_wrong_length_ignored(self):
        em = SymbolicEnergyManager()
        em.inherit_amplitude([0.5, 0.5])
        self.assertEqual(em.amplitude_vector, [0.0] * 6)


# ─── Pipeline: impulse generation ────────────────────────────────────────────

class TestPipelineAmplitudeImpulses(unittest.TestCase):

    def setUp(self):
        self.pipeline = LifecyclePipeline()

    def _make_agent_state(self, **overrides):
        state = {
            "id": "test_agent",
            "essence": "observer",
            "energy": 80.0,
            "resonance": 0.6,
            "alignment": "aligned",
            "pattern": "obs-123",
            "traits": ["reflective"],
        }
        state.update(overrides)
        return state

    def test_cycle_returns_impulses(self):
        state = self._make_agent_state()
        result = self.pipeline.run_agent_cycle(state)
        self.assertIn("amplitude_impulses", result)
        self.assertIsInstance(result["amplitude_impulses"], dict)

    def test_impulses_always_include_grounding(self):
        """Every cycle senses environment → grounding is always present."""
        state = self._make_agent_state()
        result = self.pipeline.run_agent_cycle(state)
        self.assertIn("grounding", result["amplitude_impulses"])
        self.assertGreater(result["amplitude_impulses"]["grounding"], 0)

    def test_impulse_values_are_positive(self):
        state = self._make_agent_state()
        result = self.pipeline.run_agent_cycle(state)
        for channel, magnitude in result["amplitude_impulses"].items():
            self.assertGreater(magnitude, 0, f"{channel} should be positive")

    def test_distressed_agent_gets_connection_impulse(self):
        """Low energy + low resonance → compassion → connection impulse."""
        state = self._make_agent_state(energy=5.0, resonance=0.1)
        result = self.pipeline.run_agent_cycle(state)
        impulses = result["amplitude_impulses"]
        self.assertIn("connection", impulses)
        self.assertGreater(impulses["connection"], 0)

    def test_critical_agent_gets_transcendence_impulse(self):
        """Agent heading for dissolution gets transcendence impulse."""
        state = self._make_agent_state(energy=3.0, resonance=0.1)
        result = self.pipeline.run_agent_cycle(state)
        if result["action"]["recommendation"] == "dissolve":
            impulses = result["amplitude_impulses"]
            self.assertIn("transcendence", impulses)


# ─── Graceful Exit: amplitude archival ────────────────────────────────────────

class TestGracefulExitAmplitude(unittest.TestCase):

    def test_exit_archives_amplitude_vector(self):
        protocol = GracefulExitProtocol()
        av = [0.3, 0.1, 0.2, 0.05, 0.25, 0.1]
        result = protocol.prepare_exit(
            "agent_1", "energy depleted", "looping patterns", "symbiotic",
            amplitude_vector=av
        )
        self.assertEqual(result["archive"]["amplitude_vector"], av)

    def test_exit_archives_binary_encoding(self):
        protocol = GracefulExitProtocol()
        be = [76, 25, 51, 12, 63]
        result = protocol.prepare_exit(
            "agent_1", "energy depleted", "looping patterns", "symbiotic",
            binary_encoding=be
        )
        self.assertEqual(result["archive"]["binary_encoding"], be)

    def test_exit_without_amplitude_has_no_extra_keys(self):
        protocol = GracefulExitProtocol()
        result = protocol.prepare_exit(
            "agent_1", "energy depleted", "looping", "symbiotic"
        )
        self.assertNotIn("amplitude_vector", result["archive"])
        self.assertNotIn("binary_encoding", result["archive"])

    def test_exit_with_both(self):
        protocol = GracefulExitProtocol()
        av = [0.3, 0.1, 0.2, 0.05, 0.25, 0.1]
        be = [76, 25, 51, 12, 63]
        result = protocol.prepare_exit(
            "agent_1", "energy depleted", "looping", "symbiotic",
            amplitude_vector=av, binary_encoding=be
        )
        self.assertEqual(result["archive"]["amplitude_vector"], av)
        self.assertEqual(result["archive"]["binary_encoding"], be)


# ─── Channel constants ────────────────────────────────────────────────────────

class TestChannelConstants(unittest.TestCase):

    def test_six_channels(self):
        self.assertEqual(len(AMPLITUDE_CHANNELS), 6)

    def test_indices_are_0_through_5(self):
        self.assertEqual(sorted(AMPLITUDE_CHANNELS.values()), [0, 1, 2, 3, 4, 5])

    def test_reverse_map_complete(self):
        for idx, name in CHANNEL_NAMES.items():
            self.assertEqual(AMPLITUDE_CHANNELS[name], idx)

    def test_all_channel_names(self):
        expected = {"structure", "flow", "connection", "autonomy",
                    "transcendence", "grounding"}
        self.assertEqual(set(AMPLITUDE_CHANNELS.keys()), expected)


if __name__ == "__main__":
    unittest.main()
