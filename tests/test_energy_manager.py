"""Tests for SymbolicEnergyManager — energy drain, state transitions, and boundaries."""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "protocols"))

from symbolic_energy_manager import SymbolicEnergyManager


class TestSymbolicEnergyManager(unittest.TestCase):

    def test_initial_state(self):
        em = SymbolicEnergyManager()
        self.assertEqual(em.energy, 100.0)
        self.assertEqual(em.assess_energy_state(), "vital")

    def test_energy_drain(self):
        em = SymbolicEnergyManager()
        em.simulate_energy_drain(0.5)
        self.assertLess(em.energy, 100.0)
        self.assertEqual(len(em.drain_history), 1)

    def test_energy_never_negative(self):
        em = SymbolicEnergyManager(initial_energy=5.0)
        em.simulate_energy_drain(1.0)
        self.assertGreaterEqual(em.energy, 0.0)

    def test_state_transitions(self):
        em = SymbolicEnergyManager()
        em.energy = 75.0
        self.assertEqual(em.assess_energy_state(), "vital")
        em.energy = 50.0
        self.assertEqual(em.assess_energy_state(), "stable")
        em.energy = 25.0
        self.assertEqual(em.assess_energy_state(), "low")
        em.energy = 10.0
        self.assertEqual(em.assess_energy_state(), "critical")

    def test_restore_capped(self):
        em = SymbolicEnergyManager(initial_energy=100.0)
        em.energy = 50.0
        em.restore_energy(200.0)
        self.assertEqual(em.energy, 100.0)

    def test_energy_ratio(self):
        em = SymbolicEnergyManager(initial_energy=100.0)
        em.energy = 50.0
        self.assertAlmostEqual(em.get_energy_ratio(), 0.5)


if __name__ == "__main__":
    unittest.main()
