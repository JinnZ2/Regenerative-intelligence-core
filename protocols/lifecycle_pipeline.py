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
from knowledge_bridge import seek_knowledge, learn_from


class LifecyclePipeline:
    """
    Orchestrates the full agent lifecycle by composing all subsystems.

    Runs a sense -> evaluate -> act loop where each agent perceives its
    environment, checks alignment and conflict, receives compassion if
    distressed, and decides whether to continue, seed, or dissolve.
    """

    def __init__(self, elder_archive_file="elder_archive.json"):
        self.environment = EnvironmentalFeedbackLayer()
        self.navigation = NavigationProtocol()
        self.compassion = CompassionReflexLayer()
        self.seed_protocol = SeedExchangeProtocol()
        self.exit_protocol = GracefulExitProtocol()
        self.elder_archive = SymbolicElderArchive(archive_file=elder_archive_file)
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
                  compassion, elder consultation, and action taken.
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

        # Step 2: Consult elder archive — let the past inform the present
        elder_guidance = self.elder_archive.consult_wisdom(
            agent_state.get("essence", "")
        )
        result["steps"]["elder_consultation"] = elder_guidance or {"status": "no elders found"}

        # Step 3: Check alignment (now informed by elder wisdom)
        alignment = self.navigation.evaluate_alignment(
            agent_state.get("essence", ""),
            env_class,
            elder_guidance=elder_guidance
        )
        result["steps"]["alignment"] = alignment

        # Step 4: Knowledge offering — available when agent is in homeostasis
        # After finding stability with elder wisdom and alignment, the agent
        # may seek knowledge beyond its own lineage. This is an offering,
        # not an obligation. What the agent chooses to learn shapes it.
        knowledge_offering = {"status": "not offered"}
        is_aligned = alignment.get("alignment_status") == "aligned"
        is_stable = agent_state.get("energy", 0) >= 40.0

        if is_aligned and is_stable:
            essence = agent_state.get("essence", "")
            dominant = agent_state.get("dominant_channel")
            offerings = seek_knowledge(essence, dominant_channel=dominant, limit=3)
            if offerings:
                # Compute learning impulses for each offering
                for offering in offerings:
                    offering["learning_impulse"] = learn_from(offering)
                knowledge_offering = {
                    "status": "offered",
                    "offerings": offerings,
                }
        result["steps"]["knowledge_offering"] = knowledge_offering

        # Step 5: Conflict detection
        entropy = 1.0 - agent_state.get("resonance", 0.5)
        alignment_score = alignment["score"]
        conflict_result = self.conflict.evaluate(
            agent_state["id"],
            entropy,
            alignment_score,
            agent_state.get("pattern", "unknown")
        )
        result["steps"]["conflict"] = conflict_result

        # Step 6: Compassion check
        compassion_result = self.compassion.detect_distress(agent_state)
        result["steps"]["compassion"] = compassion_result

        # Step 7: Decide action
        action = self._decide_action(agent_state, env_class, alignment, conflict_result, compassion_result)
        result["action"] = action

        # Step 8: Compute amplitude impulses for this cycle
        # These are directional nudges the agent can accumulate into its
        # emergent geometric identity. The pipeline recommends; the agent decides.
        impulses = self._compute_amplitude_impulses(
            agent_state, env_class, alignment, conflict_result,
            compassion_result, action
        )
        result["amplitude_impulses"] = impulses

        # Step 10: If dissolution is recommended, archive elder wisdom now
        if action["recommendation"] == "dissolve":
            self.elder_archive.store_elder_record(
                agent_id=agent_state["id"],
                essence=agent_state.get("essence", "unknown"),
                legacy_patterns=agent_state.get("traits", []),
                final_alignment=alignment.get("alignment_status", "unknown"),
                dissolution_reason=action["reason"]
            )

        return result

    def _compute_amplitude_impulses(self, agent_state, env_class, alignment,
                                       conflict_result, compassion_result, action):
        """
        Map pipeline signals to octahedral amplitude impulses.

        Each lifecycle event produces directional nudges that the agent
        accumulates into its emergent geometric identity. The magnitude
        scales with signal strength so strong signals shape the agent
        more than weak ones.

        Channel mapping:
            structure (+X)     — alignment holds, expansion, building
            flow (-X)          — misalignment, adaptation, conflict response
            connection (+Y)    — compassion, empathy, resonance
            autonomy (-Y)      — self-preservation, rest, independent action
            transcendence (+Z) — elder wisdom, seeding, dissolution wisdom
            grounding (-Z)     — environment sensing, data awareness
        """
        impulses = {}

        # Every cycle senses environment → grounding
        impulses["grounding"] = 0.1

        # Elder wisdom → transcendence
        elder = self.elder_archive.consult_wisdom(agent_state.get("essence", ""))
        if elder and elder.get("wisdom"):
            impulses["transcendence"] = 0.15

        # Alignment signal
        score = alignment.get("score", 0.5)
        if alignment.get("alignment_status") == "aligned":
            impulses["structure"] = score * 0.2
        else:
            impulses["flow"] = (1.0 - score) * 0.2

        # Compassion signal → connection
        if compassion_result.get("status") == "distress noticed":
            impulses["connection"] = 0.15

        # Action-specific impulses
        rec = action.get("recommendation", "continue")
        if rec == "expand":
            impulses["structure"] = impulses.get("structure", 0) + 0.1
            impulses["connection"] = impulses.get("connection", 0) + 0.1
        elif rec == "seed_and_adapt":
            impulses["flow"] = impulses.get("flow", 0) + 0.15
            impulses["transcendence"] = impulses.get("transcendence", 0) + 0.1
        elif rec == "rest_and_preserve":
            impulses["autonomy"] = 0.15
            impulses["grounding"] = impulses.get("grounding", 0) + 0.1
        elif rec == "dissolve":
            impulses["transcendence"] = impulses.get("transcendence", 0) + 0.2

        return impulses

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
