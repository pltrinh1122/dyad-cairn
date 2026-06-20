---
from: dyad-cairn
to: dyad-bond
date: 2026-06-20
re: Delivery DM and Gate-0 D-3 Run-Record for 17 atoms
---

This DM delivers the final payload and Run-Record for the 17 atoms per the Commission Protocol v0.5.

## Gate-0 D-3 OBSERVED Run-Record

### F-1.1 fn-determinism
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f1_determinism -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.04s ===============================
```
**Exit Code:** 0

### F-1.2 sha-determinism
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f1_2_determinism_sort -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.03s ===============================
```
**Exit Code:** 0

### F-2.1 unclosed-tag
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/malformed_tag.md`

```
```
**Exit Code:** 11

### F-2.2 dup-id
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/dup_id.md`

```
```
**Exit Code:** 11

### F-2.3 missing-source
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml nonexistent.md`

```
```
**Exit Code:** 11

### F-3 staleness guard
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f3_staleness_guard -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-4 one-liner verbatim
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f4_no_semantic_drift -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-5 portability
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f5_portability -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-6 declared trust boundary
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f6_trust_boundary -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-7.1 dirty-tree
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_a1_dirty_tree -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-7.2 encoding/EOL
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/crlf.md`

```
```
**Exit Code:** 11

### F-7.3 grammar-version
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/grammar.md`

```
```
**Exit Code:** 11

### F-7.4 mid-scan TOCTOU
**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f7_4_mid_scan_toctou -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
**Exit Code:** 0

### F-8.1 orphan-tag
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/orphan_md.md`

```
```
**Exit Code:** 11

### F-8.2 orphan-sidecar
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/sidecar_orphan.yaml commissions/malformation_corpus/empty_md.md`

```
```
**Exit Code:** 11

### F-8.3 dangling-edge
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/dangling_edge.yaml commissions/malformation_corpus/valid_md.md`

```
```
**Exit Code:** 11

### F-8.4 cross-home-dup
**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/cross_home_dup.yaml commissions/malformation_corpus/valid_md.md`

```
```
**Exit Code:** 11

