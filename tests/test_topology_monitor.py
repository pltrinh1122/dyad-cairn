import os
import pytest

# The Mechanical Gate for Topology Mass
# If a directory exceeds its capacity, the TDD gate will violently fail,
# forcing a physical refactor of the repository organization.

CAPACITY_LIMITS = {
    "bin": 32,
    "skills": 25,
    "kb": 21,
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
        f"🚨 TOPOLOGY MASS EXCEEDED in '{directory}/' (Current: {mass}, Limit: {limit}).\n"
        f"The Topology Mass Monitor is ARMED. The CI gate is physically sealed.\n"
        f"To DISARM this monitor, you must satisfy one of the following physical conditions:\n"
        f"  1. COMPRESS: Physically refactor '{directory}/' (e.g., into sub-packages) to reduce its mass below {limit}.\n"
        f"  2. EXPAND: Raise the limit in this file, BUT this strictly requires forging a new Ontological Bond (a formal `retro:`) proving the Dyad's cognitive capacity has permanently scaled.\n"
        f"VIOLATION: Silently increasing the limit without an anchoring Retro, or smoothing the mortar to bypass this trigger, violates the Orthogonality Invariant."
    )
