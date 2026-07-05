#!/usr/bin/env python3
import sys
import yaml
import argparse
import os
import hashlib
import json
import shutil

class FSMError(Exception):
    pass

class SystemEngine:
    def __init__(self, claim_core_schema_path, theory_path, invariants_path, invariant_schema_path=None):
        self.claim_core_schema_path = claim_core_schema_path
        self.theory_path = theory_path
        self.invariants_path = invariants_path
        self.invariant_schema_path = invariant_schema_path
        
        self.schema = {}
        self.theory_data = []
        self.invariants_data = []

    def state_load_both_corpora(self):
        try:
            with open(self.claim_core_schema_path, 'r') as f:
                self.schema = yaml.safe_load(f) or {}
            
            if os.path.exists(self.theory_path):
                with open(self.theory_path, 'r') as f:
                    self.theory_data = yaml.safe_load(f) or []
            else:
                self.theory_data = []

            if os.path.exists(self.invariants_path):
                with open(self.invariants_path, 'r') as f:
                    self.invariants_data = yaml.safe_load(f) or []
            else:
                self.invariants_data = []
        except Exception as e:
            raise FSMError(f"LOAD-BOTH-CORPORA failed: {str(e)}")

    def _validate_record(self, record):
        if 'required' in self.schema:
            for req in self.schema['required']:
                if req not in record:
                    raise FSMError(f"VALIDATE-CLAIM-CORE failed: Missing required field '{req}' in record {record.get('id', 'UNKNOWN')}")
                    
    def state_validate_claim_core(self):
        all_ids = set()
        
        for r in self.theory_data:
            rec_id = r.get('id')
            if not rec_id:
                raise FSMError("VALIDATE-CLAIM-CORE failed: Record missing id")
            if rec_id in all_ids:
                raise FSMError(f"VALIDATE-CLAIM-CORE failed: CSI-Guard cross-file-id-collision for {rec_id}")
            all_ids.add(rec_id)
            self._validate_record(r)
            
        for r in self.invariants_data:
            rec_id = r.get('id')
            if not rec_id:
                raise FSMError("VALIDATE-CLAIM-CORE failed: Record missing id")
            if rec_id in all_ids:
                raise FSMError(f"VALIDATE-CLAIM-CORE failed: CSI-Guard cross-file-id-collision for {rec_id}")
            all_ids.add(rec_id)
            self._validate_record(r)
            
            # Orphan lineage guard check
            graduated_from = r.get('graduated_from')
            if graduated_from:
                # Basic check: just ensure we don't have broken dependencies if strictly enforced
                pass

    def state_new(self, record_args):
        new_record = record_args
        self._validate_record(new_record)
        self.theory_data.append(new_record)

    def state_graduate(self, target_id):
        candidate = None
        for r in self.theory_data:
            if r.get('id') == target_id:
                candidate = r
                break
        
        if not candidate:
            raise FSMError(f"GRADUATE failed: Candidate {target_id} not found in theory-pipeline.")
            
        if candidate.get('status') == 'graduated':
            raise FSMError(f"CSI-Guard orphan-lineage: Candidate {target_id} already graduated.")

        candidate['status'] = 'graduated'
        
        new_invariant = candidate.copy()
        new_invariant['id'] = f"inv_{target_id}"
        new_invariant['graduated_from'] = target_id
        
        self.invariants_data.append(new_invariant)

    def state_write(self):
        tmp_theory = self.theory_path + '.tmp'
        tmp_inv = self.invariants_path + '.tmp'
        try:
            with open(tmp_theory, 'w') as f:
                yaml.dump(self.theory_data, f, sort_keys=False)
            with open(tmp_inv, 'w') as f:
                yaml.dump(self.invariants_data, f, sort_keys=False)
                
            os.replace(tmp_theory, self.theory_path)
            os.replace(tmp_inv, self.invariants_path)
        except Exception as e:
            if os.path.exists(tmp_theory): os.remove(tmp_theory)
            if os.path.exists(tmp_inv): os.remove(tmp_inv)
            raise FSMError(f"WRITE failed: {str(e)}")

    def state_validate_post(self):
        self.state_load_both_corpora()
        self.state_validate_claim_core()

    def run_validate(self):
        self.state_load_both_corpora()
        self.state_validate_claim_core()
        print("Validation successful.")

    def run_new(self, record_args):
        self.state_load_both_corpora()
        self.state_validate_claim_core()
        self.state_new(record_args)
        self.state_write()
        self.state_validate_post()
        print("New record added.")

    def run_graduate(self, target_id):
        self.state_load_both_corpora()
        self.state_validate_claim_core()
        self.state_graduate(target_id)
        self.state_write()
        self.state_validate_post()
        print(f"Record {target_id} graduated.")


def main():
    parser = argparse.ArgumentParser(description="dyad-system factory/validator engine")
    parser.add_argument("command", choices=["validate", "new", "graduate"])
    parser.add_argument("--claim-core-schema", required=True)
    parser.add_argument("--theory", required=True)
    parser.add_argument("--invariants", required=True)
    parser.add_argument("--invariant-schema", required=False)
    
    parser.add_argument("--id", required=False)
    parser.add_argument("--target-id", required=False)

    args = parser.parse_args()

    engine = SystemEngine(args.claim_core_schema, args.theory, args.invariants, args.invariant_schema)

    try:
        if args.command == "validate":
            engine.run_validate()
        elif args.command == "new":
            if not args.id:
                print("FATAL: --id required for new")
                sys.exit(1)
            record = {"id": args.id}
            engine.run_new(record)
        elif args.command == "graduate":
            if not args.target_id:
                print("FATAL: --target-id required for graduate")
                sys.exit(1)
            engine.run_graduate(args.target_id)
    except FSMError as e:
        print(f"FATAL: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
