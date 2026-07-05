import os

def test_backlog_item_cleared():
    assert os.path.exists('dm/dyad-steward/2026-06-11-commons-architecture-counter.md'), 'The inbound mail counter was not found.'
