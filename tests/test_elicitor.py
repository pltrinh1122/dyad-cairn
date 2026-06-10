import os

def test_invisible_elicitor_protocol_codified():
    agent_md_path = "commons/AGENT.md"
    assert os.path.exists(agent_md_path), "AGENT.md not found"
    
    with open(agent_md_path, "r") as f:
        content = f.read()
        
    assert "The Invisible Elicitor" in content, "The Invisible Elicitor protocol must be formally codified in AGENT.md"
    assert "Elicitation Seed" in content, "The protocol must dictate the WHY as the Elicitation Seed"
