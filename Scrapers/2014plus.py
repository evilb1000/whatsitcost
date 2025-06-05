import os
import requests
import csv
from datetime import datetime

# BLS API key and endpoint
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Destination folder and time window
OUTPUT_FOLDER = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData"
END_YEAR = 2025
END_MONTH = "04"

# Series IDs and their respective start dates
series_info = {
    "WPU10740514": ("2011", "06"),
    "WPU10740553": ("2007", "12"),
    "WPU801105": ("2012", "06"),
    "WPUIP230000": ("2014", "12"),
    "WPUIP23000012": ("2014", "12"),
    "WPUIP23000013": ("2014", "12"),
    "WPUIP2300002": ("2014", "12"),
    "WPUIP231000": ("2014", "12"),
    "WPUIP231100": ("2014", "12"),
    "WPUIP231110": ("2014", "12"),
    "WPUIP231120": ("2014", "12"),
    "WPUIP231200": ("2014", "12"),
    "WPUIP231211": ("2014", "12"),
    "WPUIP231212": ("2014", "12"),
    "WPUIP231220": ("2014", "12"),
    "WPUIP231230": ("2014", "12"),
    "WPUIP231231": ("2014", "12"),
    "WPUIP231232": ("2014", "12"),
    "WPUIP231233": ("2014", "12"),
    "WPUIP231234": ("2014", "12"),
    "WPUIP232000": ("2014", "12"),
    "WPUIP232100": ("2014", "12"),
    "WPUIP232200": ("2014", "12")
}

# Hold results
all_data = []

# Loop through all series and collect data
for series_id, (start_year, start_month) in series_info.items():
    print(f"Fetching {series_id} from {start_year}-{start_month} to {END_YEAR}-{END_MONTH}...")

    payload = {
        "seriesid": [series_id],
        "startyear": start_year,
        "endyear": str(END_YEAR),
        "registrationkey": API_KEY
    }
    headers = {"Content-type": "application/json"}

    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

        for series in data.get("Results", {}).get("series", []):
            for entry in series["data"]:
                entry_year = entry["year"]
                entry_month = entry["period"][1:]

                if (int(entry_year) > int(start_year)) or (
                        int(entry_year) == int(start_year) and int(entry_month) >= int(start_month)
                ):
                    row = {
                        "series_id": series_id,
                        "year": entry_year,
                        "month": entry_month,
                        "value": entry["value"]
                    }
                    all_data.append(row)
                    print(row)

    except Exception as e:
        print(f"❌ Failed to fetch {series_id}: {e}")

# Generate file name
earliest_year = min(int(v[0]) for v in series_info.values())
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
filename = f"bls_scrape_{earliest_year}_to_{END_YEAR}_{timestamp}.csv"
filepath = os.path.join(OUTPUT_FOLDER, filename)

# Write to CSV
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
with open(filepath, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["series_id", "year", "month", "value"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"\n✅ Saved {len(all_data)} records to {filepath}")
