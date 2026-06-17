import os
import shutil
import pytest
from skills import flow_state_manager as fsm

def test_set_active_anchor_overwrites_existing():
    anchor_path = "dyad-state/active_anchor"
    
    # Ensure dyad-state dir exists
    os.makedirs("dyad-state", exist_ok=True)
    
    # Create initial anchor
    if os.path.lexists(anchor_path):
        os.remove(anchor_path)
    
    with open(anchor_path, "w") as f:
        f.write("INITIAL_STATE")
        
    # Call the function to transition states
    fsm.set_active_anchor("NEW_STATE")
    
    # Verify the anchor was updated
    assert os.path.exists(anchor_path)
    
    if os.path.islink(anchor_path):
        assert os.readlink(anchor_path) == "NEW_STATE"
    else:
        with open(anchor_path, "r") as f:
            content = f.read().strip()
        assert content == "NEW_STATE"
        
    # Cleanup
    if os.path.lexists(anchor_path):
        os.remove(anchor_path)
