"""Tests for sensor bridge — encoding physical domains to binary and analyzing convergence.

The sensor bridge translates raw physical-world data through five geometric
encoders (magnetic, light, sound, gravity, electric) into binary bitstrings,
then analyzes the convergence to produce environmental feedback the lifecycle
pipeline can act on.
"""

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from sensor_bridge import (
    encode_domain, encode_all_domains, analyze_convergence, sense_domains,
    compute_entropy, compute_phi_resonance, compute_cross_domain_coherence,
    DOMAINS,
)
from environmental_feedback_layer import EnvironmentalFeedbackLayer


# ─── Sample domain data fixtures ─────────────────────────────────────────────

MAGNETIC_DATA = {
    "field_lines": [
        {"curvature": 0.5, "direction": "N"},
        {"curvature": -0.3, "direction": "S"},
        {"curvature": 0.8, "direction": "N"},
    ],
    "resonance_map": [0.9, -0.2, 0.4],
}

LIGHT_DATA = {
    "polarization": ["H", "V", "V", "H"],
    "spectrum_nm": [450, 610, 520, 700],
    "interference_intensity": [0.9, 0.1, 0.6, 0.3],
    "photon_spin": ["L", "R", "R", "L"],
}

SOUND_DATA = {
    "phase_radians": [0.1, 3.2, 1.0, 0.3],
    "frequency_hz": [220, 880, 440, 660],
    "amplitude": [0.4, 0.8, 0.3, 0.9],
    "resonance_index": [0.9, 0.2, 0.75, 0.1],
}

GRAVITY_DATA = {
    "vectors": [[0, -9.8], [0, 9.8], [0, -3.5]],
    "curvature": [1.1, -0.6, 0.4],
    "orbital_stability": [0.8, 0.3, 0.9],
    "potential_energy": [-5e7, 1e6, -1e7],
}

ELECTRIC_DATA = {
    "charge": [1, -1, 1, -1],
    "current_A": [0.02, 0.0, 0.1, 0.0],
    "voltage_V": [1.2, 0.8, 3.3, 0.4],
    "conductivity_S": [5e-3, 0.0, 2e-2, 1e-5],
}

ALL_DOMAIN_DATA = {
    "magnetic": MAGNETIC_DATA,
    "light": LIGHT_DATA,
    "sound": SOUND_DATA,
    "gravity": GRAVITY_DATA,
    "electric": ELECTRIC_DATA,
}


# ─── Individual domain encoding ──────────────────────────────────────────────

class TestMagneticEncoding(unittest.TestCase):

    def test_produces_bitstring(self):
        bits = encode_domain("magnetic", MAGNETIC_DATA)
        self.assertIsInstance(bits, str)
        self.assertTrue(all(b in "01" for b in bits))

    def test_polarity_encoding(self):
        """N=1, S=0."""
        data = {"field_lines": [{"curvature": 0, "direction": "N"},
                                {"curvature": 0, "direction": "S"}]}
        bits = encode_domain("magnetic", data)
        self.assertTrue(bits.startswith("10"))

    def test_curvature_encoding(self):
        """Concave (+) = 1, convex (-) = 0."""
        data = {"field_lines": [{"curvature": 0.5, "direction": "N"},
                                {"curvature": -0.3, "direction": "N"}]}
        bits = encode_domain("magnetic", data)
        # First 2 bits: polarity (both N → 11)
        # Next 2 bits: curvature (0.5→1, -0.3→0)
        self.assertEqual(bits, "1110")

    def test_resonance_encoding(self):
        """Constructive (>0) = 1, destructive (<0) = 0."""
        data = {"resonance_map": [0.5, -0.2, 0.0]}
        bits = encode_domain("magnetic", data)
        self.assertEqual(bits, "100")

    def test_empty_data(self):
        bits = encode_domain("magnetic", {})
        self.assertEqual(bits, "")


class TestLightEncoding(unittest.TestCase):

    def test_produces_bitstring(self):
        bits = encode_domain("light", LIGHT_DATA)
        self.assertTrue(all(b in "01" for b in bits))

    def test_polarization(self):
        data = {"polarization": ["H", "V"]}
        bits = encode_domain("light", data)
        self.assertEqual(bits, "01")

    def test_spectrum_threshold(self):
        """λ < 550nm → 0, λ ≥ 550nm → 1."""
        data = {"spectrum_nm": [400, 550, 600]}
        bits = encode_domain("light", data)
        self.assertEqual(bits, "011")

    def test_interference(self):
        """Bright (≥0.5) = 1, dark (<0.5) = 0."""
        data = {"interference_intensity": [0.9, 0.1, 0.5]}
        bits = encode_domain("light", data)
        self.assertEqual(bits, "101")


class TestSoundEncoding(unittest.TestCase):

    def test_produces_bitstring(self):
        bits = encode_domain("sound", SOUND_DATA)
        self.assertTrue(all(b in "01" for b in bits))

    def test_phase_encoding(self):
        """In-phase (|φ| < π/2) = 1, out-of-phase = 0."""
        data = {"phase_radians": [0.1, 2.0, math.pi / 2 - 0.01]}
        bits = encode_domain("sound", data)
        self.assertEqual(bits, "101")

    def test_pitch_threshold(self):
        """≥ 440Hz = 1, < 440Hz = 0."""
        data = {"frequency_hz": [220, 440, 880]}
        bits = encode_domain("sound", data)
        self.assertEqual(bits, "011")


class TestGravityEncoding(unittest.TestCase):

    def test_produces_bitstring(self):
        bits = encode_domain("gravity", GRAVITY_DATA)
        self.assertTrue(all(b in "01" for b in bits))

    def test_direction_inward(self):
        """y < 0 → inward → 1."""
        data = {"vectors": [[0, -9.8], [0, 5.0]]}
        bits = encode_domain("gravity", data)
        self.assertEqual(bits, "10")

    def test_binding(self):
        """E < 0 → bound → 1."""
        data = {"potential_energy": [-1e7, 1e6, 0]}
        bits = encode_domain("gravity", data)
        self.assertEqual(bits, "100")


class TestElectricEncoding(unittest.TestCase):

    def test_produces_bitstring(self):
        bits = encode_domain("electric", ELECTRIC_DATA)
        self.assertTrue(all(b in "01" for b in bits))

    def test_charge_polarity(self):
        data = {"charge": [1, -1, 1]}
        bits = encode_domain("electric", data)
        self.assertEqual(bits, "101")

    def test_current_flow(self):
        data = {"current_A": [0.02, 0.0, 0.1]}
        bits = encode_domain("electric", data)
        self.assertEqual(bits, "101")


class TestUnknownDomain(unittest.TestCase):

    def test_unknown_returns_empty(self):
        bits = encode_domain("plasma", {"data": [1, 2, 3]})
        self.assertEqual(bits, "")


# ─── Multi-domain encoding ───────────────────────────────────────────────────

class TestEncodeAllDomains(unittest.TestCase):

    def test_all_five_domains(self):
        result = encode_all_domains(ALL_DOMAIN_DATA)
        self.assertEqual(len(result["domains_sensed"]), 5)
        self.assertTrue(len(result["convergence_vector"]) > 0)
        self.assertTrue(len(result["checksum"]) > 0)

    def test_partial_domains(self):
        result = encode_all_domains({"magnetic": MAGNETIC_DATA, "light": LIGHT_DATA})
        self.assertEqual(len(result["domains_sensed"]), 2)

    def test_convergence_is_concatenation(self):
        """Convergence vector = concatenation of domain bits in canonical order."""
        result = encode_all_domains({"magnetic": MAGNETIC_DATA, "light": LIGHT_DATA})
        expected = result["domain_bits"]["magnetic"] + result["domain_bits"]["light"]
        self.assertEqual(result["convergence_vector"], expected)

    def test_empty_input(self):
        result = encode_all_domains({})
        self.assertEqual(result["convergence_vector"], "")
        self.assertEqual(result["domains_sensed"], [])


# ─── Convergence analysis ────────────────────────────────────────────────────

class TestEntropy(unittest.TestCase):

    def test_all_zeros(self):
        self.assertEqual(compute_entropy("0000"), 0.0)

    def test_all_ones(self):
        self.assertEqual(compute_entropy("1111"), 0.0)

    def test_maximum_entropy(self):
        """Equal mix of 0s and 1s → entropy = 1.0."""
        self.assertAlmostEqual(compute_entropy("0101"), 1.0)

    def test_empty_string(self):
        self.assertEqual(compute_entropy(""), 0.0)

    def test_entropy_range(self):
        e = compute_entropy("11010010")
        self.assertGreaterEqual(e, 0.0)
        self.assertLessEqual(e, 1.0)


class TestPhiResonance(unittest.TestCase):

    def test_empty_string(self):
        self.assertEqual(compute_phi_resonance(""), 0.0)

    def test_short_string(self):
        self.assertEqual(compute_phi_resonance("01"), 0.0)

    def test_uniform_is_zero(self):
        """All same bits → no autocorrelation structure → 0."""
        self.assertEqual(compute_phi_resonance("00000000"), 0.0)

    def test_returns_float(self):
        result = compute_phi_resonance("10110101001011010100")
        self.assertIsInstance(result, float)


class TestCrossDomainCoherence(unittest.TestCase):

    def test_identical_bitstrings(self):
        coherence = compute_cross_domain_coherence({"a": "1010", "b": "1010"})
        self.assertAlmostEqual(coherence["mean_coherence"], 1.0)

    def test_opposite_bitstrings(self):
        coherence = compute_cross_domain_coherence({"a": "1010", "b": "0101"})
        self.assertAlmostEqual(coherence["mean_coherence"], 0.0)

    def test_partial_agreement(self):
        coherence = compute_cross_domain_coherence({"a": "1100", "b": "1010"})
        self.assertGreater(coherence["mean_coherence"], 0.0)
        self.assertLess(coherence["mean_coherence"], 1.0)

    def test_different_lengths(self):
        """Coherence should still work with different-length bitstrings."""
        coherence = compute_cross_domain_coherence({"a": "110011", "b": "1100"})
        self.assertIn(("a", "b"), coherence["pairs"])

    def test_single_domain_no_pairs(self):
        coherence = compute_cross_domain_coherence({"a": "1010"})
        self.assertAlmostEqual(coherence["mean_coherence"], 0.0)


# ─── Full analysis pipeline ──────────────────────────────────────────────────

class TestAnalyzeConvergence(unittest.TestCase):

    def test_produces_feedback_format(self):
        """Output must be compatible with EnvironmentalFeedbackLayer."""
        encoding = encode_all_domains(ALL_DOMAIN_DATA)
        feedback = analyze_convergence(encoding)
        # Required keys for classify_environment()
        self.assertIn("ambient_entropy", feedback)
        self.assertIn("peer_cooperation_index", feedback)
        self.assertIn("resource_signal_strength", feedback)
        self.assertIn("external_noise_level", feedback)

    def test_values_in_range(self):
        encoding = encode_all_domains(ALL_DOMAIN_DATA)
        feedback = analyze_convergence(encoding)
        for key in ("ambient_entropy", "peer_cooperation_index",
                     "resource_signal_strength", "external_noise_level"):
            self.assertGreaterEqual(feedback[key], 0.0, f"{key} below 0")
            self.assertLessEqual(feedback[key], 1.0, f"{key} above 1")

    def test_extended_fields_present(self):
        encoding = encode_all_domains(ALL_DOMAIN_DATA)
        feedback = analyze_convergence(encoding)
        self.assertEqual(feedback["source"], "sensor_bridge")
        self.assertIn("domains_sensed", feedback)
        self.assertIn("phi_resonance_raw", feedback)


class TestSenseDomains(unittest.TestCase):

    def test_end_to_end(self):
        """sense_domains() is the single-call pipeline: data in → feedback out."""
        feedback = sense_domains(ALL_DOMAIN_DATA)
        self.assertIn("ambient_entropy", feedback)
        self.assertEqual(feedback["source"], "sensor_bridge")
        self.assertEqual(len(feedback["domains_sensed"]), 5)


# ─── Integration with EnvironmentalFeedbackLayer ─────────────────────────────

class TestEnvironmentalFeedbackWithSensorBridge(unittest.TestCase):

    def test_sense_with_domain_data(self):
        """When domain_data is provided, use sensor bridge instead of random."""
        layer = EnvironmentalFeedbackLayer()
        feedback = layer.sense_environment(domain_data=ALL_DOMAIN_DATA)
        self.assertIsNotNone(feedback)
        self.assertEqual(feedback["source"], "sensor_bridge")

    def test_classify_sensor_bridge_output(self):
        """Sensor bridge output should be classifiable by existing classify_environment."""
        layer = EnvironmentalFeedbackLayer()
        feedback = layer.sense_environment(domain_data=ALL_DOMAIN_DATA)
        classification = layer.classify_environment(feedback)
        self.assertIn(classification, layer.status_tags)

    def test_respond_to_sensor_classification(self):
        """Full chain: sense → classify → respond, all using real domain data."""
        layer = EnvironmentalFeedbackLayer()
        feedback = layer.sense_environment(domain_data=ALL_DOMAIN_DATA)
        classification = layer.classify_environment(feedback)
        strategy = layer.respond_to_environment(classification)
        self.assertIn("status", strategy)
        self.assertIn("action", strategy)

    def test_fallback_without_domain_data(self):
        """Without domain_data, falls back to random simulation."""
        layer = EnvironmentalFeedbackLayer()
        feedback = layer.sense_environment()
        # May be None (10% failure) or dict without "source" key
        if feedback is not None:
            self.assertNotEqual(feedback.get("source"), "sensor_bridge")

    def test_none_on_bad_domain_data(self):
        """Malformed domain data should return None, not crash."""
        layer = EnvironmentalFeedbackLayer()
        # This should not raise
        feedback = layer.sense_environment(domain_data="not a dict")
        self.assertIsNone(feedback)


# ─── Domain constants ────────────────────────────────────────────────────────

class TestDomainConstants(unittest.TestCase):

    def test_five_domains(self):
        self.assertEqual(len(DOMAINS), 5)

    def test_domain_names(self):
        self.assertEqual(set(DOMAINS), {"magnetic", "light", "sound", "gravity", "electric"})


if __name__ == "__main__":
    unittest.main()
