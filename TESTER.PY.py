import json

# === File path ===
file_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/JSONS/material_trendlines.json"

# === Load JSON and extract data ===
with open(file_path, "r") as f:
    data = json.load(f)

# === Target material ===
material = "#2 Diesel Fuel"

if material in data:
    print(f"Found {len(data[material])} records for '{material}':\n")
    for entry in data[material]:
        print(entry)
else:
    print(f"❌ Material '{material}' not found in the dataset.")
