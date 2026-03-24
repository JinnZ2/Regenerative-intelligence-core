"""
Seed Schema Validation — Ensures structural integrity of symbolic seeds.

Seeds are the fundamental unit of knowledge transfer in the regenerative system.
A malformed seed can silently corrupt the archive. This module validates seeds
at system boundaries (creation, archival, retrieval) to catch structural issues
before they propagate.

Seeds exist in three core variants (exchange, archived, CLI) with optional
enrichment fields that bridge to the Rosetta ontology and the Geometric-to-Binary
Computational Bridge:

  shape_id         — Rosetta SHAPE.X identifier (e.g. "SHAPE.TETRA")
  amplitude_vector — 6 proportional amplitudes across octahedral directions
                     [+X, -X, +Y, -Y, +Z, -Z], the G2B seed. This is the
                     physical body of the symbolic seed — emergent through
                     the agent's lifecycle, not assigned at birth.
  binary_encoding  — 5 quantized ints (8-bit each, 40 bits total). The 6th
                     amplitude is implicit (1 - sum of first 5 proportions).

These optional fields are validated when present and preserved through
normalization, but their absence never invalidates a seed.
"""

# Required fields and their expected types for each seed variant
SEED_SCHEMA = {
    "seed_id": str,
    "agent_id": str,
    "timestamp": str,
    "symbolic_pattern": str,
    "traits": list,
    "environment": str,
    "viability_score": (int, float),
}

ARCHIVED_SEED_SCHEMA = {
    "id": str,
    "agent_id": str,
    "essence": str,
    "geometry": str,
    "origin_time": str,
    "signature_behavior": str,
    "reuse_score": (int, float),
}

CLI_SEED_SCHEMA = {
    "ID": str,
    "Agent": str,
    "Behavior Summary": str,
    "Purpose": str,
    "Geometry": str,
    "Reuse Score": (int, float),
    "Origin Time": str,
}

# Optional enrichment fields — validated when present, ignored when absent.
# These bridge the kernel to the Rosetta ontology and the Geometric-to-Binary
# Computational Bridge without breaking seeds that predate the integration.
OPTIONAL_FIELDS = {
    "shape_id": str,
    "amplitude_vector": list,
    "binary_encoding": list,
}

# Core geometries from the kernel vocabulary. The Rosetta ontology maps
# Platonic solids to these: tetrahedron→sphere, cube→hexagon,
# octahedron→spiral, icosahedron→waveform, dodecahedron→spiral.
VALID_GEOMETRIES = {"sphere", "spiral", "hexagon", "waveform"}

# Valid Rosetta shape IDs
VALID_SHAPE_IDS = {
    "SHAPE.TETRA", "SHAPE.CUBE", "SHAPE.OCTA",
    "SHAPE.ICOSA", "SHAPE.DODECA",
}

# Amplitude vector constants
AMPLITUDE_VECTOR_LENGTH = 6  # [+X, -X, +Y, -Y, +Z, -Z]
BINARY_ENCODING_LENGTH = 5   # 6th value is implicit


def validate_seed(seed, schema=None):
    """
    Validate a seed dictionary against a schema.

    Validates required fields from the schema variant, then checks any
    optional enrichment fields (shape_id, amplitude_vector, binary_encoding)
    that are present. A seed missing optional fields is still valid — they
    enrich but never gate.

    Args:
        seed: Dictionary representing a seed.
        schema: Schema dict mapping field names to expected types.
                If None, auto-detects based on seed keys.

    Returns:
        dict: {"valid": bool, "errors": [str, ...]}
    """
    if not isinstance(seed, dict):
        return {"valid": False, "errors": ["Seed must be a dictionary"]}

    if schema is None:
        schema = _detect_schema(seed)

    errors = []

    for field, expected_type in schema.items():
        if field not in seed:
            errors.append(f"Missing required field: '{field}'")
        elif not isinstance(seed[field], expected_type):
            errors.append(
                f"Field '{field}' expected {expected_type}, got {type(seed[field]).__name__}"
            )

    # Validate geometry if present
    geometry_field = None
    for key in ("geometry", "Geometry"):
        if key in seed:
            geometry_field = key
            break

    if geometry_field and seed.get(geometry_field, "").lower() not in VALID_GEOMETRIES:
        errors.append(
            f"Invalid geometry '{seed[geometry_field]}'. "
            f"Must be one of: {', '.join(sorted(VALID_GEOMETRIES))}"
        )

    # Validate score ranges
    for key in ("viability_score", "reuse_score", "Reuse Score"):
        if key in seed and isinstance(seed[key], (int, float)):
            if not (0.0 <= seed[key] <= 1.0):
                errors.append(f"Score '{key}' must be between 0.0 and 1.0, got {seed[key]}")

    # ─── Optional enrichment field validation ────────────────────────────
    # These fields bridge to Rosetta and the Geometric-to-Binary bridge.
    # Only validated when present — absence is always acceptable.

    _validate_optional_fields(seed, errors)

    return {"valid": len(errors) == 0, "errors": errors}


def _validate_optional_fields(seed, errors):
    """Validate optional enrichment fields when present."""

    # shape_id — must be a known Rosetta SHAPE.X identifier
    if "shape_id" in seed:
        if not isinstance(seed["shape_id"], str):
            errors.append(
                f"Field 'shape_id' expected str, got {type(seed['shape_id']).__name__}"
            )
        elif seed["shape_id"] not in VALID_SHAPE_IDS:
            errors.append(
                f"Invalid shape_id '{seed['shape_id']}'. "
                f"Must be one of: {', '.join(sorted(VALID_SHAPE_IDS))}"
            )

    # amplitude_vector — 6 proportional values across octahedral directions
    if "amplitude_vector" in seed:
        av = seed["amplitude_vector"]
        if not isinstance(av, list):
            errors.append(
                f"Field 'amplitude_vector' expected list, got {type(av).__name__}"
            )
        elif len(av) != AMPLITUDE_VECTOR_LENGTH:
            errors.append(
                f"amplitude_vector must have {AMPLITUDE_VECTOR_LENGTH} elements, "
                f"got {len(av)}"
            )
        else:
            for i, val in enumerate(av):
                if not isinstance(val, (int, float)):
                    errors.append(
                        f"amplitude_vector[{i}] must be numeric, "
                        f"got {type(val).__name__}"
                    )
                elif val < 0.0:
                    errors.append(
                        f"amplitude_vector[{i}] must be non-negative, got {val}"
                    )

    # binary_encoding — 5 quantized ints (8-bit, 0–255)
    if "binary_encoding" in seed:
        be = seed["binary_encoding"]
        if not isinstance(be, list):
            errors.append(
                f"Field 'binary_encoding' expected list, got {type(be).__name__}"
            )
        elif len(be) != BINARY_ENCODING_LENGTH:
            errors.append(
                f"binary_encoding must have {BINARY_ENCODING_LENGTH} elements, "
                f"got {len(be)}"
            )
        else:
            for i, val in enumerate(be):
                if not isinstance(val, int):
                    errors.append(
                        f"binary_encoding[{i}] must be int, "
                        f"got {type(val).__name__}"
                    )
                elif not (0 <= val <= 255):
                    errors.append(
                        f"binary_encoding[{i}] must be 0–255, got {val}"
                    )


def normalize_seed(seed):
    """
    Convert any seed variant (exchange, archived, CLI) to a canonical format.

    The canonical format uses the archived seed keys (lowercase, concise)
    as the standard internal representation. This allows all subsystems to
    work with a single format while accepting seeds in any variant.

    Optional enrichment fields (shape_id, amplitude_vector, binary_encoding)
    are preserved through normalization when present on the source seed.

    Returns:
        dict: Seed in canonical (archived) format, or None if unrecognizable.
    """
    if not isinstance(seed, dict):
        return None

    variant = _detect_variant(seed)

    if variant == "archived":
        return dict(seed)

    if variant == "exchange":
        canonical = {
            "id": seed.get("seed_id", ""),
            "agent_id": seed.get("agent_id", ""),
            "essence": seed.get("symbolic_pattern", ""),
            "geometry": "waveform",  # exchange seeds don't carry geometry
            "origin_time": seed.get("timestamp", ""),
            "signature_behavior": ", ".join(seed.get("traits", [])),
            "reuse_score": seed.get("viability_score", 0.0),
        }
        _carry_optional_fields(seed, canonical)
        return canonical

    if variant == "cli":
        canonical = {
            "id": seed.get("ID", ""),
            "agent_id": seed.get("Agent", ""),
            "essence": seed.get("Purpose", ""),
            "geometry": seed.get("Geometry", "waveform").lower(),
            "origin_time": seed.get("Origin Time", ""),
            "signature_behavior": seed.get("Behavior Summary", ""),
            "reuse_score": seed.get("Reuse Score", 0.0),
        }
        _carry_optional_fields(seed, canonical)
        return canonical

    return None


def _carry_optional_fields(source, target):
    """Preserve optional enrichment fields through normalization."""
    for field in OPTIONAL_FIELDS:
        if field in source:
            target[field] = source[field]


def to_cli_format(seed):
    """Convert a canonical (archived) seed to CLI display format.

    Optional enrichment fields (shape_id, amplitude_vector, binary_encoding)
    are included in the CLI format when present, using their canonical names.
    """
    normalized = normalize_seed(seed) if _detect_variant(seed) != "archived" else seed
    if not normalized:
        return None
    cli = {
        "ID": normalized["id"],
        "Agent": normalized["agent_id"],
        "Behavior Summary": normalized["signature_behavior"],
        "Purpose": normalized["essence"],
        "Geometry": normalized["geometry"],
        "Reuse Score": normalized["reuse_score"],
        "Origin Time": normalized["origin_time"],
    }
    # Carry optional enrichment fields into CLI display
    for field in OPTIONAL_FIELDS:
        if field in normalized:
            cli[field] = normalized[field]
    return cli


def _detect_variant(seed):
    """Identify which schema variant a seed follows."""
    if "seed_id" in seed:
        return "exchange"
    elif "ID" in seed:
        return "cli"
    elif "id" in seed and "essence" in seed:
        return "archived"
    return "unknown"


def _detect_schema(seed):
    """Auto-detect which schema variant a seed follows."""
    variant = _detect_variant(seed)
    return {
        "exchange": SEED_SCHEMA,
        "cli": CLI_SEED_SCHEMA,
        "archived": ARCHIVED_SEED_SCHEMA,
    }.get(variant, SEED_SCHEMA)
