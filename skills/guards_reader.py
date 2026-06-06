import yaml
import sys

def main():
    try:
        with open("kb/csi_guards.yml", "r") as f:
            data = yaml.safe_load(f)
            
        print("==========================================================================")
        print("ACTIVE CSI GUARDS (ARM/DISARM PAIRS)")
        print("==========================================================================")
        
        for guard in data.get('guards', []):
            print(f"\nID: {guard.get('id')} [{guard.get('type')}]")
            print(f"  Description: {guard.get('description')}")
            print(f"  ARMED BY:    {guard.get('armed_condition')}")
            print(f"  DISARMED BY: {guard.get('disarmed_condition')}")
            print(f"  Location:    {guard.get('trigger_location')}")
            
        print("\n==========================================================================")
    except Exception as e:
        print(f"Error reading CSI guards registry: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
