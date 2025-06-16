import json

file_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/JSONS/material_rolling.json"

with open(file_path, "r") as f:
    data = json.load(f)

material = "Aluminum Mill Shapes"

if material in data:
    for entry in data[material]:
        print(entry)
else:
    print(f"❌ '{material}' not found in the JSON.")
