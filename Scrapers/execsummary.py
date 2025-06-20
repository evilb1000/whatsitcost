import pandas as pd
import json
from pathlib import Path

# === Load theBehemoth.csv ===
csv_path = Path("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv")
df = pd.read_csv(csv_path)

# === Fix date formatting and sorting ===
df['month'] = df['month'].str.extract(r'M(\d+)', expand=False).astype(str).str.zfill(2)
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')
df.sort_values(by=['series_id', 'date'], ascending=[True, False], inplace=True)

# === Grab the latest entry per series ===
latest_entries = df.drop_duplicates(subset='series_id', keep='first').copy()
latest_entries = latest_entries.rename(columns={
    "series_id": "material",
    "series_name": "name",
    "mom_growth": "mom"
})
latest_entries = latest_entries[["material", "name", "mom", "date"]]

import pandas as pd
import json
from pathlib import Path

# === Load theBehemoth.csv ===
csv_path = Path("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv")
df = pd.read_csv(csv_path)

# === Fix date formatting and sorting ===
df['month'] = df['month'].str.extract(r'M(\d+)', expand=False).astype(str).str.zfill(2)
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')
df.sort_values(by=['series_id', 'date'], ascending=[True, False], inplace=True)

# === Grab the latest entry per series ===
latest_entries = df.drop_duplicates(subset='series_id', keep='first').copy()
latest_entries = latest_entries.rename(columns={
    "series_id": "material",
    "series_name": "name",
    "mom_growth": "mom",
    "yoy_growth": "yoy"
})
latest_entries = latest_entries[["material", "name", "mom", "yoy", "date"]]

# 🔧 Convert to % and round
latest_entries["mom"] = (latest_entries["mom"] * 100).round(2)
latest_entries["yoy"] = (latest_entries["yoy"] * 100).round(2)

# === Classify movement ===
def classify_movement(change):
    if abs(change) < 1.0:
        return 'stable'
    elif change >= 1.0:
        return 'rising'
    elif change <= -1.0:
        return 'falling'
    else:
        return 'other'

latest_entries["movement"] = latest_entries["mom"].apply(classify_movement)

# === Compute percentages ===
total = len(latest_entries)
stable_pct = round((latest_entries["movement"] == "stable").sum() / total * 100, 1)
rising_pct = round((latest_entries["movement"] == "rising").sum() / total * 100, 1)
falling_pct = round((latest_entries["movement"] == "falling").sum() / total * 100, 1)

# === Top movers ===
risers = latest_entries[latest_entries["movement"] == "rising"].nlargest(2, "mom")
fallers = latest_entries[latest_entries["movement"] == "falling"].nsmallest(2, "mom")

# === Core materials: CPI, PPI Final Demand, PPI Construction, Industrial Products ===
core_materials_list = ["CUUR0000SA0", "WPUFD4", "WPUFD43", "WPUIP230000"]
core_materials = latest_entries[latest_entries["material"].isin(core_materials_list)]

# === Manually set snapshot date ===
snapshot_date = latest_entries["date"].max().strftime("%Y-%m")

# === Final JSON structure ===
summary = {
    "snapshot_date": snapshot_date,
    "core_materials": core_materials[["material", "name", "mom", "yoy"]].to_dict(orient="records"),
    "stable_pct": stable_pct,
    "rising_pct": rising_pct,
    "falling_pct": falling_pct,
    "risers": risers[["material", "name", "mom", "yoy"]].to_dict(orient="records"),
    "fallers": fallers[["material", "name", "mom", "yoy"]].to_dict(orient="records")
}

# === Write to disk ===
output_path = Path("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/JSONS/latest_snapshot.json")
with open(output_path, "w") as f:
    json.dump(summary, f, indent=2)

print("✅ latest_snapshot.json generated successfully.")
