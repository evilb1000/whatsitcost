import requests
import json
import pandas as pd

# === Config ===
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
JSON_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/material_map.json"
OUTPUT_CSV = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices.csv"

# === Load material map ===
with open(JSON_PATH, "r") as f:
    material_map = json.load(f)

# === Prepare ===
series_ids = list(material_map.values())
batch_size = 50
all_records = []

# === Process in batches of 50 ===
for i in range(0, len(series_ids), batch_size):
    batch = series_ids[i:i+batch_size]
    payload = {
        "seriesid": batch,
        "startyear": "2020",
        "endyear": "2025",
        "registrationKey": API_KEY
    }

    response = requests.post(API_URL, json=payload)
    data = response.json()

    for series in data.get("Results", {}).get("series", []):
        series_id = series["seriesID"]
        material_name = next((k for k, v in material_map.items() if v == series_id), series_id)

        if material_name == series_id:
            print(f"⚠️  No name match for series: {series_id}")

        for obs in series["data"]:
            year = obs["year"]
            period = obs["period"]
            value = obs["value"]

            if period.startswith("M"):
                month = int(period[1:])
                all_records.append({
                    "Material": material_name,
                    "Series ID": series_id,
                    "Year": int(year),
                    "Month": month,
                    "Value": float(value)
                })

# === Save output ===
df = pd.DataFrame(all_records)
df.sort_values(by=["Material", "Year", "Month"], inplace=True)
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Pulled {len(df['Series ID'].unique())} unique series.")
print(f"📁 Data saved to: {OUTPUT_CSV}")
