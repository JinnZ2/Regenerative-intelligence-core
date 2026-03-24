"""Tests for seed enrichment fields — shape_id, amplitude_vector, binary_encoding.

These optional fields bridge the kernel to the Rosetta ontology and the
Geometric-to-Binary Computational Bridge. Seeds without them remain valid.
Seeds with them get full structural validation.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from seed_schema import (
    validate_seed, normalize_seed, to_cli_format,
    ARCHIVED_SEED_SCHEMA, VALID_SHAPE_IDS,
    AMPLITUDE_VECTOR_LENGTH, BINARY_ENCODING_LENGTH,
)


def _base_archived_seed(**overrides):
    """Helper: minimal valid archived seed with optional overrides."""
    seed = {
        "id": "test-001",
        "agent_id": "Agent_1",
        "essence": "observer",
        "geometry": "spiral",
        "origin_time": "2025-01-01T00:00:00",
        "signature_behavior": "looping",
        "reuse_score": 0.9,
    }
    seed.update(overrides)
    return seed


def _base_exchange_seed(**overrides):
    """Helper: minimal valid exchange seed with optional overrides."""
    seed = {
        "seed_id": "exc-001",
        "agent_id": "Agent_2",
        "timestamp": "2025-06-15T12:00:00",
        "symbolic_pattern": "guard-pattern",
        "traits": ["stability", "protection"],
        "environment": "Env-Zone-B",
        "viability_score": 0.75,
    }
    seed.update(overrides)
    return seed


# ─── shape_id validation ─────────────────────────────────────────────────────

class TestShapeIdValidation(unittest.TestCase):

    def test_valid_shape_id(self):
        for shape_id in VALID_SHAPE_IDS:
            seed = _base_archived_seed(shape_id=shape_id)
            result = validate_seed(seed)
            self.assertTrue(result["valid"], f"shape_id={shape_id} should be valid")

    def test_missing_shape_id_still_valid(self):
        """Seeds without shape_id remain valid — it's optional."""
        seed = _base_archived_seed()
        self.assertNotIn("shape_id", seed)
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_invalid_shape_id_string(self):
        seed = _base_archived_seed(shape_id="SHAPE.PYRAMID")
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("shape_id" in e for e in result["errors"]))

    def test_shape_id_wrong_type(self):
        seed = _base_archived_seed(shape_id=42)
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("shape_id" in e for e in result["errors"]))


# ─── amplitude_vector validation ──────────────────────────────────────────────

class TestAmplitudeVectorValidation(unittest.TestCase):

    def test_valid_amplitude_vector(self):
        seed = _base_archived_seed(
            amplitude_vector=[0.5, 0.2, 0.15, 0.08, 0.05, 0.02]
        )
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_amplitude_vector_all_zeros(self):
        """All zeros is valid — the agent hasn't accumulated direction yet."""
        seed = _base_archived_seed(
            amplitude_vector=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        )
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_amplitude_vector_wrong_length(self):
        seed = _base_archived_seed(amplitude_vector=[0.5, 0.2, 0.15])
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("6 elements" in e for e in result["errors"]))

    def test_amplitude_vector_negative_value(self):
        seed = _base_archived_seed(
            amplitude_vector=[0.5, -0.1, 0.15, 0.08, 0.05, 0.02]
        )
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("non-negative" in e for e in result["errors"]))

    def test_amplitude_vector_non_numeric(self):
        seed = _base_archived_seed(
            amplitude_vector=[0.5, "high", 0.15, 0.08, 0.05, 0.02]
        )
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("numeric" in e for e in result["errors"]))

    def test_amplitude_vector_wrong_type(self):
        seed = _base_archived_seed(amplitude_vector="not a list")
        result = validate_seed(seed)
        self.assertFalse(result["valid"])

    def test_missing_amplitude_vector_still_valid(self):
        seed = _base_archived_seed()
        result = validate_seed(seed)
        self.assertTrue(result["valid"])


# ─── binary_encoding validation ───────────────────────────────────────────────

class TestBinaryEncodingValidation(unittest.TestCase):

    def test_valid_binary_encoding(self):
        seed = _base_archived_seed(binary_encoding=[127, 51, 38, 20, 12])
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_binary_encoding_boundary_values(self):
        """0 and 255 are valid boundary values."""
        seed = _base_archived_seed(binary_encoding=[0, 255, 0, 255, 128])
        result = validate_seed(seed)
        self.assertTrue(result["valid"])

    def test_binary_encoding_wrong_length(self):
        seed = _base_archived_seed(binary_encoding=[127, 51, 38])
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("5 elements" in e for e in result["errors"]))

    def test_binary_encoding_out_of_range(self):
        seed = _base_archived_seed(binary_encoding=[127, 256, 38, 20, 12])
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("0–255" in e for e in result["errors"]))

    def test_binary_encoding_negative(self):
        seed = _base_archived_seed(binary_encoding=[-1, 51, 38, 20, 12])
        result = validate_seed(seed)
        self.assertFalse(result["valid"])

    def test_binary_encoding_float_rejected(self):
        """Binary encoding must be ints, not floats."""
        seed = _base_archived_seed(binary_encoding=[127.0, 51, 38, 20, 12])
        result = validate_seed(seed)
        self.assertFalse(result["valid"])
        self.assertTrue(any("int" in e for e in result["errors"]))

    def test_missing_binary_encoding_still_valid(self):
        seed = _base_archived_seed()
        result = validate_seed(seed)
        self.assertTrue(result["valid"])


# ─── Combined enrichment ─────────────────────────────────────────────────────

class TestCombinedEnrichment(unittest.TestCase):

    def test_fully_enriched_seed(self):
        """A seed with all three enrichment fields passes validation."""
        seed = _base_archived_seed(
            shape_id="SHAPE.OCTA",
            amplitude_vector=[0.3, 0.3, 0.15, 0.1, 0.1, 0.05],
            binary_encoding=[76, 76, 38, 25, 25],
        )
        result = validate_seed(seed)
        self.assertTrue(result["valid"], result["errors"])

    def test_enrichment_does_not_mask_required_field_errors(self):
        """Enrichment fields don't save a seed missing required fields."""
        seed = {
            "id": "test-001",
            # missing agent_id, essence, geometry, etc.
            "shape_id": "SHAPE.TETRA",
            "amplitude_vector": [0.5, 0.2, 0.15, 0.08, 0.05, 0.02],
        }
        result = validate_seed(seed, ARCHIVED_SEED_SCHEMA)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Missing" in e for e in result["errors"]))


# ─── Normalization preserves enrichment ───────────────────────────────────────

class TestNormalizationPreservesEnrichment(unittest.TestCase):

    def test_exchange_seed_carries_shape_id(self):
        seed = _base_exchange_seed(shape_id="SHAPE.TETRA")
        norm = normalize_seed(seed)
        self.assertEqual(norm["shape_id"], "SHAPE.TETRA")

    def test_exchange_seed_carries_amplitude_vector(self):
        av = [0.5, 0.2, 0.15, 0.08, 0.05, 0.02]
        seed = _base_exchange_seed(amplitude_vector=av)
        norm = normalize_seed(seed)
        self.assertEqual(norm["amplitude_vector"], av)

    def test_exchange_seed_carries_binary_encoding(self):
        be = [127, 51, 38, 20, 12]
        seed = _base_exchange_seed(binary_encoding=be)
        norm = normalize_seed(seed)
        self.assertEqual(norm["binary_encoding"], be)

    def test_cli_seed_carries_enrichment(self):
        seed = {
            "ID": "cli-1",
            "Agent": "agent_1",
            "Behavior Summary": "looped pattern",
            "Purpose": "observe",
            "Geometry": "sphere",
            "Reuse Score": 0.95,
            "Origin Time": "2025-01-01",
            "shape_id": "SHAPE.OCTA",
            "amplitude_vector": [0.3, 0.3, 0.15, 0.1, 0.1, 0.05],
        }
        norm = normalize_seed(seed)
        self.assertEqual(norm["shape_id"], "SHAPE.OCTA")
        self.assertEqual(len(norm["amplitude_vector"]), 6)

    def test_archived_seed_preserves_enrichment(self):
        seed = _base_archived_seed(
            shape_id="SHAPE.CUBE",
            binary_encoding=[100, 80, 60, 40, 20],
        )
        norm = normalize_seed(seed)
        self.assertEqual(norm["shape_id"], "SHAPE.CUBE")
        self.assertEqual(norm["binary_encoding"], [100, 80, 60, 40, 20])

    def test_normalization_without_enrichment_has_no_extra_keys(self):
        seed = _base_exchange_seed()
        norm = normalize_seed(seed)
        self.assertNotIn("shape_id", norm)
        self.assertNotIn("amplitude_vector", norm)
        self.assertNotIn("binary_encoding", norm)


# ─── CLI format preserves enrichment ──────────────────────────────────────────

class TestCliFormatPreservesEnrichment(unittest.TestCase):

    def test_to_cli_includes_shape_id(self):
        seed = _base_archived_seed(shape_id="SHAPE.ICOSA")
        cli = to_cli_format(seed)
        self.assertEqual(cli["shape_id"], "SHAPE.ICOSA")

    def test_to_cli_includes_amplitude_vector(self):
        av = [0.1, 0.1, 0.2, 0.2, 0.3, 0.1]
        seed = _base_archived_seed(amplitude_vector=av)
        cli = to_cli_format(seed)
        self.assertEqual(cli["amplitude_vector"], av)

    def test_to_cli_without_enrichment_has_no_extra_keys(self):
        seed = _base_archived_seed()
        cli = to_cli_format(seed)
        self.assertNotIn("shape_id", cli)
        self.assertNotIn("amplitude_vector", cli)


if __name__ == "__main__":
    unittest.main()
