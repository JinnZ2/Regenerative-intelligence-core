"""
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


def resonance(shape_id_a, shape_id_b):
    """
    Compute Jaccard similarity between two shapes based on trait families.

    This replaces random.uniform() for resonance between agents that carry
    shape identity. Identical shapes → 1.0, no overlap → 0.0.

    Args:
        shape_id_a: SHAPE.X ontology ID
        shape_id_b: SHAPE.X ontology ID

    Returns:
        float: Jaccard similarity (0.0–1.0), or 0.0 if either shape is unknown.
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
        return 0.0

    return round(len(families_a & families_b) / len(union), 4)


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
