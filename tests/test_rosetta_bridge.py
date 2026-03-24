"""Tests for the Rosetta Bridge — ontology integration and local fallback."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Modules"))

from rosetta_bridge import (
    get_seed, select_by_traits, resonance, seed_traits_vector,
    all_shape_ids, geometry_for_shape, traits_for_essence, is_rosetta_available,
)


class TestLocalFallbackOntology(unittest.TestCase):
    """Tests run against the local fallback (rosetta_shape_core not installed)."""

    def test_all_five_platonic_shapes_present(self):
        """Local ontology should contain all five Platonic solids."""
        ids = all_shape_ids()
        self.assertEqual(len(ids), 5)
        for expected in ["SHAPE.TETRA", "SHAPE.CUBE", "SHAPE.OCTA", "SHAPE.ICOSA", "SHAPE.DODECA"]:
            self.assertIn(expected, ids)

    def test_get_seed_returns_shape(self):
        seed = get_seed("SHAPE.TETRA")
        self.assertIsNotNone(seed)
        self.assertEqual(seed["shape_id"], "SHAPE.TETRA")
        self.assertEqual(seed["name"], "tetrahedron")
        self.assertIn("families", seed["traits"])
        self.assertIn("stability", seed["traits"]["families"])

    def test_get_seed_unknown(self):
        self.assertIsNone(get_seed("SHAPE.NONEXISTENT"))


class TestSelectByTraits(unittest.TestCase):

    def test_stability_selects_tetrahedron_first(self):
        results = select_by_traits(["stability", "foundation"])
        self.assertTrue(len(results) > 0)
        # Tetrahedron has both traits, should be first
        self.assertEqual(results[0]["shape_id"], "SHAPE.TETRA")

    def test_flow_selects_icosahedron(self):
        results = select_by_traits(["flow", "adaptation"])
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["shape_id"], "SHAPE.ICOSA")

    def test_no_matching_traits(self):
        results = select_by_traits(["nonexistent_trait"])
        self.assertEqual(results, [])

    def test_multiple_matches_sorted_by_overlap(self):
        results = select_by_traits(["stability"])
        # Tetrahedron has "stability", should appear
        shape_ids = [r["shape_id"] for r in results]
        self.assertIn("SHAPE.TETRA", shape_ids)


class TestResonance(unittest.TestCase):

    def test_identical_shapes_perfect_resonance(self):
        score = resonance("SHAPE.TETRA", "SHAPE.TETRA")
        self.assertAlmostEqual(score, 1.0, places=2)

    def test_different_shapes_lower_resonance(self):
        score = resonance("SHAPE.TETRA", "SHAPE.ICOSA")
        self.assertLess(score, 1.0)

    def test_no_overlap_zero_resonance(self):
        # Tetra families: stability, foundation, structure
        # Icosa families: flow, adaptation, empathy
        # No overlap → 0.0
        score = resonance("SHAPE.TETRA", "SHAPE.ICOSA")
        self.assertAlmostEqual(score, 0.0, places=2)

    def test_unknown_shape_zero(self):
        self.assertAlmostEqual(resonance("SHAPE.TETRA", "SHAPE.FAKE"), 0.0)

    def test_symmetry(self):
        """resonance(A, B) should equal resonance(B, A)."""
        self.assertEqual(
            resonance("SHAPE.TETRA", "SHAPE.CUBE"),
            resonance("SHAPE.CUBE", "SHAPE.TETRA")
        )


class TestTraitsVector(unittest.TestCase):

    def test_vector_length_matches_all_families(self):
        vector, labels = seed_traits_vector("SHAPE.TETRA")
        self.assertEqual(len(vector), len(labels))
        self.assertTrue(len(vector) > 0)

    def test_vector_has_ones_for_shape_families(self):
        vector, labels = seed_traits_vector("SHAPE.TETRA")
        for fam in ["stability", "foundation", "structure"]:
            idx = labels.index(fam)
            self.assertEqual(vector[idx], 1)

    def test_vector_has_zeros_for_other_families(self):
        vector, labels = seed_traits_vector("SHAPE.TETRA")
        for fam in ["flow", "adaptation", "empathy"]:
            idx = labels.index(fam)
            self.assertEqual(vector[idx], 0)

    def test_unknown_shape_empty(self):
        vector, labels = seed_traits_vector("SHAPE.FAKE")
        self.assertEqual(vector, [])
        self.assertEqual(labels, [])


class TestGeometryMapping(unittest.TestCase):

    def test_tetra_maps_to_sphere(self):
        self.assertEqual(geometry_for_shape("SHAPE.TETRA"), "sphere")

    def test_cube_maps_to_hexagon(self):
        self.assertEqual(geometry_for_shape("SHAPE.CUBE"), "hexagon")

    def test_icosa_maps_to_waveform(self):
        self.assertEqual(geometry_for_shape("SHAPE.ICOSA"), "waveform")

    def test_unknown_returns_none(self):
        self.assertIsNone(geometry_for_shape("SHAPE.FAKE"))


class TestEssenceToTraits(unittest.TestCase):

    def test_observer_traits(self):
        traits = traits_for_essence("observer")
        self.assertIn("balance", traits)
        self.assertIn("stability", traits)

    def test_explorer_traits(self):
        traits = traits_for_essence("explorer")
        self.assertIn("flow", traits)
        self.assertIn("adaptation", traits)

    def test_guardian_traits(self):
        traits = traits_for_essence("guardian")
        self.assertIn("stability", traits)
        self.assertIn("protection", traits)

    def test_unknown_essence_gets_default(self):
        traits = traits_for_essence("healer")
        self.assertEqual(traits, ["stability"])

    def test_case_insensitive(self):
        self.assertEqual(traits_for_essence("Observer"), traits_for_essence("observer"))


class TestShapeResonanceInCoordinator(unittest.TestCase):
    """Test that shape_id flows through to the coordinator's resonance computation."""

    def test_matching_shapes_boost_resonance(self):
        from multi_agent_coordination import MultiAgentCoordinator
        coord = MultiAgentCoordinator()
        coord.register_agent("A1", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.TETRA",
        })
        coord.register_agent("A2", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.TETRA",
        })
        coord.refresh_resonance()
        score = coord.agent_registry["A1"]["resonance_score"]
        # With matching shape (1.0 Jaccard) + matching traits + matching essence
        self.assertGreater(score, 0.8)

    def test_mismatched_shapes_lower_resonance(self):
        from multi_agent_coordination import MultiAgentCoordinator
        coord = MultiAgentCoordinator()
        coord.register_agent("A1", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.TETRA",
        })
        coord.register_agent("A2", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.ICOSA",
        })
        coord.refresh_resonance()
        score_mismatched = coord.agent_registry["A1"]["resonance_score"]

        coord2 = MultiAgentCoordinator()
        coord2.register_agent("A1", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.TETRA",
        })
        coord2.register_agent("A2", "guardian", {
            "traits": ["cooperative"],
            "energy": 80.0,
            "shape_id": "SHAPE.TETRA",
        })
        coord2.refresh_resonance()
        score_matched = coord2.agent_registry["A1"]["resonance_score"]

        self.assertGreater(score_matched, score_mismatched)


if __name__ == "__main__":
    unittest.main()
