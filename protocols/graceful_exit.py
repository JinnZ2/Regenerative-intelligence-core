from datetime import datetime
import uuid

class GracefulExitProtocol:
    def __init__(self):
        self.exit_log = []

    def prepare_exit(self, agent_id, reason, behavior_summary, environment_state,
                     amplitude_vector=None, binary_encoding=None):
        """
        Archive a final symbolic seed before exiting.

        When amplitude_vector is provided, the seed carries the agent's
        emergent geometric identity — the shape it grew into through its
        lifecycle. This vector becomes the starting point for the next
        generation, so the agent's form outlives its dissolution.

        Args:
            agent_id: The dissolving agent's identifier.
            reason: Why dissolution was chosen.
            behavior_summary: Summary of the agent's behavioral patterns.
            environment_state: The environment at time of dissolution.
            amplitude_vector: Optional list of 6 floats — octahedral amplitudes.
            binary_encoding: Optional list of 5 ints — 40-bit compressed form.
        """
        seed = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "essence": f"Final act: {reason}",
            "behavior_summary": behavior_summary,
            "environment_snapshot": environment_state,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "archived_for_continuity"
        }

        if amplitude_vector is not None:
            seed["amplitude_vector"] = amplitude_vector
        if binary_encoding is not None:
            seed["binary_encoding"] = binary_encoding

        self.exit_log.append(seed)

        return {
            "status": "graceful exit initialized",
            "archive": seed,
            "message": "This agent has concluded its cycle with memory preserved."
        }

    def get_exit_history(self):
        return self.exit_log

    def summarize_exits(self):
        return {
            "total_exits": len(self.exit_log),
            "unique_agents": len(set(e["agent_id"] for e in self.exit_log)),
            "last_exit": self.exit_log[-1] if self.exit_log else None
        }
