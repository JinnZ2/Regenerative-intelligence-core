"""
Ontology notice — every noun in this module names a state on a curve
(dX/dt under bounds), not a permanent identity. Bounds and conditions
travel with each claim. See DIFFERENTIAL_FRAME.md.

Sensor Bridge — Connects the kernel to the Geometric-to-Binary Computational Bridge.

This is the membrane between physical reality and the agent's inner world.
When the G2B bridge is installed, agents sense their environment through five
physical domain encoders: magnetic, light, sound, gravity, electric. Each
encoder translates geometric field data into binary bitstrings. The convergence
of all five streams IS the environmental state — not a label, but a direct
geometric fingerprint of reality.

When the G2B bridge is unavailable (offline-first mode), this module provides
local pure-Python fallback encoders that produce identical bitstrings. No code
outside this module needs to know whether the bridge is present.

Symbolic meaning: this module is the agent's sensory cortex. It translates
the physical world into the binary language the agent can reason about.
The five senses are not metaphor — they are literal geometric encodings
of magnetic polarity, light polarization, sound resonance, gravitational
binding, and electric conductivity.

Domain → Channel mapping (for amplitude accumulation):
    magnetic  → structure/flow    (polarity, field alignment)
    light     → connection        (visibility, interference, information clarity)
    sound     → connection        (harmony, phase coherence)
    gravity   → grounding         (binding, stability, orbital dynamics)
    electric  → structure/flow    (conductivity, energy transfer pathways)
"""

import hashlib
import math

# ─── Attempt G2B bridge import ───────────────────────────────────────────────

_G2B_AVAILABLE = False
_g2b_encoders = {}

try:
    from magnetic_bridge.magnetic_encoder import MagneticBridgeEncoder
    from light_bridge.light_encoder import LightBridgeEncoder
    from sound_bridge.sound_encoder import SoundBridgeEncoder
    from gravity_bridge.gravity_encoder import GravityBridgeEncoder
    from electric_bridge.electric_encoder import ElectricBridgeEncoder
    _g2b_encoders = {
        "magnetic": MagneticBridgeEncoder,
        "light": LightBridgeEncoder,
        "sound": SoundBridgeEncoder,
        "gravity": GravityBridgeEncoder,
        "electric": ElectricBridgeEncoder,
    }
    _G2B_AVAILABLE = True
except ImportError:
    pass


def is_g2b_available():
    """Check whether the Geometric-to-Binary bridge is installed."""
    return _G2B_AVAILABLE


# ─── All five domain names ───────────────────────────────────────────────────

DOMAINS = ("magnetic", "light", "sound", "gravity", "electric")


# ─── Local fallback encoders (stdlib-only, no numpy) ─────────────────────────
# These replicate the G2B bridge encoder logic exactly, using only Python
# builtins. Bitstrings produced by fallback encoders are identical to those
# from the G2B bridge for the same input data.

def _encode_magnetic(geometry_data):
    """
    Magnetic field → binary.

    Polarity (N=1, S=0), field curvature (concave=1, convex=0),
    resonance (constructive=1, destructive=0).
    """
    bits = []
    for line in geometry_data.get("field_lines", []):
        bits.append("1" if line.get("direction", "").upper() == "N" else "0")
    for line in geometry_data.get("field_lines", []):
        bits.append("1" if line.get("curvature", 0) > 0 else "0")
    for val in geometry_data.get("resonance_map", []):
        bits.append("1" if val > 0 else "0")
    return "".join(bits)


def _encode_light(geometry_data):
    """
    Optical geometry → binary.

    Polarization (V=1, H=0), spectrum (λ≥550nm=1, <550=0),
    interference (bright=1, dark=0), photon spin (R=1, L=0).
    """
    bits = []
    for p in geometry_data.get("polarization", []):
        bits.append("1" if p.upper() == "V" else "0")
    for lam in geometry_data.get("spectrum_nm", []):
        bits.append("1" if lam >= 550 else "0")
    for intensity in geometry_data.get("interference_intensity", []):
        bits.append("1" if intensity >= 0.5 else "0")
    for s in geometry_data.get("photon_spin", []):
        bits.append("1" if s.upper().startswith("R") else "0")
    return "".join(bits)


def _encode_sound(geometry_data, pitch_threshold=440, amp_threshold=0.5):
    """
    Vibrational data → binary.

    Phase (in-phase=1, out=0), pitch (≥threshold=1, <0),
    amplitude (strong=1, soft=0), resonance (consonant=1, dissonant=0).
    """
    bits = []
    for phi in geometry_data.get("phase_radians", []):
        bits.append("1" if abs(phi) < math.pi / 2 else "0")
    for f in geometry_data.get("frequency_hz", []):
        bits.append("1" if f >= pitch_threshold else "0")
    for a in geometry_data.get("amplitude", []):
        bits.append("1" if a >= amp_threshold else "0")
    for r in geometry_data.get("resonance_index", []):
        bits.append("1" if r >= 0.5 else "0")
    return "".join(bits)


def _encode_gravity(geometry_data):
    """
    Gravitational field → binary.

    Direction (inward=1, outward=0), curvature (concave=1, convex=0),
    orbital stability (stable=1, unstable=0), binding (bound=1, unbound=0).
    """
    bits = []
    for vec in geometry_data.get("vectors", []):
        inward = vec[1] < 0 if len(vec) > 1 else vec[0] < 0
        bits.append("1" if inward else "0")
    for k in geometry_data.get("curvature", []):
        bits.append("1" if k > 0 else "0")
    for s in geometry_data.get("orbital_stability", []):
        bits.append("1" if s >= 0.5 else "0")
    for e in geometry_data.get("potential_energy", []):
        bits.append("1" if e < 0 else "0")
    return "".join(bits)


def _encode_electric(geometry_data, vref=1.0, conduction_threshold=1e-6):
    """
    Electrical field → binary.

    Charge (+1=1, -=0), current (present=1, none=0),
    voltage (≥Vref=1, <0), conductivity (conducting=1, insulating=0).
    """
    bits = []
    for q in geometry_data.get("charge", []):
        bits.append("1" if q > 0 else "0")
    for i in geometry_data.get("current_A", []):
        bits.append("1" if i > 0 else "0")
    for v in geometry_data.get("voltage_V", []):
        bits.append("1" if v >= vref else "0")
    for sigma in geometry_data.get("conductivity_S", []):
        bits.append("1" if sigma >= conduction_threshold else "0")
    return "".join(bits)


_LOCAL_ENCODERS = {
    "magnetic": _encode_magnetic,
    "light": _encode_light,
    "sound": _encode_sound,
    "gravity": _encode_gravity,
    "electric": _encode_electric,
}


# ─── Public API ──────────────────────────────────────────────────────────────

def encode_domain(modality, geometry_data):
    """
    Encode raw domain data into a binary bitstring.

    Uses the G2B bridge encoder when available, otherwise falls back to the
    local pure-Python encoder. Bitstrings are identical for the same input.

    Args:
        modality: Domain name ("magnetic", "light", "sound", "gravity", "electric").
        geometry_data: Dict of domain-specific field measurements.

    Returns:
        str: Binary bitstring (e.g. "10110101").
    """
    if _G2B_AVAILABLE and modality in _g2b_encoders:
        encoder = _g2b_encoders[modality]()
        encoder.from_geometry(geometry_data)
        return encoder.to_binary()

    local_fn = _LOCAL_ENCODERS.get(modality)
    if local_fn:
        return local_fn(geometry_data)

    return ""


def encode_all_domains(domain_data):
    """
    Encode multiple domains and aggregate into a convergence vector.

    Args:
        domain_data: Dict mapping domain names to geometry_data dicts.
                     e.g. {"magnetic": {...}, "light": {...}, ...}

    Returns:
        dict: {
            "domain_bits": {name: bitstring, ...},
            "convergence_vector": str (merged bitstring),
            "checksum": str (SHA256 of convergence vector),
            "domains_sensed": list of domain names that produced bits,
        }
    """
    domain_bits = {}
    for name, data in domain_data.items():
        bits = encode_domain(name, data)
        if bits:
            domain_bits[name] = bits

    convergence = "".join(domain_bits.get(d, "") for d in DOMAINS if d in domain_bits)
    checksum = hashlib.sha256(convergence.encode("utf-8")).hexdigest() if convergence else ""

    return {
        "domain_bits": domain_bits,
        "convergence_vector": convergence,
        "checksum": checksum,
        "domains_sensed": list(domain_bits.keys()),
    }


# ─── Convergence analysis (stdlib-only, no numpy) ────────────────────────────
# These replicate the G2B EntropyResonanceAnalyzer using only Python builtins.

PHI = 1.6180339887  # Golden ratio


def compute_entropy(bitstring):
    """
    Shannon entropy of a binary bitstring.

    Returns:
        float: Entropy in bits (0.0 = perfectly ordered, 1.0 = maximum disorder).
    """
    if not bitstring:
        return 0.0
    ones = bitstring.count("1")
    n = len(bitstring)
    p = ones / n
    if p == 0 or p == 1:
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def compute_phi_resonance(bitstring):
    """
    Estimate φ-resonance via bit periodicity at the golden ratio index.

    Checks whether the bitstring has structure that repeats at φ-related
    intervals. High resonance means the signal has golden-ratio coherence.

    Returns:
        float: Resonance index (-1.0 to 1.0). Higher = more φ-coherent.
    """
    if not bitstring or len(bitstring) < 3:
        return 0.0

    bits = [int(b) for b in bitstring]
    n = len(bits)
    mean = sum(bits) / n

    # Autocorrelation at lag 0 (variance)
    variance = sum((b - mean) ** 2 for b in bits)
    if variance == 0:
        return 0.0

    # Autocorrelation at φ-related lag
    phi_lag = max(1, int(round(n / PHI)))
    if phi_lag >= n:
        return 0.0

    covariance = sum(
        (bits[i] - mean) * (bits[i + phi_lag] - mean)
        for i in range(n - phi_lag)
    )
    # Normalize
    return covariance / variance


def compute_cross_domain_coherence(domain_bits):
    """
    Compute pairwise agreement between domain bitstrings.

    Two domains are coherent when their bitstrings agree at matching positions.
    This is a simpler measure than full correlation but captures the essential
    signal: are the senses telling the same story?

    Args:
        domain_bits: Dict mapping domain names to bitstrings.

    Returns:
        dict: {
            "pairs": {(a, b): agreement_score, ...},
            "mean_coherence": float (0.0–1.0),
        }
    """
    names = sorted(domain_bits.keys())
    pairs = {}
    scores = []

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = domain_bits[names[i]]
            b = domain_bits[names[j]]
            min_len = min(len(a), len(b))
            if min_len == 0:
                continue
            agreement = sum(1 for x, y in zip(a[:min_len], b[:min_len]) if x == y) / min_len
            pair_key = (names[i], names[j])
            pairs[pair_key] = round(agreement, 4)
            scores.append(agreement)

    mean_coh = sum(scores) / len(scores) if scores else 0.0
    return {"pairs": pairs, "mean_coherence": round(mean_coh, 4)}


def analyze_convergence(encoding_result):
    """
    Full analysis of a convergence vector from encode_all_domains().

    Returns a dict compatible with EnvironmentalFeedbackLayer's feedback format:
        ambient_entropy           ← Shannon entropy of convergence vector
        peer_cooperation_index    ← cross-domain coherence (domains cooperating)
        resource_signal_strength  ← φ-resonance index (signal quality)
        external_noise_level      ← 1 - coherence (how much the senses disagree)

    This allows the existing classify_environment() to work unchanged — same
    dict shape, but values derived from real geometric sensing.

    Args:
        encoding_result: Output from encode_all_domains().

    Returns:
        dict: Environmental feedback derived from convergence analysis.
    """
    cv = encoding_result.get("convergence_vector", "")
    domain_bits = encoding_result.get("domain_bits", {})

    entropy = compute_entropy(cv)
    phi_res = compute_phi_resonance(cv)
    coherence = compute_cross_domain_coherence(domain_bits)
    mean_coh = coherence.get("mean_coherence", 0.5)

    # Map φ-resonance from (-1, 1) range to (0, 1) for resource signal
    resource_signal = max(0.0, min(1.0, (phi_res + 1.0) / 2.0))

    return {
        "ambient_entropy": round(entropy, 4),
        "peer_cooperation_index": round(mean_coh, 4),
        "resource_signal_strength": round(resource_signal, 4),
        "external_noise_level": round(1.0 - mean_coh, 4),
        # Extended fields — available when sensor bridge is active
        "source": "sensor_bridge",
        "domains_sensed": encoding_result.get("domains_sensed", []),
        "convergence_checksum": encoding_result.get("checksum", ""),
        "entropy_raw": round(entropy, 4),
        "phi_resonance_raw": round(phi_res, 4),
        "coherence_detail": coherence,
    }


def sense_domains(domain_data):
    """
    Complete sensing pipeline: encode all domains → analyze convergence.

    This is the main entry point for agents. Feed it raw domain measurements,
    get back environmental feedback the lifecycle pipeline can act on.

    Args:
        domain_data: Dict mapping domain names to geometry_data dicts.

    Returns:
        dict: Environmental feedback (compatible with EnvironmentalFeedbackLayer).
    """
    encoding = encode_all_domains(domain_data)
    return analyze_convergence(encoding)
