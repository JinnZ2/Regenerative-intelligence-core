"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Rosetta Bridge — Connects the kernel to rosetta_shape_core when available.

This is the crossing point between the Regenerative Intelligence kernel and
the Rosetta Shape Core ontology. When rosetta_shape_core is installed, seeds
carry real geometric identity from the SHAPE.X ontology, resonance uses
Jaccard similarity over trait families, and geometry selection is driven by
symbolic traits rather than hardcoded strings.

When the package is unavailable (offline-first mode), the bridge provides
local fallbacks that preserve the same interface. No code outside this module
needs to know whether Rosetta is present — the bridge handles it.

Symbolic meaning: this module is the membrane between the kernel's internal
lifecycle logic and the broader ontological universe. It translates shape
identity into something the lifecycle pipeline can act on.
"""

# ─── Attempt Rosetta import ───────────────────────────────────────────────────

_ROSETTA_AVAILABLE = False
_rosetta_seeds = None

try:
    from rosetta_shape_core import seeds as _rosetta_seeds
    _ROSETTA_AVAILABLE = True
except ImportError:
    pass


def is_rosetta_available():
    """Check whether rosetta_shape_core is installed and importable."""
    return _ROSETTA_AVAILABLE


# ─── Local fallback data ──────────────────────────────────────────────────────
# Minimal shape ontology for offline operation. Mirrors the Rosetta schema
# closely enough that seeds created offline can be upgraded later.

_LOCAL_SHAPES = {
    "SHAPE.TETRA": {
        "shape_id": "SHAPE.TETRA",
        "name": "tetrahedron",
        "geometry": "sphere",  # maps to kernel geometry vocabulary
        "traits": {
            "families": ["stability", "foundation", "structure"],
            "element": "earth",
        },
    },
    "SHAPE.CUBE": {
        "shape_id": "SHAPE.CUBE",
        "name": "cube",
        "geometry": "hexagon",
        "traits": {
            "families": ["order", "containment", "protection"],
            "element": "earth",
        },
    },
    "SHAPE.OCTA": {
        "shape_id": "SHAPE.OCTA",
        "name": "octahedron",
        "geometry": "spiral",
        "traits": {
            "families": ["balance", "mediation", "air"],
            "element": "air",
        },
    },
    "SHAPE.ICOSA": {
        "shape_id": "SHAPE.ICOSA",
        "name": "icosahedron",
        "geometry": "waveform",
        "traits": {
            "families": ["flow", "adaptation", "empathy"],
            "element": "water",
        },
    },
    "SHAPE.DODECA": {
        "shape_id": "SHAPE.DODECA",
        "name": "dodecahedron",
        "geometry": "spiral",
        "traits": {
            "families": ["transcendence", "unity", "cosmos"],
            "element": "aether",
        },
    },
}

# All known trait families across the local ontology
_ALL_FAMILIES = sorted({
    fam
    for shape in _LOCAL_SHAPES.values()
    for fam in shape["traits"]["families"]
})

# ─── Polyhedral duality topology ─────────────────────────────────────────────
# Cube and octahedron are duals (connected). Dodecahedron and icosahedron are
# duals (connected). Tetrahedron is self-dual but bridges to cube (via shared
# "stability" trait ground) and to dodecahedron (via shared boundary/cosmos).
#
# Duality means the shapes share a deep structural relationship — vertices of
# one map to faces of the other. In the kernel, dual shapes get a resonance
# bonus because they are complementary, not identical.
_DUALITY_PAIRS = {
    frozenset({"SHAPE.CUBE", "SHAPE.OCTA"}),      # earth-air duality
    frozenset({"SHAPE.DODECA", "SHAPE.ICOSA"}),    # aether-water duality
    frozenset({"SHAPE.TETRA"}),                     # self-dual
}

# Bridge connections: tetra connects to cube (stability) and dodeca (boundary)
_BRIDGE_CONNECTIONS = {
    frozenset({"SHAPE.TETRA", "SHAPE.CUBE"}),
    frozenset({"SHAPE.TETRA", "SHAPE.DODECA"}),
}

# Resonance bonus for dual pairs (complementary resonance)
_DUALITY_BONUS = 0.15
# Smaller bonus for bridge connections (indirect resonance)
_BRIDGE_BONUS = 0.08


def _are_duals(shape_id_a, shape_id_b):
    """Check if two shapes are polyhedral duals."""
    return frozenset({shape_id_a, shape_id_b}) in _DUALITY_PAIRS


def _are_bridged(shape_id_a, shape_id_b):
    """Check if two shapes are connected via bridge topology."""
    return frozenset({shape_id_a, shape_id_b}) in _BRIDGE_CONNECTIONS


# ─── Essence-to-shape mapping ────────────────────────────────────────────────
# Direct mapping from kernel essences to their primary shape. This is the local
# fallback for rosetta_shape_core.seeds.select_by_essence().
_ESSENCE_SHAPE_MAP = {
    "observer": "SHAPE.OCTA",     # balance, mediation — the watcher at the center
    "explorer": "SHAPE.ICOSA",    # flow, adaptation — the shape of water
    "guardian": "SHAPE.TETRA",    # stability, foundation — the shape of fire/earth
    "builder": "SHAPE.CUBE",     # order, containment — the shape of structure
    "weaver": "SHAPE.DODECA",    # transcendence, unity — the shape of cosmos
}


# ─── Public API (matches rosetta_shape_core.seeds interface) ──────────────────

def get_seed(shape_id):
    """
    Get a shape seed by its ontology ID (e.g. "SHAPE.TETRA").

    Returns the Rosetta seed if available, otherwise falls back to the
    local minimal ontology.
    """
    if _ROSETTA_AVAILABLE:
        return _rosetta_seeds.get_seed(shape_id)
    return _LOCAL_SHAPES.get(shape_id)


def select_by_traits(trait_list):
    """
    Select shape seeds whose trait families overlap with the requested traits.

    Args:
        trait_list: List of trait family names (e.g. ["stability", "foundation"]).

    Returns:
        List of shape seeds, sorted by number of matching traits (best first).
    """
    if _ROSETTA_AVAILABLE:
        return _rosetta_seeds.select_by_traits(trait_list)

    requested = set(t.lower() for t in trait_list)
    scored = []
    for shape in _LOCAL_SHAPES.values():
        families = set(shape["traits"]["families"])
        overlap = len(families & requested)
        if overlap > 0:
            scored.append((overlap, shape))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [shape for _, shape in scored]


def select_by_essence(essence):
    """
    Select shape seeds that match a kernel essence directly.

    This is the clean path: essence → shape, no intermediate trait lookup.
    Replaces random.choice(["sphere", "spiral", "hexagon"]) with ontology-
    grounded selection.

    Args:
        essence: Kernel essence string (e.g. "observer", "guardian", "explorer").

    Returns:
        List of matching shape seeds (primary match first, then trait-based).
    """
    if _ROSETTA_AVAILABLE:
        try:
            return _rosetta_seeds.select_by_essence(essence)
        except AttributeError:
            # Rosetta version may not have select_by_essence yet; fall through
            pass

    essence_lower = essence.lower()
    results = []

    # Primary match: direct essence→shape mapping
    primary_id = _ESSENCE_SHAPE_MAP.get(essence_lower)
    if primary_id and primary_id in _LOCAL_SHAPES:
        results.append(_LOCAL_SHAPES[primary_id])

    # Secondary matches: trait-based overlap (excluding primary)
    trait_list = traits_for_essence(essence_lower)
    trait_matches = select_by_traits(trait_list)
    for shape in trait_matches:
        if shape["shape_id"] != primary_id:
            results.append(shape)

    return results


def resonance(shape_id_a, shape_id_b):
    """
    Compute resonance between two shapes based on trait families and topology.

    Resonance = Jaccard similarity on trait families + topology bonuses:
      - Identical shapes → 1.0
      - Polyhedral duals (cube↔octa, dodeca↔icosa) → Jaccard + 0.15
      - Bridge connections (tetra↔cube, tetra↔dodeca) → Jaccard + 0.08
      - No trait overlap, no topology → 0.0

    The duality bonus reflects complementary resonance — dual shapes share
    deep structural relationship (vertices↔faces) even when their trait
    families don't overlap.

    Args:
        shape_id_a: SHAPE.X ontology ID
        shape_id_b: SHAPE.X ontology ID

    Returns:
        float: Resonance score (0.0–1.0), or 0.0 if either shape is unknown.
    """
    if _ROSETTA_AVAILABLE:
        return _rosetta_seeds.resonance(shape_id_a, shape_id_b)

    shape_a = _LOCAL_SHAPES.get(shape_id_a)
    shape_b = _LOCAL_SHAPES.get(shape_id_b)

    if not shape_a or not shape_b:
        return 0.0

    families_a = set(shape_a["traits"]["families"])
    families_b = set(shape_b["traits"]["families"])

    union = families_a | families_b
    if not union:
        jaccard = 0.0
    else:
        jaccard = len(families_a & families_b) / len(union)

    # Topology bonuses — complementary resonance through polyhedral duality
    bonus = 0.0
    if _are_duals(shape_id_a, shape_id_b):
        bonus = _DUALITY_BONUS
    elif _are_bridged(shape_id_a, shape_id_b):
        bonus = _BRIDGE_BONUS

    return round(min(jaccard + bonus, 1.0), 4)


def seed_traits_vector(shape_id):
    """
    Return a binary vector over all known trait families for a shape.

    Useful for dot-product or cosine similarity computations in the kernel.

    Returns:
        tuple: (vector: list[int], family_labels: list[str])
               vector[i] = 1 if the shape has family_labels[i], else 0.
               Returns ([], []) if shape is unknown.
    """
    if _ROSETTA_AVAILABLE:
        return _rosetta_seeds.seed_traits_vector(shape_id)

    shape = _LOCAL_SHAPES.get(shape_id)
    if not shape:
        return ([], [])

    families = set(shape["traits"]["families"])
    vector = [1 if fam in families else 0 for fam in _ALL_FAMILIES]
    return (vector, list(_ALL_FAMILIES))


def all_shape_ids():
    """Return all known shape ontology IDs."""
    if _ROSETTA_AVAILABLE:
        # Rosetta may expose this differently; adapt when integrating
        try:
            return list(_rosetta_seeds.SEEDS.keys())
        except AttributeError:
            pass
    return list(_LOCAL_SHAPES.keys())


def geometry_for_shape(shape_id):
    """
    Map a SHAPE.X ID to the kernel's geometry vocabulary.

    The kernel uses: sphere, spiral, hexagon, waveform.
    The ontology uses Platonic solid names. This function bridges them.
    """
    seed = get_seed(shape_id)
    if not seed:
        return None
    # Rosetta seeds may use "geometry" directly or we extract from name
    return seed.get("geometry", "waveform")


def traits_for_essence(essence):
    """
    Map a kernel essence to trait families for shape selection.

    This bridges the kernel's essence vocabulary (observer, explorer, guardian)
    to the Rosetta trait vocabulary, enabling trait-based geometry grounding.
    """
    essence_trait_map = {
        "observer": ["balance", "mediation", "stability"],
        "explorer": ["flow", "adaptation", "transcendence"],
        "guardian": ["stability", "protection", "containment"],
    }
    return essence_trait_map.get(essence.lower(), ["stability"])
