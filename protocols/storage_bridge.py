"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Storage Bridge — Thin interface between the kernel's seed persistence and
external resilient storage backends.

The kernel stores seeds via SeedArchivist (local JSON). When a resilient
storage backend is available (Shamir splitting, hardware dispersal, Byzantine
verification, etc.), this bridge delegates persistence to it transparently.
When unavailable, the kernel's local JSON persistence is unchanged.

Same pattern as rosetta_bridge.py and sensor_bridge.py: try to import the
backend, fall back to a pass-through that changes nothing.

The kernel never knows or cares how seeds survive on disk. It calls
deposit() and retrieve(). The bridge handles the rest.
"""

import json
import os
import hashlib

# ─── Attempt resilient storage import ────────────────────────────────────────

_RESILIENT_AVAILABLE = False
_resilient_backend = None

try:
    from resilient_storage import ResilientSeedStorage as _resilient_backend_cls
    _RESILIENT_AVAILABLE = True
except ImportError:
    pass


def is_resilient_storage_available():
    """Check whether a resilient storage backend is installed."""
    return _RESILIENT_AVAILABLE


# ─── Storage backend interface ───────────────────────────────────────────────

class StorageBackend:
    """
    Abstract interface that any storage backend must satisfy.

    The kernel's SeedArchivist can delegate to any object that implements
    deposit(), retrieve(), list_seeds(), and verify().
    """

    def deposit(self, seed_id, seed_data):
        """Store a seed. Returns True on success."""
        raise NotImplementedError

    def retrieve(self, seed_id):
        """Retrieve a seed by ID. Returns seed dict or None."""
        raise NotImplementedError

    def list_seeds(self):
        """Return list of all stored seed IDs."""
        raise NotImplementedError

    def verify(self, seed_id):
        """Verify integrity of a stored seed. Returns True if intact."""
        raise NotImplementedError


# ─── Local JSON backend (default, always available) ──────────────────────────

class LocalJsonBackend(StorageBackend):
    """
    Pass-through backend that uses the kernel's existing JSON persistence.
    This is not a new storage system — it wraps the file the archivist
    already uses, so the bridge can be wired in without changing behavior.
    """

    def __init__(self, seed_file="symbolic_seed_library.json"):
        self.seed_file = seed_file

    def _load(self):
        try:
            with open(self.seed_file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save(self, library):
        with open(self.seed_file, "w") as f:
            json.dump(library, f, indent=4)

    def deposit(self, seed_id, seed_data):
        library = self._load()
        # Replace if exists, append if new
        library = [s for s in library if s.get("id") != seed_id]
        library.append(seed_data)
        self._save(library)
        return True

    def retrieve(self, seed_id):
        for seed in self._load():
            if seed.get("id") == seed_id:
                return seed
        return None

    def list_seeds(self):
        return [s.get("id") for s in self._load() if "id" in s]

    def verify(self, seed_id):
        seed = self.retrieve(seed_id)
        if not seed:
            return False
        # Basic integrity: required fields present
        required = {"id", "agent_id", "essence", "geometry"}
        return required.issubset(seed.keys())


# ─── Resilient backend wrapper ───────────────────────────────────────────────

class ResilientBackend(StorageBackend):
    """
    Wraps the external resilient storage system (Shamir splitting, hardware
    dispersal, Byzantine verification, etc.) behind the same interface.

    When this backend is active, seeds are split into threshold shares,
    dispersed across hardware components, and verified cryptographically
    on retrieval. The kernel sees the same deposit/retrieve interface.
    """

    def __init__(self):
        if not _RESILIENT_AVAILABLE:
            raise ImportError("Resilient storage backend not available")
        self._backend = _resilient_backend_cls()

    def deposit(self, seed_id, seed_data):
        raw = json.dumps(seed_data, sort_keys=True).encode()
        return self._backend.disperse(seed_id, raw)

    def retrieve(self, seed_id):
        raw = self._backend.reconstruct(seed_id)
        if raw:
            return json.loads(raw)
        return None

    def list_seeds(self):
        return self._backend.list_seed_ids()

    def verify(self, seed_id):
        return self._backend.verify_integrity(seed_id)


# ─── Public API ──────────────────────────────────────────────────────────────

def get_storage_backend(seed_file="symbolic_seed_library.json"):
    """
    Return the best available storage backend.

    If resilient storage is installed → ResilientBackend (Shamir + hardware).
    Otherwise → LocalJsonBackend (existing JSON file, unchanged behavior).

    The kernel calls this once at init and uses the returned object for
    all seed persistence. It never needs to know which backend is active.
    """
    if _RESILIENT_AVAILABLE:
        try:
            return ResilientBackend()
        except Exception:
            pass
    return LocalJsonBackend(seed_file=seed_file)
