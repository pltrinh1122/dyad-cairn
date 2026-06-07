import os
import glob
import json

base = os.path.expanduser("~/.gemini/antigravity-cli/brain")
transcripts = glob.glob(f"{base}/*/.system_generated/logs/transcript.jsonl")
latest = max(transcripts, key=os.path.getmtime)
print(latest)
