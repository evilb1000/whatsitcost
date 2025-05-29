import json

with open("material_trends.json", "r") as f:
    data = json.load(f)

# Print one date
print(json.dumps(data["2023-04"], indent=2))

# Show one date + top 3 series
for date, series in data.items():
    print(f"{date} → {list(series.keys())[:3]}...")
    break
