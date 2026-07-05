import os
import shutil
import pytest

# Ensure all tests run in the sandboxed test ledger
os.environ["DYAD_TEST_ENV"] = "true"

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_ledger():
    # Setup
    yield
    # Teardown: clean up test_ledger at the end of the test session
    test_ledger_dir = "test_ledger"
    if os.path.exists(test_ledger_dir):
        shutil.rmtree(test_ledger_dir)
