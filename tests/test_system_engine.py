import pytest
import os
import tempfile
import yaml
import sys
from importlib.machinery import SourceFileLoader

engine_module = SourceFileLoader("system_engine", os.path.abspath(os.path.join(os.path.dirname(__file__), '../bin/system-engine.py'))).load_module()

def test_system_engine_fsm_load_both_corpora():
    """Test FSM LOAD-BOTH-CORPORA -> VALIDATE-CLAIM-CORE with id collision"""
    with tempfile.TemporaryDirectory() as d:
        schema = os.path.join(d, "schema.yaml")
        theory = os.path.join(d, "theory.yaml")
        inv = os.path.join(d, "inv.yaml")
        
        with open(schema, "w") as f: yaml.dump({"required": ["id"]}, f)
        with open(theory, "w") as f: yaml.dump([{"id": "claim_1"}], f)
        with open(inv, "w") as f: yaml.dump([{"id": "claim_1"}], f) # Collision
        
        engine = engine_module.SystemEngine(schema, theory, inv)
        
        engine.state_load_both_corpora()
        with pytest.raises(engine_module.FSMError, match="cross-file-id-collision"):
            engine.state_validate_claim_core()

def test_system_engine_new_fsm():
    """Test successful new command flow"""
    with tempfile.TemporaryDirectory() as d:
        schema = os.path.join(d, "schema.yaml")
        theory = os.path.join(d, "theory.yaml")
        inv = os.path.join(d, "inv.yaml")
        
        with open(schema, "w") as f: yaml.dump({"required": ["id"]}, f)
        with open(theory, "w") as f: yaml.dump([], f)
        with open(inv, "w") as f: yaml.dump([], f)
        
        engine = engine_module.SystemEngine(schema, theory, inv)
        engine.run_new({"id": "claim_2"})
        
        with open(theory, "r") as f:
            data = yaml.safe_load(f)
            assert data[0]["id"] == "claim_2"

def test_system_engine_graduate_fsm():
    """Test successful graduate command flow"""
    with tempfile.TemporaryDirectory() as d:
        schema = os.path.join(d, "schema.yaml")
        theory = os.path.join(d, "theory.yaml")
        inv = os.path.join(d, "inv.yaml")
        
        with open(schema, "w") as f: yaml.dump({"required": ["id"]}, f)
        with open(theory, "w") as f: yaml.dump([{"id": "claim_2"}], f)
        with open(inv, "w") as f: yaml.dump([], f)
        
        engine = engine_module.SystemEngine(schema, theory, inv)
        engine.run_graduate("claim_2")
        
        with open(theory, "r") as f:
            t_data = yaml.safe_load(f)
            assert t_data[0]["status"] == "graduated"
            
        with open(inv, "r") as f:
            i_data = yaml.safe_load(f)
            assert i_data[0]["id"] == "inv_claim_2"
            assert i_data[0]["graduated_from"] == "claim_2"
