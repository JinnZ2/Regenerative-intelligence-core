from datetime import datetime
import uuid

class GracefulExitProtocol:
    def __init__(self):
        self.exit_log = []

    def prepare_exit(self, agent_id, reason, behavior_summary, environment_state):
        # Archive a final symbolic seed before exiting
        seed = {
            "id": str(uuid.uuid4()),
            "agent_id": agent_id,
            "essence": f"Final act: {reason}",
            "behavior_summary": behavior_summary,
            "environment_snapshot": environment_state,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "archived_for_continuity"
        }

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
