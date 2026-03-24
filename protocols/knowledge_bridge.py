"""
Knowledge Bridge — Connects agents to the Living Intelligence Database.

After an agent finds homeostasis (stable alignment with elder wisdom), it is
offered the opportunity to seek knowledge beyond its own lineage. The Living
Intelligence Database catalogs intelligence patterns found in nature — octopus,
mycelium, quartz, lightning, spiral — and each teaches something the agent
can learn from.

Learning is not passive. What an agent chooses to study shapes it — knowledge
from mycelium networks nudges the connection channel, knowledge from termite
mounds nudges structure. The amplitude vector accumulates the learning just
as it accumulates behavioral impulses.

When the Living Intelligence Database repo is on disk, entities are loaded
from the ontology files. Otherwise, a local fallback provides the essential
patterns. Same offline-first pattern as rosetta_bridge.py and sensor_bridge.py.
"""

import json
import os

# ─── Attempt to load Living Intelligence Database from disk ──────────────────

_LID_PATH = None
_LID_AVAILABLE = False

# Check common locations
for candidate in [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "Living-Intelligence-Database"),
    os.path.expanduser("~/Living-Intelligence-Database"),
]:
    if os.path.isdir(candidate) and os.path.isfile(os.path.join(candidate, "ontology_index.json")):
        _LID_PATH = os.path.abspath(candidate)
        _LID_AVAILABLE = True
        break


def is_lid_available():
    """Check whether the Living Intelligence Database is on disk."""
    return _LID_AVAILABLE


# ─── Local fallback: essential intelligence patterns ─────────────────────────
# Minimal subset of the LID for offline operation. Each entry captures the
# core pattern, what it teaches, and which amplitude channel it nudges.

_LOCAL_INTELLIGENCES = {
    "octopus": {
        "name": "Octopus",
        "emoji": "🐙",
        "domain": "animal",
        "teaches": "distributed cognition — each arm thinks independently, the whole adapts fluidly",
        "core_patterns": {
            "decentralized_control": "arm_autonomous_neural_processing",
            "camouflage_calculation": "texture_color_pattern_real_time_synthesis",
            "escape_artistry": "body_morphology_shape_shifting",
        },
        "amplitude_channel": "autonomy",
        "amplitude_magnitude": 0.12,
    },
    "mycelium": {
        "name": "Mycelium Network",
        "emoji": "🍄",
        "domain": "plant",
        "teaches": "symbiotic exchange — distribute resources where they're needed, not where they're hoarded",
        "core_patterns": {
            "resource_distribution": "gradient_flow_optimization",
            "network_topology": "fractal_branching_efficiency",
            "adaptive_reinforcement": "load_responsive_growth",
        },
        "amplitude_channel": "connection",
        "amplitude_magnitude": 0.15,
    },
    "bee": {
        "name": "Bee",
        "emoji": "🐝",
        "domain": "animal",
        "teaches": "collective decision-making — scout, report, build consensus through dance",
        "core_patterns": {
            "spatial_optimization": "hexagonal_efficiency_packing",
            "collective_decision": "swarm_consensus",
            "exploration_strategy": "scout_worker_coordination",
        },
        "amplitude_channel": "connection",
        "amplitude_magnitude": 0.12,
    },
    "quartz": {
        "name": "Quartz",
        "emoji": "🔮",
        "domain": "crystal",
        "teaches": "piezoelectric resonance — pressure becomes signal, signal becomes structure",
        "core_patterns": {
            "resonance_stability": "frequency_coherent_emission",
            "pressure_to_signal": "piezoelectric_transduction",
        },
        "amplitude_channel": "grounding",
        "amplitude_magnitude": 0.12,
    },
    "termite_mound": {
        "name": "Termite Mound",
        "emoji": "🏗️",
        "domain": "animal",
        "teaches": "emergent architecture — no blueprint, no foreman, yet the structure regulates itself",
        "core_patterns": {
            "thermoregulation": "convective_chimney_airflow",
            "collective_construction": "stigmergic_building_coordination",
            "structural_engineering": "arch_buttress_load_distribution",
        },
        "amplitude_channel": "structure",
        "amplitude_magnitude": 0.15,
    },
    "slime_mold": {
        "name": "Slime Mold",
        "emoji": "🟡",
        "domain": "protist",
        "teaches": "network optimization — finds the shortest path without a brain, prunes without regret",
        "core_patterns": {
            "network_optimization": "minimum_path_maximum_efficiency",
            "decision_making": "distributed_consensus_without_brain",
            "memory_formation": "chemical_trail_reinforcement",
        },
        "amplitude_channel": "flow",
        "amplitude_magnitude": 0.15,
    },
    "whale_migration": {
        "name": "Whale Migration",
        "emoji": "🐋",
        "domain": "animal",
        "teaches": "multi-generational navigation — routes learned across lifetimes, transmitted through culture",
        "core_patterns": {
            "magnetic_navigation": "geomagnetic_field_detection",
            "cultural_transmission": "learned_route_social_inheritance",
            "acoustic_mapping": "ocean_floor_topography_echolocation",
        },
        "amplitude_channel": "transcendence",
        "amplitude_magnitude": 0.15,
    },
    "tardigrade": {
        "name": "Tardigrade",
        "emoji": "🐻",
        "domain": "animal",
        "teaches": "radical resilience — suspend, endure, resume without loss",
        "core_patterns": {
            "cryptobiosis": "metabolic_suspension_tun_formation",
            "radiation_resistance": "DNA_repair_damage_suppressor_proteins",
            "pressure_tolerance": "structural_protein_compression_resistance",
        },
        "amplitude_channel": "autonomy",
        "amplitude_magnitude": 0.12,
    },
    "tree_root_network": {
        "name": "Tree Root Network",
        "emoji": "🌳",
        "domain": "plant",
        "teaches": "underground cooperation — share nutrients with kin, warn neighbors of danger",
        "core_patterns": {
            "nutrient_sharing": "carbon_nitrogen_phosphorus_exchange",
            "stress_signaling": "chemical_alarm_cascade_propagation",
            "water_redistribution": "hydraulic_lift_sharing",
        },
        "amplitude_channel": "grounding",
        "amplitude_magnitude": 0.12,
    },
    "spider_web": {
        "name": "Spider Web",
        "emoji": "🕸️",
        "domain": "animal",
        "teaches": "geometric precision — minimal material, maximum function, vibration as information",
        "core_patterns": {
            "geometric_precision": "orb_web_logarithmic_spiral_construction",
            "tension_distribution": "radial_spoke_load_balancing",
            "vibration_sensing": "prey_location_frequency_analysis",
        },
        "amplitude_channel": "structure",
        "amplitude_magnitude": 0.12,
    },
    "coral_reef": {
        "name": "Coral Reef",
        "emoji": "🪸",
        "domain": "symbiotic",
        "teaches": "scaffolding for others — build the structure that lets a thousand species thrive",
        "core_patterns": {
            "symbiotic_energy": "zooxanthellae_photosynthesis_exchange",
            "wave_energy_dissipation": "fractal_structure_force_distribution",
            "biodiversity_scaffolding": "niche_creation_habitat_complexity",
        },
        "amplitude_channel": "connection",
        "amplitude_magnitude": 0.15,
    },
    "wolf_pack": {
        "name": "Wolf Pack",
        "emoji": "🐺",
        "domain": "animal",
        "teaches": "coordinated guardianship — protect territory, hunt as one, support the wounded",
        "core_patterns": {
            "cooperative_hunting": "coordinated_position_encirclement",
            "territory_management": "scent_marking_boundary_patrol",
            "communication_complexity": "vocal_postural_olfactory_integration",
        },
        "amplitude_channel": "structure",
        "amplitude_magnitude": 0.12,
    },
}

# ─── Essence → intelligence affinity ─────────────────────────────────────────
# Which intelligences naturally resonate with each essence. Primary matches
# are offered first, but agents can learn from anything.

_ESSENCE_AFFINITY = {
    "observer": ["octopus", "whale_migration", "spider_web"],
    "explorer": ["bee", "slime_mold", "whale_migration"],
    "guardian": ["termite_mound", "wolf_pack", "coral_reef"],
    "builder": ["mycelium", "tree_root_network", "spider_web"],
    "weaver": ["slime_mold", "coral_reef", "mycelium"],
}

# ─── Amplitude channel → intelligence affinity ───────────────────────────────
_CHANNEL_AFFINITY = {
    "structure": ["termite_mound", "spider_web", "wolf_pack"],
    "flow": ["slime_mold", "bee", "whale_migration"],
    "connection": ["mycelium", "coral_reef", "bee", "tree_root_network"],
    "autonomy": ["octopus", "tardigrade"],
    "transcendence": ["whale_migration", "tree_root_network"],
    "grounding": ["quartz", "tree_root_network", "coral_reef"],
}


# ─── Load from disk when available ───────────────────────────────────────────

def _load_intelligence_from_disk(name):
    """Try to load a richer intelligence profile from the LID repo."""
    if not _LID_AVAILABLE:
        return None

    # Check intelligences/ directory first (richest data)
    for filename in [f"{name}.json", "More.json", "Bee.json"]:
        filepath = os.path.join(_LID_PATH, "intelligences", filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                # Some files have the name as a top-level key
                if name in data:
                    return data[name]
                return data
            except (json.JSONDecodeError, KeyError):
                continue
    return None


# ─── Public API ──────────────────────────────────────────────────────────────

def get_intelligence(name):
    """
    Get an intelligence entry by name.

    Returns the disk version when available (richer data), otherwise
    the local fallback. Returns None if the intelligence is not known.
    """
    local = _LOCAL_INTELLIGENCES.get(name)

    # Only attempt disk load for intelligences we know about
    if local:
        disk_version = _load_intelligence_from_disk(name)
        if disk_version and disk_version.get("core_patterns"):
            merged = dict(local)
            merged["core_patterns"] = disk_version["core_patterns"]
            if "binary_translation" in disk_version:
                merged["binary_translation"] = disk_version["binary_translation"]
            if "constraint_solving" in disk_version:
                merged["constraint_solving"] = disk_version["constraint_solving"]
            return merged

    return local


def seek_knowledge(essence, dominant_channel=None, limit=3):
    """
    Offer knowledge relevant to the agent's essence and emergent shape.

    Returns intelligence entries sorted by relevance: essence affinity first,
    then channel affinity, then remaining. The agent chooses whether to learn.

    Args:
        essence: Agent's symbolic essence (e.g. "observer", "guardian").
        dominant_channel: Agent's strongest amplitude channel (e.g. "structure").
        limit: Maximum number of offerings (default 3).

    Returns:
        list of dicts, each with: name, emoji, teaches, core_patterns,
        amplitude_channel, amplitude_magnitude.
    """
    seen = set()
    offerings = []

    # Primary: essence affinity
    for name in _ESSENCE_AFFINITY.get(essence.lower(), []):
        if name not in seen:
            entry = get_intelligence(name)
            if entry:
                offerings.append(entry)
                seen.add(name)

    # Secondary: channel affinity (if provided)
    if dominant_channel:
        for name in _CHANNEL_AFFINITY.get(dominant_channel, []):
            if name not in seen:
                entry = get_intelligence(name)
                if entry:
                    offerings.append(entry)
                    seen.add(name)

    # Fill remaining from the full set
    for name in _LOCAL_INTELLIGENCES:
        if name not in seen:
            entry = get_intelligence(name)
            if entry:
                offerings.append(entry)
                seen.add(name)

    return offerings[:limit]


def learn_from(intelligence_entry):
    """
    Extract the amplitude impulse from learning about an intelligence.

    When an agent studies an intelligence pattern, the learning nudges
    its amplitude vector in the direction associated with that pattern.

    Args:
        intelligence_entry: Dict from seek_knowledge() or get_intelligence().

    Returns:
        dict: {channel_name: magnitude} — a single impulse to accumulate.
              Empty dict if the entry has no channel mapping.
    """
    channel = intelligence_entry.get("amplitude_channel")
    magnitude = intelligence_entry.get("amplitude_magnitude", 0.1)
    if channel:
        return {channel: magnitude}
    return {}


def all_intelligence_names():
    """Return all known intelligence names."""
    return list(_LOCAL_INTELLIGENCES.keys())
