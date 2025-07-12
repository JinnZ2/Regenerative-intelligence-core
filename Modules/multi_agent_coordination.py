import uuid
import random

class MultiAgentCoordinator:
    """
    Manages registration, group resonance evaluation, and merge proposals
    for symbolic agents in a shared intelligence system.
    """

    def __init__(self):
        self.agent_registry = {}
        self.resonance_threshold = 0.7  # Minimum average resonance for coherent group

    def register_agent(self, agent_id, essence, current_state):
        """
        Registers an agent with its symbolic essence and current state.
        Assigns a random resonance score.
        """
        self.agent_registry[agent_id] = {
            "essence": essence,
            "state": current_state,
            "resonance_score": round(random.uniform(0.0, 1.0), 2)
        }

    def evaluate_group_resonance(self):
        """
        Computes average resonance of all registered agents
        and recommends a group-level action.
        """
        if not self.agent_registry:
            return "no agents"
        
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
