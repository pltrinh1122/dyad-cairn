import os
import pytest

# The Mechanical Gate for Topology Mass
# If a directory exceeds its capacity, the TDD gate will violently fail,
# forcing a physical refactor of the repository organization.

CAPACITY_LIMITS = {
    "bin": 20,
    "skills": 20,
    "kb": 15,
}

def count_files(directory):
    if not os.path.exists(directory):
        return 0
    # Count only physical files, ignore directories and __pycache__
    count = 0
    for root, dirs, files in os.walk(directory):
        if "__pycache__" in root:
            continue
        count += len(files)
    return count

@pytest.mark.parametrize("directory, limit", CAPACITY_LIMITS.items())
def test_topology_capacity(directory, limit):
    mass = count_files(directory)
    
    # The Cybernetic Steering Vector (CSI) for refactoring
    assert mass <= limit, (
        f"🚨 TOPOLOGY MASS EXCEEDED in '{directory}/'. "
        f"Current: {mass}, Limit: {limit}. "
        f"It is time to refactor the repo organization (e.g., sub-packages). "
        f"Do not bypass this test."
    )
