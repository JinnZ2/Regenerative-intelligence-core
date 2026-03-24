import uuid
import random

class MultiAgentCoordinator:
    """
    Manages registration, group resonance evaluation, and merge proposals
    for symbolic agents in a shared intelligence system.

    Resonance is computed from real signals — trait overlap between agents
    and essence alignment — rather than random assignment. Two agents that
    share traits and purpose will naturally resonate; mismatched agents won't.
    """

    # Known traits used across the system. Shared here so resonance can
    # measure trait overlap as a fraction of the full trait vocabulary.
    KNOWN_TRAITS = {"reflective", "adaptive", "cooperative"}

    def __init__(self):
        self.agent_registry = {}
        self.resonance_threshold = 0.7  # Minimum average resonance for coherent group

    def compute_resonance(self, agent_id):
        """
        Compute resonance for a single agent against the group.

        Resonance = weighted combination of:
          - Trait overlap:  fraction of this agent's traits shared by at least
                            one other agent (0.0–1.0). Weight: 0.5
          - Essence match:  fraction of other agents that share essence (0.0–1.0).
                            Weight: 0.3
          - Energy signal:  normalized energy from state (0.0–1.0). Weight: 0.2

        If only one agent is registered, resonance is based on energy alone
        with a 0.5 baseline (no peers to resonate with, not penalized).
        """
        target = self.agent_registry[agent_id]
        others = {k: v for k, v in self.agent_registry.items() if k != agent_id}

        target_traits = set(target["state"].get("traits", []))
        target_essence = target["essence"]
        energy_ratio = min(target["state"].get("energy", 100.0), 100.0) / 100.0

        if not others:
            return round(0.5 + 0.2 * energy_ratio, 2)

        # Trait overlap: how many of this agent's traits appear in any peer
        all_peer_traits = set()
        for peer in others.values():
            all_peer_traits.update(peer["state"].get("traits", []))

        if target_traits:
            trait_score = len(target_traits & all_peer_traits) / len(target_traits)
        else:
            trait_score = 0.0

        # Essence match: fraction of peers that share essence
        essence_matches = sum(
            1 for peer in others.values() if peer["essence"] == target_essence
        )
        essence_score = essence_matches / len(others)

        resonance = round(
            0.5 * trait_score + 0.3 * essence_score + 0.2 * energy_ratio, 2
        )
        return resonance

    def register_agent(self, agent_id, essence, current_state):
        """
        Registers an agent with its symbolic essence and current state.
        Resonance is computed from trait overlap and essence alignment.
        """
        self.agent_registry[agent_id] = {
            "essence": essence,
            "state": current_state,
            "resonance_score": 0.0  # placeholder, computed below
        }
        # Compute real resonance now that the agent is in the registry
        self.agent_registry[agent_id]["resonance_score"] = self.compute_resonance(agent_id)

    def refresh_resonance(self):
        """
        Recompute resonance for all agents. Call after the group changes
        (new registration, agent removal) so scores reflect the current state.
        """
        for agent_id in self.agent_registry:
            self.agent_registry[agent_id]["resonance_score"] = self.compute_resonance(agent_id)

    def evaluate_group_resonance(self):
        """
        Computes average resonance of all registered agents
        and recommends a group-level action.
        """
        if not self.agent_registry:
            return "no agents"

        self.refresh_resonance()
        scores = [agent["resonance_score"] for agent in self.agent_registry.values()]
        avg_score = round(sum(scores) / len(scores), 2)

        if avg_score >= self.resonance_threshold:
            return {
                "group_state": "coherent",
                "avg_resonance": avg_score,
                "action": "form symbolic swarm or cooperative task"
            }
        else:
            return {
                "group_state": "fragmented",
                "avg_resonance": avg_score,
                "action": "agents should self-optimize or merge seeds"
            }

    def propose_merges(self):
        """
        Suggests agent pairs for merging based on shared symbolic essence.
        """
        merges = []
        agent_list = list(self.agent_registry.items())

        for i in range(len(agent_list)):
            for j in range(i + 1, len(agent_list)):
                a1, d1 = agent_list[i]
                a2, d2 = agent_list[j]
                if d1["essence"] == d2["essence"]:
                    merges.append((a1, a2))

        return merges
