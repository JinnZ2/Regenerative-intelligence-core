"""
Seed Schema Validation — Ensures structural integrity of symbolic seeds.

Seeds are the fundamental unit of knowledge transfer in the regenerative system.
A malformed seed can silently corrupt the archive. This module validates seeds
at system boundaries (creation, archival, retrieval) to catch structural issues
before they propagate.
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

VALID_GEOMETRIES = {"sphere", "spiral", "hexagon", "waveform"}


def validate_seed(seed, schema=None):
    """
    Validate a seed dictionary against a schema.

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

    return {"valid": len(errors) == 0, "errors": errors}


def _detect_schema(seed):
    """Auto-detect which schema variant a seed follows."""
    if "seed_id" in seed:
        return SEED_SCHEMA
    elif "ID" in seed:
        return CLI_SEED_SCHEMA
    elif "id" in seed and "essence" in seed:
        return ARCHIVED_SEED_SCHEMA
    else:
        return SEED_SCHEMA
