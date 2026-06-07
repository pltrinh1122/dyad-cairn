import pytest
from skills.frontier_reader import derive_status

def test_derive_status_done():
    all_nodes = {
        "node_1": {"dependencies": []}
    }
    ledger = "Something something node_1 is merged."
    status = derive_status("node_1", all_nodes["node_1"], all_nodes, ledger_content=ledger, active_branches="")
    assert status == "DONE"

def test_derive_status_active():
    all_nodes = {
        "node_2": {"dependencies": []}
    }
    branches = "  main\n* feat/node_2_stuff"
    status = derive_status("node_2", all_nodes["node_2"], all_nodes, ledger_content="", active_branches=branches)
    assert status == "ACTIVE"

def test_derive_status_ready():
    all_nodes = {
        "node_3": {"dependencies": []}
    }
    status = derive_status("node_3", all_nodes["node_3"], all_nodes, ledger_content="", active_branches="")
    assert status == "READY"

def test_derive_status_blocked_by_dependency():
    all_nodes = {
        "node_1": {"dependencies": []}, # Not done
        "node_2": {"dependencies": ["node_1"]}
    }
    status = derive_status("node_2", all_nodes["node_2"], all_nodes, ledger_content="", active_branches="")
    assert status == "BLOCKED"

def test_derive_status_ready_with_done_dependency():
    all_nodes = {
        "node_1": {"dependencies": []},
        "node_2": {"dependencies": ["node_1"]}
    }
    ledger = "node_1 completed."
    status = derive_status("node_2", all_nodes["node_2"], all_nodes, ledger_content=ledger, active_branches="")
    assert status == "READY"

def test_build_tree_returns_list():
    from skills.frontier_reader import build_tree
    nodes = {
        "node_1": {"title": "Node 1", "dependencies": []},
        "node_2": {"title": "Node 2", "dependencies": ["node_1"]}
    }
    lines = build_tree(nodes)
    assert isinstance(lines, list)
    assert len(lines) == 2
    assert "node_1" in lines[0]
    assert "node_2" in lines[1]
    assert "├──" in lines[0] or "└──" in lines[0]
    assert "├──" in lines[1] or "└──" in lines[1]
