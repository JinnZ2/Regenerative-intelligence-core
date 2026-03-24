"""
Deterministic Mode — Enables reproducible simulations via RNG seeding.

Non-deterministic behavior makes debugging and testing difficult.
This module provides a simple way to seed Python's random module globally,
so that simulations produce identical results given the same seed.

Usage:
    from deterministic_mode import enable_deterministic_mode
    enable_deterministic_mode(42)  # All random calls now reproducible
"""

import random

_current_seed = None


def enable_deterministic_mode(seed=42):
    """
    Seed the global RNG for reproducible simulation runs.

    Args:
        seed: Integer seed value. Same seed produces same sequence.
    """
    global _current_seed
    _current_seed = seed
    random.seed(seed)


def disable_deterministic_mode():
    """Re-enable true randomness by unseeding the RNG."""
    global _current_seed
    _current_seed = None
    random.seed()


def get_current_seed():
    """Return the active seed, or None if in non-deterministic mode."""
    return _current_seed


def is_deterministic():
    """Check whether deterministic mode is active."""
    return _current_seed is not None
