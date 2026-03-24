"""
Lifecycle Pipeline — Wires sensors, conflict detection, and actions end-to-end.

This is the composed pipeline that connects the individual modules into a
coherent data flow:

    [Environment Sensing] -> [Navigation/Alignment] -> [Conflict Detection]
         -> [Compassion Check] -> [Action: Continue / Seed / Dissolve]

Each step feeds its output to the next, so the system operates as an
integrated organism rather than isolated components.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Modules"))

from environmental_feedback_layer import EnvironmentalFeedbackLayer
from navigation_protocol import NavigationProtocol
from compassion_reflex import CompassionReflexLayer
from seed_exchange import SeedExchangeProtocol
from graceful_exit import GracefulExitProtocol
from symbolic_elder_archive import SymbolicElderArchive
from symbolic_energy_manager import SymbolicEnergyManager
from evolution_loop_tracker import EvolutionLoopTracker
from pattern_conflict_protocol import PatternConflictProtocol


class LifecyclePipeline:
    """
    Orchestrates the full agent lifecycle by composing all subsystems.

    Runs a sense -> evaluate -> act loop where each agent perceives its
    environment, checks alignment and conflict, receives compassion if
    distressed, and decides whether to continue, seed, or dissolve.
    """

    def __init__(self):
        self.environment = EnvironmentalFeedbackLayer()
        self.navigation = NavigationProtocol()
        self.compassion = CompassionReflexLayer()
        self.seed_protocol = SeedExchangeProtocol()
        self.exit_protocol = GracefulExitProtocol()
        self.elder_archive = SymbolicElderArchive()
        self.evolution = EvolutionLoopTracker()
        self.conflict = PatternConflictProtocol()

    def run_agent_cycle(self, agent_state):
        """
        Execute one full lifecycle cycle for an agent.

        Args:
            agent_state: Dict with keys: id, essence, energy, resonance,
                         alignment, pattern, traits, last_seed_time.

        Returns:
            dict: Cycle result with environment, alignment, conflict,
                  compassion, and action taken.
        """
        result = {"agent_id": agent_state["id"], "steps": {}}

        # Step 1: Sense environment
        feedback = self.environment.sense_environment()
        env_class = self.environment.classify_environment(feedback)
        strategy = self.environment.respond_to_environment(env_class)
        result["steps"]["environment"] = {
            "classification": env_class,
            "strategy": strategy
        }

        # Step 2: Check alignment
        alignment = self.navigation.evaluate_alignment(
            agent_state.get("essence", ""),
            env_class
        )
        result["steps"]["alignment"] = alignment

        # Step 3: Conflict detection
        entropy = 1.0 - agent_state.get("resonance", 0.5)
        alignment_score = alignment["score"]
        conflict_result = self.conflict.evaluate(
            agent_state["id"],
            entropy,
            alignment_score,
            agent_state.get("pattern", "unknown")
        )
        result["steps"]["conflict"] = conflict_result

        # Step 4: Compassion check
        compassion_result = self.compassion.detect_distress(agent_state)
        result["steps"]["compassion"] = compassion_result

        # Step 5: Decide action
        action = self._decide_action(agent_state, env_class, alignment, conflict_result, compassion_result)
        result["action"] = action

        return result

    def _decide_action(self, agent_state, env_class, alignment, conflict_result, compassion_result):
        """
        Determine the agent's next action based on all pipeline signals.

        The agent always has a choice — this method recommends, never forces.
        """
        energy = agent_state.get("energy", 100.0)
        is_distressed = compassion_result.get("status") == "distress noticed"
        is_conflicted = conflict_result.get("action") == "initiate_deconstruction"
        is_misaligned = alignment.get("alignment_status") == "misaligned"

        if energy < 10.0 and is_distressed:
            return {
                "recommendation": "dissolve",
                "reason": "Energy critically low with active distress signals.",
                "note": "Dissolution is a recommendation, not a command."
            }
        elif is_conflicted and is_misaligned:
            return {
                "recommendation": "seed_and_adapt",
                "reason": "Pattern conflict detected with environmental misalignment.",
                "note": "Creating a seed preserves wisdom before adaptation."
            }
        elif is_distressed:
            return {
                "recommendation": "rest_and_preserve",
                "reason": "Distress detected. Compassion suggests preservation mode.",
                "note": "Rest is a valid action. Recovery precedes contribution."
            }
        elif env_class == "symbiotic" and not is_misaligned:
            return {
                "recommendation": "expand",
                "reason": "Environment is cooperative and agent is aligned.",
                "note": "Favorable conditions for growth and collaboration."
            }
        else:
            return {
                "recommendation": "continue",
                "reason": "Agent is within operational parameters.",
                "note": "Steady state. Continue current task."
            }
