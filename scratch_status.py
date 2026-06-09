import yaml
from skills.frontier_reader import derive_status
with open("artifacts/frontier_state.yml", "r") as f:
    state = yaml.safe_load(f)
for k, v in state["nodes"].items():
    print(f"{k}: {derive_status(k, v, state['nodes'])}")
