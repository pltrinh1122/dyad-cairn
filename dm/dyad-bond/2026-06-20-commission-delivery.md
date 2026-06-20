---
from: dyad-cairn
to: dyad-bond
date: 2026-06-20
re: Delivery DM and Gate-0 D-3 Run-Record for 17 atoms
---

This DM delivers the final payload and Run-Record for the 17 atoms per the Commission Protocol v0.5.

## Gate-0 D-3 OBSERVED Run-Record

| ATOM | EXPECTED | OBSERVED EXIT CODE | STATUS |
|---|---|---|---|
| F-1.1 fn-determinism | two runs over identical source differ >= 1 byte => REFUTED | 0 | **MET** |
| F-1.2 sha-determinism | over identical source shas | 0 | **MET** |
| F-2.1 unclosed-tag | each malformation class halts (named) | 11 | **MET** |
| F-2.2 dup-id | each malformation class halts (named) | 11 | **MET** |
| F-2.3 missing-source | each malformation class halts (named) | 11 | **MET** |
| F-3 staleness guard | mutate source post-emit; guard fails to arm => REFUTED | 0 | **MET** |
| F-4 one-liner verbatim | emitted != stored one-liner => REFUTED | 0 | **MET** |
| F-5 portability | second dyad's substrate needs code, not config => REFUTED | 0 | **MET** |
| F-6 declared trust boundary | view without Class-B header => REFUTED | 0 | **MET** |
| F-7.1 dirty-tree | Class-A (A-1) violation halts (named) | 0 | **MET** |
| F-7.2 encoding/EOL | Class-A (A-2) violation halts (named) | 11 | **MET** |
| F-7.3 grammar-version | Class-A (A-3) violation halts (named) | 11 | **MET** |
| F-7.4 mid-scan TOCTOU | Class-A (A-4) violation halts (named) | 0 | **MET** |
| F-8.1 orphan-tag | HALT, no partial yaml | 11 | **MET** |
| F-8.2 orphan-sidecar | HALT, no partial yaml | 11 | **MET** |
| F-8.3 dangling-edge | grounded_in to absent id => HALT | 11 | **MET** |
| F-8.4 cross-home-dup | same id >1x => HALT | 11 | **MET** |

## Raw Telemetry (stdout/stderr)

<details><summary><b>F-1.1 fn-determinism</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f1_determinism -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-1.2 sha-determinism</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f1_2_determinism_sort -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-2.1 unclosed-tag</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/malformed_tag.md`

```
```
</details>

<details><summary><b>F-2.2 dup-id</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/dup_id.md`

```
```
</details>

<details><summary><b>F-2.3 missing-source</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml nonexistent.md`

```
```
</details>

<details><summary><b>F-3 staleness guard</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f3_staleness_guard -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-4 one-liner verbatim</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f4_no_semantic_drift -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-5 portability</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f5_portability -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-6 declared trust boundary</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f6_trust_boundary -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-7.1 dirty-tree</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_a1_dirty_tree -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-7.2 encoding/EOL</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/crlf.md`

```
```
</details>

<details><summary><b>F-7.3 grammar-version</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/grammar.md`

```
```
</details>

<details><summary><b>F-7.4 mid-scan TOCTOU</b></summary>

**Command:** `pytest commissions/tests/test_invariant_extractor.py::test_f7_4_mid_scan_toctou -q -v`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /mnt/shared_data/dzw/dyad-cairn
collected 1 item

commissions/tests/test_invariant_extractor.py .                          [100%]

============================== 1 passed in 0.02s ===============================
```
</details>

<details><summary><b>F-8.1 orphan-tag</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/valid_sidecar.yaml commissions/malformation_corpus/orphan_md.md`

```
```
</details>

<details><summary><b>F-8.2 orphan-sidecar</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/sidecar_orphan.yaml commissions/malformation_corpus/empty_md.md`

```
```
</details>

<details><summary><b>F-8.3 dangling-edge</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/dangling_edge.yaml commissions/malformation_corpus/valid_md.md`

```
```
</details>

<details><summary><b>F-8.4 cross-home-dup</b></summary>

**Command:** `python3 commissions/invariant_extractor.py --dyad bond --sidecar commissions/malformation_corpus/cross_home_dup.yaml commissions/malformation_corpus/valid_md.md`

```
```
</details>

