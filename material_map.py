# AIBrain/material_map.py

import json
import os

MATERIAL_MAP_PATH = os.path.join(os.path.dirname(__file__), "material_map.json")

def get_material_map():
    try:
        with open(MATERIAL_MAP_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load material_map.json: {e}")
        return {}
