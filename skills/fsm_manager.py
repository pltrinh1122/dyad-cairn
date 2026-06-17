import os
import yaml

class FSMManager:
    def __init__(self, state_file="artifacts/fsm_state.yml"):
        self.state_file = state_file
        self.state = {}
        
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                self.state = yaml.safe_load(f) or {}
