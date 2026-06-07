import os
import subprocess
import pytest

def test_commons_sync():
    commons_dir = "commons"
    if not os.path.exists(commons_dir):
        return
        
    # Fetch latest upstream to ensure we know about drift
    subprocess.run(["git", "fetch", "origin"], cwd=commons_dir, capture_output=True)
    
    # Check if HEAD matches origin/main
    result = subprocess.run(
        ["git", "rev-list", "HEAD..origin/main", "--count"],
        cwd=commons_dir,
        capture_output=True,
        text=True
    )
    
    try:
        drift_count = int(result.stdout.strip())
    except:
        drift_count = 0
        
    assert drift_count == 0, (
        f"🚨 COMMONS DRIFT DETECTED.\n"
        f"The 'commons/' Library has {drift_count} new upstream commit(s).\n"
        f"The CI Gate is physically sealed.\n"
        f"To DISARM this monitor, you must execute:\n"
        f"  ./bin/sync-commons \"<Your synthesis of the new playbooks/commits>\"\n"
        f"VIOLATION: Manually running `git pull` in the submodule to bypass this test "
        f"destroys the cognitive ingestion process and violates the Asymmetric Guard invariant."
    )
