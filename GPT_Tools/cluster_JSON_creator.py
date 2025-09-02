import pandas as pd
import json
from cluster_definitions import CLUSTERS

# === Load the Behemoth dataset ===
behemoth_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
df = pd.read_csv(behemoth_path)

# Fix month and year formatting
df['month'] = df['month'].astype(str).str.zfill(2)
df['year'] = df['year'].astype(str)

# === Create cluster summary ===
cluster_data = {}

for cluster_name, series_objects in CLUSTERS.items():
    materials = []

    for obj in series_objects:
        sid = obj["id"]
        sub = df[df['series_id'] == sid]
        if not sub.empty:
            latest = sub.sort_values(['year', 'month'], ascending=False).iloc[0]
            materials.append({
                "series_name": latest["series_name"],
                "series_id": latest["series_id"],
                "month": latest["month"],
                "year": latest["year"],
                "MoM": latest["mom_growth"],
                "YoY": latest["yoy_growth"]
            })

    # Get max year-month from what we pulled (for display purposes)
    if materials:
        latest_year = max(m["year"] for m in materials)
        latest_month = max(m["month"] for m in materials if m["year"] == latest_year)
        latest_date_str = f"{latest_year}-{latest_month}"
    else:
        latest_date_str = None

    cluster_data[cluster_name] = {
        "as_of": latest_date_str,
        "count": len(materials),
        "materials": materials
    }

# === Save to JSON ===
output_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/JSONS/cluster_data.json"
with open(output_path, "w") as f:
    json.dump(cluster_data, f, indent=2)

print(f"✅ Cluster data saved to: {output_path}")
