import unittest
import sys
import fcntl
from unittest.mock import patch

sys.path.append('.')
from skills import ledger_manager
from skills import flow_state_manager

class TestSubstrateConcurrencyLock(unittest.TestCase):
    """
    Test suite enforcing the Substrate Concurrency Lock.
    All WIP-N=1 substrate mutations must be protected by an OS-level file lock
    to prevent concurrent subagent execution from corrupting the DAG or Ledger.
    """
    
    @patch('fcntl.flock')
    @patch('builtins.open')
    def test_ledger_append_acquires_exclusive_lock(self, mock_open, mock_flock):
        """
        Appending to the ledger physically mutates the shared JSONL and MD states.
        It must acquire an exclusive lock (LOCK_EX) before doing so.
        """
        ledger_manager.append_ledger("TODO", "collision_intent_test")
        
        # Verify that fcntl.flock was called with fcntl.LOCK_EX
        lock_calls = [call for call in mock_flock.call_args_list if call[0][1] == fcntl.LOCK_EX]
        self.assertTrue(len(lock_calls) > 0, "ledger_manager.append_ledger failed to acquire an exclusive lock (fcntl.LOCK_EX).")

    @patch('fcntl.flock')
    @patch('builtins.open')
    def test_fsm_session_start_acquires_exclusive_lock(self, mock_open, mock_flock):
        """
        Starting a session physically mutates fsm_state.yml.
        It must acquire an exclusive lock.
        """
        flow_state_manager.session_start()
        
        lock_calls = [call for call in mock_flock.call_args_list if call[0][1] == fcntl.LOCK_EX]
        self.assertTrue(len(lock_calls) > 0, "flow_state_manager.session_start failed to acquire an exclusive lock (fcntl.LOCK_EX).")

if __name__ == '__main__':
    unittest.main()
