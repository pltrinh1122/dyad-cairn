import sys
sys.path.append('.')
from skills.frontier_editor import load_state, save_state
state = load_state()
state["nodes"]["node_99_review"] = {"status": "IN_REVIEW", "type": "PLAN", "title": "test", "goal": "test", "scope": "SUBSTRATE"}
save_state(state)
