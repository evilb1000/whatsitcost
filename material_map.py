# AIBrain/material_map.py

import json
import os

HERE = os.path.dirname(__file__)
MATERIAL_MAP_PATH_PRIMARY = os.path.join(HERE, "material_map.json")
MATERIAL_MAP_PATH_FALLBACK = os.path.join(HERE, "AIBrain", "material_map.json")

def get_material_map():
    try:
        path = MATERIAL_MAP_PATH_PRIMARY
        if not os.path.exists(path):
            path = MATERIAL_MAP_PATH_FALLBACK
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load material_map.json: {e}")
        return {}
