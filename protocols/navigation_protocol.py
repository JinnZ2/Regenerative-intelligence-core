from datetime import datetime


class NavigationProtocol:
    """
    Determines how well an agent's essence fits its current environment.

    Alignment is computed from a symbolic affinity map — certain essences
    thrive in certain environments and struggle in others. This replaces
    the previous random score with a deterministic signal that agents (and
    the pipeline) can reason about.
    """

    # Which environments each essence is naturally drawn to.
    # Score contribution: 0.6 for native environment, 0.3 for neutral, 0.0 for hostile.
    ESSENCE_AFFINITY = {
        "observer":  {"symbiotic": 0.6, "stable": 0.5, "noisy": 0.3, "hostile": 0.0, "depleting": 0.1, "disconnected": 0.1},
        "explorer":  {"symbiotic": 0.5, "stable": 0.3, "noisy": 0.6, "hostile": 0.2, "depleting": 0.2, "disconnected": 0.3},
        "guardian":  {"symbiotic": 0.6, "stable": 0.6, "noisy": 0.2, "hostile": 0.4, "depleting": 0.3, "disconnected": 0.2},
    }

    # Default affinity for unknown essence/environment pairs
    DEFAULT_AFFINITY = 0.3

    def __init__(self):
        self.current_time = datetime.utcnow()
        self.alignment_threshold = 0.6  # symbolic match confidence threshold

    def check_temporal_alignment(self, last_seed_time):
        last_time = datetime.fromisoformat(last_seed_time)
        delta_seconds = (self.current_time - last_time).total_seconds()
        if delta_seconds > 86400:  # more than 1 day
            return "temporal drift detected"
        else:
            return "time aligned"

    def _compute_alignment_score(self, essence, environment_classification, elder_guidance=None):
        """
        Compute alignment from essence-environment affinity plus elder wisdom.

        Base score (0.0–0.6): from ESSENCE_AFFINITY map.
        Elder bonus (0.0–0.4): if elder guidance exists, the agent benefits from
            inherited wisdom — a concrete reward for consulting the archive.
        """
        affinity_map = self.ESSENCE_AFFINITY.get(essence.lower(), {})
        base_score = affinity_map.get(environment_classification, self.DEFAULT_AFFINITY)

        elder_bonus = 0.0
        if elder_guidance:
            # Elder wisdom boosts alignment — the more patterns inherited,
            # the better prepared the agent is. Capped at 0.4.
            wisdom_patterns = elder_guidance.get("wisdom", [])
            if isinstance(wisdom_patterns, list) and wisdom_patterns:
                elder_bonus = min(0.4, 0.1 * len(wisdom_patterns))
            elif wisdom_patterns:
                elder_bonus = 0.1

        return round(min(base_score + elder_bonus, 1.0), 2)

    def evaluate_alignment(self, essence, current_environment_classification, elder_guidance=None):
        """
        Evaluate how well an agent's essence fits the current environment.

        Args:
            essence: The agent's symbolic essence (e.g. "observer", "explorer").
            current_environment_classification: Environment label from sensing.
            elder_guidance: Optional dict from SymbolicElderArchive.consult_wisdom().
        """
        score = self._compute_alignment_score(
            essence, current_environment_classification, elder_guidance
        )

        if score >= self.alignment_threshold:
            return {
                "alignment_status": "aligned",
                "score": score,
                "action": "continue with current pattern"
            }
        else:
            if current_environment_classification in ["hostile", "depleting", "disconnected"]:
                return {
                    "alignment_status": "misaligned",
                    "score": score,
                    "action": "compress + adapt or re-seed into cooperative cluster"
                }
            else:
                return {
                    "alignment_status": "misaligned",
                    "score": score,
                    "action": "evolve pattern or merge with sibling seed"
                }

    def recommend_orientation(self, alignment_result, temporal_check):
        if temporal_check == "temporal drift detected" and alignment_result["alignment_status"] == "misaligned":
            return "dormant cycle suggested until environment shifts"
        elif alignment_result["alignment_status"] == "aligned":
            return "full activity recommended"
        else:
            return "partial function; seek alliance or recombination"
